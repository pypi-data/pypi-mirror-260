// SPDX-License-Identifier: LGPL-2.0
/*
 * control.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <map>
#include <stdint.h>
#include <string>

#include <linux/version.h>

#include <nlohmann/json.hpp>

#if PYTHON
	#include <pybind11/numpy.h>
namespace py = pybind11;
#else
	#include <opencv2/core/mat.hpp>
#endif

#include "utils.h"

using json = nlohmann::json;

namespace qamlib
{
/*
 * Class for V4L2 control flags.
 */
class ControlFlags {
    public:
	uint32_t flags;

	ControlFlags(uint32_t flags) : flags(flags)
	{
	}

	flag_function(disabled, V4L2_CTRL_FLAG_DISABLED);
	flag_function(grabbed, V4L2_CTRL_FLAG_GRABBED);
	flag_function(read_only, V4L2_CTRL_FLAG_READ_ONLY);
	flag_function(update, V4L2_CTRL_FLAG_UPDATE);
	flag_function(inactive, V4L2_CTRL_FLAG_INACTIVE);
	flag_function(slider, V4L2_CTRL_FLAG_SLIDER);
	flag_function(write_only, V4L2_CTRL_FLAG_WRITE_ONLY);
	flag_function(is_volatile, V4L2_CTRL_FLAG_VOLATILE);
	flag_function(has_payload, V4L2_CTRL_FLAG_HAS_PAYLOAD);
	flag_function(execute_on_write, V4L2_CTRL_FLAG_EXECUTE_ON_WRITE);
	flag_function(modify_layout, V4L2_CTRL_FLAG_MODIFY_LAYOUT);

#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 0, 0)
	flag_function(dynamic_array, V4L2_CTRL_FLAG_DYNAMIC_ARRAY);
#endif

	// Pretty string representation
	std::string to_string() const;

	json to_json() const;
};

// Util function
std::string type_to_string(v4l2_ctrl_type type);

class Control {
    public:
	uint32_t id;
	std::string name;
	v4l2_ctrl_type type;
	ControlFlags flags;

	Control(v4l2_query_ext_ctrl *query)
		: id(query->id), name(static_cast<char *>(query->name)),
		  type(static_cast<v4l2_ctrl_type>(query->type)),
		  flags(query->flags)
	{
	}

	// This is to let Pybind11 do automatic downcasting
	virtual ~Control() = default;

	virtual std::string to_string() const;

	virtual json to_json() const;
};

class ValueControl : public Control {
    public:
	int64_t min;
	int64_t max;
	int64_t default_value;
	uint64_t step;

	ValueControl(v4l2_query_ext_ctrl *query)
		: Control(query), min(query->minimum), max(query->maximum),
		  default_value(query->default_value), step(query->step)
	{
	}

	std::string to_string() const override;

	json to_json() const override;
};

class MenuControl : public ValueControl {
    public:
	std::map<uint32_t, std::string> items;

	MenuControl(v4l2_query_ext_ctrl *query,
		    std::map<uint32_t, std::string> items)
		: ValueControl(query), items(items)
	{
	}

	std::string to_string() const override;

	json to_json() const override;
};

class IntegerMenuControl : public ValueControl {
    public:
	std::map<uint32_t, int64_t> items;

	IntegerMenuControl(v4l2_query_ext_ctrl *query,
			   std::map<uint32_t, int64_t> items)
		: ValueControl(query), items(items)
	{
	}

	std::string to_string() const override;

	json to_json() const override;
};

class ExtendedControl : public ValueControl {
    public:
	uint32_t elem_size;
	uint32_t elems;
	std::vector<uint32_t> dimensions;

	ExtendedControl(v4l2_query_ext_ctrl *query)
		: ValueControl(query), elem_size(query->elem_size),
		  elems(query->elems),
		  dimensions(query->dims, query->dims + query->nr_of_dims)
	{
	}

	std::string to_string() const override;

	json to_json() const override;
};

class ControlValue {
    public:
	virtual ~ControlValue() = default;

	/**
	 * Internal ``qamlib`` function not to be used otherwise
	 */
	virtual void check_value(std::shared_ptr<Control> ctrl)
	{
		(void)ctrl; // Silence warning
	}
	/**
	 * Internal ``qamlib`` function not to be used otherwise
	 */
	virtual void ready_control(v4l2_ext_control &ctrl)
	{
		(void)ctrl; // Silence warning
	}
	/**
	 * Internal ``qamlib`` function not to be used otherwise
	 */
	virtual void update_value(v4l2_ext_control &ctrl)
	{
		(void)ctrl; // Silence warning
	}

	virtual std::string to_string() const = 0;
	virtual json to_json() const = 0;
};

class StringControlValue : public ControlValue {
	char *value;
	uint32_t size;

    public:
	/**
	 * Internal ``qamlib`` function not to be used otherwise
	 */
	StringControlValue(uint32_t max_size) : size(max_size)
	{
		value = new char[max_size + 1];
	}

	StringControlValue(std::string &val) : StringControlValue(val.size())
	{
		auto len = val.copy(value, val.size());
		value[len] = '\0';
	}

	void check_value(std::shared_ptr<Control> ctrl) override;

	void ready_control(v4l2_ext_control &ctrl) override;

	~StringControlValue() override
	{
		delete[] value;
	}

	std::string to_string() const override;

	json to_json() const override;
};

class IntegerControlValue : public ControlValue {
	int64_t value = 0;

	// This is set either by the constructor or by check_value(), so that
	// ready_control() and update_value() can correctly set or get the value
	// of the v4l2_ext_control
	v4l2_ctrl_type type;

    public:
	/**
	 * Internal ``qamlib`` function not to be used otherwise
	 */
	IntegerControlValue(v4l2_ctrl_type type) : type(type)
	{
	}

	IntegerControlValue(int64_t value) : value(value)
	{
	}

	IntegerControlValue(int32_t value) : value(value)
	{
	}

	int64_t get_value() const;

	void check_value(std::shared_ptr<Control> ctrl) override;

	void ready_control(v4l2_ext_control &ctrl) override;

	virtual void update_value(v4l2_ext_control &ctrl) override;

	std::string to_string() const override;

	json to_json() const override;
};

class ArrayControlValue : public ControlValue {
	uint8_t *value;
	uint32_t elems;
	uint32_t element_size;
	std::vector<uint32_t> dims;
	bool sign = false;

    public:
	ArrayControlValue(uint32_t elements, uint32_t element_size,
			  std::vector<uint32_t> dims, bool sign = false)
		: elems(elements), element_size(element_size), dims(dims),
		  sign(sign)
	{
		value = new uint8_t[elements * element_size];
	}

#if PYTHON
	ArrayControlValue(py::array array)
	{
		elems = array.size();
		element_size = array.itemsize();

		char kind = array.dtype().kind();

		if (kind == 'i') {
			sign = true;
		} else if (kind != 'u') {
			std::string msg = "Unsupported array kind: ";
			msg += kind;
			throw V4L2Exception(msg);
		}

		dims = std::vector<uint32_t>(array.shape(),
					     array.shape() + array.ndim());

		value = new uint8_t[elems * element_size];
		memcpy(value, array.data(), elems * element_size);
	}

	py::array get_array() const;
#else
	ArrayControlValue(cv::Mat array)
	{
		switch (array.depth()) {
		case CV_8S:
		case CV_16S:
		case CV_32S:
			sign = true; // fall through
		case CV_8U:
		case CV_16U:
			element_size = array.elemSize() /
				       static_cast<uint32_t>(array.channels());
			break;
		default:
			throw V4L2Exception("Unsupported data type for Array "
					    "control");
		}

		elems = 1;

		for (int i = 0; i < array.dims; ++i) {
			auto size = static_cast<uint32_t>(array.size[i]);
			elems *= size;

			dims.push_back(size);
		}
		if (array.channels() > 1) {
			auto channels = static_cast<uint32_t>(array.channels());
			elems *= channels;

			dims.push_back(channels);
		}

		// array is empty so set elems to 0;
		if (elems == 1) {
			elems = 0;
		}

		value = new uint8_t[elems * element_size];
		memcpy(value, array.data, elems * element_size);
	}

	cv::Mat get_array() const;
#endif

	void check_value(std::shared_ptr<Control> ctrl) override;

	void ready_control(v4l2_ext_control &ctrl) override;

	~ArrayControlValue() override
	{
		delete[] value;
	}

	std::string to_string() const override;

	json to_json() const override;
};

// Have local versions of the v4l2_trigger_sequence structs when not building
// with the Qtec headers.
#ifndef QTEC_HEADER
struct trigger_sequence {
	__u32 exposure_time;
	__u32 flash_time;
	__u32 frame_delay;
	__u32 trigger_delay;
};

	#define MAX_TRIG_SEQ 16
struct v4l2_trigger_sequence {
	__u8 n_sequences;
	struct trigger_sequence sequence[MAX_TRIG_SEQ];
};
#endif

std::string
representation_trigger_sequence(const struct trigger_sequence &trig_seq);

class TriggerSequenceValue : public ControlValue {
	struct v4l2_trigger_sequence trig_seq;

    public:
	TriggerSequenceValue()
	{
		CLEAR(trig_seq);
	}

	void ready_control(v4l2_ext_control &ctrl) override;

	void clear();

	void add_exposure(uint32_t exposure_time, uint32_t flash_time,
			  uint32_t frame_delay, uint32_t trigger_delay);

	std::vector<trigger_sequence> get_sequence() const;

	std::string to_string() const override;

	json to_json() const override;
};
} // namespace qamlib
