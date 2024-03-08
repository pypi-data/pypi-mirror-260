// SPDX-License-Identifier: LGPL-2.0
/*
 * utils.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "utils.h"

namespace qamlib
{
/*
 * Utils
 */
std::string name_to_key(const std::string &name)
{
	auto res = std::string();
	bool add_underscore = false;
	res.reserve(name.size());
	for (const auto &c : name) {
		if (isalnum(c)) {
			if (add_underscore) {
				res.push_back('_');
				add_underscore = false;
			}
			res.push_back(tolower(c));
		} else {
			add_underscore = true;
		}
	}
	return res;
}
} // namespace qamlib
