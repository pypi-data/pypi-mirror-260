// SPDX-License-Identifier: LGPL-2.0
/*
 * framerate.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "framerate.h"

namespace qamlib
{
std::string DiscreteFrameRate::to_string() const
{
	std::string res = "[ ";
	for (size_t i = 0; i < values.size(); i++) {
		res += std::to_string(values[i]) + " ";
	}

	res += "]";
	return res;
}

json DiscreteFrameRate::to_json() const
{
	return json{ { "values", values } };
}

std::string ContinuousFrameRate::to_string() const
{
	return "Min: " + std::to_string(min) + ", Max: " + std::to_string(max);
}

json ContinuousFrameRate::to_json() const
{
	return json{ { "min", min }, { "max", max } };
}

std::string StepwiseFrameRate::to_string() const
{
	return ContinuousFrameRate::to_string() +
	       ", Step: " + std::to_string(step);
}

json StepwiseFrameRate::to_json() const
{
	auto res = ContinuousFrameRate::to_json();

	res["step"] = step;

	return res;
}
} // namespace qamlib
