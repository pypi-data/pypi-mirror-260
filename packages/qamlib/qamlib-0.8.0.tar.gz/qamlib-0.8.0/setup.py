import os

from pybind11.setup_helpers import build_ext
from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup

__version__ = "0.8.0"

# We will try to keep warning free
compile_args = ["-Werror", "-std=c++20"]

macros = [
    ("VERSION_INFO", __version__),
    ("PYTHON", None),  # Enable Python for camera.cpp
]

if os.environ.get("DEBUG"):
    # Enable debug print for C++ parts
    macros.append(("DEBUG", None))


ext_modules = [
    Pybind11Extension(
        "qamlib",
        sources=[
            "src/camera.cpp",
            "src/control.cpp",
            "src/device.cpp",
            "src/event_device.cpp",
            "src/events.cpp",
            "src/format.cpp",
            "src/framerate.cpp",
            "src/pymod.cpp",
            "src/streaming_device.cpp",
            "src/utils.cpp",
        ],
        include_dirs=["includes"],
        define_macros=[
            ("VERSION_INFO", __version__),
            ("PYTHON", None),  # Enable Python for camera.cpp
        ],
        extra_compile_args=compile_args,
    ),
]

setup_kwargs = {
    "name": "qamlib",
    "version": __version__,
    "description": "A project for controlling v4l2 calls from python through a high level wrapper class",
    "author": "Daniel Lundberg Pedersen",
    "author_email": "dlp@qtec.com",
    "python_requires": ">=3.8,<4.0",
    "ext_modules": ext_modules,
    "cmdclass": {"build_ext": build_ext},
    "zip_safe": False,
}
setup(**setup_kwargs)
