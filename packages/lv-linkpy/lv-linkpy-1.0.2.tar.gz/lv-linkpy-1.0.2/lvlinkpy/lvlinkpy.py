import json
import os
import time
from datetime import datetime
import numpy as np
import inspect
import socket

# i1, i2, i4, i8 int
# u1, u2, u4, u8 unsigned int
# f4, f8         float
# ?              bool
# U              string
# C              cluster(array not supported)
LVTypeMap = {
    "I8": "i1",
    "I16": "i2",
    "I32": "i4",
    "I64": "i8",
    "U8": "u1",
    "U16": "u2",
    "U32": "u4",
    "U64": "u8",
    "Single Float": "f4",
    "Double Float": "f8",
    "Extended Float": "f8",
    "Enum U8" : "u1",
    "Enum U16": "u2",
    "Enum U32": "u4",
    "Enum U64": "u8",
    "Boolean": "?",
    "String": "U",
    "Cluster": "C",
    "Variant": "C",
    "Fixed Point": "f8",
}



class Buffer:

    def __init__(self, sock):
        self.sock = sock
        self.buffer = b''

    def read_all(self) -> str:
        while b'\0' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                # print("None")
                return None
            self.buffer += data
            # print("buffer", self.buffer)
            break
        line, sep, self.buffer = self.buffer.partition(b'\0')
        return line.decode()






class Session:

    def __init__(self, port: int):
        # if os.environ.get("Pykit") is None:
        #     raise ValueError("can not find session key: %s in sessions" % session_key)
        #
        # try:
        #     sessions = json.loads(os.environ.get("Pykit"))
        #     if session_key in sessions:
        #         pass
        #     else:
        #         raise ValueError("")
        # except Exception as error:
        #     print("An exception occurred:", type(error).__name__, "–", error)

        self.port = port
        # cache: name, type, dim
        self._control_ref_dict = {}
        self._control_ref_name_list = []
        self._data_end_char = b"\r\n"
        self._buffer = Buffer(None)

        delay = self.check_response() * 1000
        print("LVLinkpy session constructed. Estimated latency is %.2f ms" % delay)
        self.update_session()

    def print_control_info(self):
        print("===================================")
        for it in self._control_ref_dict.keys():
            print(it + ":" + json.dumps(self._control_ref_dict[it]))
        print("===================================")

    def update_session(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", self.port))
            s.send(b"conf" + self._data_end_char)
            self._buffer.sock = s
            msg = self._buffer.read_all()
            if msg is None:
                raise RuntimeError("data is not received from server.")

            var_list = json.loads(msg)
            d = {}
            for it in var_list:
                if it[""] in LVTypeMap:
                    d[it["name"]] = {"_dim": it['number of dimensions'], "_type": LVTypeMap[it[""]]}
                else:
                    Warning("%s is not a supported value (%s)." % (it["name"], it[""]))
            self._control_ref_dict = d
            self._control_ref_name_list = list(d.keys())
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)


    def set_value(self, valueName, value, mechaction=False, ignore_check=False):
        item_data = {
            'Name': valueName,
            'mechanic': mechaction,  # not work to global variables
            '_type': "?",
            '_value': "",
            '_dim': ""
        }
        item_data = self._build_item_data(item_data, value)


        try:
            if not ignore_check:
                self._check_item_data_type(item_data)
            data_to_send = json.dumps(item_data)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", self.port))
            s.send(b"set=" + data_to_send.encode() + self._data_end_char)
            self._buffer.sock = s
            msg = self._buffer.read_all()
            if msg != "OK":
                raise RuntimeError("detect communication error from server.")

        except Exception as e:
            print("An exception occurred:", type(e).__name__, "–", e)


    def get_value(self, valueName):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", self.port))
            s.send(b"get=" + valueName.encode() + self._data_end_char)
            self._buffer.sock = s
            msg = self._buffer.read_all()
            if msg is None:
                raise RuntimeError("data is not received from server.")

            if msg == "":
                raise KeyError("ValueName: %s is not a valid variable on server site." % valueName)
            d = json.loads(msg)
            return d

        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)


    def _build_item_data(self, item_data: dict, obj):
        if isinstance(obj, str):
            return self._build_item_data(item_data, np.array(obj))
        elif isinstance(obj, list):
            return self._build_item_data(item_data, np.array(obj))
        elif isinstance(obj, int):
            return self._build_item_data(item_data, np.array(obj))
        elif isinstance(obj, float):
            return self._build_item_data(item_data, np.array(obj))
        elif isinstance(obj, dict):
            item_data["_dim"] = 0
            item_data["_value"] = json.dumps(obj)
            item_data["_type"] = "C"
        elif inspect.isclass(type(obj)) and hasattr(obj, "__dict__"):
            item_data["_dim"] = 0
            item_data["_value"] = json.dumps(obj.__dict__)
            item_data["_type"] = "C"
        elif isinstance(obj, np.ndarray):
            item_data["_dim"] = len(obj.shape)
            item_data["_value"] = json.dumps(obj.tolist())

            if obj.dtype.kind == "b":
                item_data["_type"] = "?"
            elif obj.dtype.kind in ["i", "u", "f"]:
                item_data["_type"] = obj.dtype.kind + str(obj.dtype.alignment)
            elif obj.dtype.kind == "U":
                item_data["_type"] = obj.dtype.kind
            else:
                raise ValueError("Unsupport type.")
        else:
            raise ValueError("Unsupport type.")
        return item_data


    def _check_item_data_type(self, item_data: dict):
        if item_data['Name'] not in self._control_ref_name_list:
            raise ValueError("can not find control name %s in session. "
                             "please check the name or try to call update session function" % item_data['Name'])

        if item_data['_dim'] != self._control_ref_dict[item_data['Name']]["_dim"]:
            raise ValueError("the dimension of the data(%s, dim: %d) does not fit to the origin data(dim: %d). "
                             "please check the data type or try to call update session function"
                             % (item_data['Name'], item_data['_dim'], self._control_ref_dict[item_data['Name']]["_dim"]))

        if item_data['_type'] != self._control_ref_dict[item_data['Name']]["_type"]:
            raise ValueError("the data type of the data(%s, type: %s) does not fit to the origin data(type: %s). "
                             "please check the data type or try to call update session function"
                             % (item_data['Name'], item_data['_type'], self._control_ref_dict[item_data['Name']]["_type"]))


    def check_response(self) -> float:
        t = float(''.join(s for s in str(datetime.now().time()).split(':')))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", self.port))
            s.send(b"ping" + self._data_end_char)
            self._buffer.sock = s
            msg = self._buffer.read_all()
            if msg is None:
                raise RuntimeError("data is not received from server.")
            return max(float(msg) - t, 0)
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "–", error)




