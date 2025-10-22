

def get_ori_data(task_data, snip_data, event_name):
    channels = [int(chan) for chan in sorted(snip_data['channels'].unique())]
    ori_data = [{'channel': c, 'task_data': task_data, 'snip_data': snip_data, 'event_name': event_name} for c in channels]

    return ori_data
