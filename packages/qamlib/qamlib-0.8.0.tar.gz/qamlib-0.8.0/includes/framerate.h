// SPDX-License-Identifier: LGPL-2.0
/*
 * framerate.h
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#pragma once

#include <string>
#include <vector>

#include <nlohmann/json.hpp>

#include "utils.h"

using json = nlohmann::json;

namespace qamlib
{
class FrameRate {
    public:
	v4l2_frmivaltypes type;

	// This is to let Pybind11 do automatic downcasting
	virtual ~FrameRate() = default;
};

class DiscreteFrameRate : public FrameRate {
    public:
	std::vector<double> values;

	DiscreteFrameRate(std::vector<double> values) : values(values)
	{
		type = V4L2_FRMIVAL_TYPE_DISCRETE;
	}

	std::string to_string() const;

	json to_json() const;
};

class ContinuousFrameRate : public FrameRate {
    public:
	double min;
	double max;

	ContinuousFrameRate(double min, double max) : min(min), max(max)
	{
		type = V4L2_FRMIVAL_TYPE_CONTINUOUS;
	}

	std::string to_string() const;

	json to_json() const;
};

class StepwiseFrameRate : public ContinuousFrameRate {
    public:
	double step;

	StepwiseFrameRate(double min, double max, double step)
		: ContinuousFrameRate(min, max), step(step)
	{
		type = V4L2_FRMIVAL_TYPE_STEPWISE;
	}

	std::string to_string() const;

	json to_json() const;
};
} // namespace qamlib
