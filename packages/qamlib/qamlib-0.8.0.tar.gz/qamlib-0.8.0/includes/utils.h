// SPDX-License-Identifier: LGPL-2.0
/*
 * utils.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <exception>
#include <string>
#include <string.h>
#include <vector>

// Import here for use in other headers
#if __has_include(<linux/videodev2_qtec.h>)
	#include <linux/videodev2_qtec.h>
	#define QTEC_HEADER 1
	#define MAX_CROP_RECTS 8
#else
	#include <linux/videodev2.h>
#endif

// Macro to ease creation of functions to show singular flags
#define flag_function(name, flag)                                              \
	bool(name)() const                                                     \
	{                                                                      \
		return flags & (flag);                                         \
	}

#define toggle_flag_function(name, flag)                                       \
	void toggle_(name)()                                                   \
	{                                                                      \
		flags ^= (flag);                                               \
	}

// Zero struct
#define CLEAR(x) memset(&(x), 0, sizeof(x))

namespace qamlib
{
/*
 * Custom exception for the camera class
 */
class V4L2Exception : public std::exception {
    public:
	V4L2Exception(const std::string &msg, int err_num)
	{
		message = msg;
		message += " : (" + std::to_string(err_num) + ") ";
		message += strerror(err_num);
	}

	V4L2Exception(const std::string &msg) : message{ msg }
	{
	}

	V4L2Exception(const std::string &name, const std::string &msg)
	{
		message = "(" + name + ") " + msg;
	}

	const char *what() const noexcept override
	{
		return message.c_str();
	}

    private:
	std::string message;
};

class TimeoutException : public std::exception {
    public:
	TimeoutException()
	{
	}

	const char *what() const noexcept override
	{
		return "TimeoutException";
	}
};

class DroppedFrameException : public std::exception {
    public:
	DroppedFrameException()
	{
	}

	const char *what() const noexcept override
	{
		return "DroppedFrameException";
	}
};

std::string name_to_key(const std::string &name);

class Rectangle {
    public:
	int left = 0;
	int top = 0;
	uint32_t width = 0;
	uint32_t height = 0;

	Rectangle()
	{
	}

	Rectangle(int left, int top, uint32_t width, uint32_t height)
		: left(left), top(top), width(width), height(height)
	{
	}

	std::string to_string()
	{
		return "Left: " + std::to_string(left) +
		       ", Top: " + std::to_string(top) +
		       ", Width: " + std::to_string(width) +
		       ", Height: " + std::to_string(height);
	}

	std::vector<int> as_vector()
	{
		// We don't expect to hit width/height > INTMAX
		return { left, top, static_cast<int>(width),
			 static_cast<int>(height) };
	}

	bool operator==(const Rectangle &rhs) const
	{
		return left == rhs.left && top == rhs.top &&
		       width == rhs.width && height == rhs.height;
	}

	bool operator!=(const Rectangle &rhs) const
	{
		return left != rhs.left || top != rhs.top ||
		       width != rhs.width || height != rhs.height;
	}
};

enum PixelSize {
	BITS8,
	BITS16,
};
} // namespace qamlib
