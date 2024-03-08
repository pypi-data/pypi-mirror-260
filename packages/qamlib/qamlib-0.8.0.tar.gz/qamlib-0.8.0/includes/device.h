// SPDX-License-Identifier: LGPL-2.0
/*
 * device.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <atomic>
#include <map>
#include <memory>
#include <sys/ioctl.h>
#include <string>

#include "control.h"
#include "format.h"
#include "framerate.h"
#include "utils.h"

namespace qamlib
{
class DeviceInfo {
    public:
	std::string driver;
	std::string card;
	std::string bus_info;

	DeviceInfo(struct v4l2_capability device_caps)
		: driver(reinterpret_cast<char *>(device_caps.driver)),
		  card(reinterpret_cast<char *>(device_caps.card)),
		  bus_info(reinterpret_cast<char *>(device_caps.bus_info))
	{
	}

	std::string to_string() const;
};
/**
 * Create ControlValue object corrensponding to a given Control
 */
std::unique_ptr<ControlValue> get_control_class(std::shared_ptr<Control> &ctrl);

class Device {
    protected:
	v4l2_buf_type device_type;
	uint32_t needed_cap;
	int fd;
	DeviceInfo open_device(std::string device);

	Device(const std::string &device, v4l2_buf_type device_type,
	       uint32_t needed_cap)
		: device_type(device_type), needed_cap(needed_cap), fd(-1),
		  device_info(open_device(device))
	{
	}

    public:
	DeviceInfo device_info;
	/*
	 * CONTROLS
	 */

	/*
	 * Query all controls for device and return a map of the controls with
	 * their name (lower case) mapped to a sub-type of Control
	 */
	std::map<std::string, std::shared_ptr<Control> > list_controls();

	/**
	 * Set named control to ``value``
	 */
	virtual void set_control(const std::string &name, int value);

	/**
	 * Set control of ``id`` to ``value``
	 */
	void set_control(uint32_t id, int value);

	int get_control(const std::string &name);
	int get_control(uint32_t id);

	void set_ext_control(const std::string &name, ControlValue &value);
	std::unique_ptr<ControlValue>
	get_ext_control(const std::string &name, bool default_value = false);

	std::map<std::string, std::unique_ptr<ControlValue> >
	get_controls(std::vector<std::string> names,
		     bool default_value = false);
	void set_controls(std::map<std::string, ControlValue *> values);

	virtual ~Device()
	{
		if (fd != -1) {
			close(fd);
		}
	};
};
} // namespace qamlib
