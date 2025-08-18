from tdt import read_block
import pandas as pd


def get_snip_data(tdt_data, start_time, stop_time):
    channels = tdt_data['snips']['eSpa']['chan'][0]
    times = tdt_data['snips']['eSpa']['ts'][0]
    snip_data = pd.DataFrame({"channels": channels, "times": times})
    snip_data = snip_data[(snip_data['times'] > start_time) & (snip_data['times'] < stop_time)]

    return snip_data
