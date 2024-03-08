// SPDX-License-Identifier: LGPL-2.0
/*
 * device.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include <fcntl.h>

#include "device.h"

namespace qamlib
{
std::string DeviceInfo::to_string() const
{
	return "Driver: " + driver + ", card: " + card +
	       ", bus_info: " + bus_info;
}

DeviceInfo Device::open_device(std::string device)
{
	if (fd != -1) {
		throw V4L2Exception("Device already open");
	}

	fd = open(device.c_str(), O_RDWR | O_NONBLOCK, 0);

	if (fd == -1) {
		throw V4L2Exception("Failed to open device");
	}

	struct v4l2_capability caps;
	if (ioctl(fd, VIDIOC_QUERYCAP, &caps)) {
		throw V4L2Exception("Error querying device capabilities",
				    errno);
	}

	if (needed_cap != 0 && !(caps.device_caps & needed_cap)) {
		throw V4L2Exception(
			"Device does not support necessary capabilities");
	}

	return DeviceInfo(caps);
}

/*
 * CONTROLS
 */
std::map<std::string, std::shared_ptr<Control> > Device::list_controls()
{
	struct v4l2_query_ext_ctrl query;
	std::map<std::string, std::shared_ptr<Control> > controls;

	// Struct for menu queries
	struct v4l2_querymenu qmenu;

	query.id = V4L2_CTRL_FLAG_NEXT_CTRL | V4L2_CTRL_FLAG_NEXT_COMPOUND;
	while (ioctl(fd, VIDIOC_QUERY_EXT_CTRL, &query) == 0) {
		auto n = std::string(reinterpret_cast<char *>(query.name));
		auto name = name_to_key(n);

		auto it = controls.find(name);

		if (it != controls.end()) {
			throw V4L2Exception(
				"Two or more controls map to same name: " +
				name);
		}

		std::shared_ptr<Control> ctrl;
		switch (query.type) {
		case V4L2_CTRL_TYPE_MENU: {
			std::map<uint32_t, std::string> items;

			qmenu.id = query.id;

			for (uint32_t i = query.minimum; i <= query.maximum;
			     i++) {
				qmenu.index = i;

				if (ioctl(fd, VIDIOC_QUERYMENU, &qmenu)) {
					if (errno == EINVAL) {
						continue;
					}
					throw V4L2Exception(
						"Error while querying menu items",
						errno);
				}

				items[qmenu.index] = std::string(
					reinterpret_cast<char *>(qmenu.name));
			}

			ctrl = std::shared_ptr<Control>(
				new MenuControl(&query, items));
			break;
		}
		case V4L2_CTRL_TYPE_INTEGER_MENU: {
			std::map<uint32_t, int64_t> items;

			qmenu.id = query.id;

			for (uint32_t i = query.minimum; i <= query.maximum;
			     i++) {
				qmenu.index = i;

				if (ioctl(fd, VIDIOC_QUERYMENU, &qmenu)) {
					// Not all indices in the range have to
					// be populated
					if (errno == EINVAL) {
						continue;
					}
					throw V4L2Exception(
						"Error while querying menu items",
						errno);
				}

				items[qmenu.index] = qmenu.value;
			}

			ctrl = std::shared_ptr<Control>(
				new IntegerMenuControl(&query, items));
			break;
		}
		case V4L2_CTRL_TYPE_INTEGER:
		case V4L2_CTRL_TYPE_INTEGER64:
			if (query.flags & V4L2_CTRL_FLAG_HAS_PAYLOAD) {
				ctrl = std::shared_ptr<Control>(
					new ExtendedControl(&query));
				break;
			}
			// fall through
		case V4L2_CTRL_TYPE_BOOLEAN:
		case V4L2_CTRL_TYPE_BITMASK:
		case V4L2_CTRL_TYPE_STRING:
			ctrl = std::shared_ptr<Control>(
				new ValueControl(&query));
			break;
		case V4L2_CTRL_TYPE_BUTTON:
		case V4L2_CTRL_TYPE_CTRL_CLASS:
			ctrl = std::shared_ptr<Control>(new Control(&query));
			break;
		default:
			ctrl = std::shared_ptr<Control>(
				new ExtendedControl(&query));
			break;
		}

		controls[name] = ctrl;

		query.id |=
			V4L2_CTRL_FLAG_NEXT_CTRL | V4L2_CTRL_FLAG_NEXT_COMPOUND;
	}

	return controls;
}

void Device::set_control(const std::string &ctrl_name, int value)
{
	auto name = name_to_key(ctrl_name);
	auto controls = list_controls();

	auto it = controls.find(name);

	if (it == controls.end()) {
		throw V4L2Exception("Could not find control: " + name);
	}

	// Take out control from iterator
	auto ctrl = it->second;

	if (ctrl->type != V4L2_CTRL_TYPE_INTEGER &&
	    ctrl->type != V4L2_CTRL_TYPE_BOOLEAN &&
	    ctrl->type != V4L2_CTRL_TYPE_MENU &&
	    ctrl->type != V4L2_CTRL_TYPE_INTEGER_MENU &&
	    ctrl->type != V4L2_CTRL_TYPE_BUTTON &&
	    ctrl->type != V4L2_CTRL_TYPE_BITMASK) {
		throw V4L2Exception(
			"set_control() doesn't support controls of this type");
	}

	struct v4l2_control control = {
		.id = ctrl->id,
		.value = value,
	};

	if (ioctl(fd, VIDIOC_S_CTRL, &control) != 0) {
		throw V4L2Exception("Failed to set control", errno);
	}
}

void Device::set_control(uint32_t id, int value)
{
	struct v4l2_control control = {
		.id = id,
		.value = value,
	};

	if (ioctl(fd, VIDIOC_S_CTRL, &control) != 0) {
		throw V4L2Exception("Failed to set control", errno);
	}
}

int Device::get_control(const std::string &ctrl_name)
{
	auto name = name_to_key(ctrl_name);
	auto controls = list_controls();

	auto it = controls.find(name);

	if (it == controls.end()) {
		throw V4L2Exception("Could not find control: " + name);
	}

	// Take out control from iterator
	auto ctrl = it->second;

	if (ctrl->type != V4L2_CTRL_TYPE_INTEGER &&
	    ctrl->type != V4L2_CTRL_TYPE_BOOLEAN &&
	    ctrl->type != V4L2_CTRL_TYPE_MENU &&
	    ctrl->type != V4L2_CTRL_TYPE_INTEGER_MENU &&
	    ctrl->type != V4L2_CTRL_TYPE_BUTTON &&
	    ctrl->type != V4L2_CTRL_TYPE_BITMASK) {
		throw V4L2Exception(
			"getControl() doesn't support extended controls");
	}

	struct v4l2_control control = {
		.id = ctrl->id,
	};

	if (ioctl(fd, VIDIOC_G_CTRL, &control) != 0) {
		throw V4L2Exception("Failed to get control", errno);
	}

	return control.value;
}

int Device::get_control(uint32_t id)
{
	struct v4l2_control control = {
		.id = id,
	};

	if (ioctl(fd, VIDIOC_G_CTRL, &control) != 0) {
		throw V4L2Exception("Failed to get control", errno);
	}

	return control.value;
}

/*
 * Gives an "empty" ControlValue object
 */
std::unique_ptr<ControlValue> get_control_class(std::shared_ptr<Control> &ctrl)
{
	switch (ctrl->type) {
	case V4L2_CTRL_TYPE_STRING: {
		//auto string_ctrl = (ValueControl*)ctrl.get();
		auto string_ctrl = std::static_pointer_cast<ValueControl>(ctrl);
		return std::unique_ptr<ControlValue>(
			new StringControlValue(string_ctrl->max));
	}
	case V4L2_CTRL_TYPE_U8:
	case V4L2_CTRL_TYPE_U16:
	case V4L2_CTRL_TYPE_U32: {
		auto ext_ctrl = std::static_pointer_cast<ExtendedControl>(ctrl);
		return std::unique_ptr<ControlValue>(new ArrayControlValue(
			ext_ctrl->elems, ext_ctrl->elem_size,
			ext_ctrl->dimensions));
	}
	case V4L2_CTRL_TYPE_INTEGER:
	case V4L2_CTRL_TYPE_INTEGER64: {
		if (ctrl->flags.has_payload()) {
			auto ext_ctrl =
				std::static_pointer_cast<ExtendedControl>(ctrl);
			return std::unique_ptr<ControlValue>(
				new ArrayControlValue(
					ext_ctrl->elems, ext_ctrl->elem_size,
					ext_ctrl->dimensions, true));
		} else {
			return std::unique_ptr<ControlValue>(
				new IntegerControlValue(ctrl->type));
		}
	}
	case V4L2_CTRL_TYPE_BOOLEAN:
	case V4L2_CTRL_TYPE_MENU:
	case V4L2_CTRL_TYPE_INTEGER_MENU:
	case V4L2_CTRL_TYPE_BITMASK:
	case V4L2_CTRL_TYPE_BUTTON:
		return std::unique_ptr<ControlValue>(
			new IntegerControlValue(ctrl->type));
#ifdef QTEC_HEADER
	case V4L2_CTRL_TYPE_TRIG_SEQ:
		return std::unique_ptr<ControlValue>(
			new TriggerSequenceValue());
#endif
	default:
		throw V4L2Exception("Extended control class not implemented for"
				    " this type: " +
				    type_to_string(ctrl->type));
	}
}

void Device::set_ext_control(const std::string &ctrl_name, ControlValue &value)
{
	auto name = name_to_key(ctrl_name);
	auto controls = list_controls();

	auto it = controls.find(name);

	if (it == controls.end()) {
		throw V4L2Exception("Could not find control: " + name);
	}

	// Take out control from iterator
	auto ctrl = it->second;

	struct v4l2_ext_control ctrls[1];

	ctrls[0].id = ctrl->id;

	// Validity check of values
	value.check_value(ctrl);

	// Setup the struct with values and pointers
	value.ready_control(ctrls[0]);

	struct v4l2_ext_controls ext_ctrl = {
		.which = V4L2_CTRL_WHICH_CUR_VAL,
		.count = 1,
		.controls = ctrls,
	};

	if (ioctl(fd, VIDIOC_S_EXT_CTRLS, &ext_ctrl) != 0) {
		throw V4L2Exception("Failed to set extended control", errno);
	}
}

std::unique_ptr<ControlValue>
Device::get_ext_control(const std::string &ctrl_name, bool default_value)
{
	auto name = name_to_key(ctrl_name);
	auto controls = list_controls();

	auto it = controls.find(name);

	if (it == controls.end()) {
		throw V4L2Exception("Could not find control: " + name);
	}

	// Take out control from iterator
	auto ctrl = it->second;

	struct v4l2_ext_control ctrls[1];

	auto ctrl_val = get_control_class(ctrl);

	ctrls[0].id = ctrl->id;

	ctrl_val->ready_control(ctrls[0]);

	uint32_t which = default_value ? V4L2_CTRL_WHICH_DEF_VAL
				       : V4L2_CTRL_WHICH_CUR_VAL;

	struct v4l2_ext_controls ext_ctrl = {
		.which = which,
		.count = 1,
		.controls = ctrls,
	};

	if (ioctl(fd, VIDIOC_G_EXT_CTRLS, &ext_ctrl) != 0) {
		throw V4L2Exception("Failed to get extended control", errno);
	}

	// Ponter to the ext_control
	ctrl_val->update_value(ctrls[0]);

	return ctrl_val;
}

std::map<std::string, std::unique_ptr<ControlValue> >
Device::get_controls(std::vector<std::string> names, bool default_value)
{
	std::vector<std::unique_ptr<ControlValue> > values;
	auto controls = list_controls();

	std::vector<struct v4l2_ext_control> ctrls;
	ctrls.reserve(names.size());

	auto lower_names = std::vector<std::string>();

	for (auto n : names) {
		auto name = name_to_key(n);
		lower_names.push_back(name);

		auto it = controls.find(name);

		if (it == controls.end()) {
			throw V4L2Exception("Could not find control: " + name);
		}

		// Take out control from iterator
		auto ctrl = it->second;

		auto ctrl_val = get_control_class(ctrl);

		ctrls.push_back(v4l2_ext_control());

		ctrls.back().id = ctrl->id;

		ctrl_val->ready_control(ctrls.back());

		values.push_back(std::move(ctrl_val));
	}

	uint32_t which = default_value ? V4L2_CTRL_WHICH_DEF_VAL
				       : V4L2_CTRL_WHICH_CUR_VAL;

	struct v4l2_ext_controls ext_ctrl = {
		.which = which,
		.count = static_cast<uint32_t>(names.size()),
		.controls = &ctrls[0], // vector data is contiguous
	};

	if (ioctl(fd, VIDIOC_G_EXT_CTRLS, &ext_ctrl) != 0) {
		throw V4L2Exception("Failed to get controls", errno);
	}

	std::map<std::string, std::unique_ptr<ControlValue> > result;

	for (size_t i = 0; i < values.size(); i++) {
		values[i]->update_value(ctrls[i]);

		auto name = lower_names[i];
		result[name] = std::move(values[i]);
	}

	return result;
}

void Device::set_controls(std::map<std::string, ControlValue *> values)
{
	auto controls = list_controls();
	std::vector<struct v4l2_ext_control> ctrls;
	ctrls.reserve(values.size());

	for (auto &[n, value] : values) {
		auto name = name_to_key(n);
		auto it = controls.find(name);

		if (it == controls.end()) {
			throw V4L2Exception("Could not find control: " + name);
		}

		// Take out control from iterator
		auto ctrl = it->second;

		ctrls.push_back(v4l2_ext_control());

		ctrls.back().id = ctrl->id;

		value->check_value(ctrl);
		value->ready_control(ctrls.back());
	}

	struct v4l2_ext_controls ext_ctrl = {
		.which = V4L2_CTRL_WHICH_CUR_VAL,
		.count = static_cast<uint32_t>(values.size()),
		.controls = &ctrls[0], // vector data is contiguous
	};

	if (ioctl(fd, VIDIOC_S_EXT_CTRLS, &ext_ctrl) != 0) {
		throw V4L2Exception("Failed to set controls", errno);
	}
}
} // namespace qamlib
