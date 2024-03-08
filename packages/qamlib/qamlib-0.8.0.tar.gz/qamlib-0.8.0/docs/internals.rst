qamlib Internals
=================

Buffering and V4L2 buffers
--------------------------
To allow buffering and still be able drop the oldest frames if we run out of
buffer space, ``qamlib`` implements a ring buffer in userspace where we hold
the latest V4L2 buffers untill they are wanted or dropped/skipped. This means
that we create more V4L2 buffers than strictly necessary, so that we can fill
the userspace ringbuffer while still having buffers for the driver.

The user is able to specify the amount of buffering they want by setting the
``buffers`` argument for the :class:`.Camera` constructor, if set, starting the
stream will result in an exception if we are unable to allocate enough V4L2
buffers to reach the desired amount of buffers. If the user does not request a
specific amount of buffers then ``qamlib`` will default to a ringbuffer of size
10 but it may be smaller if we are not able to allocate enough V4L2 buffers to
reach that size, but if we can't allocate more than 2 V4L2 buffers, then it
will also result in an exception.

When streaming, to use the buffered call ``get_frame(buffered=True)``, this
will get the next frame in the buffer as opposed to the newest frame. When
calling ``get_frame(buffered=True)`` if ``qamlib`` detects that one or more
frames have been dropped from the ringbuffer then a
:class:`.DroppedFrameException` will be thrown, it is possible to suppress
throwing this exception.


Streaming
-----------
Changing format, resolution or crop will force a stop, restart of streaming and
thus the possibility of not being able to get the same amount of V4L2 buffers
as before
