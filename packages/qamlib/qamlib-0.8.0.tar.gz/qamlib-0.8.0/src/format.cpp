// SPDX-License-Identifier: LGPL-2.0
/*
 * format.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include <vector>

#include "format.h"

namespace qamlib
{
/*
 * PixelFormat
 */
std::string PixelFormat::get_fourcc() const
{
	return fourcc;
}

void PixelFormat::set_fourcc(std::string &new_fourcc)
{
	if (new_fourcc.size() > 4) {
		throw V4L2Exception("PixelFormat name too long: " +
				    std::to_string(new_fourcc.size()));
	}
	fourcc = new_fourcc;

	// Strip trailing spaces
	for (size_t i = 1; i <= fourcc.size(); i++) {
		size_t elem = fourcc.size() - i;
		if (fourcc[elem] == ' ') {
			fourcc.erase(elem, 1);
		} else {
			break;
		}
	}
}

uint32_t PixelFormat::get_code() const
{
	uint32_t res = 0;

	for (size_t i = 0; i < 4; i++) {
		// Use spaces to fill up to 4 characters
		if (i < fourcc.size()) {
			res |= static_cast<uint32_t>(fourcc[i] << (i * 8));
		} else {
			res |= static_cast<uint32_t>(' ' << (i * 8));
		}
	}

	if (big_endian) {
		res |= static_cast<uint32_t>(1 << 31);
	}

	return res;
}

std::string PixelFormat::to_string() const
{
	if (big_endian) {
		return fourcc + "_BE";
	} else {
		return fourcc;
	}
}

/*
 * ImageFormatFlags
 */
std::string ImageFormatFlags::to_string() const
{
	std::string res = "<";
	std::vector<std::string> active;

	if (compressed()) {
		active.push_back("compressed");
	}
	if (emulated()) {
		active.push_back("emulated");
	}
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
	if (continuous_bytestream()) {
		active.push_back("continuous_bytestream");
	}
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
	if (dyn_resolution()) {
		active.push_back("dyn_resolution");
	}
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 9, 0)
	if (enc_cap_frame_interval()) {
		active.push_back("enc_cap_frame_interval");
	}
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
	if (csc_colorspace()) {
		active.push_back("csc_colorspace");
	}
	if (csc_xfer_func()) {
		active.push_back("csc_xfer_func");
	}
	if (csc_ycbcr_enc()) {
		active.push_back("csc_ycbcr_enc");
	}
	if (csc_hsv_enc()) {
		active.push_back("csc_hsv_enc");
	}
	if (csc_quantization()) {
		active.push_back("csc_quantization");
	}
#endif

	for (size_t i = 1; i < active.size(); i++) {
		res += ", " + active[i];
	}

	res += ">";

	return res;
}

json ImageFormatFlags::to_json() const
{
	return json
	{
		{ "compressed", compressed() }, { "emulated", emulated() },
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
			{ "continuous_bytestream", continuous_bytestream() },
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
			{ "dyn_resolution", dyn_resolution() },
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 9, 0)
			{ "enc_cap_frame_interval", enc_cap_frame_interval() },
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
			{ "csc_colorspace", csc_colorspace() },
			{ "csc_xfer_func", csc_xfer_func() },
			{ "csc_ycbcr_enc", csc_ycbcr_enc() },
			{ "csc_hsv_enc", csc_hsv_enc() },
		{
			"csc_quantization", csc_quantization()
		}
#endif
	};
}

std::string ImageFormat::to_string() const
{
	std::string res = "Index: " + std::to_string(index) +
			  ", Description: " + description +
			  ", Pixelformat: " + pixelformat.to_string() +
			  ", Flags: " + flags.to_string();

	return res;
}

json ImageFormat::to_json() const
{
	return json{ { "index", index },
		     { "description", description },
		     { "pixelformat", pixelformat.to_string() },
		     { "flags", flags.to_json() } };
}

std::string PixelFormatFlags::to_string() const
{
	std::string res = "<";
	std::vector<std::string> active;

	if (premul_alpha()) {
		active.push_back("premul_alpha");
	}
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
	if (set_csc()) {
		active.push_back("set_csc");
	}
#endif

	for (size_t i = 1; i < active.size(); i++) {
		res += ", " + active[i];
	}

	res += ">";

	return res;
}

json PixelFormatFlags::to_json() const
{
	return json{ { "premul_alpha", premul_alpha() }
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
		     ,
		     { "set_csc", set_csc() }
#endif
	};
}

std::string colorspace_to_string(const v4l2_colorspace cs)
{
	switch (cs) {
	case V4L2_COLORSPACE_DEFAULT:
		return "Default";
	case V4L2_COLORSPACE_SMPTE170M:
		return "SMPTE170M";
	case V4L2_COLORSPACE_REC709:
		return "REC709";
	case V4L2_COLORSPACE_SRGB:
		return "SRGB";
	case V4L2_COLORSPACE_OPRGB:
		return "OPRGB";
	case V4L2_COLORSPACE_BT2020:
		return "BT2020";
	case V4L2_COLORSPACE_DCI_P3:
		return "DCI P3";
	case V4L2_COLORSPACE_SMPTE240M:
		return "SMPTE240M";
	case V4L2_COLORSPACE_470_SYSTEM_M:
		return "470 System M";
	case V4L2_COLORSPACE_470_SYSTEM_BG:
		return "470 System BG";
	case V4L2_COLORSPACE_JPEG:
		return "JPEG";
	case V4L2_COLORSPACE_RAW:
		return "Raw";
	default:
		return "Unkown";
	}
}

std::string field_to_string(const v4l2_field field)
{
	switch (field) {
	case V4L2_FIELD_ANY:
		return "Any";
	case V4L2_FIELD_NONE:
		return "None";
	case V4L2_FIELD_TOP:
		return "Top";
	case V4L2_FIELD_BOTTOM:
		return "Bottom";
	case V4L2_FIELD_INTERLACED:
		return "Interlaced";
	case V4L2_FIELD_SEQ_TB:
		return "Sequencial Top/Bottom";
	case V4L2_FIELD_SEQ_BT:
		return "Sequencial Bottom/Top";
	case V4L2_FIELD_ALTERNATE:
		return "Alternating";
	case V4L2_FIELD_INTERLACED_TB:
		return "Interlaced Top/Bottom";
	case V4L2_FIELD_INTERLACED_BT:
		return "Interlaced Bottom/Top";
	default:
		return "Unkown";
	}
}

std::string SinglePlaneFormat::to_string() const
{
	std::string res = "Height: " + std::to_string(height) +
			  ", Width: " + std::to_string(width) +
			  ", Pixel format: " + pixelformat.to_string() +
			  ", Colorspace: " + colorspace_to_string(colorspace) +
			  ", Field: " + field_to_string(field) +
			  ", Bytes per line: " + std::to_string(bytesperline) +
			  ", Size image: " + std::to_string(sizeimage) +
			  ", Priv: " + (priv ? "True" : "False") +
			  ", Flags: " + flags.to_string();

	return res;
}

json SinglePlaneFormat::to_json() const
{
	return json{ { "height", height },
		     { "width", width },
		     { "pixelformat", pixelformat.to_string() },
		     { "colorspace", colorspace_to_string(colorspace) },
		     { "field", field_to_string(field) },
		     { "bytes_per_line", bytesperline },
		     { "size", sizeimage },
		     { "priv", (priv ? "true" : "false") },
		     { "flags", flags.to_json() } };
}
} // namespace qamlib
