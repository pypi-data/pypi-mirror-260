// SPDX-License-Identifier: LGPL-2.0
/*
 * format.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <stdint.h>
#include <string>

#include <linux/version.h>

#include <nlohmann/json.hpp>

#include "utils.h"

using json = nlohmann::json;

namespace qamlib
{
class PixelFormat {
	std::string fourcc;

    public:
	bool big_endian = false;

	PixelFormat(uint32_t code)
	{
		std::string tmp;
		uint32_t last_bit = static_cast<uint32_t>(1 << 31);
		big_endian = code >= last_bit;

		// Unset potential BE bit
		code &= ~last_bit;

		tmp += static_cast<char>(code);
		tmp += static_cast<char>(code >> 8);
		tmp += static_cast<char>(code >> 16);
		tmp += static_cast<char>(code >> 24);

		set_fourcc(tmp);
	}

	PixelFormat(std::string &fourcc, bool big_endian)
		: big_endian(big_endian)
	{
		set_fourcc(fourcc);
	}

	PixelFormat(std::string &fourcc)
	{
		if (fourcc.size() > 3) {
			int res = fourcc.compare(fourcc.size() - 3, 3, "_BE");
			big_endian = res == 0;
		}

		if (big_endian) {
			fourcc.erase(fourcc.size() - 4, 3);
		}

		set_fourcc(fourcc);
	}

	std::string get_fourcc() const;

	void set_fourcc(std::string &new_name);

	uint32_t get_code() const;

	std::string to_string() const;
};

class ImageFormatFlags {
    public:
	uint32_t flags;

	ImageFormatFlags(uint32_t flags) : flags(flags)
	{
	}

	flag_function(compressed, V4L2_FMT_FLAG_COMPRESSED);
	flag_function(emulated, V4L2_FMT_FLAG_EMULATED);
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
	flag_function(continuous_bytestream,
		      V4L2_FMT_FLAG_CONTINUOUS_BYTESTREAM);
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
	flag_function(dyn_resolution, V4L2_FMT_FLAG_DYN_RESOLUTION);
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 9, 0)
	flag_function(enc_cap_frame_interval,
		      V4L2_FMT_FLAG_ENC_CAP_FRAME_INTERVAL);
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
	flag_function(csc_colorspace, V4L2_FMT_FLAG_CSC_COLORSPACE);
	flag_function(csc_xfer_func, V4L2_FMT_FLAG_CSC_XFER_FUNC);
	flag_function(csc_ycbcr_enc, V4L2_FMT_FLAG_CSC_YCBCR_ENC);
	flag_function(csc_hsv_enc, V4L2_FMT_FLAG_CSC_HSV_ENC);
	flag_function(csc_quantization, V4L2_FMT_FLAG_CSC_QUANTIZATION);
#endif

	// Pretty string representation
	std::string to_string() const;

	json to_json() const;
};

class ImageFormat {
    public:
	uint32_t index;
	ImageFormatFlags flags;
	std::string description;
	// Maybe have a translation layer, for pixelformat?
	PixelFormat pixelformat;

	ImageFormat(struct v4l2_fmtdesc *fmt)
		: index(fmt->index), flags(fmt->flags),
		  description(reinterpret_cast<char *>(fmt->description)),
		  pixelformat(fmt->pixelformat)
	{
	}

	std::string to_string() const;

	json to_json() const;
};

class PixelFormatFlags {
    public:
	uint32_t flags;

	PixelFormatFlags(uint32_t flags) : flags(flags)
	{
	}

	flag_function(premul_alpha, V4L2_PIX_FMT_FLAG_PREMUL_ALPHA);

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
	flag_function(set_csc, V4L2_PIX_FMT_FLAG_SET_CSC);
#endif
	//toggle_flag_function(set_csc, V4L2_PIX_FMT_FLAG_SET_CSC);

	// Pretty string representation
	std::string to_string() const;

	json to_json() const;
};

class Format {
    public:
	v4l2_buf_type type;

	Format(v4l2_buf_type type) : type(type)
	{
	}

	// This is to let Pybind11 do automatic downcasting
	virtual ~Format() = default;
};

std::string colorspace_to_string(const v4l2_colorspace cs);
std::string field_to_string(const v4l2_field field);

class SinglePlaneFormat : public Format {
    public:
	uint32_t width;
	uint32_t height;
	PixelFormat pixelformat;
	v4l2_field field;
	uint32_t bytesperline;
	uint32_t sizeimage;
	v4l2_colorspace colorspace;
	bool priv;
	PixelFormatFlags flags;

	// TODO Y'CbCr and HSV encoding enum union

	v4l2_quantization quantization;
	v4l2_xfer_func xfer_func;

	SinglePlaneFormat(struct v4l2_pix_format *fmt, v4l2_buf_type type)
		: Format(type), width(fmt->width), height(fmt->height),
		  pixelformat(fmt->pixelformat),
		  field(static_cast<v4l2_field>(fmt->field)),
		  bytesperline(fmt->bytesperline), sizeimage(fmt->sizeimage),
		  colorspace(static_cast<v4l2_colorspace>(fmt->colorspace)),
		  priv(fmt->priv == V4L2_PIX_FMT_PRIV_MAGIC), flags(fmt->flags),
		  quantization(
			  static_cast<v4l2_quantization>(fmt->quantization)),
		  xfer_func(static_cast<v4l2_xfer_func>(fmt->xfer_func))
	{
	}

	std::string to_string() const;

	json to_json() const;
};
} // namespace qamlib
