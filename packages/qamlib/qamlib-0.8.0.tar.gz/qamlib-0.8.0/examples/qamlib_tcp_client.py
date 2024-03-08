import socket
import time

BUFFER_SIZE = 1024

FRAME_WIDTH = 1024
FRAME_HEIGHT = 1024
N_CHANNELS = 3  # RGB
N_BYTES = 1
# N_CHANNELS = 1 #GRAY
# N_BYTES = 2 #GRAY16_LE
FRAME_SIZE = FRAME_WIDTH * FRAME_HEIGHT * N_BYTES * N_CHANNELS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("connecting")
try:
    s.connect(
        ("10.10.150.225", 12345)
    )  # here you must past the public external ipaddress of the server machine, not that local address
except ConnectionRefusedError:
    print("Could not connect to camera")
print("connected")

MJPEG = True
PRINT_FPS = True
MAX_NR_IMGS = 20

old_time = time.time()
n_frames = 0

n_imgs = 0
while True:
    data = bytearray()
    if MJPEG:
        bytes = b""
        while True:
            bytes += s.recv(1024)
            # look for JPEG header and footer
            a = bytes.find(b"\xff\xd8")
            b = bytes.find(b"\xff\xd9")
            if a != -1 and b != -1:
                jpg = bytes[a : b + 2]
                bytes = bytes[b + 2 :]
                # print metadata, if any
                print(bytes)
                break
    else:
        while len(data) < FRAME_SIZE:
            try:
                msg = s.recv(FRAME_SIZE - len(data))
                data.extend(msg)

            except:
                pass

    n_imgs = n_imgs + 1
    # print("Got frame: " + str(n_imgs))

    # print(len(jpg))

    # with open("/tmp/test.jpeg", "wb") as f:
    #    f.write(jpg)

    if PRINT_FPS:
        # time_stamp = time.time()
        # print("FPS: " + str(1/(time_stamp - old_time)))
        # old_time = time_stamp

        n_frames = n_frames + 1
        if n_frames % 5 == 0:
            time_now = time.time()
            print("FPS: " + str(n_frames / (time_now - old_time)))
            old_time = time_now
            n_frames = 0

    if MAX_NR_IMGS:
        if n_imgs >= MAX_NR_IMGS:
            break

print(f"Done receiving: {n_imgs} imgs")

s.close()
print("done")
