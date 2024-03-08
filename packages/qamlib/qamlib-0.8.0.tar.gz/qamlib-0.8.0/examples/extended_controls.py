import qamlib
import numpy as np

cam = qamlib.Camera() # /dev/qtec/video0

ctrls = cam.list_controls()

ctrl_lut = ctrls["lut red"]

assert ctrl_lut.type == qamlib.ControlType.INTEGER

# If the control is INTEGER and has a payload it is an ArrayControl
assert ctrl_lut.flags.has_payload

arr = np.ones([ctrl_lut.elements], dtype=np.int32)

arr[500:] = 12 ** 2

lut_red = qamlib.ArrayControlValue(arr)

lut_green = cam.get_ext_control("lut green")

exposure = qamlib.IntegerControlValue(9992)

new_values = {
    "lut red": lut_red,
    "lut blue": lut_green,
    "exposure time absolute": exposure,
}

cam.set_controls(new_values)

print(cam.get_controls(["lut red", "lut blue", "exposure time absolute"]))
