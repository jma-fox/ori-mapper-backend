import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def plot_all_maps(loc_maps):
    sigma_level=1.0

    fig, ax = plt.subplots(figsize=(6.4, 6))

    map_fits = []
    channels = []
    for loc_map in loc_maps:
        if loc_map['popt'] is None:
            continue
        A, x0, y0, sx, sy, offset = loc_map['popt']
        if not np.isfinite([A, x0, y0, sx, sy, offset]).all():
            continue
        channel = loc_map['channel']
        map_fits.append((channel, A, x0, y0, sx, sy, offset))
        channels.append(channel)

    if not map_fits:
        return None

    colors = {}
    cmap = plt.cm.get_cmap('tab20')
    for i, chan in enumerate(channels):
        colors[chan] = cmap(i % cmap.N)

    x_all, y_all = [], []
    for (chan, A, x0, y0, sx, sy, offset) in map_fits:
        w = 2 * sigma_level * abs(sx)
        h = 2 * sigma_level * abs(sy)
        e = Ellipse(
            (x0, y0), 
            width=w, 
            height=h, 
            angle=0, 
            fill=False, 
            linewidth=2.0,
            edgecolor=colors[chan], 
            facecolor=colors[chan], 
            label=chan
        )
        ax.add_patch(e)
        x_all.append(x0)
        y_all.append(y0)

    ax.legend(
        title='Channel', 
        bbox_to_anchor=(1.01, 1),
        loc='upper left',
        borderaxespad=0., 
        frameon=True, 
        fontsize='small'
    )

    x_all, y_all = np.array(x_all), np.array(y_all)
    max_sx = max(abs(e[4]) for e in map_fits)
    max_sy = max(abs(e[5]) for e in map_fits)
    pad_x = 2 * max_sx
    pad_y = 2 * max_sy
    ax.set_xlim(x_all.min() - pad_x, x_all.max() + pad_x)
    ax.set_ylim(y_all.min() - pad_y, y_all.max() + pad_y)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('X position (dva)')
    ax.set_ylabel('Y position (dva)')
    ax.grid(True, linestyle=':', linewidth=0.8)

    plt.tight_layout()
    plt.close(fig)

    return fig
