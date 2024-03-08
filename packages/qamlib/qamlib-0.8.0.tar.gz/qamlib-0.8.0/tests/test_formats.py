import qamlib

cam = qamlib.Camera("/dev/qtec/video0")

fmts = cam.list_formats()

for fmt in fmts:
    f = fmts[fmt]

    name = f.pixelformat.fourcc
    if f.pixelformat.big_endian:
        name += "_BE"

    tmp = cam.set_format(name)

    assert tmp.pixelformat.get_code() == f.pixelformat.get_code()

    with cam:
        _, frame = cam.get_frame()

        assert frame is not None
        print(frame.shape)
