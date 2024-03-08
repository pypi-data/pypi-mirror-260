Version 0.8.0
=============

New
---

* Add :py:class:`DeviceInfo` to hold some V4L2 driver information for the
  device.

* Exposure :py:class:`TriggerSequenceValue` in non-Qtec builds.

Fixes
-----

* Add missing fields to :py:class:`BaseEvent`.

* Fix an issue with not freeing buffers if we fail to start the stream.

* Allow opening a camera device without needing format IOCTLs to function.

* Fix :py:meth:`.set_crop` to only do :py:meth:`.set_resolution` if necessary.

Version 0.7.3
=============

New
---

* Added :py:attr:`.device_info` and :py:class:`DeviceInfo`.

Fixes
-----

* Made the ``Camera`` constructor a bit more accepting of video devices that are
  not fully V4L2 compliant.

Version 0.7.2
=============

Fixes
-----

* Fix duplicated line causing an import error.

Version 0.7.1
=============

Fixes
-----

* Fix not being able to start the stream if starting the stream previously
  failed due to the device being busy.

Version 0.7.0
=============

Changes
-------

* Do control name mapping for the keys of the dictionary returned by
  :py:meth:`.list_controls` and the control name arguments for
  :py:meth:`.get_control`, :py:meth:`.set_control`, :py:meth:`.get_controls`,
  and :py:meth:`.set_controls` will be mapped similarly to ``v4l2-ctl``.

Fixes
-----

* Fix :py:func:`qamlib.ArrayControlValue.to_json` flattening JSON array, it now
  outputs the values in the correct dimensions.

* No longer try to flip croppings if horizontal or vertical flip is set in
  :py:meth:`.set_control`.

Version 0.6.0
=============

Fixes
-----

* Fix :py:meth:`.list_controls` not getting updated control information at
  every call, since this information could be out of date.

* Fix :py:meth:`.get_frame` not aborting on ``SIGINT`` (``Ctrl-C``) from Python.

Version 0.5.0
=============

New
---

* Added ``default_value`` argument to :py:meth:`.get_ext_control` and
  :py:meth:`.get_controls`, to make it possible to get the default value of
  extended controls.

Fixes
-----

* Fix FourCC's not being stripped of trailing space.

Version 0.4.0
=============

New
---

* Added example of using the :code:`EventDevice` class

Changes
-------

* Deprecate :code:`TriggerSequenceValue.add_sequence` in favor of
  :code:`TriggerSequenceValue.add_exposure`

* Improved the C++ interface by adding namespaces and fixing the
  :code:`meson.build` to work again and produce a static library.

  * Changed the get/set control functions to work better for C++
  * Made :code:`ArrayControlValue` usable from C++ by using OpenCV's
    :code:`Mat` class to get and set the value.

Fixes
-----

* Fix :code:`get_framerate()` to return fractional framerates (eg. 23.6)

Version 0.3.0
=============

New
---

* Implement buffering of frames.

  * Let user get a buffered frame with :code:`get_frame(buffered=True)`,
    :code:`get_frame()` will still get the newest frame.
  * Add :code:`DroppedFrameException` to signal if :code:`buffered=True` and we
    detect that frames have been dropped. The exception can be disabled with
    :code:`Camera(overflow_exception=False)`
  * A :code:`runtime_error` will be thrown if we detect that :code:`qamlib`
    can't keep up with the driver

Version 0.2.0
==============

New
----

* Support multi-crop (Qtec builds)

* Support extended controls (integer, string, array and trigger sequence)

  * Added functions :code:`get_ext_control` and :code:`set_ext_control`
  * Added functions :code:`get_controls` and :code:`set_controls` that allows
    getting/setting multiple controls at once.
  * Added support classes :code:`IntegerControlValue`,
    :code:`StringControlValue`, :code:`ArrayControlValue` and
    :code:`TriggerSequenceValue`.

* Add :code:`to_json` for data structures to allow JSON serialization

* Support V4L2 events on a device, with new ``EventDevice`` class

  * Also added support classes (:code:`BaseEvent`, :code:`ControlEvent` and
    :code:`SourceEvent`) for the events.

* Added optional timeout to :code:`Camera.get_frame()`

* Add option of requesting a different amount of V4L2 buffers with a
  :code:`buffers=10` argument in constructors

Fixes
------

* Fix flipping selections even when the value of the flip control does not
  change

* Fix sometimes giving an old frame, when the stream is started again. When a
  frame from a previous stream start, was not retrieved (:code:`get_frame`)

* Fix FPS resolution not allowing fractional framerates, e.g. :code:`19.3`
