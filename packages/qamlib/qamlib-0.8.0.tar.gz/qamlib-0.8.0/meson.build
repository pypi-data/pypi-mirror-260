project(
  'qamlib',
  'cpp',
  default_options : [
    'warning_level=3',
    'buildtype=debugoptimized',
    'cpp_std=c++20',
  ],
  version : '0.8.0'
)

# Option to build the Python module or the C++ library
build_python = get_option('python')

add_project_arguments(
  [
    '-pedantic',
    '-Wcast-align',
    '-Wcast-qual',
    '-Wctor-dtor-privacy',
    '-Wdisabled-optimization',
    '-Wformat=2',
    '-Winit-self',
    '-Wlogical-op',
    '-Wmissing-declarations',
    '-Wmissing-include-dirs',
    '-Wno-missing-field-initializers',
    '-Wno-unused',
    '-Wnoexcept',
    '-Wold-style-cast',
    '-Woverloaded-virtual',
    '-Wredundant-decls',
    '-Wsign-conversion',
    '-Wsign-promo',
    '-Wstrict-null-sentinel',
    '-Wstrict-overflow=5',
    '-Wswitch-default',
    '-std=c++20',
  ],
  language : 'cpp',
)

# Dependencies
nlohmann_json_dep = dependency(
  'nlohmann_json',
  fallback: ['nlohmann_json', 'nlohmann_json_dep'],
  required: true
)

if build_python
  py = import('python').find_installation()
  py3_dep = py.dependency()

  pybind11_dep = dependency('pybind11', required : true)

  pybind11_json_dep = dependency(
    'pybind11_json',
    fallback: ['pybind11_json', 'pybind11_json_dep'],
    required: true,
  )
else
  cv_dep = dependency('opencv4', required : true, include_type : 'system')
endif


includes = include_directories('includes')

subdir('includes')
subdir('src')
