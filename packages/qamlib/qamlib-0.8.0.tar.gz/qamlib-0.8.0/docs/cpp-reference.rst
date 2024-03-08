C++ reference
#############

This is for the most part identical to the Python reference, so much of the
descriptions are not here, The descriptions are mostly for the parts that differ
from the Python interface.

Devices
=======

Device
------
.. doxygenclass:: qamlib::Device

StreamingDevice
---------------
.. doxygenclass:: qamlib::StreamingDevice

Camera
------
.. doxygenclass:: qamlib::Camera

Controls
========

Control
-------
.. doxygenclass:: qamlib::Control

MenuControl
------------
.. doxygenclass:: qamlib::MenuControl

IntegerMenuControl
------------------
.. doxygenclass:: qamlib::IntegerMenuControl

ControlFlags
------------------
.. doxygenclass:: qamlib::ControlFlags

ControlValue classes
====================

IntegerControlValue
--------------------
.. doxygenclass:: qamlib::IntegerControlValue

StringControlValue
--------------------
.. doxygenclass:: qamlib::StringControlValue

ArrayControlValue
--------------------
.. doxygenclass:: qamlib::ArrayControlValue

Formats
=======

ImageFormat
--------------------
.. doxygenclass:: qamlib::ImageFormat

ImageFormatFlags
--------------------
.. doxygenclass:: qamlib::ImageFormatFlags

Format
--------------------
.. doxygenclass:: qamlib::Format

SinglePlaneFormat
--------------------
.. doxygenclass:: qamlib::SinglePlaneFormat

PixelFormat
--------------------
.. doxygenclass:: qamlib::PixelFormat

PixelFormatFlags
--------------------
.. doxygenclass:: qamlib::PixelFormatFlags


Framerates
===========

FrameRate
--------------------
.. doxygenclass:: qamlib::FrameRate

DiscreteFrameRate
--------------------
.. doxygenclass:: qamlib::DiscreteFrameRate

ContinuousFrameRate
--------------------
.. doxygenclass:: qamlib::ContinuousFrameRate

StepwiseFrameRate
--------------------
.. doxygenclass:: qamlib::StepwiseFrameRate


Events
======

BaseEvent
--------------------
.. doxygenclass:: qamlib::BaseEvent

ControlEvent
--------------------
.. doxygenclass:: qamlib::ControlEvent

EventType
--------------------
.. doxygenenum:: qamlib::EventType

ControlChangesFlags
--------------------
.. doxygenclass:: qamlib::ControlChangesFlags


Misc
====

FrameMetadata
--------------------
.. doxygenclass:: qamlib::FrameMetadata

Rectangle
--------------------
.. doxygenclass:: qamlib::Rectangle


Exceptions
==========

V4L2Exception
--------------------
.. doxygenclass:: qamlib::V4L2Exception

TimeoutException
--------------------
.. doxygenclass:: qamlib::TimeoutException

DroppedFrameException
---------------------
.. doxygenclass:: qamlib::DroppedFrameException
