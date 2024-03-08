// SPDX-License-Identifier: LGPL-2.0
/*
 * event_device.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "event_device.h"

#include <sys/ioctl.h>

namespace qamlib
{
void EventDevice::event_manager()
{
	int ret;
	fd_set fds;
	struct timeval tv;
	struct v4l2_event event;

	while (running) {
		do {
			FD_ZERO(&fds);
			FD_SET(fd, &fds);

			/* Timeout. */
			tv.tv_sec = 0;
			tv.tv_usec = 20000;

			// V4L2 events use exceptions so use exceptfds
			ret = select(fd + 1, NULL, NULL, &fds, &tv);
		} while ((ret == -1 && (errno == EINTR)));

		if (ret == 0) {
			// Timeout, so we try again
			continue;
		} else if (ret == -1) {
			throw V4L2Exception("Got error on select()", errno);
		}

		CLEAR(event);

		if (ioctl(fd, VIDIOC_DQEVENT, &event)) {
			throw V4L2Exception("Could not dequeue event", errno);
		}

		switch (event.type) {
		case V4L2_EVENT_VSYNC:
		case V4L2_EVENT_EOS:
		case V4L2_EVENT_FRAME_SYNC:
		case V4L2_EVENT_MOTION_DET:
			throw V4L2Exception("Event type not supported yet: " +
					    event_type_representation(
						    EventType(event.type)));
		case V4L2_EVENT_SOURCE_CHANGE:
			cb_lock.lock();
			callback(std::unique_ptr<BaseEvent>(
				new SourceEvent(event)));
			cb_lock.unlock();
			break;
		case V4L2_EVENT_CTRL:
			cb_lock.lock();
			callback(std::unique_ptr<BaseEvent>(
				new ControlEvent(event)));
			cb_lock.unlock();
			break;
		default:
			throw V4L2Exception("Unkown event type");
		}
	}
}

/*
 * PUBLIC
 */
void EventDevice::set_callback(
	const std::function<void(std::unique_ptr<BaseEvent>)> &cb)
{
	cb_lock.lock();
	callback = cb;
	cb_lock.unlock();
}

void EventDevice::start()
{
	running = true;

	event_thread = std::thread(&EventDevice::event_manager, this);
}

void EventDevice::stop()
{
	running = false;
	event_thread.join();
}

void EventDevice::subscribe(uint32_t type, uint32_t id)
{
	struct v4l2_event_subscription event_sub;

	switch (type) {
	case V4L2_EVENT_ALL:
		throw V4L2Exception("Type ALL not allowed in subscribe");
	case V4L2_EVENT_VSYNC:
	case V4L2_EVENT_EOS:
	case V4L2_EVENT_FRAME_SYNC:
	case V4L2_EVENT_MOTION_DET:
		throw V4L2Exception("Type not supported yet");
	case V4L2_EVENT_SOURCE_CHANGE:
	case V4L2_EVENT_CTRL:
		event_sub.type = type;
		event_sub.id = id;
		break;

	default:
		throw V4L2Exception("Unknown event type");
	}

	if (ioctl(fd, VIDIOC_SUBSCRIBE_EVENT, &event_sub)) {
		throw V4L2Exception("Could not subscribe to event", errno);
	}
}

void EventDevice::unsubscribe(uint32_t type, uint32_t id)
{
	struct v4l2_event_subscription event_sub;

	switch (type) {
	case V4L2_EVENT_ALL:
		event_sub.type = type;
		break;
	case V4L2_EVENT_VSYNC:
	case V4L2_EVENT_EOS:
	case V4L2_EVENT_FRAME_SYNC:
	case V4L2_EVENT_MOTION_DET:
		throw V4L2Exception("Type not supported yet");
	case V4L2_EVENT_SOURCE_CHANGE:
		event_sub.type = type;
		break;
	case V4L2_EVENT_CTRL:
		event_sub.type = type;
		event_sub.id = id;
		break;

	default:
		throw V4L2Exception("Unknown event type");
	}

	if (ioctl(fd, VIDIOC_UNSUBSCRIBE_EVENT, &event_sub)) {
		throw V4L2Exception("Could not unsubscribe from event", errno);
	}
}
} // namespace qamlib
