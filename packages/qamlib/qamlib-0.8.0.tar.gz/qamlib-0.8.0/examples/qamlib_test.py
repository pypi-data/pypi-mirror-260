import qamlib
import sys


def needs_byteswap(frame):
    # 8-bit
    if frame.itemsize == 1:
        return False
    # Big Endian
    if frame.dtype.byteorder == ">":
        return False
    # Big Endian native byte order
    if frame.dtype.byteorder == "=" and sys.byteorder == "big":
        return False
    return True


def write_ppm(name, frame):
    with open(name, "wb") as f:
        height, width, channels = frame.shape

        if channels == 1:
            type = "P5"
        else:
            type = "P6"

        if frame.nbytes == width * height * channels:
            if frame.dtype == "uint8":
                max_val = 255
            else:
                max_val = 65535
        else:
            max_val = 65535

        ppm_header = f"{type} {width} {height} {max_val}\n"
        f.write(bytearray(ppm_header, "ascii"))

        if needs_byteswap(frame):
            # swap data in memory in order to properly write PNM
            # since PPM is Big Endian by definition
            # Note that if the operation is done in place
            # it will mess up the endianess when reading single values out
            # so in this case use: frame = frame.byteswap(True).newbyteorder()
            # in order to keep the correct byte order
            frame.byteswap().tofile(f)
        else:
            frame.tofile(f)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        device = sys.argv[1]
    else:
        device = "/dev/qtec/video0"

    # Open video capture device
    try:
        cam = qamlib.Camera(device)
    except Exception as e:
        print(e)
        exit(-1)

    print("List of formats:")
    fmts = cam.list_formats()
    for name in fmts:
        print(fmts[name])
    print("\n")

    # V4l2 "Settings"
    fps = 20.0
    width = 800
    height = 600

    cam.set_format("Y16_BE")
    # cam.set_format("Y16")
    # cam.set_format("GREY")
    cam.set_framerate(fps)
    cam.set_resolution(width, height)

    # crop to center
    bounds = cam.get_crop_bounds()
    def_rect = cam.get_crop_default()
    left = int(((bounds.width - bounds.left) - width) / 2) + bounds.left
    top = int(((bounds.height - bounds.top) - height) / 2) + bounds.top
    cam.set_crop(left, top, width, height)

    img_format = cam.get_format()
    px_format = img_format.pixelformat

    print(f"FPS: {cam.get_framerate()}")
    print(f"Frame Size: {cam.get_resolution()}")
    print(f"Crop: {cam.get_crop()}")
    print(f"Pixel format: {img_format}")
    print("\n")

    # V4l2 Controls
    ctrls = cam.list_controls()
    print("Found ", len(ctrls), " controls")
    for name in ctrls:
        print(ctrls[name])
    print("\n")

    cam.set_control("Exposure Time Absolute", 5000)
    print(f"Exposure: {cam.get_control('Exposure Time Absolute')}")

    # Frame capture
    print("Starting Streaming")
    with cam:
        for i in range(10):
            metadata, frame = cam.get_frame()

            print(metadata)
            print(frame.size, " ", frame.shape)

            write_ppm(f"/tmp/img{i}.pnm", frame)
    print("Done Streaming")
