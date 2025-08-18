import h5py
import numpy as np


def get_tdt_data(tdt_data_file):
    def unpack_struct(struct):
        data_dict = {}
        for k, v in struct.items():
            if isinstance(v, h5py.Dataset):
                data_dict[k] = np.array(v)
            elif isinstance(v, h5py.Group):
                data_dict[k] = unpack_struct(v)
        return data_dict

    with h5py.File(tdt_data_file, 'r') as f:
        tdt_data = unpack_struct(f)

    return tdt_data
    