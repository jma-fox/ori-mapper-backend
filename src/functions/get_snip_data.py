from tdt import read_block
import pandas as pd


def get_snip_data(tdt_data):
    channels = tdt_data['snips']['eSpa']['chan'][0]
    times = tdt_data['snips']['eSpa']['ts'][0]
    snip_data = pd.DataFrame({"channels": channels, "times": times})

    return snip_data
