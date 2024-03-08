// SPDX-License-Identifier: LGPL-2.0
/*
 * camera.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

#include <algorithm>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <thread>

#if !(PYTHON)
	#include <opencv2/core/mat.hpp>
#endif

#include "camera.h"

/**
 * @mainpage qamlib Documentation
 * Testing
 */

namespace qamlib
{
/**
 * Function to "pretty-print" the FrameMetadata struct
 */
std::string FrameMetadata::to_string()
{
	std::string res = "Time: " + std::to_string(time) + ", " +
			  "Clock: " + std::to_string(clock) + ", " +
			  "Sequence #:" + std::to_string(sequence);

	return res;
}

/*
 * Start streaming from the camera
 */
void Camera::start()
{
	if (fd == -1) {
		throw std::runtime_error("Device is not open");
	}

	ready_buffers();

#if PYTHON
	// Import NumPy now, so that it does not need to be done when creating
	// the first NumPy array for a requested frame
	py::module_(py::module_::import("numpy"));
#endif

	enum v4l2_buf_type type;
	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	if (0 != ioctl(fd, VIDIOC_STREAMON, &type)) {
		unmap();
		throw V4L2Exception("Failed to start streaming", errno);
	}

	// Update format to make sure it is fully up to date
	update_format();

	buffer_thread = std::thread(&Camera::buffer_manager, this);

	streaming = true;
}

/*
 * Stop streaming from the camera
 */
void Camera::stop()
{
	if (fd == -1) {
		throw std::runtime_error("Device is not open");
	}

	streaming = false;
	buffer_thread.join();

	enum v4l2_buf_type type;
	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	if (0 != ioctl(fd, VIDIOC_STREAMOFF, &type)) {
		DPRINT("VIDIOC_STREAMOFF");
		throw std::runtime_error("Failed to stop streaming");
	}
	unmap();
}

#ifdef PYTHON
std::tuple<FrameMetadata, py::array> Camera::get_frame(uint32_t timeout,
						       bool buffered)
#else
std::tuple<FrameMetadata, cv::Mat> Camera::get_frame(uint32_t timeout,
						     bool buffered)
#endif
{
	if (!streaming) {
		throw std::runtime_error("Device is not streaming");
	}

	std::unique_lock<std::mutex> lock(frame_lock);

	auto closure = [&] { return frames->items() > 0; };

	if (timeout == 0) {
// Python does it's own signal handling so SIGINT eg. Ctrl-C will not propergate
// and abort the wait like in C++ therefore we need to check once in a while if
// a error signal has been sent, and abort.
#ifdef PYTHON
		auto duration = std::chrono::seconds(1);
		while (!frame_bell.wait_for(lock, duration, closure)) {
			// Stop if we get error signal from Python, eg. Ctrl-C
			if (PyErr_CheckSignals() != 0) {
				throw py::error_already_set();
			}
		}
#else
		frame_bell.wait(lock, [&] { return frames->items() > 0; });
#endif
	} else {
#ifdef PYTHON
		auto duration = std::chrono::seconds(1);
		bool ready = false;

		for (uint32_t i = 0; i < timeout; i++) {
			ready = frame_bell.wait_for(lock, duration, closure);
			// Stop if we get error signal from Python, eg. Ctrl-C
			if (PyErr_CheckSignals() != 0) {
				throw py::error_already_set();
			}
			if (ready) {
				break;
			}
		}

		if (!ready) {
			throw TimeoutException();
		}
#else
		auto duration = std::chrono::seconds(timeout);
		bool ready = frame_bell.wait_for(lock, duration, [&] {
			return frames->items() > 0;
		});

		if (!ready) {
			throw TimeoutException();
		}
#endif
	}

	struct v4l2_buffer *frame;

	if (buffered) {
		if (frames->frames_dropped && overflow_exception) {
			throw DroppedFrameException();
		}
		frame = frames->pop();
	} else {
		frame = frames->pop_latest();
	}

#ifdef PYTHON
	// array_t copies the data
	py::array result = py::array_t<uint8_t>(
		// We use expected imagesize instead of bytesused,
		// since Gstreamer (v4l2sink) seems to not set the
		// correct bytesused and instead sets it to buffersize.
		streaming_format.fmt.pix.sizeimage,
		static_cast<uint8_t *>(buffers[frame->index].start));

	if (pix_size == BITS16) {
		if (big_endian) {
			result = result.view(">u2");
		} else {
			result = result.view("<u2");
		}
	}
#else
	int height = static_cast<int>(streaming_format.fmt.pix.height);
	int width = static_cast<int>(streaming_format.fmt.pix.width);

	uint32_t size = streaming_format.fmt.pix.sizeimage;

	int32_t type;
	if (pix_size == BITS16) {
		type = CV_16U;
	} else {
		uint32_t frame_size = static_cast<uint32_t>(width * height);
		if (size % frame_size != 0) {
			throw V4L2Exception("Frame size does not match number "
					    "expected pixels");
		}
		type = CV_MAKETYPE(CV_8U, static_cast<int>(size / frame_size));
	}
	auto result = cv::Mat(height, width, type);
	std::memcpy(result.data, buffers[frame->index].start, size);
#endif

	FrameMetadata metadata;
	metadata.sequence = frame->sequence;

	metadata.time = static_cast<double>(frame->timestamp.tv_sec);
	metadata.time += frame->timestamp.tv_usec / 1000000.0;

	if (frame->flags & V4L2_BUF_FLAG_TIMESTAMP_MONOTONIC) {
		metadata.clock = CLOCK_MONOTONIC;
	} else {
		metadata.clock = CLOCK_REALTIME;
	}

	lock.unlock();

// Currently only reshape for Python
#ifdef PYTHON
	int height = static_cast<int>(streaming_format.fmt.pix.height);
	int width = static_cast<int>(streaming_format.fmt.pix.width);

	// TODO for some formats we might not want to shape the array
	// Using -1 as the last dimension will let it autosize
	std::vector<int> shape{ height, width, -1 };
	result = result.reshape(shape);
#endif

	return { metadata, result };
}

/*
 * FORMATS
 */
std::unique_ptr<Format> Camera::get_format()
{
	auto current_format = read_format();

	return std::unique_ptr<Format>(new SinglePlaneFormat(
		&current_format.fmt.pix, V4L2_BUF_TYPE_VIDEO_CAPTURE));
}

std::unique_ptr<Format> Camera::set_format(Format &format)
{
	auto current_format = read_format();

	if (format.type == V4L2_BUF_TYPE_VIDEO_CAPTURE) {
		auto tmp = static_cast<SinglePlaneFormat &>(format);

		current_format.type = format.type;
		current_format.fmt.pix.width = tmp.width;
		current_format.fmt.pix.height = tmp.height;
		current_format.fmt.pix.pixelformat = tmp.pixelformat.get_code();
		current_format.fmt.pix.field = tmp.field;
		current_format.fmt.pix.bytesperline = tmp.bytesperline;

		// TODO check flags before setting these
		current_format.fmt.pix.sizeimage = tmp.sizeimage;
		current_format.fmt.pix.colorspace = tmp.colorspace;

		// TODO does priv need to be true to set the remaining fields?
		current_format.fmt.pix.priv = tmp.priv;
		current_format.fmt.pix.flags = tmp.flags.flags;
		current_format.fmt.pix.quantization = tmp.quantization;
		current_format.fmt.pix.xfer_func = tmp.xfer_func;
	} else {
		throw V4L2Exception(
			"set_format does not support this buffer type");
	}

	if (ioctl(fd, VIDIOC_S_FMT, &current_format)) {
		throw V4L2Exception("Failed to set format", errno);
	}

	if (current_format.type == V4L2_BUF_TYPE_VIDEO_CAPTURE) {
		return std::unique_ptr<Format>(new SinglePlaneFormat(
			&current_format.fmt.pix, V4L2_BUF_TYPE_VIDEO_CAPTURE));
	}

	throw V4L2Exception("set_format does not support this buffer type");
}

std::unique_ptr<Format> Camera::set_format(std::string &name, bool big_endian)
{
	auto current_format = read_format();
	if (big_endian) {
		name += "_BE";
	}

	update_formats();
	auto it = formats.find(name);

	if (it == formats.end()) {
		throw V4L2Exception("Could not find format: " + name);
	}

	auto format = it->second;

	bool restart_stream = false;
	if (streaming) {
		stop();
	}

	if (ioctl(fd, VIDIOC_G_FMT, &current_format)) {
		throw V4L2Exception("Failed to get format", errno);
	}

	current_format.fmt.pix.pixelformat = format.pixelformat.get_code();

	auto old_default = get_crop_default();
	auto selection = get_crop();

	if (ioctl(fd, VIDIOC_S_FMT, &current_format)) {
		if (restart_stream) {
			start();
		}
		throw V4L2Exception("Failed to set format", errno);
	}

	update_selection(selection, old_default, get_crop_default());

	if (restart_stream) {
		start();
	}
	return std::unique_ptr<Format>(new SinglePlaneFormat(
		&current_format.fmt.pix, V4L2_BUF_TYPE_VIDEO_CAPTURE));
}

/*
 * FRAMERATE
 */
std::unique_ptr<FrameRate> Camera::get_framerates()
{
	auto current_format = read_format();

	return enum_framerates(current_format.fmt.pix.pixelformat,
			       current_format.fmt.pix.width,
			       current_format.fmt.pix.height);
}

std::unique_ptr<FrameRate> Camera::get_framerates(uint32_t width,
						  uint32_t height)
{
	auto current_format = read_format();

	return enum_framerates(current_format.fmt.pix.pixelformat, width,
			       height);
}

std::unique_ptr<FrameRate> Camera::get_framerates(uint32_t width,
						  uint32_t height,
						  std::string &format,
						  bool big_endian)
{
	auto pix = PixelFormat(format, big_endian);

	return enum_framerates(pix.get_code(), width, height);
}

std::unique_ptr<FrameRate>
Camera::enum_framerates(uint32_t pixelformat, uint32_t width, uint32_t height)
{
	struct v4l2_frmivalenum frenum = {
		.index = 0,
		.pixel_format = pixelformat,
		.width = width,
		.height = height,
	};

	if (ioctl(fd, VIDIOC_ENUM_FRAMEINTERVALS, &frenum) != 0) {
		throw V4L2Exception("Could not enumerate framerates", errno);
	}

	if (frenum.type == V4L2_FRMIVAL_TYPE_DISCRETE) {
		double fps = static_cast<double>(frenum.discrete.denominator) /
			     frenum.discrete.numerator;
		std::vector<double> values = { fps };

		frenum.index++;
		while (ioctl(fd, VIDIOC_ENUM_FRAMEINTERVALS, &frenum) == 0) {
			fps = static_cast<double>(frenum.discrete.denominator) /
			      frenum.discrete.numerator;
			values.push_back(fps);
			frenum.index++;
		}
		if (errno != EINVAL) {
			throw V4L2Exception(
				"Got error while enumerating discrete framerates",
				errno);
		}

		auto val = new DiscreteFrameRate(values);

		return std::unique_ptr<FrameRate>(val);
	}

	// Swap min -> max since V4L2 is frame intervals and we prefer FPS
	double min = static_cast<double>(frenum.stepwise.max.denominator) /
		     frenum.stepwise.max.numerator;
	double max = static_cast<double>(frenum.stepwise.min.denominator) /
		     frenum.stepwise.min.numerator;

	if (frenum.type == V4L2_FRMIVAL_TYPE_CONTINUOUS) {
		auto val = new ContinuousFrameRate(min, max);

		return std::unique_ptr<FrameRate>(val);
	} else {
		double step =
			static_cast<double>(frenum.stepwise.step.denominator) /
			frenum.stepwise.step.numerator;
		auto val = new StepwiseFrameRate(min, max, step);

		return std::unique_ptr<FrameRate>(val);
	}
}

double Camera::get_framerate()
{
	struct v4l2_streamparm parm = {
		.type = V4L2_BUF_TYPE_VIDEO_CAPTURE,
	};

	if (ioctl(fd, VIDIOC_G_PARM, &parm) != 0) {
		throw V4L2Exception("Could not query framerate parameters",
				    errno);
	}

	auto frametime = parm.parm.capture.timeperframe;
	return static_cast<double>(frametime.denominator) / frametime.numerator;
}

double Camera::set_framerate(double value)
{
	uint32_t num = 100000;
	uint32_t den = static_cast<uint32_t>(value * num);

	struct v4l2_streamparm parm = {
		.type = V4L2_BUF_TYPE_VIDEO_CAPTURE,
		.parm = {
			.capture = {
				.timeperframe = {
					.numerator = num,
					.denominator = den
				},
			},
		},
	};

	if (ioctl(fd, VIDIOC_S_PARM, &parm) != 0) {
		throw V4L2Exception("Could not set framerate parameters",
				    errno);
	}

	auto frametime = parm.parm.capture.timeperframe;
	return static_cast<double>(frametime.denominator) / frametime.numerator;
}

/*
 * Private
 */
void scale_rect(Rectangle &rect, const Rectangle &old_default,
		const Rectangle &new_default)
{
	if (old_default.width != new_default.width) {
		double scale_width = static_cast<double>(new_default.width) /
				     old_default.width;
		rect.left = std::max(static_cast<int>(rect.left * scale_width),
				     new_default.left);
		rect.width = static_cast<uint32_t>(rect.width * scale_width);
	}
	if (old_default.height != new_default.height) {
		double scale_height = static_cast<double>(new_default.height) /
				      old_default.height;
		rect.top = std::max(static_cast<int>(rect.top * scale_height),
				    new_default.top);
		rect.height = static_cast<uint32_t>(rect.height * scale_height);
	}
}

#ifdef QTEC_HEADER
void Camera::update_selection(std::vector<Rectangle> selection,
			      const Rectangle &old_default,
			      const Rectangle &new_default)
#else
void Camera::update_selection(Rectangle selection, const Rectangle &old_default,
			      const Rectangle &new_default)
#endif
{
	if (old_default == new_default) {
		return;
	}

#ifdef QTEC_HEADER
	if (selection.size() == 1 && old_default == selection[0]) {
		set_crop({ get_crop_default() });
		return;
	}
	for (auto &rect : selection) {
		scale_rect(rect, old_default, new_default);
	}
#else
	if (old_default == selection) {
		set_crop(get_crop_default());
		return;
	}

	scale_rect(selection, old_default, new_default);
#endif
	set_crop(selection);
}

/*
 * INITIALIZATION
 */
void Camera::init_mmap()
{
	if (mmaped) {
		throw V4L2Exception("Internal error - Already mapped memory");
	}

	struct v4l2_requestbuffers reqBuf;

	CLEAR(reqBuf);

	reqBuf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	reqBuf.memory = V4L2_MEMORY_MMAP;

	// Default to requesting 10 buffers for userspace
	userspace_buffers = req_usr_buffers.value_or(10);
	driver_buffers = req_drv_buffers;

	reqBuf.count = userspace_buffers + driver_buffers;

	if (ioctl(fd, VIDIOC_REQBUFS, &reqBuf) != 0) {
		throw V4L2Exception("Failed to request buffers", errno);
	}

	// Check if we got enough buffers to continue
	if (reqBuf.count < userspace_buffers + driver_buffers) {
		std::cerr << "Got fewer V4L2 buffers than expected"
			  << std::endl;

		if (reqBuf.count < 5) {
			V4L2Exception("Got too few V4L2 buffers (<5)");
		} else {
			// If the user set a specific amount of buffers we won't
			// continue when we can't fulfill that request
			if (req_usr_buffers) {
				throw V4L2Exception(
					"Did not get enough V4L2 "
					"buffers to fulfill the requested "
					"amount of userspace buffers, maybe try"
					" with a lower amount?");
			}

			userspace_buffers =
				std::min(userspace_buffers, reqBuf.count - 2);
			driver_buffers = reqBuf.count - userspace_buffers;
		}
		std::cerr << "Continuing with smaller buffering, userspace: "
			  << userspace_buffers << ", driver: " << driver_buffers
			  << std::endl;
	}

	buffer *newBuffers = new buffer[reqBuf.count]();

	struct v4l2_buffer buf;

	for (uint32_t i = 0; i < reqBuf.count; i++) {
		CLEAR(buf);

		buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
		buf.memory = V4L2_MEMORY_MMAP;
		buf.index = i;

		if (ioctl(fd, VIDIOC_QUERYBUF, &buf) != 0) {
			throw V4L2Exception("Failed to query V4L2 buffer",
					    errno);
		}

		newBuffers[i].length = buf.length;
		newBuffers[i].start =
			mmap(NULL, buf.length, PROT_READ | PROT_WRITE,
			     MAP_SHARED, fd, buf.m.offset);
	}

	buffers = newBuffers;

	mmaped = true;
}

void Camera::ready_buffers()
{
	struct v4l2_buffer buf;
	init_mmap();

	// We keep one buffer dequeued to avoid a null check in the
	// mainloop
	struct v4l2_buffer *userspace =
		new struct v4l2_buffer[userspace_buffers];

	for (uint32_t i = 0; i < userspace_buffers; ++i) {
		CLEAR(userspace[i]);
		userspace[i].index = i;
		userspace[i].type = device_type;
		userspace[i].memory = V4L2_MEMORY_MMAP;
	}

	frames = std::unique_ptr<RingBuffer>(
		new RingBuffer(*this, userspace_buffers, userspace));

	for (uint32_t i = 0; i < driver_buffers; ++i) {
		CLEAR(buf);

		// Index starting from where we left with userspace ringbuffer
		buf.index = i + userspace_buffers;
		buf.type = device_type;
		buf.memory = V4L2_MEMORY_MMAP;

		if (ioctl(fd, VIDIOC_QBUF, &buf) != 0) {
			DPRINT("VIDIOC_QBUF");
			throw V4L2Exception("Failed to queue V4L2 buffer",
					    errno);
		}
	}
}

void Camera::unmap()
{
	if (!mmaped) {
		throw V4L2Exception("Internal error - memory not mapped");
	}

	struct v4l2_requestbuffers reqBuf;

	CLEAR(reqBuf);
	reqBuf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	reqBuf.memory = V4L2_MEMORY_MMAP;
	reqBuf.count = 0;

	if (ioctl(fd, VIDIOC_REQBUFS, &reqBuf) != 0) {
		DPRINT(strerror(errno));
	}

	for (uint32_t i = 0; i < driver_buffers + userspace_buffers; i++) {
		munmap(buffers[i].start, buffers[i].length);
	}
	delete buffers;
	buffers = NULL;
	mmaped = false;
}

/*
 * Manager function / thread
 */
void Camera::buffer_manager()
{
	int ret;
	fd_set fds;
	struct timeval tv;
	struct v4l2_buffer buf;

	while (streaming) {
		// Wait (with timeout) until device has a frame ready
		do {
			FD_ZERO(&fds);
			FD_SET(fd, &fds);

			/* Timeout. */
			tv.tv_sec = 0;
			tv.tv_usec = 20000;

			ret = select(fd + 1, &fds, NULL, NULL, &tv);
		} while ((ret == -1 && (errno == EINTR)));

		if (ret == 0) {
			// Timeout, so we try again
			continue;
		} else if (ret == -1) {
			throw V4L2Exception("Got error on select()", errno);
		}

		CLEAR(buf);
		buf.type = device_type;
		buf.memory = V4L2_MEMORY_MMAP;

		if (ioctl(fd, VIDIOC_DQBUF, &buf) != 0) {
			throw V4L2Exception("Failed to dequeue buffer", errno);
		}

		std::unique_lock<std::mutex> lock(frame_lock);

		frames->insert(buf);

		//frame_lock.unlock();
		frame_bell.notify_one();
	}
}

void Camera::RingBuffer::insert(v4l2_buffer &buffer)
{
	if (full) {
		dropped++;
		frames_dropped = true;

		pop();
	}

	increment_end();

	// Queue previous buffer
	if (ioctl(cam.fd, VIDIOC_QBUF, buffers + end)) {
		throw V4L2Exception("Failed to queue buffer", errno);
	}

	// If we reach start, we have dropped a frame
	full = start == end;

	buffers[end] = buffer;
}

void Camera::RingBuffer::skip(uint32_t count)
{
	uint32_t itms = items();
	if (itms <= count) {
		start = end;
		dropped += itms;
		full = false;
	} else {
		increment_start(count);
		dropped += count;
	}
	frames_dropped = false;
}

struct v4l2_buffer *Camera::RingBuffer::pop()
{
	increment_start();

	full = false;

	return buffers + start;
}

struct v4l2_buffer *Camera::RingBuffer::pop_latest()
{
	uint32_t itms = items();

	dropped += itms - 1;

	start = end;

	full = false;

	frames_dropped = false;

	return buffers + end;
}

inline void Camera::RingBuffer::increment_start(uint32_t count)
{
	start += count;
	if (start >= size) {
		start -= size;
	}
}

inline void Camera::RingBuffer::increment_end(uint32_t count)
{
	end += count;
	if (end >= size) {
		end -= size;
	}
}

inline uint32_t Camera::RingBuffer::items()
{
	if (full) {
		return size;
	}

	int32_t res = static_cast<int>(end - start) % static_cast<int>(size);

	return res >= 0 ? static_cast<uint32_t>(res)
			: static_cast<uint32_t>(res + static_cast<int>(size));
}
} // namespace qamlib
