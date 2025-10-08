import numpy as np
from scipy.optimize import curve_fit


def gaussian_2d(coords, A, x0, y0, sigma_x, sigma_y, offset):
    x, y = coords
    fit = A * np.exp(-(((x - x0) ** 2) / (2 * sigma_x**2) + ((y - y0) ** 2) / (2 * sigma_y**2))) + offset

    return fit

def _build_heatmap_from_counts(pos_spike_counts):
    xs = sorted({x for (x, _) in pos_spike_counts.keys()})
    ys = sorted({y for (_, y) in pos_spike_counts.keys()})
    x_idx = {x:i for i, x in enumerate(xs)}
    y_idx = {y:i for i, y in enumerate(ys)}
    Z = np.full((len(ys), len(xs)), np.nan, dtype=float)

    for (x, y), counts in pos_spike_counts.items():
        Z[y_idx[y], x_idx[x]] = float(np.mean(counts))

    grid_x, grid_y = np.meshgrid(np.array(xs, dtype=float), np.array(ys, dtype=float))

    return grid_x, grid_y, Z

def get_loc_map(channel_data):
    channel = channel_data['channel']
    task_data = channel_data['task_data']
    snip_data = channel_data['snip_data']
    channel_snips = snip_data[snip_data['channels'] == channel]

    t_window = (0.0, 0.2)
    bin_res = 1.0

    # collect spike counts per (x,y) position (already binned to bin_res)
    pos_spike_counts = {}
    for _, trial_row in task_data.iterrows():
        onset_time = trial_row['GaborOnsetTm']
        xpos = trial_row['TargPosX']
        ypos = trial_row['TargPosY']

        pos_key = (round(xpos / bin_res) * bin_res, round(ypos / bin_res) * bin_res)
        if pos_key not in pos_spike_counts:
            pos_spike_counts[pos_key] = []

        spikes_in_window = channel_snips[
            (channel_snips['times'] >= onset_time + t_window[0]) &
            (channel_snips['times'] <= onset_time + t_window[1])
        ]

        pos_spike_counts[pos_key].append(len(spikes_in_window))

    # prepare x,y,z arrays from the mean counts
    x_vals, y_vals, z_vals = [], [], []
    for (x, y), counts in pos_spike_counts.items():
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(np.mean(counts))

    x_vals = np.array(x_vals, dtype=float)
    y_vals = np.array(y_vals, dtype=float)
    z_vals = np.array(z_vals, dtype=float)

    # Always compute the original heatmap grids (for fallback and optional inspection)
    hm_grid_x, hm_grid_y, hm_grid_z = _build_heatmap_from_counts(pos_spike_counts)

    channel_result = {
        'channel': channel,
        'heatmap_grid_x': hm_grid_x,
        'heatmap_grid_y': hm_grid_y,
        'heatmap_grid_z': hm_grid_z,
    }

    can_fit = (
        len(z_vals) >= 6 and
        np.isfinite(z_vals).all() and
        np.nanstd(z_vals) > 0
    )

    if not can_fit:
        # Fallback: use the original heat map as the main output
        channel_result.update({'grid_x': hm_grid_x, 'grid_y': hm_grid_y,
                            'grid_z': hm_grid_z, 'popt': None})
        return channel_result

    try:
        # set reasonable initial guess and bounds (positive sigmas)
        peak_idx = int(np.nanargmax(z_vals))
        initial_guess = [
            float(np.nanmax(z_vals)),        # A
            float(x_vals[peak_idx]),         # x0
            float(y_vals[peak_idx]),         # y0
            max(np.std(x_vals)*0.5, 1e-3),   # sigma_x
            max(np.std(y_vals)*0.5, 1e-3),   # sigma_y
            float(np.nanmin(z_vals))         # offset
        ]
        bounds = (
            [0, np.min(x_vals), np.min(y_vals), 1e-6, 1e-6, -np.inf],
            [np.inf, np.max(x_vals), np.max(y_vals), np.inf, np.inf,  np.inf],
        )

        # create a smooth grid for the Gaussian render
        x_lines = np.linspace(np.min(x_vals), np.max(x_vals), 100)
        y_lines = np.linspace(np.min(y_vals), np.max(y_vals), 100)
        grid_x, grid_y = np.meshgrid(x_lines, y_lines)

        popt, _ = curve_fit(
            gaussian_2d, (x_vals, y_vals), z_vals,
            p0=initial_guess, bounds=bounds, maxfev=20000
        )
        grid_z = gaussian_2d((grid_x, grid_y), *popt).reshape(grid_x.shape)

        # Success: return Gaussian surface
        channel_result.update({'grid_x': grid_x, 'grid_y': grid_y,
                            'grid_z': grid_z, 'popt': popt})
    except Exception:
        # Fallback: return the original spike-count heat map
        channel_result.update({'grid_x': hm_grid_x, 'grid_y': hm_grid_y,
                            'grid_z': hm_grid_z, 'popt': None})

    return channel_result
