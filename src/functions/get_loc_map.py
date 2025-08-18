import numpy as np
from scipy.optimize import curve_fit


def gaussian_2d(coords, A, x0, y0, sigma_x, sigma_y, offset):
    x, y = coords
    return A * np.exp(
        -(((x - x0) ** 2) / (2 * sigma_x**2) + ((y - y0) ** 2) / (2 * sigma_y**2))
    ) + offset

def get_loc_map(chan_data):
    chan, onset_data, snip_data = chan_data['chan'], chan_data['onset_data'], chan_data['snip_data']
    chan_snips = snip_data[snip_data['channels'] == chan]

    t_window = (0.05, 0.2)
    bin_res=1.0

    pos_spike_counts = {}
    for _, trial_row in onset_data.iterrows():
        onset_time = trial_row['OnsetTm']
        xpos, ypos = trial_row['TargPosX'], trial_row['TargPosY']
        pos_key = (round(xpos / bin_res) * bin_res, round(ypos / bin_res) * bin_res)

        if pos_key not in pos_spike_counts:
            pos_spike_counts[pos_key] = []

        spikes_in_window = chan_snips[
            (chan_snips['times'] >= onset_time + t_window[0]) &
            (chan_snips['times'] <= onset_time + t_window[1])
        ]

        pos_spike_counts[pos_key].append(len(spikes_in_window))

    x_vals, y_vals, z_vals = [], [], []
    for (x, y), counts in pos_spike_counts.items():
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(np.mean(counts))

    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z_vals = np.array(z_vals)

    chan_res = {}

    try:
        grid_x, grid_y = np.meshgrid(
            np.linspace(min(x_vals), max(x_vals), 100),
            np.linspace(min(y_vals), max(y_vals), 100)
        )

        initial_guess = [z_vals.max(), x_vals[np.argmax(z_vals)], y_vals[np.argmax(z_vals)], 1, 1, z_vals.min()]
        popt, _ = curve_fit(gaussian_2d, (x_vals, y_vals), z_vals, p0=initial_guess)
        grid_z = gaussian_2d((grid_x, grid_y), *popt).reshape(grid_x.shape)

        chan_res[chan] = {
            'grid_x': grid_x,
            'grid_y': grid_y,
            'grid_z': grid_z,
            'popt': popt
        }

    except:
        chan_res[chan] = None

    return chan_res