Usage
===========
Here is a small usage example of setting exposure time, and printing what value
actually got set (this might not always be exactly the value we requested), then
start the stream and get a single frame and frame metadata

::

    import qamlib

    cam = qamlib.Camera() # Opens /dev/qtec/video0

    # Try to set exposure time (us)
    cam.set_control("Exposure Time, Absolute", 1000)

    exp = cam.get_control("Exposure Time, Absolute")

    # Print the exposure time that we ended up with
    print(f"Got exposure time {exp}us")

    # Start and stop streaming with context manager
    with cam:
        meta, frame = cam.get_frame()

        print(meta.sequence) # Frame number since start of streaming

Bigger example
--------------
.. literalinclude:: ../examples/qamlib_test.py
   :language: python
   :linenos:

ExtendedControl usage
---------------------
.. literalinclude:: ../examples/extended_controls.py
   :language: python
   :linenos:

HDR example
------------

.. literalinclude:: ../examples/hdr_capture_and_save.py
   :language: python
   :linenos:

Events example
--------------

.. literalinclude:: ../examples/events.py
   :language: python
   :linenos:
