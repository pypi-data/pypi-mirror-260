import qamlib

# pip3 install flask
# pip3 install json-rpc

# for Flask and JSON
from flask import Flask
from jsonrpc.backend.flask import Dispatcher
from jsonrpc.backend.flask import JSONRPCAPI

# tcp socket for sending raw imgs
import socket

import threading
import signal
import time

# JPEG encoding
import cv2

running = True
streaming = False
clients = []
streaming_thread = None

d = Dispatcher()
app = Flask(__name__)

# curl to test commands, no reply
# curl -v --data-binary '{"jsonrpc": "2.0", "params": {"name": "test"}, "method": "get_control"}' -H 'content-type:application/json;' http://10.10.150.225:5000


def create_streaming_thread():
    return threading.Thread(target=start_streaming)


def socket_thread():
    global running
    global clients
    global streaming_thread

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1)

        s.bind(
            ("", 12345)
        )  # if the clients/server are on different network you shall bind to ('', port)
        s.listen(10)

        while running:
            # time.sleep(1.0)
            try:
                c, addr = s.accept()
                print("{} connected.".format(addr))
                clients.append(c)
                print(f"Number of clients: {len(clients)}")
                if not streaming_thread.is_alive():
                    streaming_thread = create_streaming_thread()
                    streaming_thread.start()
            except socket.timeout:
                continue
    except Exception as e:
        print(f"Exception caught in socket thread: {e}")
        running = False
        # sys.exit(0)


def ctrl_flags_to_dict(flags):
    d = dict()
    if flags.raw_flags:
        d["raw_flags"] = flags.raw_flags
    else:
        return None
    if flags.disabled:
        d["disabled"] = flags.disabled
    if flags.grabbed:
        d["grabbed"] = flags.grabbed
    if flags.read_only:
        d["read_only"] = flags.read_only
    if flags.update:
        d["update"] = flags.update
    if flags.inactive:
        d["inactive"] = flags.inactive
    if flags.slider:
        d["slider"] = flags.slider
    if flags.write_only:
        d["write_only"] = flags.write_only
    if flags.is_volatile:
        d["is_volatile"] = flags.is_volatile
    if flags.has_payload:
        d["has_payload"] = flags.has_payload
    if flags.execute_on_write:
        d["execute_on_write"] = flags.execute_on_write
    if flags.modify_layout:
        d["modify_layout"] = flags.modify_layout
    return d


def ctrl_to_dict(ctrl):
    d = dict()
    d["id"] = ctrl.id
    d["name"] = ctrl.name
    d["type"] = ctrl.type.name
    d["min"] = ctrl.min
    d["max"] = ctrl.max
    d["step"] = ctrl.step
    d["default"] = ctrl.default_value
    if (
        ctrl.type == qamlib.ControlType.MENU
        or ctrl.type == qamlib.ControlType.INTEGER_MENU
    ):
        d["items"] = ctrl.items
    flags = ctrl_flags_to_dict(ctrl.flags)
    if flags:
        d["flags"] = flags
    return d


def fourcc_to_pixelformat(fourcc, be=False):
    if type(fourcc) != str or len(fourcc) != 4:
        return -1
    pixelformat = ord(fourcc[0])
    pixelformat += ord(fourcc[1]) << 8
    pixelformat += ord(fourcc[2]) << 16
    pixelformat += ord(fourcc[3]) << 24
    if be:
        pixelformat |= 1 << 31
    return pixelformat


def pixelformat_to_fourcc(pixelformat):
    text = ""
    text += chr(pixelformat & 0xFF)
    text += chr((pixelformat >> 8) & 0xFF)
    text += chr((pixelformat >> 16) & 0xFF)
    tmp = (pixelformat >> 24) & 0xFF

    # BE handling
    if tmp & 0xFF >= 0x80:
        tmp &= 0x7F
    text += chr(tmp)

    return text


def is_pixelformat_be(pixelformat):
    tmp = (pixelformat >> 24) & 0xFF
    if tmp & 0xFF >= 0x80:
        return True
    return False


def px_fmt_to_dict(pixelformat):
    d = dict()
    d["fourcc"] = pixelformat.fourcc
    d["code"] = pixelformat.get_code()
    if pixelformat.big_endian:
        d["BE"] = pixelformat.big_endian
    return d


def img_fmt_to_dict(fmt):
    d = dict()
    d["pixelformat"] = px_fmt_to_dict(fmt.pixelformat)
    d["description"] = fmt.description
    # d["flags"] = fmt.flags
    return d


def single_plane_fmt_to_dict(fmt):
    d = dict()
    d["width"] = fmt.width
    d["height"] = fmt.height
    d["pixelformat"] = px_fmt_to_dict(fmt.pixelformat)
    return d


@d.add_method
def test(val):
    print("Testing: " + str(val))

    return {"val": val}


@d.add_method
def list_controls(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        ctrls = cam.list_controls()
    except Exception as e:
        raise e

    # for key in ctrls:
    #    print(ctrls[key])
    #    print(dict(ctrls[key]))
    #    print(json.dumps(ctrls[key], default=vars))
    #    print(json.dumps(ctrls[key].__dict__))

    return {"controls": [ctrl_to_dict(ctrls[key]) for key in ctrls]}
    # return {"controls": [ctrls[key].name for key in ctrls]}
    # return {"controls": ctrls}


@d.add_method
def get_control(name, device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        value = cam.get_control(name)
    except Exception as e:
        raise e
    return {"value": value}


@d.add_method
def set_control(name, value, device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        cam.set_control(name, value)
        value = cam.get_control(name)
    except Exception as e:
        raise e
    return {"value": value}


@d.add_method
def list_formats(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        fmts = cam.list_formats()
    except Exception as e:
        raise e

    return {"formats": [img_fmt_to_dict(fmts[key]) for key in fmts]}
    return {"formats": [img_fmt_to_dict(fmt) for fmt in fmts]}
    # return {"formats": fmts}


@d.add_method
def get_format(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        fmt = cam.get_format()
    except Exception as e:
        raise e
    return {"format": single_plane_fmt_to_dict(fmt)}


@d.add_method
def set_format(pixelformat, big_endian=False, device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        cam.set_format(pixelformat, big_endian)
        fmt = cam.get_format()
    except Exception as e:
        raise e
    return {"format": single_plane_fmt_to_dict(fmt)}


@d.add_method
def get_fps(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        fps = cam.get_framerate()
    except Exception as e:
        raise e
    return {"fps": fps}


@d.add_method
def set_fps(value, device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        cam.set_framerate(value)
        fps = cam.get_framerate()
    except Exception as e:
        raise e
    return {"fps": fps}


@d.add_method
def get_resolution(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        width, height = cam.get_resolution()
    except Exception as e:
        raise e
    return {"width": width, "height": height}


def auto_center_crop(cam, width, height):
    try:
        bounds = cam.get_selection_bounds()
        # def_rect = cam.get_selection_default()
        left = int(((bounds.width - bounds.left) - width) / 2) + bounds.left
        top = int(((bounds.height - bounds.top) - height) / 2) + bounds.top
    except Exception as e:
        raise e

    return left, top


@d.add_method
def set_resolution(width, height, center=True, device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        if center:
            left, top = auto_center_crop(cam, width, height)
            cam.set_selection(left, top, width, height)
        else:
            cam.set_resolution(width, height)
        width, height = cam.get_resolution()
    except Exception as e:
        raise e
    return {"width": width, "height": height}


def selection_to_dict(rects):
    if type(rects) is list:
        rect_list = []
        for r in rects:
            d = dict()
            d["left"] = r.left
            d["top"] = r.top
            d["width"] = r.width
            d["height"] = r.height
            rect_list.append(d)
        return rect_list
    else:
        d = dict()
        d["left"] = rects.left
        d["top"] = rects.top
        d["width"] = rects.width
        d["height"] = rects.height
        return d


@d.add_method
def get_selection(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        selection = selection_to_dict(cam.get_selection())
    except Exception as e:
        raise e
    return {"selection": selection}


@d.add_method
def get_selection_default(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        selection = selection_to_dict(cam.get_selection_default())
    except Exception as e:
        raise e
    return {"selection": selection}


@d.add_method
def get_selection_bounds(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        selection = selection_to_dict(cam.get_selection_bounds())
    except Exception as e:
        raise e
    return {"selection": selection}


@d.add_method
def set_selection(width, height, left=None, top=None, device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        # auto center crop
        if left is None or top is None:
            center_left, center_top = auto_center_crop(cam, width, height)
            if left is None:
                left = center_left
            if top is None:
                top = center_top
        cam.set_selection(left, top, width, height)
        selection = selection_to_dict(cam.get_selection())
    except Exception as e:
        raise e
    return {"selection": selection}


@d.add_method
def set_max_image_size(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        cam.set_selection([cam.get_selection_default()])
        selection = selection_to_dict(cam.get_selection())
    except Exception as e:
        raise e
    return {"selection": selection}


@d.add_method
def set_max_sensor_size(device="/dev/qtec/video0"):
    try:
        cam = qamlib.Camera(device)
        cam.set_selection([cam.get_selection_bounds()])
        selection = selection_to_dict(cam.get_selection())
    except Exception as e:
        raise e
    return {"selection": selection}


from base64 import b64encode


@d.add_method
def get_raw_frame(device="/dev/qtec/video0"):
    # TODO: consider encoding data to base64
    try:
        cam = qamlib.Camera(device)
        with cam:
            metadata, frame = cam.get_frame()
            h, w, chs = frame.shape

            base64_bytes = b64encode(frame.data)
            base64_string = base64_bytes.decode("utf-8")
    except Exception as e:
        raise e
    # return {"size": {"width": w, "height": h, "channels": chs}, "timestamp":metadata.time, "frame_nr": metadata.sequence, "base64_data": base64_string}
    return {
        "size": {"width": w, "height": h, "channels": chs},
        "timestamp": metadata.time,
        "frame_nr": metadata.sequence,
        "data": frame.tolist(),
        "base64_data": base64_string,
    }
    # return {"size": {"width": w, "height": h, "channels": chs}, "timestamp":metadata.time, "frame_nr": metadata.sequence, "data": frame.tolist()}


def package_mjpeg(img_bytes, metadata=None):
    mjpeg = b"--frame\r\n" + b"Content-Type: image/jpeg\r\n\r\n"
    mjpeg += img_bytes

    if metadata:
        mjpeg += b"Timestamp:" + bytes(str(metadata.time), "utf-8")
        mjpeg += b"\r\n"
        mjpeg += b"Sequence:" + bytes(str(metadata.sequence), "utf-8")

    mjpeg += b"\r\n"

    return mjpeg


def handler_stop_signals(signum, frame):
    print("Received stop signal!")
    global running
    running = False
    raise KeyboardInterrupt


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


def main():
    global running
    global streaming_thread

    streaming_thread = create_streaming_thread()

    # start socket thread
    print("Starting socket thread")
    t = threading.Thread(target=socket_thread)
    t.start()

    # start server thread
    print("Starting JSON server thread")

    overwritten = list(d.keys())
    api = JSONRPCAPI(dispatcher=d)
    app.add_url_rule("/", "api", api.as_view(), methods=["POST"])
    app.run("0.0.0.0")

    while running:
        time.sleep(1.0)
    t.join()
    if streaming_thread.is_alive():
        streaming_thread.join()


def save_ppm(frame, path="/tmp/img.pnm"):
    with open(path, "wb") as f:
        height, width, channels = frame.shape
        if channels == 1:
            type = "P5"
        else:
            type = "P6"
        if frame.size == width * height * channels:
            max_val = 255
        else:
            max_val = 65535
        ppm_header = f"{type} {width} {height} {max_val}\n"
        f.write(bytearray(ppm_header, "ascii"))
        f.write(frame)


# raw
# vlc --demux rawvideo --rawvid-chroma RV24 --rawvid-fps 20 --rawvid-width 1024 --rawvid-height 1024 tcp://10.10.150.225:12345

# jpeg:
# vlc tcp://10.10.150.225:12345

MJPEG = True


def start_streaming(device="/dev/qtec/video0"):
    global running
    global streaming
    global clients
    if not streaming:
        streaming = True
        try:
            cam = qamlib.Camera(device)
            print("Starting Streaming")
            with cam:
                while running:
                    if len(clients) == 0:
                        break
                    metadata, frame = cam.get_frame()
                    print(metadata)
                    # print(frame.size, " ", frame.shape)
                    for c in clients:
                        try:
                            if MJPEG:
                                jpeg_frame = cv2.imencode(
                                    ".JPEG", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                )
                                # print(len(jpeg_frame[1].tobytes()))
                                mjpeg = package_mjpeg(jpeg_frame[1].tobytes(), metadata)
                                c.send(mjpeg)
                                # c.send(jpeg_frame[1].tobytes())
                            else:
                                c.send(frame)
                        except socket.error:
                            print("Client disconnected")
                            c.close()
                            clients.remove(c)
                            print(f"Number of clients: {len(clients)}")
            streaming = False
            print("Done Streaming")
        except Exception as e:
            print(e)
            streaming = False


if __name__ == "__main__":
    main()
