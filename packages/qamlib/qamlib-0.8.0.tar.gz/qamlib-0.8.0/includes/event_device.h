// SPDX-License-Identifier: LGPL-2.0
/*
 * event_device.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <atomic>
#include <fcntl.h>
#include <functional>
#include <mutex>
#include <thread>
#include <unistd.h>

#if PYTHON
	#include <pybind11/numpy.h>
namespace py = pybind11;
#endif

#include "utils.h"
#include "events.h"

namespace qamlib
{
class EventDevice {
	int fd;

	std::thread event_thread;
	std::atomic<bool> running = false;

	std::function<void(std::unique_ptr<BaseEvent>)> callback;
	std::mutex cb_lock;

	void event_manager();

    public:
	EventDevice(std::string device)
	{
		fd = open(device.c_str(), O_RDWR | O_NONBLOCK, 0);

		if (fd == -1) {
			throw V4L2Exception("Failed to open device");
		}
	}

	EventDevice(uint32_t device_num)
		: EventDevice("/dev/video" + std::to_string(device_num))
	{
	}

#ifdef QTEC_HEADER
	EventDevice() : EventDevice("/dev/qtec/video0")
	{
	}
#endif

	~EventDevice()
	{
		if (running) {
#if PYTHON
			// Need to realease GIL before trying to stop thread
			py::gil_scoped_release release;
			stop();
			py::gil_scoped_acquire acquire;
#else
			stop();
#endif
		}

		if (fd != -1) {
			close(fd);
		}
	}

	void
	set_callback(const std::function<void(std::unique_ptr<BaseEvent>)> &cb);

	void start();
	void stop();

	void subscribe(uint32_t type, uint32_t id = 0);
	void unsubscribe(uint32_t type, uint32_t id = 0);
};
} // namespace qamlib
