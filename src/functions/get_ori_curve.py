import numpy as np


def get_ori_curve(channel_data):
    channel = channel_data['channel']
    task_data = channel_data['task_data']
    snip_data = channel_data['snip_data']
    channel_snips = snip_data[snip_data['channels'] == channel]

    t_window=(0.0, 0.2)

    ori_spike_counts = {}
    for _, trial_row in task_data.iterrows():
        onset_time = trial_row['GaborOnsetTm']
        ori_val = trial_row['TargOri']
        ori_key = (180 - abs(ori_val)) if ori_val < 0 else ori_val

        if ori_key not in ori_spike_counts:
            ori_spike_counts[ori_key] = []

        spikes_in_window = channel_snips[
            (channel_snips['times'] >= onset_time + t_window[0]) &
            (channel_snips['times'] <= onset_time + t_window[1])
        ]

        ori_spike_counts[ori_key].append(len(spikes_in_window))

    x_vals, y_vals = [], []
    for ori, counts in ori_spike_counts.items():
        x_vals.append(ori)
        y_vals.append(np.mean(counts))

    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)

    sort_idx = np.argsort(x_vals)
    x_vals = x_vals[sort_idx]
    y_vals = y_vals[sort_idx]

    channel_result = {'channel': channel, 'x_vals': x_vals, 'y_vals': y_vals}

    return channel_result
