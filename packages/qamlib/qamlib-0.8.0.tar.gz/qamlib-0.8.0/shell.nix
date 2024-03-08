with (import <nixpkgs> {});
mkShell {
    buildInputs = [
        cmake # Need this for meson to find pybind11
        meson
        ninja
        nlohmann_json
        opencv
        pkg-config
        python3Packages.build
        python3Packages.numpy
        python3Packages.pybind11
        python3Packages.setuptools
        virtualenv
    ];
}
