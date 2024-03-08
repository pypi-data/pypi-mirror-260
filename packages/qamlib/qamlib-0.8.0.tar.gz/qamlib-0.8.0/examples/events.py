import qamlib
from qamlib import EventType

def cb(event):
    global num_events
    if event.type == qamlib.EventType.CTRL:
        print("Got control event")
    else:
        raise Exception("Unkown event type")

evs = qamlib.EventDevice()

evs.set_callback(cb)

cam = qamlib.Camera()
ctrls = cam.list_controls()

# Subscribe to events for all controls
for c in ctrls:
    evs.subscribe(qamlib.EventType.CTRL, ctrls[c].id)

# Start listening
evs.start()

# Do stuff

# Stop listening
evs.stop()
