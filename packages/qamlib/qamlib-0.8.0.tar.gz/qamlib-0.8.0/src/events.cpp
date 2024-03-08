// SPDX-License-Identifier: LGPL-2.0
/*
 * events.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "events.h"

namespace qamlib
{
std::string event_type_representation(const EventType type)
{
	switch (type) {
	case ALL:
		return "ALL";
	case VSYNC:
		return "VSYNC";
	case CTRL:
		return "CTRL";
	case FRAME_SYNC:
		return "FRAME_SYNC";
	case SOURCE_CHANGE:
		return "SOURCE_CHANGE";
	case MOTION_DET:
		return "MOTION_DET";
	default:
		return "UNKOWN";
	}
}

std::string BaseEvent::to_string() const
{
	return "Type: " + event_type_representation(type) +
	       ", Pending: " + std::to_string(pending) +
	       ", Sequence: " + std::to_string(sequence) +
	       ", Timestamp: " + std::to_string(timestamp) +
	       ", Id: " + std::to_string(id);
}

std::string ControlChangesFlags::to_string() const
{
	std::string res = "<";

	std::vector<std::string> active;

	if (value()) {
		active.push_back("value");
	}
	if (ch_flags()) {
		active.push_back("flags");
	}
	if (range()) {
		active.push_back("range");
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

std::string ControlEvent::to_string() const
{
	return BaseEvent::to_string() + ", Value: " + std::to_string(value) +
	       ", Min: " + std::to_string(min) +
	       ", Max: " + std::to_string(max) +
	       ", Default value: " + std::to_string(default_value) +
	       ", Step: " + std::to_string(step);
}

std::string SourceChangesFlags::to_string() const
{
	std::string res = "<";

	std::vector<std::string> active;

	if (resolution()) {
		active.push_back("resolution");
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

std::string SourceEvent::to_string() const
{
	return "Changes: " + changes.to_string();
}
} // namespace qamlib
