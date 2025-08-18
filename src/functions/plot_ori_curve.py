import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def plot_ori_curve(chan, onset_data, snip_data, t_window=(0.05, 0.2)):
    chan_snips = snip_data[snip_data['channels'] == chan]
    ori_spike_counts = {}

    for _, trial_row in onset_data.iterrows():
        onset_time = trial_row['OnsetTm']
        ori_val = trial_row['TargOri']
        ori_key = ori_val #+ 180 if ori_val < 0 else ori_val

        if ori_key not in ori_spike_counts:
            ori_spike_counts[ori_key] = []

        spikes_in_window = chan_snips[
            (chan_snips['times'] >= onset_time + t_window[0]) &
            (chan_snips['times'] <= onset_time + t_window[1])
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

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(x_vals, y_vals, 'ko', markersize=8)
    ax.set_title(f"Channel {chan} - RF Tuning")
    ax.set_xlabel('Orientation (degrees)')
    ax.set_ylabel('Spike Count')
    ax.set_xlim(min(x_vals) - 10, max(x_vals) + 10)
    ax.grid(True, alpha=0.3)

    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)






    
