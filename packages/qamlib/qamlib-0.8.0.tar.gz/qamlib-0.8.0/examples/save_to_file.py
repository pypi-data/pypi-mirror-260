import qamlib

cam = qamlib.Camera("/dev/video0")
for _ in range(10):
    (
        seq,
        A,
    ) = (
        cam.getImage()
    )  # returns a tupple with a frame sequence number(int) and a numpy array(the image)

    with open(f"img/img{seq}.jpeg", "wb") as f:
        A.tofile(f)
