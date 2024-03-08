// SPDX-License-Identifier: LGPL-2.0
/*
 * control.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "control.h"

#include <linux/version.h>
#include <climits>
#include <vector>

#if PYTHON
	#include <pybind11/numpy.h>
namespace py = pybind11;
#else
	#include <opencv2/core/mat.hpp>
#endif

namespace qamlib
{
/*
 * Class for V4L2 control flags.
 */
// Pretty string representation
std::string ControlFlags::to_string() const
{
	std::string res = "<";
	std::vector<std::string> active;

	if (disabled()) {
		active.push_back("disabled");
	}
	if (grabbed()) {
		active.push_back("grabbed");
	}
	if (read_only()) {
		active.push_back("read_only");
	}
	if (update()) {
		active.push_back("update");
	}
	if (inactive()) {
		active.push_back("inactive");
	}
	if (slider()) {
		active.push_back("slider");
	}
	if (write_only()) {
		active.push_back("write_only");
	}
	if (is_volatile()) {
		active.push_back("volatile");
	}
	if (has_payload()) {
		active.push_back("has_payload");
	}
	if (execute_on_write()) {
		active.push_back("execute_on_write");
	}
	if (modify_layout()) {
		active.push_back("modify_layout");
	}

	if (active.size() > 0) {
		res += active[0];
	}

	for (size_t i = 1; i < active.size(); i++) {
		res += ", " + active[i];
	}

	res += ">";

	return res;
}

json ControlFlags::to_json() const
{
	return json{ { "disabled", disabled() },
		     { "grabbed", grabbed() },
		     { "read_only", read_only() },
		     { "update", update() },
		     { "inactive", inactive() },
		     { "slider", slider() },
		     { "write_only", write_only() },
		     { "volatile", is_volatile() },
		     { "has_payload", has_payload() },
		     { "execute_on_write", execute_on_write() },
		     { "modify_layout", modify_layout() } };
}

/*
 * Control class
 */
std::string type_to_string(v4l2_ctrl_type type)
{
	switch (type) {
	case V4L2_CTRL_TYPE_INTEGER:
		return "Int";
	case V4L2_CTRL_TYPE_BOOLEAN:
		return "Bool";
	case V4L2_CTRL_TYPE_MENU:
		return "Menu";
	case V4L2_CTRL_TYPE_INTEGER_MENU:
		return "Int menu";
	case V4L2_CTRL_TYPE_BITMASK:
		return "Bitmask";
	case V4L2_CTRL_TYPE_BUTTON:
		return "Button";
	case V4L2_CTRL_TYPE_INTEGER64:
		return "Int64";
	case V4L2_CTRL_TYPE_STRING:
		return "String";
	case V4L2_CTRL_TYPE_CTRL_CLASS:
		return "Control class";
	case V4L2_CTRL_TYPE_U8:
		return "Uint8";
	case V4L2_CTRL_TYPE_U16:
		return "Uint16";
	case V4L2_CTRL_TYPE_U32:
		return "Uint32";
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 5, 0)
	case V4L2_CTRL_TYPE_AREA:
		return "Area";
#endif
#ifdef QTEC_HEADER
	case V4L2_CTRL_TYPE_TRIG_SEQ:
		return "Trigger sequence";
	case V4L2_CTRL_TYPE_POINT:
		return "Point";
#endif
// Make sure kernel is new enough to haveall the encoding controls
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 14, 0)
	case V4L2_CTRL_TYPE_HDR10_CLL_INFO:
		return "HDR10 CLL info";
	case V4L2_CTRL_TYPE_HDR10_MASTERING_DISPLAY:
		return "HDR10 mastering display";
	case V4L2_CTRL_TYPE_MPEG2_QUANTISATION:
		return "MPEG2 quantization";
	case V4L2_CTRL_TYPE_MPEG2_SEQUENCE:
		return "MPEG2 sequence";
	case V4L2_CTRL_TYPE_MPEG2_PICTURE:
		return "MPEG2 picture";
	case V4L2_CTRL_TYPE_H264_SPS:
		return "H264 SPS";
	case V4L2_CTRL_TYPE_H264_PPS:
		return "H264 PPS";
	case V4L2_CTRL_TYPE_H264_SCALING_MATRIX:
		return "H264 scaling matrix";
	case V4L2_CTRL_TYPE_H264_SLICE_PARAMS:
		return "H264 Slice parameters";
	case V4L2_CTRL_TYPE_H264_DECODE_PARAMS:
		return "H264 decode parameters";
	case V4L2_CTRL_TYPE_H264_PRED_WEIGHTS:
		return "H264 pred weights";
	case V4L2_CTRL_TYPE_FWHT_PARAMS:
		return "FWHT parameters";
	case V4L2_CTRL_TYPE_VP8_FRAME:
		return "VP8 frame";
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 17, 0)
	case V4L2_CTRL_TYPE_VP9_COMPRESSED_HDR:
		return "VP9 compressed HDR";
	case V4L2_CTRL_TYPE_VP9_FRAME:
		return "VP9 frame";
#endif
	default:
		return "Unkown type";
	}
}
std::string Control::to_string() const
{
	std::string res = "ID: " + std::to_string(id) + ", Name: " + name +
			  ", Type: " + type_to_string(type) +
			  ", Flags: " + flags.to_string();

	return res;
}

json Control::to_json() const
{
	return json{ { "id", id },
		     { "name", name },
		     { "type", type_to_string(type) },
		     { "flags", flags.to_json() } };
}

std::string ValueControl::to_string() const
{
	return Control::to_string() + ", Min: " + std::to_string(min) +
	       ", Max: " + std::to_string(max) +
	       ", Default value: " + std::to_string(default_value) +
	       ", Step: " + std::to_string(step);
}

json ValueControl::to_json() const
{
	auto res = Control::to_json();
	res["min"] = min;
	res["max"] = max;
	res["default_value"] = default_value;
	res["step"] = step;

	return res;
}

std::string MenuControl::to_string() const
{
	auto res = ValueControl::to_string() + ", Items: [";

	for (auto const &[key, val] : items) {
		res += std::to_string(key) + ": " + val + ", ";
	}

	// Remove trailing ", "
	if (items.size() > 0) {
		res.erase(res.end() - 2);
	}

	res += "]";

	return res;
}

json MenuControl::to_json() const
{
	auto res = ValueControl::to_json();

	for (auto it = items.begin(); it != items.end(); ++it) {
		res["items"][std::to_string(it->first)] = it->second;
	}

	return res;
}

std::string IntegerMenuControl::to_string() const
{
	auto res = ValueControl::to_string() + ", Items: [";

	for (auto const &[key, val] : items) {
		res += std::to_string(key) + ": " + std::to_string(val) + ", ";
	}

	// Remove trailing ", "
	if (items.size() > 0) {
		res.erase(res.end() - 2);
	}

	res += "]";

	return res;
}

json IntegerMenuControl::to_json() const
{
	auto res = ValueControl::to_json();

	for (auto it = items.begin(); it != items.end(); ++it) {
		res["items"][std::to_string(it->first)] = it->second;
	}

	return res;
}

std::string ExtendedControl::to_string() const
{
	auto res = ValueControl::to_string() +
		   ", Elements: " + std::to_string(elems) +
		   ", Element size: " + std::to_string(elem_size) +
		   ", Dimensions: [";

	for (auto dim : dimensions) {
		res += " " + std::to_string(dim);
	}

	return res + " ]";
}

json ExtendedControl::to_json() const
{
	auto res = ValueControl::to_json();

	res["elements"] = elems;
	res["element_size"] = elem_size;
	res["dimensions"] = dimensions;

	return res;
}

void StringControlValue::ready_control(v4l2_ext_control &ctrl)
{
	ctrl.size = size + 1;
	ctrl.string = value;
}

void StringControlValue::check_value(std::shared_ptr<Control> ctrl)
{
	auto ext_ctrl = std::static_pointer_cast<ExtendedControl>(ctrl);

	if (ext_ctrl->min > size || ext_ctrl->max < size) {
		throw V4L2Exception("String size does not match control limits:"
				    " (min: " +
				    std::to_string(ext_ctrl->min) +
				    ", max: " + std::to_string(ext_ctrl->max) +
				    "), size: " + std::to_string(size));
	}

	if ((size - ext_ctrl->min) % static_cast<int64_t>(ext_ctrl->step) !=
	    0) {
		throw V4L2Exception("String size does not match control step "
				    "size: " +
				    std::to_string(ext_ctrl->step));
	}
}

std::string StringControlValue::to_string() const
{
	return std::string(value);
}

json StringControlValue::to_json() const
{
	return json{ { "value", value } };
}

int64_t IntegerControlValue::get_value() const
{
	return value;
}

void IntegerControlValue::check_value(std::shared_ptr<Control> ctrl)
{
	if (ctrl->type == V4L2_CTRL_TYPE_INTEGER &&
	    ((value > INT_MAX) || (value < INT_MIN))) {
		throw V4L2Exception("Control expects 32bit signed but value "
				    "exceeds 32bit bounds: " +
				    std::to_string(value));
	}
	type = ctrl->type;
}

void IntegerControlValue::ready_control(v4l2_ext_control &ctrl)
{
	switch (type) {
	case V4L2_CTRL_TYPE_INTEGER:
	case V4L2_CTRL_TYPE_BOOLEAN:
	case V4L2_CTRL_TYPE_MENU:
	case V4L2_CTRL_TYPE_INTEGER_MENU:
	case V4L2_CTRL_TYPE_BITMASK:
	case V4L2_CTRL_TYPE_BUTTON:
		ctrl.value = static_cast<int32_t>(value);
		break;
	case V4L2_CTRL_TYPE_INTEGER64:
		ctrl.value64 = value;
		break;
	default:
		throw V4L2Exception("Control is not of integer type");
	}
}

void IntegerControlValue::update_value(v4l2_ext_control &ctrl)
{
	switch (type) {
	case V4L2_CTRL_TYPE_INTEGER:
	case V4L2_CTRL_TYPE_BOOLEAN:
	case V4L2_CTRL_TYPE_MENU:
	case V4L2_CTRL_TYPE_INTEGER_MENU:
	case V4L2_CTRL_TYPE_BITMASK:
	case V4L2_CTRL_TYPE_BUTTON:
		value = ctrl.value;
		break;
	case V4L2_CTRL_TYPE_INTEGER64:
		value = ctrl.value64;
		break;
	default:
		throw V4L2Exception("Unkown type of integer control");
	}
}

std::string IntegerControlValue::to_string() const
{
	return std::to_string(value);
}

json IntegerControlValue::to_json() const
{
	return json{ { "value", value } };
}

void ArrayControlValue::ready_control(v4l2_ext_control &ctrl)
{
	ctrl.size = elems * element_size;

	// Ensure we set the correct pointer, might not be necessary (could
	// maybe use ctrl->ptr instead)
	switch (element_size) {
	case 1:
		ctrl.p_u8 = value;
		break;
	case 2:
		ctrl.p_u16 = reinterpret_cast<uint16_t *>(value);
		break;
	case 4:
		if (sign) {
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 5, 0)
			ctrl.p_s32 = reinterpret_cast<int32_t *>(value);
#else
			ctrl.ptr = static_cast<void *>(value);
#endif
		} else {
			ctrl.p_u32 = reinterpret_cast<uint32_t *>(value);
		}
		break;
	case 8:
		// Use void* because of __s64 != int64_t (in some cases)
		ctrl.ptr = static_cast<void *>(value);
		break;
	default:
		throw std::logic_error(
			"Invalid type size in ArrayControlValue");
	}
}

void ArrayControlValue::check_value(std::shared_ptr<Control> ctrl)
{
	auto ext_ctrl = std::static_pointer_cast<ExtendedControl>(ctrl);

	// Ensure we the array type is supported by V4L2
	if (sign && (element_size < 4)) {
		throw V4L2Exception(ctrl->name,
				    ">32bit signed arrays are not supported");
	}

	if (!sign && (element_size == 8)) {
		throw V4L2Exception(ctrl->name,
				    "64bit unsigned arrays are not supported");
	}

	// Make sure they array type matches the control type
	switch (ctrl->type) {
	case V4L2_CTRL_TYPE_U8:
	case V4L2_CTRL_TYPE_U16:
	case V4L2_CTRL_TYPE_U32:
		if (sign) {
			throw V4L2Exception(ctrl->name,
					    "Control expects unsigned but was "
					    "given signed");
		}
		break;
	case V4L2_CTRL_TYPE_INTEGER:
	case V4L2_CTRL_TYPE_INTEGER64:
		if (!sign) {
			throw V4L2Exception(ctrl->name,
					    "Control expects signed but was "
					    "given unsigned");
		}
		break;
	default:
		throw V4L2Exception(ctrl->name, "Unsupported array type");
	}

	if (ext_ctrl->elems != elems) {
		throw V4L2Exception(ctrl->name,
				    "Number of value elements differ from "
				    "control query: " +
					    std::to_string(ext_ctrl->elems) +
					    " (got " + std::to_string(elems) +
					    ")");
	}
	if (ext_ctrl->elem_size != element_size) {
		throw V4L2Exception(
			ctrl->name,
			"Value element size differ from control query: " +
				std::to_string(ext_ctrl->elem_size) + " vs. " +
				std::to_string(element_size));
	}
	if (ext_ctrl->dimensions.size() != dims.size()) {
		throw V4L2Exception(
			ctrl->name,
			"Value dimensions differ from control query: " +
				std::to_string(ext_ctrl->dimensions.size()) +
				" vs. " + std::to_string(dims.size()));
	}

	for (size_t i = 0; i < dims.size(); i++) {
		if (ext_ctrl->dimensions[i] != dims[i]) {
			throw V4L2Exception(
				ctrl->name,
				"Dimension (" + std::to_string(i) +
					") differ from control query: " +
					std::to_string(
						ext_ctrl->dimensions[i]) +
					" vs. " + std::to_string(dims[i]));
		}
	}
}

#if PYTHON
py::array ArrayControlValue::get_array() const
{
	py::array result;
	switch (element_size) {
	case 1:
		result = py::array_t<uint8_t>(elems, value);
		break;
	case 2:
		result = py::array_t<uint16_t>(
			elems, reinterpret_cast<uint16_t *>(value));
		break;
	case 4:
		if (sign) {
			result = py::array_t<int32_t>(
				elems, reinterpret_cast<int32_t *>(value));
		} else {
			result = py::array_t<uint32_t>(
				elems, reinterpret_cast<uint32_t *>(value));
		}
		break;
	case 8:
		if (sign) {
			result = py::array_t<int64_t>(
				elems, reinterpret_cast<int64_t *>(value));
		} else {
			result = py::array_t<uint64_t>(
				elems, reinterpret_cast<uint64_t *>(value));
		}
		break;
	default:
		throw std::logic_error(
			"Invalid type size in ArrayControlValue");
	}

	return result.reshape(dims);
}
#else
cv::Mat ArrayControlValue::get_array() const
{
	int type;

	switch (element_size) {
	case 1:
		if (sign) {
			type = CV_8S;
		} else {
			type = CV_8U;
		}
		break;
	case 2:
		if (sign) {
			type = CV_16U;
		} else {
			type = CV_16S;
		}
		break;
	case 4:
		if (sign) {
			type = CV_32S;
		} else {
			throw std::runtime_error("OpenCV Mat does not support "
						 "unsigned 32 bit ints");
		}
		break;
	default:
		throw std::logic_error(
			"Invalid type size in ArrayControlValue: " +
			std::to_string(element_size));
	}

	auto res = cv::Mat(static_cast<int>(dims.size()),
			   reinterpret_cast<const int *>(dims.data()), type);

	return res;
}
#endif

std::string ArrayControlValue::to_string() const
{
	std::string res = "[Elements: " + std::to_string(elems) +
			  ", Element size: " + std::to_string(element_size) +
			  ", Dimensions: [ ";

	for (auto dim : dims) {
		res += std::to_string(dim) + " ";
	}

	return res + "]]";
}

template <typename T> json array_to_json(T *ptr, std::vector<uint32_t> dims)
{
	json array;

	auto inds = std::vector<uint32_t>();
	auto arrays = std::vector<json>();

	uint32_t elems = 1;

	for (uint32_t i = 0; i < dims.size(); i++) {
		inds.push_back(0);
		arrays.push_back(json());
		elems *= dims[i];
	}

	for (uint32_t i = 0; i < elems; i++) {
		uint32_t ind = inds.size() - 1;
		arrays[ind].push_back(ptr[i]);

		// Count of how many elements are in the array on this index
		inds[ind] += 1;

		// Recursively push_back arrays until it is no longer needed.
		while (ind > 0 && inds[ind] == dims[ind]) {
			if (!(inds[ind] < dims[ind])) {
				inds[ind - 1] += 1;
				arrays[ind - 1].push_back(arrays[ind]);
				arrays[ind] = json();
			}

			inds[ind] = 0;
			ind -= 1;
		}
	}

	return arrays[0];
}

json ArrayControlValue::to_json() const
{
	json array;
	switch (element_size) {
	case 1:
		array = array_to_json<uint8_t>(value, dims);
		break;
	case 2:
		if (sign) {
			int16_t *ptr = reinterpret_cast<int16_t *>(value);
			array = array_to_json<int16_t>(ptr, dims);
		} else {
			uint16_t *ptr = reinterpret_cast<uint16_t *>(value);
			array = array_to_json<uint16_t>(ptr, dims);
		}
		break;
	case 4:
		if (sign) {
			int32_t *ptr = reinterpret_cast<int32_t *>(value);
			array = array_to_json<int32_t>(ptr, dims);
		} else {
			uint32_t *ptr = reinterpret_cast<uint32_t *>(value);
			array = array_to_json<uint32_t>(ptr, dims);
		}
		break;
	case 8:
		if (sign) {
			int64_t *ptr = reinterpret_cast<int64_t *>(value);
			array = array_to_json<int64_t>(ptr, dims);
		} else {
			uint64_t *ptr = reinterpret_cast<uint64_t *>(value);
			array = array_to_json<uint64_t>(ptr, dims);
		}
		break;
	default:
		throw std::logic_error(
			"Invalid type size in ArrayControlValue");
	}

	return json{ { "value", array } };
}

std::string
representation_trigger_sequence(const struct trigger_sequence &trig_seq)
{
	return "Exposure time: " + std::to_string(trig_seq.exposure_time) +
	       ", Flash time: " + std::to_string(trig_seq.flash_time) +
	       ", Frame delay: " + std::to_string(trig_seq.frame_delay) +
	       ", Trigger delay: " + std::to_string(trig_seq.trigger_delay);
}

std::vector<trigger_sequence> TriggerSequenceValue::get_sequence() const
{
	return std::vector<trigger_sequence>(
		trig_seq.sequence, trig_seq.sequence + trig_seq.n_sequences);
}

void TriggerSequenceValue::ready_control(v4l2_ext_control &ctrl)
{
	ctrl.size = sizeof(v4l2_trigger_sequence);
#ifdef QTEC_HEADER
	ctrl.p_trig_seq = &trig_seq;
#else
	ctrl.ptr = &trig_seq;
#endif
}

void TriggerSequenceValue::clear()
{
	CLEAR(trig_seq);
}

void TriggerSequenceValue::add_exposure(uint32_t exposure_time,
					uint32_t flash_time,
					uint32_t frame_delay,
					uint32_t trigger_delay)
{
	trig_seq.sequence[trig_seq.n_sequences] = {
		.exposure_time = exposure_time,
		.flash_time = flash_time,
		.frame_delay = frame_delay,
		.trigger_delay = trigger_delay,
	};

	trig_seq.n_sequences++;
}

std::string TriggerSequenceValue::to_string() const
{
	std::string res = "[ ";

	for (size_t i = 0; i < trig_seq.n_sequences; i++) {
		res += representation_trigger_sequence(trig_seq.sequence[i]) +
		       " ";
	}

	return res + "]";
}

json TriggerSequenceValue::to_json() const
{
	json array;

	for (size_t i = 0; i < trig_seq.n_sequences; i++) {
		auto &ts = trig_seq.sequence[i];
		array.push_back(json{ { "exposure_time", ts.exposure_time },
				      { "flash_time", ts.flash_time },
				      { "frame_delay", ts.frame_delay },
				      { "trigger_delay", ts.trigger_delay } });
	}

	return json{ { "value", array } };
}
} // namespace qamlib
