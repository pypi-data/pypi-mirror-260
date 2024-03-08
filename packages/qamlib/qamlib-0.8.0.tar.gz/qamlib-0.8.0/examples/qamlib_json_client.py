import importlib.util

# adjust to match path of v4l2_jsonrpc_connection.py
spec = importlib.util.spec_from_file_location(
    "v4l2_jsonrpc_connection", "/home/msb/QtecGit/python-jsonrpc-tools/RpcConnection.py"
)
rpc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rpc)

conn = rpc.RpcConnection("http://10.10.150.225:5000")

conn.run_func("test", {"val": 2})

# conn.run_func("list_controls", {"device":"/dev/qtec/video0"})

conn.run_func("list_controls")

conn.run_func("set_control", {"name": "exposure time, absolute", "value": 5000})
conn.run_func("get_control", {"name": "exposure time, absolute"})

conn.run_func("get_fps")
conn.run_func("set_fps", {"value": 20})

conn.run_func("get_resolution")
conn.run_func("set_resolution", {"width": 200, "height": 149})
conn.run_func("set_resolution", {"width": 200, "height": 150, "center": False})

conn.run_func("get_selection")
conn.run_func("set_selection", {"left": 0, "top": 0, "width": 200, "height": 149})
conn.run_func("set_selection", {"top": 100, "width": 200, "height": 100})

print(conn.run_func("get_selection_bounds"))
print(conn.run_func("get_selection_default"))

conn.run_func("set_max_image_size")
conn.run_func("set_sensor_image_size")

conn.run_func("list_formats")

conn.run_func("get_format")
conn.run_func("set_format", {"pixelformat": "RGB3"})
# conn.run_func("set_format", {"pixelformat":"BLA"})
# conn.run_func("set_format", {"pixelformat": "Y16", "big_endian": True})

conn.run_func("get_raw_frame")
