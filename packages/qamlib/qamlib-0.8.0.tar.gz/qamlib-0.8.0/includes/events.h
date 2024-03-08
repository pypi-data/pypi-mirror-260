// SPDX-License-Identifier: LGPL-2.0
/*
 * events.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <string>

#include "control.h"

namespace qamlib
{
// Make enum from V4L2 defines
enum EventType {
	ALL = V4L2_EVENT_ALL,
	VSYNC = V4L2_EVENT_VSYNC,
	EOS = V4L2_EVENT_EOS,
	CTRL = V4L2_EVENT_CTRL,
	FRAME_SYNC = V4L2_EVENT_FRAME_SYNC,
	SOURCE_CHANGE = V4L2_EVENT_SOURCE_CHANGE,
	MOTION_DET = V4L2_EVENT_MOTION_DET,
};

std::string event_type_representation(const EventType type);

class BaseEvent {
    public:
	EventType type;
	uint32_t pending;
	uint32_t sequence;
	double timestamp;
	uint32_t id;

	BaseEvent(v4l2_event &event)
		: type(EventType(event.type)), pending(event.pending),
		  sequence(event.sequence), id(event.id)
	{
		timestamp = static_cast<double>(event.timestamp.tv_sec);
		timestamp += event.timestamp.tv_nsec / 1000000000.0;
	}

	// This is to let Pybind11 do automatic downcasting
	virtual ~BaseEvent() = default;

	std::string to_string() const;
};

class ControlChangesFlags {
	uint32_t flags;

    public:
	ControlChangesFlags(uint32_t flags) : flags(flags)
	{
	}

	flag_function(value, V4L2_EVENT_CTRL_CH_VALUE);
	flag_function(ch_flags, V4L2_EVENT_CTRL_CH_FLAGS);
	flag_function(range, V4L2_EVENT_CTRL_CH_RANGE);

	std::string to_string() const;
};

class ControlEvent : public BaseEvent {
    public:
	ControlChangesFlags changes;
	v4l2_ctrl_type control_type;
	int64_t value;
	ControlFlags flags;
	int min;
	int max;
	int step;
	int default_value;

	ControlEvent(v4l2_event &event)
		: BaseEvent(event), changes(event.u.ctrl.changes),
		  control_type(static_cast<v4l2_ctrl_type>(event.u.ctrl.type)),
		  flags(event.u.ctrl.flags), min(event.u.ctrl.minimum),
		  max(event.u.ctrl.maximum), step(event.u.ctrl.step),
		  default_value(event.u.ctrl.default_value)
	{
		if (control_type == V4L2_CTRL_TYPE_INTEGER64) {
			value = event.u.ctrl.value64;
		} else {
			value = event.u.ctrl.value;
		}
	}

	std::string to_string() const;
};

class SourceChangesFlags {
	uint32_t flags;

    public:
	SourceChangesFlags(uint32_t flags) : flags(flags)
	{
	}

	flag_function(resolution, V4L2_EVENT_SRC_CH_RESOLUTION);

	std::string to_string() const;
};

class SourceEvent : public BaseEvent {
    public:
	SourceChangesFlags changes;

	SourceEvent(v4l2_event &event)
		: BaseEvent(event), changes(event.u.src_change.changes)
	{
	}

	std::string to_string() const;
};
} // namespace qamlib
