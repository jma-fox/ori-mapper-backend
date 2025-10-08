

def get_loc_data(task_data, snip_data):
    channels = [int(chan) for chan in sorted(snip_data['channels'].unique())]
    loc_data = [{'channel': c, 'task_data': task_data, 'snip_data': snip_data} for c in channels]

    return loc_data