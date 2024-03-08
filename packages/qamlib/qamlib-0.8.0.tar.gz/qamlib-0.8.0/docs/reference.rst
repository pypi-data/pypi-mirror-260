:tocdepth: 3

Reference
###########
.. module:: qamlib

Devices
============
.. autoclass:: Device

.. autoclass:: StreamingDevice
   :special-members: __enter__, __exit__

.. autoclass:: Camera
   :special-members: __init__

.. autoclass:: EventDevice
   :special-members: __init__

Controls
========

.. autoclass:: Control
.. autoclass:: MenuControl
.. autoclass:: IntegerMenuControl
.. autoclass:: ControlFlags


ControlValue classes
====================

.. autoclass:: ControlValue
.. autoclass:: IntegerControlValue
   :special-members: __init__
.. autoclass:: StringControlValue
   :special-members: __init__
.. autoclass:: ArrayControlValue
   :special-members: __init__
.. autoclass:: TriggerSequenceValue
   :special-members: __init__


Formats
=======

.. autoclass:: ImageFormat
.. autoclass:: ImageFormatFlags
.. autoclass:: Format
.. autoclass:: SinglePlaneFormat
.. autoclass:: PixelFormat
.. autoclass:: PixelFormatFlags


Framerates
==========

.. autoclass:: FrameRate
.. autoclass:: DiscreteFrameRate
.. autoclass:: ContinuousFrameRate
.. autoclass:: StepwiseFrameRate


Events
=======

.. autoclass:: BaseEvent
.. autoclass:: ControlEvent
.. autoclass:: EventType
.. autoclass:: ControlChangesFlags


Misc
====

.. autoclass:: FrameMetadata
.. autoclass:: Rectangle
.. autoclass:: DeviceInfo

Exceptions
==========
.. autoexception:: V4L2Exception
.. autoexception:: TimeoutException
.. autoexception:: DroppedFrameException
