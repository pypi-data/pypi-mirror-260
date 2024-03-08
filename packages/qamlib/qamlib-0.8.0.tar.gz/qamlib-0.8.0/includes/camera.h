// SPDX-License-Identifier: LGPL-2.0
/*
 * camera.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <atomic>
#include <condition_variable>
#include <map>
#include <mutex>
#include <optional>
#include <string>
#include <thread>
#include <tuple>
#include <unistd.h>
#include <vector>

#include "control.h"
#include "format.h"
#include "framerate.h"
#include "streaming_device.h"

#if PYTHON
	#include <pybind11/numpy.h>
namespace py = pybind11;
#else
	#include <opencv2/core/mat.hpp>
#endif

// Print when debug is enabled
#ifdef DEBUG
	#include <stdio.h>
	#define DPRINT(str) perror(str)
#else
	#define DPRINT(str) /* Don't do anything */
#endif

namespace qamlib
{
/**
 * Metadata for a frame.
 * time is in machine clock with clock specifying which clock is used
 * sequence is the framenumber since the stream was started
 */
class FrameMetadata {
    public:
	double time;
	clockid_t clock;
	uint32_t sequence;

	std::string to_string();
};

/**
 * Scale rectangle based on new default rectangle
 */
void scale_rect(Rectangle &rect, const Rectangle &old_default,
		const Rectangle &new_default);

/**
 * @brief Class for interacting with a V4L2 capture device
 */
class Camera : public StreamingDevice {
    public:
	Camera(const std::string &device,
	       std::optional<uint32_t> buffers = std::nullopt,
	       bool overflow_exception = true)
		: StreamingDevice(device, V4L2_BUF_TYPE_VIDEO_CAPTURE,
				  V4L2_CAP_VIDEO_CAPTURE),
		  req_usr_buffers(buffers),
		  overflow_exception(overflow_exception)
	{
		if (req_usr_buffers && req_usr_buffers.value() < 1) {
			throw V4L2Exception(
				"Can't function with no userspace buffers");
		}
	}

	Camera(uint32_t device_num,
	       std::optional<uint32_t> buffers = std::nullopt,
	       bool overflow_exception = true)
		: Camera("/dev/video" + std::to_string(device_num), buffers,
			 overflow_exception)
	{
	}

#ifdef QTEC_HEADER
	Camera(bool overflow_exception = true)
		: Camera("/dev/qtec/video0", std::nullopt, overflow_exception)
	{
	}
#endif

	~Camera() override
	{
		if (streaming) {
			stop();
		}
	}

	/**
	 * Start streaming from the camera
	 */
	void start() override;

	/**
	 * Stop streaming from the camera
	 */
	void stop() override;

#ifdef PYTHON
	std::tuple<FrameMetadata, py::array> get_frame(uint32_t timeout = 0,
						       bool buffered = false);
#else
	/**
	 * @brief Get latest frame from the camera as a OpenCV Mat object
	 * @param timeout Time in seconds to wait before throwing a
	 * TimeoutException. If 0 then there is no timeout.
	 *
	 * @param buffered If true then the first frame in the buffer is
	 * returned, if false then the latest frame is returned.
	 */
	std::tuple<struct FrameMetadata, cv::Mat>
	get_frame(uint32_t timeout = 0, bool buffered = false);
#endif

	/*
	 * FORMATS
	 */
	std::unique_ptr<Format> get_format();

	std::unique_ptr<Format> set_format(Format &format);

	std::unique_ptr<Format> set_format(std::string &format,
					   bool big_endian = false);

	/*
	 * FRAMERATE
	 */
	std::unique_ptr<FrameRate> get_framerates();
	std::unique_ptr<FrameRate> get_framerates(uint32_t width,
						  uint32_t height);
	std::unique_ptr<FrameRate> get_framerates(uint32_t width,
						  uint32_t height,
						  std::string &format,
						  bool big_endian = false);

	double get_framerate();

	double set_framerate(double value);

    private:
	// Number of buffers we want for the driver side
	static const uint32_t req_drv_buffers = 5;

	// Optional, number of userspace buffers requested by user
	std::optional<uint32_t> req_usr_buffers;

	// The actual number of buffers we ended up getting when starting the
	// stream
	uint32_t driver_buffers;
	uint32_t userspace_buffers;

	// These are for checking that we are not dropping frames from the
	// driver
	uint32_t next_frame_nr = 0;

	const bool overflow_exception;

	std::thread buffer_thread;

	bool mmaped = false;

	struct buffer {
		void *start;
		size_t length;
	};

	/*
	 * Helper functions
	 */
	void set_format(v4l2_format *fmt);

#ifdef QTEC_HEADER
	void update_selection(std::vector<Rectangle> selection,
			      const Rectangle &old_default,
			      const Rectangle &new_default);
#else
	void update_selection(Rectangle selection, const Rectangle &old_default,
			      const Rectangle &new_default);
#endif

	// Array of the mmapped buffers
	struct buffer *buffers;

	/*
	 * INITIALIZATION
	 */
	void init_mmap();

	void ready_buffers();

	void unmap();

	/*
	 * Private framerate helper functions
	 */
	std::unique_ptr<FrameRate>
	enum_framerates(uint32_t pixelformat, uint32_t width, uint32_t height);

	/*
	 * Manager function / thread
	 */
	void buffer_manager();

	/*
	 * Class used for handling a userspace ringbuffer of V4L2 buffers, with
	 * FIFO semantics (and possible skip). It also keeps track of whether
	 * frames have been dropped (and how many have been skipped/dropped)
	 */
	class RingBuffer {
		Camera &cam;
		uint32_t size;
		struct v4l2_buffer *buffers;
		uint32_t end = 0;
		uint32_t start = 0;
		uint32_t dropped = 0;
		bool full = false;

		// Updates indices
		void increment_start(uint32_t count = 1);
		void increment_end(uint32_t count = 1);

	    public:
		bool frames_dropped = false;

		RingBuffer(Camera &cam, uint32_t size,
			   struct v4l2_buffer *buffers)
			: cam(cam), size(size), buffers(buffers)
		{
		}

		~RingBuffer()
		{
			delete[] buffers;
		}

		void insert(v4l2_buffer &buffer);

		void skip(uint32_t count);

		struct v4l2_buffer *pop();

		struct v4l2_buffer *pop_latest();

		uint32_t items();
	};

	/*
	 * BUFFERS
	 */
	std::mutex frame_lock;
	std::condition_variable frame_bell;

	// Current available V4L2 buffer
	std::unique_ptr<RingBuffer> frames;
};
} // namespace qamlib
