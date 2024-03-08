// SPDX-License-Identifier: LGPL-2.0
/*
 * streaming_device.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <atomic>
#include <map>

#include "device.h"

namespace qamlib
{
class StreamingDevice : public Device {
    protected:
	StreamingDevice(const std::string &device, v4l2_buf_type device_type,
			uint32_t needed_cap)
		: Device(device, device_type, needed_cap)
	{
	}

	std::map<std::string, ImageFormat> formats;

	std::atomic<bool> streaming = false;

	// Used for all set/get of format and for knowing the currently used
	// format is
	struct v4l2_format streaming_format;
	PixelSize pix_size = BITS8;
	bool big_endian = false;

	/*
	 * Private format helper functions
	 */
	struct v4l2_format read_format();

	void update_format();

	void update_formats();

    public:
	virtual void start();
	virtual void stop();

	/*
	 * Get current camera resolution
	 */
	std::tuple<uint32_t, uint32_t> get_resolution();

	/*
	 * Set camera resolution
	 * Returns actual new resolution
	 */
	std::tuple<uint32_t, uint32_t> set_resolution(uint32_t newWidth,
						      uint32_t newHeight);

	/*
	 * CROPPING
	 */
#ifdef QTEC_HEADER
	std::vector<Rectangle> get_crop();
#else
	Rectangle get_crop();
#endif

	void set_crop(int left, int top, uint32_t width, uint32_t height);
	void set_crop(Rectangle rectangle);

#ifdef QTEC_HEADER
	void set_crop(std::vector<Rectangle> rectangles);
#endif

	Rectangle get_crop_default();
	Rectangle get_crop_bounds();

	/*
	 * FORMATS
	 */
	std::map<std::string, ImageFormat> list_formats();
};
} // namespace qamlib
