import qamlib
import numpy as np
import sys
import time

# This test assumes that /dev/qtec/video0 -> /dev/video1
# and that it is a Qtec camera with all the supported features

def main():
    cam = qamlib.Camera()

    ctrls = cam.list_controls()

    print("Checking certain controls are present")
    assert "exposure_time_absolute" in ctrls
    assert "vertical_flip" in ctrls

    # Set a low but reasonable framerate
    cam.set_framerate(10)

    test_formats(cam)

    test_16bit(cam)

    test_extended_controls(cam)

    test_frame_out(cam)


def test_formats(cam: qamlib.Camera):
    print("Testing formats")
    fmts = cam.list_formats()

    assert "RGB3" in fmts
    assert "BGR3" in fmts

    # Use full resolution
    cam.set_crop([cam.get_crop_default()])

    # Use external trigger.
    cam.set_control("Trigger Mode", 1)

    for f in fmts:
        # The extra spaces are to clear a potential longer previous format name
        sys.stdout.write(f"\rTrying format: {f}     ")
        sys.stdout.flush()
        cam.set_format(f)

        with cam:
            # Trigger the camera
            cam.set_control("Manual Trigger", 1)

            # Don't wait forever, timeout -> error
            meta, frame = cam.get_frame(timeout=1)

        assert meta.sequence == 0

        _, _, width, height = cam.get_crop_default()
        assert frame.shape[:2] == (height, width)

    print()
    # Set back to self timed
    cam.set_control("Trigger Mode", 0)

def test_16bit(cam: qamlib.Camera):
    print("Testing 16 bit")

    fmts = cam.list_formats()
    if "Y16" not in fmts:
        print("Can't find 16 bit format")
        return

    cam.set_format("Y16")

    with cam:
        _, frame = cam.get_frame(timeout=1)

        assert frame.dtype == np.uint16

def test_extended_controls(cam: qamlib.Camera):
    print("Testing extended controls")

    ctrls = cam.list_controls()

    if "trigger sequence" in ctrls:
        print("Testing trigger sequence")
        trig_seq = cam.get_ext_control("Trigger Sequence").value

        # External trigger sequence
        cam.set_control("Trigger Mode", 5)

        assert len(trig_seq) == 1

        trig = qamlib.TriggerSequenceValue()

        trig.add_exposure(50000, 50000, 200000, 0)
        trig.add_exposure(100000, 100000, 200000, 0)

        cam.set_ext_control("Trigger Sequence", trig)

        trig_seq = cam.get_ext_control("Trigger Sequence").value

        trig_val = trig.value
        assert len(trig_val) == len(trig_seq)

        for i in range(len(trig_seq)):
            lhs = trig_seq[i]
            rhs = trig_val[i]

            assert lhs.exposure_time == rhs.exposure_time
            assert lhs.flash_time == rhs.flash_time
            assert lhs.frame_delay == rhs.frame_delay
            assert lhs.trigger_delay == rhs.trigger_delay

        count = 0
        with cam:
            cam.set_control("Manual Trigger", 1)
            while True:
                # We should not get this many frames
                if count > 2:
                    assert False
                try:
                    # Buffered so we don't accidentaly skip frames
                    # Timeout so we get all frames untill none are available
                    cam.get_frame(timeout = 4, buffered=True)
                    count += 1
                except qamlib.TimeoutException:
                    # We expect a timeout to exit loop
                    break

        assert count == len(trig_val)
    else:
        print("Trigger sequence not availabile skipping")

    print("Testing string controls")
    assert isinstance(cam.get_ext_control("Sensor type").value, str)
    assert isinstance(cam.get_ext_control("Sensor serial").value, str)

    print("Testing Array controls")

    prev = cam.get_ext_control("LUT Red")

    npa = np.ones(prev.value.shape, dtype=np.int32)
    arrc = qamlib.ArrayControlValue(npa)
    cam.set_ext_control("LUT Red", arrc)

    cur = cam.get_ext_control("LUT Red").value
    assert np.sum(cur) == prev.value.shape[0]

    # Reset trigger mode
    cam.set_control("Trigger Mode", 0)

def test_frame_out(cam: qamlib.Camera):
    print("Testing frame sequence and timings")

    cam.set_control("Trigger mode", 0)
    cam.set_format("BGR3")
    cam.set_resolution(200, 200)
    cam.set_framerate(450)

    print(f"Testing if we can keep up with high framerate: {cam.get_framerate()}")

    with cam:
        for i in range(1000):
            meta, _ = cam.get_frame(timeout=2)
            assert i == meta.sequence

    cam.set_crop(cam.get_crop_default())

    # Extrenal trigger
    cam.set_control("Trigger Mode", 1)

    print("Checking sequence number for manual trigger and buffered")
    with cam:
        for i in range(20):
            cam.set_control("Manual trigger", 1)

            meta, _ = cam.get_frame(timeout=2, buffered=True)
            assert meta.sequence == i

        try:
            cam.get_frame(timeout=1)
            assert False
        except qamlib.TimeoutException:
            # There should not be any frames left ready
            # so we expect a timeout
            pass

    print("Testing DroppedFrameException")

    # Default is no more than 10 buffers, so using 11 to make sure we need to
    # drop one
    with cam:
        for _ in range(11):
            cam.set_control("Manual trigger", 1)
            time.sleep(.2)

        # Should just work
        cam.get_frame(timeout=1)

        for _ in range(11):
            cam.set_control("Manual trigger", 1)
            time.sleep(.2)

        # Wait a bit so we are sure all frames have been captured
        time.sleep(1)

        try:
            cam.get_frame(timeout=1, buffered=True)
            assert False
        except qamlib.DroppedFrameException:
            # We expect to have dropped a frame
            # Since we're only using 10 V4L2 buffers
            pass

    cam_no_exc = qamlib.Camera(overflow_exception=False)

    with cam_no_exc:
        for _ in range(11):
            cam.set_control("Manual trigger", 1)
            time.sleep(.2)

        cam_no_exc.get_frame(timeout=1, buffered=True)


if __name__ == "__main__":
    main()
