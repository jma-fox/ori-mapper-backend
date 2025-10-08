import numpy as np
from datetime import timedelta


def _decode_matlab_u16(arr):
    a = np.array(arr, dtype=np.uint16).reshape(-1)

    return a.tobytes().decode('utf-16le')

def get_start_time(tdt_data):
    start_time = tdt_data['info']['starttime']
    start_time = _decode_matlab_u16(start_time)
    h, m, s = start_time.split(':')
    delta = timedelta(hours=int(h), minutes=int(m), seconds=float(s))
    start_time = delta.total_seconds()

    return start_time
