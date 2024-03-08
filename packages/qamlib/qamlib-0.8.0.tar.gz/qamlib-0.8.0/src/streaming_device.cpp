// SPDX-License-Identifier: LGPL-2.0
/*
 * streaming_device.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "streaming_device.h"

namespace qamlib
{
struct v4l2_format StreamingDevice::read_format()
{
	struct v4l2_format fmt {
		.type = device_type,
	};

	if (0 != ioctl(fd, VIDIOC_G_FMT, &fmt)) {
		throw V4L2Exception("Error getting format from V4L2", errno);
	}

	return fmt;
}

void StreamingDevice::update_format()
{
	streaming_format = read_format();

	uint32_t pix = streaming_format.fmt.pix.pixelformat;

	big_endian = false;

	if (pix & static_cast<uint32_t>(1 << 31)) {
		big_endian = true;

		// Unset big endian bit
		pix &= ~(1 << 31);
	}

	switch (pix) {
	case V4L2_PIX_FMT_Y16:
	case V4L2_PIX_FMT_Z16:
#ifdef QTEC_HEADER
	case V4L2_PIX_FMT_BGR48:
	case V4L2_PIX_FMT_RGB48:
	case V4L2_PIX_FMT_QTEC_GREEN16:
#endif
		pix_size = BITS16;
		break;
	default:
		pix_size = BITS8;
		break;
	}
}

void StreamingDevice::update_formats()
{
	struct v4l2_fmtdesc fmt = { .index = 0, .type = device_type };

	formats.clear();

	while (ioctl(fd, VIDIOC_ENUM_FMT, &fmt) >= 0) {
		auto format = ImageFormat(&fmt);
		auto name = format.pixelformat.get_fourcc();
		if (format.pixelformat.big_endian) {
			name += "_BE";
		}
		formats.insert(
			std::pair<std::string, ImageFormat>(name, format));
		fmt.index += 1;
	}
}

void StreamingDevice::start()
{
}

void StreamingDevice::stop()
{
}

/*
 * Get current camera resolution
 */
std::tuple<uint32_t, uint32_t> StreamingDevice::get_resolution()
{
	auto current_format = read_format();

	return { current_format.fmt.pix.width, current_format.fmt.pix.height };
}

/*
 * Set camera resolution
 * Returns actual new resolution
 */
std::tuple<uint32_t, uint32_t>
StreamingDevice::set_resolution(uint32_t newWidth, uint32_t newHeight)
{
	bool restart = false;

	// Make sure 'format' is up to date
	struct v4l2_format current_format = read_format();

	current_format.fmt.pix.width = newWidth;
	current_format.fmt.pix.height = newHeight;

	if (streaming) {
		stop();
		restart = true;
	}

	if (0 != ioctl(fd, VIDIOC_S_FMT, &current_format)) {
		throw V4L2Exception("Error setting format for new resolution",
				    errno);
	}

#if DEBUG
	uint32_t height = current_format.fmt.pix.height;
	uint32_t width = current_format.fmt.pix.width;
	if (width != newWidth || height != newHeight) {
		DPRINT("Failed to get the requested resolution\n");
	}
#endif

	if (restart) {
		start();
	}

	return { current_format.fmt.pix.width, current_format.fmt.pix.height };
}

/*
 * CROPPING
 */

#ifdef QTEC_HEADER
std::vector<Rectangle> StreamingDevice::get_crop()
#else
Rectangle StreamingDevice::get_crop()
#endif
{
	struct v4l2_selection selection = {
		.type = device_type,
		.target = V4L2_SEL_TGT_CROP,
	};

#ifdef QTEC_HEADER
	struct v4l2_ext_rect rects[MAX_CROP_RECTS];
	selection.pr = rects;
	selection.rectangles = MAX_CROP_RECTS;
#endif

	if (ioctl(fd, VIDIOC_G_SELECTION, &selection) != 0) {
		throw V4L2Exception(
			"Selection likely not supported for this device",
			errno);
	}

#ifdef QTEC_HEADER
	// If there is only one crop rectangle, rectangles is set to 0 and the
	// "normal" selection rectangle is populated
	if (selection.rectangles == 0) {
		auto rect = Rectangle(selection.r.left, selection.r.top,
				      selection.r.width, selection.r.height);
		return { rect };
	}

	std::vector<Rectangle> res;
	for (size_t i = 0; i < selection.rectangles; i++) {
		auto rect = selection.pr[i].r;
		auto rectangle =
			Rectangle(rect.left, rect.top, rect.width, rect.height);
		res.push_back(rectangle);
	}

	return res;
#else
	auto rect = Rectangle(selection.r.left, selection.r.top,
			      selection.r.width, selection.r.height);
	return rect;
#endif
}

void StreamingDevice::set_crop(int left, int top, uint32_t width,
			       uint32_t height)
{
	auto rect = Rectangle(left, top, width, height);

	set_crop(rect);
}

void StreamingDevice::set_crop(Rectangle rectangle)
{
	bool restart_stream = false;
	if (streaming) {
		stop();
		restart_stream = true;
	}

	auto [cur_width, cur_height] = get_resolution();
	if (cur_width != rectangle.width || cur_height != rectangle.height) {
		// Set resolution before selection
		set_resolution(rectangle.width, rectangle.height);
	}

	struct v4l2_selection selection = {
		.type = device_type,
		.target = V4L2_SEL_TGT_CROP,
	};
	selection.r.left = rectangle.left;
	selection.r.top = rectangle.top;
	selection.r.width = rectangle.width;
	selection.r.height = rectangle.height;

	if (ioctl(fd, VIDIOC_S_SELECTION, &selection) != 0) {
		if (restart_stream) {
			start();
		}
		throw V4L2Exception("Could not set desired selection", errno);
	}

	if (restart_stream) {
		start();
	}
}

#ifdef QTEC_HEADER
void StreamingDevice::set_crop(std::vector<Rectangle> rectangles)
{
	if (rectangles.size() == 1) {
		set_crop(rectangles[0]);
		return;
	}

	if (rectangles.size() > MAX_CROP_RECTS) {
		throw V4L2Exception(
			"More than 8 crop rectangles not supported");
	}

	bool restart_stream = false;
	if (streaming) {
		stop();
		restart_stream = true;
	}

	uint32_t width = rectangles[0].width;
	uint32_t height = 0;

	// Check for overlapping rectangles, we only check in height, since
	// they should all be at the same left and width.
	for (size_t i = 0; i < rectangles.size(); i++) {
		auto a = rectangles[i];

		// Only check for the remaining part of the list, since we have
		// already checked with the previous rectangles.
		for (size_t j = i + 1; j < rectangles.size(); j++) {
			auto b = rectangles[j];

			// Bottom most point for the rectangles
			int a_bottom = a.top + static_cast<int>(a.height);
			int b_bottom = b.top + static_cast<int>(b.height);

			if (a.top == b.top ||
			    (a.top < b.top && a_bottom > b.top) ||
			    (a.top > b.top && b_bottom > a.top)) {
				throw V4L2Exception("Multi-crop rectangles "
						    "must not overlap");
			}
		}

		// Sum height for the new resolution
		height += a.height;
	}

	auto [cur_width, cur_height] = get_resolution();
	if (cur_width != width || cur_height != height) {
		// Set resolution before selection
		set_resolution(width, height);
	}

	struct v4l2_ext_rect rects[MAX_CROP_RECTS];

	for (size_t i = 0; i < rectangles.size(); i++) {
		rects[i].r.left = rectangles[i].left;
		rects[i].r.top = rectangles[i].top;
		rects[i].r.width = rectangles[i].width;
		rects[i].r.height = rectangles[i].height;
	}

	struct v4l2_selection selection = {
		.type = device_type,
		.target = V4L2_SEL_TGT_CROP,
		.rectangles = static_cast<uint32_t>(rectangles.size()),
		.pr = rects,
	};

	if (ioctl(fd, VIDIOC_S_SELECTION, &selection) != 0) {
		if (restart_stream) {
			start();
		}
		throw V4L2Exception("Could not set desired selection", errno);
	}

	if (restart_stream) {
		start();
	}
}
#endif

Rectangle StreamingDevice::get_crop_default()
{
	struct v4l2_selection selection = {
		.type = device_type,
		.target = V4L2_SEL_TGT_CROP_DEFAULT,
	};

	if (ioctl(fd, VIDIOC_G_SELECTION, &selection) != 0) {
		throw V4L2Exception(
			"Selection likely not supported for this device",
			errno);
	}

	return Rectangle(selection.r.left, selection.r.top, selection.r.width,
			 selection.r.height);
}

Rectangle StreamingDevice::get_crop_bounds()
{
	struct v4l2_selection selection = {
		.type = device_type,
		.target = V4L2_SEL_TGT_CROP_BOUNDS,
	};

	if (ioctl(fd, VIDIOC_G_SELECTION, &selection) != 0) {
		throw V4L2Exception(
			"Selection likely not supported for this device",
			errno);
	}

	return Rectangle(selection.r.left, selection.r.top, selection.r.width,
			 selection.r.height);
}

/*
 * FORMATS
 */
std::map<std::string, ImageFormat> StreamingDevice::list_formats()
{
	update_formats();
	return formats;
}
} // namespace qamlib
