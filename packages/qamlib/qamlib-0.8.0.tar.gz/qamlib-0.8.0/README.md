# qamlib

This is a library meant to be an easy way to interact with a V4L2 camera, by
having a simple interface to capture images, and change camera controls. It is
a C++20 class (+ a few structs) together with Python bindings via `pybind11`.

While the Python bindings are the main usage of `qamlib`, it is also possible to
build `qamlib` as a (static) C++ library.

### Supported features

- Get/set "normal" and extended V4L2 controls.
- Get/set image formats.
- Get/set framesize and cropping.
- Get/set framerate (FPS).
- Read out frames from a capture video device as a NumPy array. With or without
  buffering.
- Subscribe to events for a V4L2 device.

### Planned features

- Pushing frames to a output video device.
- Supporting multiplane devices.

There are also some features supported that are currently exclusive to
Qtechnology A/S cameras, but these are not compiled when main-line kernel
headers are detected.

## Example

```python
import qamlib

cam = qamlib.Camera("/dev/video0")

# Use context manager to start and stop streaming
with cam:
    metadata, frame = cam.get_frame() # gets an image as raw bytes
    # process image
```

See more in the
[documentation](https://qtec.gitlab.io/public/qamlib/index.html)

## Building

### Python

Building the Python module is done via `mesonpy`.

Dependencies

- `gcc`
- `libstdc++-dev`
- `meson`
- `mesonpy`
- `nlohmann-json`
- `pybind11`
- `pybind11_json`
- `python3-build`
- `python3-dev`

To build the module:

```sh
python -m build
```

### C++

Dependicies

- `gcc`
- `meson`
- `ninja`
- `nlohmann-json`

To build the library we start by running `meson` setup:

```sh
meson setup build -Dpython=false
```

Then to compile do

```sh
meson compile -C build
```

To install the package.

```sh
meson install
```

## Testing

Under `tests/` are some tests, these have only been actually tested on
Qtechnology A/S cameras.
