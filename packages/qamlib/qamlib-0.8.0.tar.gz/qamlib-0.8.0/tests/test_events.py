import time
import qamlib
from qamlib import EventType

num_events = 0

def cb(event):
    global num_events
    num_events += 1

    if event.type == qamlib.EventType.CTRL:
        pass
    elif event.type == EventType.SOURCE_CHANGE:
        raise Exception("Driver doesn't support SOURCE_CHANGE event yet")
    else:
        raise Exception("Unkown event type")


cam = qamlib.Camera()

evs = qamlib.EventDevice()

evs.set_callback(cb)

ctrls = cam.list_controls()

# Subscribe to events for all controls
for c in ctrls:
    evs.subscribe(qamlib.EventType.CTRL, ctrls[c].id)

evs.start()

num_send = 50


print("Creating exposure events")
for i in range(num_send):
    cam.set_control("exposure time absolute", ctrls["exposure time absolute"].min + 5 * i)
    time.sleep(.1) # Sleep to ensure the events are seperated


# Ensure that all events have been received
time.sleep(.5)

assert num_events == num_send, f"Did not receive expected number of events: {num_events} vs {num_send}"

evs.stop()
