if build_python
  py.extension_module(
    'qamlib',
    [
      'camera.cpp',
      'device.cpp',
      'control.cpp',
      'event_device.cpp',
      'events.cpp',
      'format.cpp',
      'framerate.cpp',
      'streaming_device.cpp',
      'utils.cpp',
      'pymod.cpp',
    ],
    install : true,
    include_directories : includes,
    dependencies : [
      nlohmann_json_dep,
      py3_dep,
      pybind11_dep,
      pybind11_json_dep,
    ],
    cpp_args: [
      # Define PYTHON so the Python part of the library is built
      '-DPYTHON',
      '-DVERSION_INFO=' + meson.project_version(),
      # pybind11_json has some redundant moves so we the warnings here.
      '-Wno-redundant-move',
    ],
  )
else
  static_library(
    'qamlib',
    [
      'camera.cpp',
      'device.cpp',
      'control.cpp',
      'event_device.cpp',
      'events.cpp',
      'format.cpp',
      'framerate.cpp',
      'streaming_device.cpp',
      'utils.cpp',
    ],
    install : true,
    name_prefix : '',
    include_directories : includes,
    dependencies : [
      cv_dep,
      nlohmann_json_dep,
    ],
  )
endif
