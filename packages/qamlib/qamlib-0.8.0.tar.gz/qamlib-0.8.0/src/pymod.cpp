// SPDX-License-Identifier: LGPL-2.0
/*
 * pymod.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "pybind11_json/pybind11_json.hpp"

#include <iostream>
#include <vector>
#include <linux/version.h>

#include "device.h"
#include "camera.h"
#include "event_device.h"
#include "framerate.h"
#include "streaming_device.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

using namespace qamlib;
/*
 * Iterator class for Rectangle because I could not get py::make_iterator to
 * work, and we want to have Rectangle be iterable to we can do
 * left, top, width, height = Rectangle()
 */
template <typename T> class VectorIterator {
	size_t index = 0;
	std::vector<T> values;

    public:
	VectorIterator(std::vector<T> values) : values(values)
	{
	}

	T next()
	{
		if (index >= values.size()) {
			throw py::stop_iteration();
		}
		int res = values[index];
		index++;
		return res;
	}
};

/* Device */
char device_info_docs[] = ":py:class:`DeviceInfo` object";

char get_control_docs0[] =
	"Get current value of control by name\n\n"
	"This is only for non-extended controls (eg. integer, menu, etc.)\n\n"
	":param name: Full name of the control, case is ignored.\n\n"
	":returns: The integer value of the given control.";
char get_control_docs1[] =
	"Get current value of control by id.\n\n"
	"This is only for non-extended controls (eg. integer, menu, etc.)\n\n"
	":param id: ID of the control, there is no check if a control with that"
	" ID actually exists.\n\n"
	":returns: The integer value of the given control";

char get_controls_docs[] =
	"Get current values of a list of (extended) control names\n\n"
	":param names: List of full control names, case is ignored\n\n"
	":param default_value: If ``True`` the default value of the control is "
	"returned.\n\n"
	":returns: A dictionary with lower-case control names as keys, and a "
	":class:`ControlValue` with the value of the given control.";

char get_ext_control_docs[] =
	"Get current value of an (extended) control\n\n"
	":param name: Full name of the control, case is ignored.\n\n"
	":param default_value: If ``True`` the default value of the control is "
	"returned.\n\n"
	":returns: A :class:`ControlValue` with the value of the given control";

char list_controls_docs[] =
	"List all the controls for the device\n\n"
	":returns: A list of all controls and their information.";

char set_control_docs0[] =
	"Set a normal named control to desired value.\n\n"
	":param name: Full name of the control, case is ignored.\n\n"
	":param value: Integer value to set.\n\n"
	"NOTE: If the chosen control is either VFLIP or HFLIP, it tries to flip"
	" the selection as well";

char set_control_docs1[] =
	"Set a normal control, by id to desired value\n\n"
	":param id: ID of the control, there is no check if a control with that"
	" ID actually exists.\n\n"
	":param value: Integer value to set.\n\n"
	" NOTE: This function does not do any checks of the control ID or value";

char set_controls_docs[] =
	"Set values of (extended) controls by name\n\n"
	":param values: A dictionary of control names as keys (case is ignored)"
	", and a :class:`ControlValue` derived class with the value to be set "
	"for the control.";

char set_ext_control_docs[] =
	"Set value of an (extended) control\n\n"
	":param name: Full name of the control, case is ignored.\n\n"
	":param ctrl_val: A :class:`ControlValue` derived class with the value"
	" to set for the control.";

/* StreamingDevice */
char streaming_device_docs[] =
	"Base class for devices that support streaming, inherits from "
	":class:`.Device`";

char enter_docs[] = "Enter runtime context, starts the device stream";
char exit_docs[] = "Exit runtime context, stops the stream";
char get_crop_docs[] = "Get current crop selection (left, top, width, height)";
char get_crop_bounds_docs[] = "Get crop selection bounds (left, top, width, "
			      "height)";
char get_crop_default_docs[] = "Get default crop selection (left, top, width, "
			       "height)";
char list_formats_docs[] = "List all available formats for the device";
char set_crop_docs0[] = "Set crop selection using V4L2s selection API";
char set_crop_docs1[] =
	"Set crop selections, using V4L2s selection API, there "
	"are some driver and logic limitations to multi-crop, because of this, "
	"all lefts/widths will be the same as the first rectangle, and the "
	"rectangles cannot overlap (this will result in an exception)";
char start_docs[] = "Starts the device stream";
char stop_docs[] = "Stops the device stream";
char get_resolution_docs[] = "Get current resolution";
char set_format_docs0[] = "Set image format";
char set_format_docs1[] = "Set image format by format name, this function also"
			  "scales selection for the new format";
char set_framerate_docs[] = "Tries to set the desired framerate, returns the "
			    "actual framerate that we got";
char set_resolution_docs[] = "Try to set the desired resolution, and returns "
			     "the resolution that was set";

/* Camera */
char camera_docs[] = "Class for a V4L2 capture device, inherits from "
		     ":class:`StreamingDevice`";

char camera_init0[] =
	"Open V4L2 device at ``path``.\n\n"
	":param path: Path to the V4L2 capture device\n\n"
	":param buffers: The size of the userspace ring-buffer. ``qamlib`` will"
	" request a small amount ``>buffers`` so the driver always has a buffer"
	" ready. See ``get_frame`` for when and how the buffer is used.\n\n"
	":param overflow_exception: Whether to throw "
	":class:`DroppedFrameException` when frames are dropped in  "
	"``get_frame(buffered=True)``";

char camera_init1[] =
	"Open V4L2 device number: ``device_num``.\n\n"
	":param device_num: Video device number. (``/dev/videoX``)\n\n"
	":param buffers: The size of the userspace ring-buffer. ``qamlib`` will"
	" request a small amount ``>buffers`` so the driver always has a buffer"
	" ready. See ``get_frame`` for when and how the buffer is used.\n\n"
	":param overflow_exception: Whether to throw "
	":class:`DroppedFrameException` when frames are dropped in  "
	"``get_frame(buffered=True)``";

char camera_init2[] =
	"Opens ``/dev/qtec/video0``\n\n"
	":param overflow_exception: Whether to throw "
	":class:`DroppedFrameException` when frames are dropped in  "
	"``get_frame(buffered=True)``";

char get_format_docs[] = "Get the currently set format";

char get_frame_docs[] =
	"Get frame from camera.\n\n"
	":param timeout: If >0 then the call will throw "
	":class:`TimeoutException` if no frame is ready after the set amount "
	"of seconds.\n\n"
	":param buffered: If ``True`` then the next frame in the buffer is "
	"returned, otherwise the newest frame in the buffer is returned.\n\n"
	":returns: The :class:`FrameMetadata` for the frame and the frame as a "
	"NumPy ``ndarray``\n\n"
	":raises TimeoutException: If the ``timeout>0`` is reached.\n\n"
	":raises DroppedFrameException: If ``buffered=True`` and the buffer has"
	" overrun.\n\n";

char get_framerate_docs[] = "Get current framerate in frames per second (FPS)";

char get_framerates_docs0[] =
	"Get possible framerates for current resolution and format\n\n"
	":returns: A :class:`FrameRate` derived object with the possible "
	"framerates.";
char get_framerates_docs1[] =
	"Get possible framerates for current format at the given resolution\n\n"
	":param width: Frame width.\n\n"
	":param height: Frame height.\n\n"
	":returns: A :class:`FrameRate` derived object with the possible "
	"framerates.";
char get_framerates_docs2[] =
	"Get possible framerates for the given format at the given "
	"resolution\n\n"
	":param width: Frame width.\n\n"
	":param height: Frame height.\n\n"
	":param pixelformat: FourCC name of the format (eg. \"RGB\")\n\n"
	":param big_endian: Whether the format is big endian. This is "
	"also true if the ``pixelformat`` name has \"_BE\" appended to it\n\n"
	":returns: A :class:`FrameRate` derived object with the possible "
	"framerates.";

/* EventDevice */
char event_device_docs[] = "Class for getting events from a V4L2 device";
char set_callback_docs[] = "Set the callback function";
char start_events_docs[] = "Start capturing events";
char stop_events_docs[] = "Stop capturing events";
char subscribe_docs[] = "Subscribe to event";
char unsubscribe_docs[] = "Unsubscribe from event";

PYBIND11_MODULE(qamlib, m)
{
	m.doc() =
		"The qamlib module is an interface to V4L2 IOCTL calls, written "
		"in C++"; // optional module docstring

	m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);

	/*
	 * Custom iterators for vectors, could not get pybind11::make_iterator
	 * to work.
	 */
	py::class_<VectorIterator<int> >(m, "IntVectorIterator")
		.def("__next__", &VectorIterator<int>::next);

	py::class_<VectorIterator<double> >(m, "DoubleVectorIterator")
		.def("__next__", &VectorIterator<double>::next);

	/*
	 * FrameRate classes
	 */
	py::enum_<v4l2_frmivaltypes>(m, "FrameRateType")
		.value("DISCRETE", V4L2_FRMIVAL_TYPE_DISCRETE)
		.value("CONTINUOUS", V4L2_FRMIVAL_TYPE_CONTINUOUS)
		.value("STEPWISE", V4L2_FRMIVAL_TYPE_STEPWISE);

	py::class_<FrameRate>(m, "FrameRate", "Base class for FrameRate types")
		.def_readonly("type", &FrameRate::type);

	py::class_<DiscreteFrameRate, FrameRate>(
		m, "DiscreteFrameRate",
		"Represents a list of discrete framerates")
		.def_readonly("values", &DiscreteFrameRate::values,
			      "FPS values")
		.def("to_json", &DiscreteFrameRate::to_json)
		.def("__repr__", &DiscreteFrameRate::to_string)
		.def("__str__", &DiscreteFrameRate::to_string)
		.def(
			"__iter__",
			[](DiscreteFrameRate &fps) {
				return VectorIterator<double>(fps.values);
			},
			py::keep_alive<0, 1>());

	py::class_<ContinuousFrameRate, FrameRate>(
		m, "ContinuousFrameRate", "Represents a continous framerate")
		.def_readonly("min", &ContinuousFrameRate::min, "Minimum FPS")
		.def_readonly("max", &ContinuousFrameRate::max, "Maximum FPS")
		.def("to_json", &ContinuousFrameRate::to_json)
		.def("__repr__", &ContinuousFrameRate::to_string)
		.def("__str__", &ContinuousFrameRate::to_string)
		.def(
			"__iter__",
			[](ContinuousFrameRate &fps) {
				return VectorIterator<double>(
					{ fps.min, fps.max });
			},
			py::keep_alive<0, 1>());

	py::class_<StepwiseFrameRate, ContinuousFrameRate>(
		m, "StepwiseFrameRate",
		"Inherits from ContinuousFrameRate. "
		"Represents a stepwise framerate")
		.def_readonly("step", &StepwiseFrameRate::min, "FPS step size")
		.def("to_json", &StepwiseFrameRate::to_json)
		.def("__repr__", &StepwiseFrameRate::to_string)
		.def("__str__", &StepwiseFrameRate::to_string)
		.def(
			"__iter__",
			[](StepwiseFrameRate &fps) {
				return VectorIterator<double>(
					{ fps.min, fps.max, fps.step });
			},
			py::keep_alive<0, 1>());

	/*
	 * CONTROLS
	 */
	py::enum_<v4l2_ctrl_type>(m, "ControlType")
		.value("INTEGER", v4l2_ctrl_type::V4L2_CTRL_TYPE_INTEGER)
		.value("BOOLEAN", v4l2_ctrl_type::V4L2_CTRL_TYPE_BOOLEAN)
		.value("MENU", v4l2_ctrl_type::V4L2_CTRL_TYPE_MENU)
		.value("INTEGER_MENU",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_INTEGER_MENU)
		.value("STRING", v4l2_ctrl_type::V4L2_CTRL_TYPE_STRING)
		.value("BITMASK", v4l2_ctrl_type::V4L2_CTRL_TYPE_BITMASK)
		.value("BUTTON", v4l2_ctrl_type::V4L2_CTRL_TYPE_BUTTON)
		.value("INTEGER64", v4l2_ctrl_type::V4L2_CTRL_TYPE_INTEGER64)
		// Compound types
		.value("U8", v4l2_ctrl_type::V4L2_CTRL_TYPE_U8)
		.value("U16", v4l2_ctrl_type::V4L2_CTRL_TYPE_U16)
		.value("U32", v4l2_ctrl_type::V4L2_CTRL_TYPE_U32)
#ifdef QTEC_HEADER
		.value("TRIG_SEQ", v4l2_ctrl_type::V4L2_CTRL_TYPE_TRIG_SEQ)
		.value("POINT", v4l2_ctrl_type::V4L2_CTRL_TYPE_POINT)
#endif
// Make sure kernel is new enough to have all the encoding controls
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 14, 0)
		.value("HDR10_CLL_INFO",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_HDR10_CLL_INFO)
		.value("HDR10_MASTERING_DISPLAY",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_HDR10_MASTERING_DISPLAY)
		.value("MPEG2_QUANTISATION",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_MPEG2_QUANTISATION)
		.value("MPEG2_SEQUENCE",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_MPEG2_SEQUENCE)
		.value("MPEG2_PICTURE",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_MPEG2_PICTURE)

		.value("H264_SPS", v4l2_ctrl_type::V4L2_CTRL_TYPE_H264_SPS)
		.value("H264_PPS", v4l2_ctrl_type::V4L2_CTRL_TYPE_H264_PPS)
		.value("H264_SCALING_MATRIX",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_H264_SCALING_MATRIX)
		.value("H264_SLICE_PARAMS",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_H264_SLICE_PARAMS)
		.value("H264_DECODE_PARAMS",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_H264_DECODE_PARAMS)

		.value("FWHT_PARAMS",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_FWHT_PARAMS)
		.value("VP8_FRAME", v4l2_ctrl_type::V4L2_CTRL_TYPE_VP8_FRAME)
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 5, 0)
		.value("AREA", v4l2_ctrl_type::V4L2_CTRL_TYPE_AREA)
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 17, 0)
		.value("VP9_COMPRESSED_HDR",
		       v4l2_ctrl_type::V4L2_CTRL_TYPE_VP9_COMPRESSED_HDR)
		.value("VP9_FRAME", v4l2_ctrl_type::V4L2_CTRL_TYPE_VP9_FRAME)
#endif
		// This is moved to last, just to have a permanent line ending
		// with a semicolon (;)
		.value("CTRL_CLASS", v4l2_ctrl_type::V4L2_CTRL_TYPE_CTRL_CLASS);

	py::class_<Control, std::shared_ptr<Control> >(
		m, "Control",
		"This class represents the information about a camera "
		"control.")
		.def_readonly("id", &Control::id, "ID of the camera control")
		.def_readonly("name", &Control::name,
			      "Name of the camera control")
		.def_readonly("type", &Control::type,
			      "Type of the camera control")
		.def_readonly("flags", &Control::flags,
			      "Class representing the control flags")
		.def("to_json", &Control::to_json)
		.def("__repr__", &Control::to_string)
		.def("__str__", &Control::to_string);

	py::class_<ValueControl, std::shared_ptr<ValueControl>, Control>(
		m, "ValueControl",
		"Inherits from Control, represents a normal control with a "
		"single value")
		.def_readonly("min", &ValueControl::min,
			      "The minimum value of the camera control")
		.def_readonly("max", &ValueControl::max,
			      "The maximum value of the camera control")
		.def_readonly("default_value", &ValueControl::default_value,
			      "The default value of the camera control")
		.def_readonly("step", &ValueControl::step,
			      "The step size of the camera control")
		.def("to_json", &ValueControl::to_json)
		.def("__repr__", &ValueControl::to_string)
		.def("__str__", &ValueControl::to_string);

	py::class_<MenuControl, std::shared_ptr<MenuControl>, ValueControl>(
		m, "MenuControl",
		"Inherits from ValueControl. Represents a menu control, with "
		"the names of the items")
		.def_readonly("items", &MenuControl::items,
			      "Names of the menu items")
		.def("to_json", &MenuControl::to_json)
		.def("__repr__", &MenuControl::to_string)
		.def("__str__", &MenuControl::to_string);

	py::class_<IntegerMenuControl, std::shared_ptr<IntegerMenuControl>,
		   ValueControl>(
		m, "IntegerMenuControl",
		"Inherits from Control. Reprenests an integer menu control, "
		"with the values of the items")
		.def_readonly("items", &IntegerMenuControl::items,
			      "Values of the menu items")
		.def("to_json", &IntegerMenuControl::to_json)
		.def("__repr__", &IntegerMenuControl::to_string)
		.def("__str__", &IntegerMenuControl::to_string);

	py::class_<ExtendedControl, std::shared_ptr<ExtendedControl>,
		   ValueControl>(
		m, "ExtendedControl",
		"Inherits from Control, represents a extended control "
		"control with a single value")
		.def_readonly("element_size", &ExtendedControl::elem_size,
			      "The size of the control elements")
		.def_readonly("elements", &ExtendedControl::elems,
			      "The number of control elemets")
		.def_readonly("dimensions", &ExtendedControl::dimensions,
			      "The dimensions of the element array")
		.def("to_json", &ExtendedControl::to_json)
		.def("__repr__", &ExtendedControl::to_string)
		.def("__str__", &ExtendedControl::to_string);

	py::class_<ControlFlags>(
		m, "ControlFlags",
		"Class that represents the flags of a control.\nFor more "
		"information about their meaning see `here "
		"<https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-queryctrl.html#control-flags>`__.")
		.def_readonly("raw_flags", &ControlFlags::flags,
			      "The integer containing the V4L2 control flags")
		.def_property_readonly("disabled", &ControlFlags::disabled)
		.def_property_readonly("grabbed", &ControlFlags::grabbed)
		.def_property_readonly("read_only", &ControlFlags::read_only)
		.def_property_readonly("update", &ControlFlags::update)
		.def_property_readonly("inactive", &ControlFlags::inactive)
		.def_property_readonly("slider", &ControlFlags::slider)
		.def_property_readonly("write_only", &ControlFlags::write_only)
		.def_property_readonly("is_volatile",
				       &ControlFlags::is_volatile)
		.def_property_readonly("has_payload",
				       &ControlFlags::has_payload)
		.def_property_readonly("execute_on_write",
				       &ControlFlags::execute_on_write)
		.def_property_readonly("modify_layout",
				       &ControlFlags::modify_layout)
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 0, 0)
		.def_property_readonly("dynamic_array",
				       &ControlFlags::dynamic_array)
#endif
		.def("to_json", &ControlFlags::to_json)
		.def("__repr__", &ControlFlags::to_string)
		.def("__str__", &ControlFlags::to_string);

	/*
	 * EXTENDED CONTROLS
	 */
	py::class_<ControlValue>(m, "ControlValue",
				 "Base class for extended control values");

	py::class_<StringControlValue, ControlValue>(
		m, "StringControlValue",
		"Class that represents a string control value")
		.def(py::init<std::string &>(), py::arg("value"))
		.def_property_readonly("value", &StringControlValue::to_string)
		.def("to_json", &StringControlValue::to_json)
		.def("__repr__", &StringControlValue::to_string)
		.def("__str__", &StringControlValue::to_string);

	py::class_<IntegerControlValue, ControlValue>(
		m, "IntegerControlValue",
		"Class that represents a integer control value")
		.def(py::init<int64_t>(), py::arg("value"))
		.def_property_readonly("value", &IntegerControlValue::get_value)
		.def("to_json", &IntegerControlValue::to_json)
		.def("__repr__", &IntegerControlValue::to_string)
		.def("__str__", &IntegerControlValue::to_string);

	py::class_<ArrayControlValue, ControlValue>(
		m, "ArrayControlValue",
		"Class that represents an array control value")
		.def(py::init<py::array>(), py::arg("array"))
		.def_property_readonly("value", &ArrayControlValue::get_array)
		.def("to_json", &ArrayControlValue::to_json)
		.def("__repr__", &ArrayControlValue::to_string)
		.def("__str__", &ArrayControlValue::to_string);
	py::class_<trigger_sequence>(m, "trigger_sequence",
				     "V4L2 struct for a sequence")
		.def_readwrite("exposure_time",
			       &trigger_sequence::exposure_time)
		.def_readwrite("flash_time", &trigger_sequence::flash_time)
		.def_readwrite("frame_delay", &trigger_sequence::frame_delay)
		.def_readwrite("trigger_delay",
			       &trigger_sequence::trigger_delay)
		.def("__repr__", &representation_trigger_sequence)
		.def("__str__", &representation_trigger_sequence);

	py::class_<TriggerSequenceValue, ControlValue>(
		m, "TriggerSequenceValue",
		"Class that represents the values of a trigger sequence\n\n"
		"NOTE: Qtec specific control at the moment. The trigger "
		"sequence control is not implemented for all Qtec cameras "
		"and/or sensors configurations.")
		.def(py::init())
		.def_property_readonly("value",
				       &TriggerSequenceValue::get_sequence,
				       "The list of sequences")
		.def("clear", &TriggerSequenceValue::clear,
		     "Clear the sequences")
		.def("add_exposure", &TriggerSequenceValue::add_exposure,
		     py::arg("exposure_time"), py::arg("flash_time"),
		     py::arg("frame_delay"), py::arg("trigger_delay"),
		     "Add an exposure to the sequence")
		.def("to_json", &TriggerSequenceValue::to_json)
		.def("__repr__", &TriggerSequenceValue::to_string)
		.def("__str__", &TriggerSequenceValue::to_string);

	/*
	 * MISC
	 */
	py::class_<FrameMetadata>(m, "FrameMetadata",
				  "This class contains the frame metadata.")
		.def_readonly("time", &FrameMetadata::time,
			      "Kernel time for when the frame was taken")
		.def_readonly("clock", &FrameMetadata::clock,
			      "CLOCKID for which kernel clock was used")
		.def_readonly("sequence", &FrameMetadata::sequence,
			      "The sequence number of the frame")
		.def("__repr__", &FrameMetadata::to_string)
		.def("__str__", &FrameMetadata::to_string);

	/*
	 * FORMATS
	 */
	py::class_<ImageFormatFlags>(
		m, "ImageFormatFlags",
		"Class that represents the flags for an image format.\nFor more "
		"information see `here "
		"<https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-enum-fmt.html#fmtdesc-flags>`__.")
		.def_property_readonly("compressed",
				       &ImageFormatFlags::compressed)
		.def_property_readonly("emulated", &ImageFormatFlags::emulated)
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
		.def_property_readonly("continuous_bytestream",
				       &ImageFormatFlags::continuous_bytestream)
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 4, 0)
		.def_property_readonly("dyn_resolution",
				       &ImageFormatFlags::dyn_resolution)
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 9, 0)
		.def_property_readonly(
			"enc_cap_frame_interval",
			&ImageFormatFlags::enc_cap_frame_interval)
#endif
#if LINUX_VERSION_CODE >= KERNEL_VERSION(5, 10, 0)
		.def_property_readonly("csc_colorspace",
				       &ImageFormatFlags::csc_colorspace)
		.def_property_readonly("csc_xfer_func",
				       &ImageFormatFlags::csc_xfer_func)
		.def_property_readonly("csc_ycbcr_enc",
				       &ImageFormatFlags::csc_ycbcr_enc)
		.def_property_readonly("csc_hsv_enc",
				       &ImageFormatFlags::csc_hsv_enc)
		.def_property_readonly("csc_quantization",
				       &ImageFormatFlags::csc_quantization)
#endif
		.def("to_json", &ImageFormatFlags::to_json)
		.def("__repr__", &ImageFormatFlags::to_string)
		.def("__str__", &ImageFormatFlags::to_string);

	py::class_<ImageFormat>(m, "ImageFormat",
				"Class that represents an image format")
		.def_readonly("index", &ImageFormat::index)
		.def_readonly("flags", &ImageFormat::flags)
		.def_readonly("description", &ImageFormat::description)
		.def_readonly("pixelformat", &ImageFormat::pixelformat)
		.def("to_json", &ImageFormat::to_json)
		.def("__repr__", &ImageFormat::to_string)
		.def("__str__", &ImageFormat::to_string);

	py::enum_<v4l2_field>(m, "Field")
		.value("ANY", v4l2_field::V4L2_FIELD_ANY)
		.value("NONE", v4l2_field::V4L2_FIELD_NONE)
		.value("TOP", v4l2_field::V4L2_FIELD_TOP)
		.value("BOTTOM", v4l2_field::V4L2_FIELD_BOTTOM)
		.value("INTERLACED", v4l2_field::V4L2_FIELD_INTERLACED)
		.value("SEQ_TB", v4l2_field::V4L2_FIELD_SEQ_TB)
		.value("SEQ_BT", v4l2_field::V4L2_FIELD_SEQ_BT)
		.value("ALTERNATE", v4l2_field::V4L2_FIELD_ALTERNATE)
		.value("INTERLACED_TB", v4l2_field::V4L2_FIELD_INTERLACED_TB)
		.value("INTERLACED_BT", v4l2_field::V4L2_FIELD_INTERLACED_BT);

	py::enum_<v4l2_colorspace>(m, "ColorSpace")
		.value("DEFAULT", v4l2_colorspace::V4L2_COLORSPACE_DEFAULT)
		.value("SMPTE170M", v4l2_colorspace::V4L2_COLORSPACE_SMPTE170M)
		.value("REC709", v4l2_colorspace::V4L2_COLORSPACE_REC709)
		.value("SRGB", v4l2_colorspace::V4L2_COLORSPACE_SRGB)
		.value("OPRGB", v4l2_colorspace::V4L2_COLORSPACE_OPRGB)
		.value("BT2020", v4l2_colorspace::V4L2_COLORSPACE_BT2020)
		.value("DCI_P3", v4l2_colorspace::V4L2_COLORSPACE_DCI_P3)
		.value("SMPTE240M", v4l2_colorspace::V4L2_COLORSPACE_SMPTE240M)
		.value("470_SYSTEM_M",
		       v4l2_colorspace::V4L2_COLORSPACE_470_SYSTEM_M)
		.value("470_SYSTEM_BG",
		       v4l2_colorspace::V4L2_COLORSPACE_470_SYSTEM_BG)
		.value("JPEG", v4l2_colorspace::V4L2_COLORSPACE_JPEG)
		.value("RAW", v4l2_colorspace::V4L2_COLORSPACE_RAW);

	py::class_<PixelFormatFlags>(
		m, "PixelFormatFlags",
		"Class that represents the flags for a pixel format.\nFor more "
		"information see `here "
		"<https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/pixfmt-v4l2.html#format-flags>`__.")
		.def("to_json", &PixelFormatFlags::to_json)
		.def("__repr__", &PixelFormatFlags::to_string)
		.def("__str__", &PixelFormatFlags::to_string);

	py::class_<PixelFormat>(m, "PixelFormat",
				"Class that represents a V4L2 fourcc code")
		.def_property("fourcc", &PixelFormat::get_fourcc,
			      &PixelFormat::set_fourcc)
		.def("get_code", &PixelFormat::get_code)
		.def_readwrite("big_endian", &PixelFormat::big_endian)
		.def("__repr__", &PixelFormat::to_string)
		.def("__str__", &PixelFormat::to_string);

	py::class_<Format>(m, "Format", "Class that represents the format")
		.def_readonly("type", &Format::type);

	py::class_<SinglePlaneFormat, Format>(
		m, "SinglePlaneFormat",
		"Class that represents a single plane pixel format")
		.def_readwrite("width", &SinglePlaneFormat::width)
		.def_readwrite("height", &SinglePlaneFormat::height)
		.def_readwrite("pixelformat", &SinglePlaneFormat::pixelformat)
		.def_readwrite("field", &SinglePlaneFormat::field)
		.def_readwrite("bytesperline", &SinglePlaneFormat::bytesperline)
		.def_readwrite("sizeimage", &SinglePlaneFormat::sizeimage)
		.def_readwrite("colorspace", &SinglePlaneFormat::colorspace)
		.def_readwrite("priv", &SinglePlaneFormat::priv)
		.def_readwrite("flags", &SinglePlaneFormat::flags)
		.def_readwrite("quantization", &SinglePlaneFormat::quantization)
		.def_readwrite("xfer_func", &SinglePlaneFormat::xfer_func)
		.def("to_json", &SinglePlaneFormat::to_json)
		.def("__repr__", &SinglePlaneFormat::to_string)
		.def("__str__", &SinglePlaneFormat::to_string);

	py::enum_<v4l2_buf_type>(m, "BufferType")
		.value("VIDEO_CAPTURE",
		       v4l2_buf_type::V4L2_BUF_TYPE_VIDEO_CAPTURE)
		.value("VIDEO_CAPTURE_MPLANE",
		       v4l2_buf_type::V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE)
		.value("VIDEO_OUTPUT",
		       v4l2_buf_type::V4L2_BUF_TYPE_VIDEO_OUTPUT)
		.value("VIDEO_OUTPUT_MPLANE",
		       v4l2_buf_type::V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE)
		.value("VIDEO_OVERLAY",
		       v4l2_buf_type::V4L2_BUF_TYPE_VIDEO_OVERLAY)
		.value("VBI_CAPTURE", v4l2_buf_type::V4L2_BUF_TYPE_VBI_CAPTURE)
		.value("VBI_OUTPUT", v4l2_buf_type::V4L2_BUF_TYPE_VBI_OUTPUT)
		.value("SLICED_VBI_CAPTURE",
		       v4l2_buf_type::V4L2_BUF_TYPE_SLICED_VBI_CAPTURE)
		.value("SLICED_VBI_OUTPUT",
		       v4l2_buf_type::V4L2_BUF_TYPE_SLICED_VBI_OUTPUT)
		.value("VIDEO_OUTPUT_OVERLAY",
		       v4l2_buf_type::V4L2_BUF_TYPE_VIDEO_OUTPUT_OVERLAY)
		.value("SDR_CAPTURE", v4l2_buf_type::V4L2_BUF_TYPE_SDR_CAPTURE)
		.value("SDR_OUTPUT", v4l2_buf_type::V4L2_BUF_TYPE_SDR_OUTPUT)
		.value("META_CAPTURE",
		       v4l2_buf_type::V4L2_BUF_TYPE_META_CAPTURE)
		.value("META_OUTPUT", v4l2_buf_type::V4L2_BUF_TYPE_META_OUTPUT);

	py::class_<Rectangle>(m, "Rectangle",
			      "Class to represent a selection rectangle")
		.def(py::init())
		.def(py::init<int, int, int, int>(), py::arg("left"),
		     py::arg("top"), py::arg("width"), py::arg("height"))
		.def_readwrite("left", &Rectangle::left)
		.def_readwrite("top", &Rectangle::top)
		.def_readwrite("width", &Rectangle::width)
		.def_readwrite("height", &Rectangle::height)
		.def(py::self == py::self)
		.def(py::self != py::self)
		.def("__repr__", &Rectangle::to_string)
		.def("__str__", &Rectangle::to_string)
		.def(
			"__iter__",
			[](Rectangle &r) {
				auto vec = r.as_vector();
				return VectorIterator<int>(vec);
			},
			py::keep_alive<0, 1>());

	py::class_<DeviceInfo>(
		m, "DeviceInfo",
		"Class containing information about the video device")
		.def_readonly("driver", &DeviceInfo::driver, "String")
		.def_readonly("card", &DeviceInfo::card, "String")
		.def_readonly("bus_info", &DeviceInfo::bus_info, "String")
		.def("__repr__", &DeviceInfo::to_string)
		.def("__str__", &DeviceInfo::to_string);

	/*
	 * Device classes
	 */
	py::class_<Device>(m, "Device", "Base class for a V4L2 device")
		.def_readonly("device_info", &Device::device_info,
			      device_info_docs)
		.def("get_control",
		     py::overload_cast<const std::string &>(
			     &Device::get_control),
		     py::arg("name"), get_control_docs0)
		.def("get_control",
		     py::overload_cast<uint32_t>(&Device::get_control),
		     py::arg("id"), get_control_docs1)
		.def("get_controls", &Device::get_controls, py::arg("names"),
		     py::arg("default_value") = false, get_controls_docs)
		.def("get_ext_control", &Device::get_ext_control,
		     py::arg("name"), py::arg("default_value") = false,
		     get_ext_control_docs)
		.def("list_controls", &Device::list_controls,
		     list_controls_docs)
		.def("set_control",
		     py::overload_cast<const std::string &, int>(
			     &Device::set_control),
		     py::arg("name"), py::arg("value"), set_control_docs0)
		.def("set_control",
		     py::overload_cast<uint32_t, int>(&Device::set_control),
		     py::arg("id"), py::arg("value"), set_control_docs1)
		.def("set_controls", &Device::set_controls, py::arg("values"),
		     set_controls_docs)
		.def("set_ext_control", &Device::set_ext_control,
		     py::arg("name"), py::arg("ctrl_val"),
		     set_ext_control_docs);

	py::class_<StreamingDevice, Device>(m, "StreamingDevice",
					    streaming_device_docs)
		.def(
			"__enter__", [&](StreamingDevice &dev) { dev.start(); },
			enter_docs)
		.def(
			"__exit__",
			[&](StreamingDevice &dev, py::object exc_type,
			    py::object exc_value,
			    py::object traceback) { dev.stop(); },
			exit_docs)
		.def("get_crop", &StreamingDevice::get_crop, get_crop_docs)
		.def("get_crop_bounds", &StreamingDevice::get_crop_bounds,
		     get_crop_bounds_docs)
		.def("get_crop_default", &StreamingDevice::get_crop_default,
		     get_crop_default_docs)
		.def("list_formats", &StreamingDevice::list_formats,
		     list_formats_docs)
		.def("set_crop",
		     py::overload_cast<int, int, uint32_t, uint32_t>(
			     &StreamingDevice::set_crop),
		     py::arg("left"), py::arg("top"), py::arg("width"),
		     py::arg("height"), set_crop_docs0)
		.def("set_crop",
		     py::overload_cast<Rectangle>(&StreamingDevice::set_crop),
		     py::arg("rectangles"), set_crop_docs0)
#ifdef QTEC_HEADER
		.def("set_crop",
		     py::overload_cast<std::vector<Rectangle> >(
			     &StreamingDevice::set_crop),
		     py::arg("rectangles"), set_crop_docs1)
#endif
		.def("start", &StreamingDevice::start, start_docs)
		.def("stop", &StreamingDevice::stop, stop_docs);

	py::class_<Camera, StreamingDevice>(m, "Camera", camera_docs)
		.def(py::init<const std::string &, std::optional<uint32_t>,
			      bool>(),
		     py::arg("path"), py::arg("buffers") = std::nullopt,
		     py::arg("overflow_exception") = true, camera_init0)
		.def(py::init<uint32_t, std::optional<uint32_t>, bool>(),
		     py::arg("device_num"), py::arg("buffers") = std::nullopt,
		     py::arg("overflow_exception") = true, camera_init1)
#ifdef QTEC_HEADER
		.def(py::init<bool>(), py::arg("overflow_exception") = true,
		     camera_init2)
#endif
		.def("get_format", &Camera::get_format, get_format_docs)
		.def("get_frame", &Camera::get_frame, py::arg("timeout") = 0,
		     py::arg("buffered") = false, get_frame_docs)
		.def("get_framerate", &Camera::get_framerate,
		     get_framerate_docs)
		.def("get_framerates",
		     py::overload_cast<>(&Camera::get_framerates),
		     get_framerates_docs0)
		.def("get_framerates",
		     py::overload_cast<uint32_t, uint32_t>(
			     &Camera::get_framerates),
		     py::arg("width"), py::arg("height"), get_framerates_docs1)
		.def("get_framerates",
		     py::overload_cast<uint32_t, uint32_t, std::string &, bool>(
			     &Camera::get_framerates),
		     py::arg("width"), py::arg("height"),
		     py::arg("pixelformat"), py::arg("big_endian") = false,
		     get_framerates_docs2)
		.def("get_resolution", &Camera::get_resolution,
		     get_resolution_docs)
		.def("set_format",
		     py::overload_cast<Format &>(&Camera::set_format),
		     py::arg("format"), set_format_docs0)
		.def("set_format",
		     py::overload_cast<std::string &, bool>(
			     &Camera::set_format),
		     py::arg("format"), py::arg("big_endian") = false,
		     set_format_docs1)
		.def("set_framerate", &Camera::set_framerate,
		     py::arg("framerate"), set_framerate_docs)
		.def("set_resolution", &Camera::set_resolution,
		     py::arg("width"), py::arg("height"), set_resolution_docs);

	/*
	 * EVENTS
	 */
	py::class_<EventDevice>(m, "EventDevice", event_device_docs)
#ifdef QTEC_HEADER
		.def(py::init())
#endif
		.def(py::init<std::string &>())
		.def(py::init<uint32_t>())
		.def("set_callback", &EventDevice::set_callback,
		     set_callback_docs)
		// These function deal with a threaded callback to Python and
		// therefore need to manage the GIL when stopping and starting
		// the thread.
		.def("start", &EventDevice::start,
		     py::call_guard<py::gil_scoped_release>(),
		     start_events_docs)
		.def("stop", &EventDevice::stop,
		     py::call_guard<py::gil_scoped_release>(), stop_events_docs)
		.def("subscribe", &EventDevice::subscribe, py::arg("type"),
		     py::arg("id") = 0, subscribe_docs)
		.def("unsubscribe", &EventDevice::unsubscribe, py::arg("type"),
		     py::arg("id") = 0, unsubscribe_docs);

	py::enum_<EventType>(m, "EventType")
		.value("ALL", EventType::ALL)
		.value("VSYNC", EventType::VSYNC)
		.value("EOS", EventType::EOS)
		.value("CTRL", EventType::CTRL)
		.value("FRAME_SYNC", EventType::FRAME_SYNC)
		.value("SOURCE_CHANGE", EventType::SOURCE_CHANGE)
		.value("MOTION_DET", EventType::MOTION_DET);

	py::class_<BaseEvent>(m, "BaseEvent", "Base class for Event types")
		.def_readonly("type", &BaseEvent::type, "Type of the event")
		.def_readonly("pending", &BaseEvent::id,
			      "Number of pending events")
		.def_readonly("sequence", &BaseEvent::sequence,
			      "Event sequence number")
		.def_readonly("timestamp", &BaseEvent::timestamp,
			      "Event timestamp")
		.def_readonly(
			"id", &BaseEvent::id,
			"Control ID associated with the event source. If the event does not have an associated ID, this value is 0.");
	;

	py::class_<ControlChangesFlags>(
		m, "ControlChangesFlags",
		"Class that represents the flags for a control event.\nFor more"
		" information see `here "
		"<https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-dqevent.html#ctrl-changes-flags>`__.")
		.def_property_readonly("value", &ControlChangesFlags::value)
		.def_property_readonly("flags", &ControlChangesFlags::ch_flags)
		.def_property_readonly("range", &ControlChangesFlags::range)
		.def("__repr__", &ControlChangesFlags::to_string)
		.def("__str__", &ControlChangesFlags::to_string);

	py::class_<ControlEvent, BaseEvent>(
		m, "ControlEvent", "Class that represents a control event")
		.def_readonly(
			"changes", &ControlEvent::changes,
			"Flags that show what has changed for the control")
		.def_readonly("value", &ControlEvent::value,
			      "Potentially new value of the control")
		.def_readonly("control_type", &ControlEvent::control_type,
			      "Type of the control")
		.def_readonly("flags", &ControlEvent::flags,
			      "Potentially new flags of the control")
		.def_readonly("min", &ControlEvent::min,
			      "Potentially new minimum of the control")
		.def_readonly("max", &ControlEvent::max,
			      "Potentially new maximum of the control")
		.def_readonly("step", &ControlEvent::step,
			      "Potentially new step of the control")
		.def_readonly("default_value", &ControlEvent::default_value,
			      "Potentially new default_value of the control")
		.def("__repr__", &ControlEvent::to_string)
		.def("__str__", &ControlEvent::to_string);

	py::class_<SourceChangesFlags>(
		m, "SourceChangesFlags",
		"Class that represents the flags for a source change event.\n"
		"For more information see `here "
		"<https://www.kernel.org/doc/html/latest/userspace-api/media/v4l/vidioc-dqevent.html#ctrl-changes-flags>`__.")
		.def_property_readonly("resolution",
				       &SourceChangesFlags::resolution)
		.def("__repr__", &SourceChangesFlags::to_string)
		.def("__str__", &SourceChangesFlags::to_string);

	py::class_<SourceEvent, BaseEvent>(
		m, "SourceEvent", "Class that represents a source event")
		.def_readonly("changes", &SourceEvent::changes,
			      "Flags that show what has changed for the source")
		.def("__repr__", &SourceEvent::to_string)
		.def("__str__", &SourceEvent::to_string);
	/*
	 * EXCEPTIONS
	 */
	// Translation of V4l2Exception to Python exception of same name
	static py::exception<V4L2Exception> ex(m, "V4L2Exception");
	py::register_exception_translator([](std::exception_ptr p) {
		try {
			if (p) {
				rethrow_exception(p);
			}
		} catch (const V4L2Exception &e) {
			ex(e.what());
		}
	});

	py::register_exception<TimeoutException>(m, "TimeoutException");
	py::register_exception<DroppedFrameException>(m,
						      "DroppedFrameException");
}
