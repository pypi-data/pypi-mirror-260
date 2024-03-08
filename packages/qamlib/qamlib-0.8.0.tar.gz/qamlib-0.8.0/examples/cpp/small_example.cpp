// Compile with:
// g++ small_example.cpp -isystem/usr/include/opencv4 -l:qamlib.a -lopencv_core

#include <qamlib.h>
#include <iostream>

using namespace std;

int main() {
        auto cam = qamlib::Camera();

        cout << "Exposure time: " << cam.get_control("exposure time, absolute") << endl;

        cam.set_control("trigger mode", 0);

        cout << "Starting streaming (10 frames)" << endl;
        cam.start();

        for (int i = 0; i < 10; i++) {
                auto [meta, frame] = cam.get_frame();
                auto size = frame.size();
                cout << "Frame shape: " << size.width << "x" << size.height << endl;
        }

        cam.stop();

        return 0;
}
