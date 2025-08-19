import matplotlib.pyplot as plt
import streamlit as st


def plot_loc_map(chan_result):
    chan = chan_result['chan']
    grid_x = chan_result['grid_x']
    grid_y = chan_result['grid_y']
    grid_z = chan_result['grid_z']

    fig, ax = plt.subplots(figsize=(6, 5))
    extent = [grid_x.min(), grid_x.max(), grid_y.min(), grid_y.max()]
    c = ax.imshow(grid_z, extent=extent, origin='lower', cmap="viridis", aspect='auto')
    ax.set_xlabel("X position (dva)")
    ax.set_ylabel("Y position (dva)")
    ax.set_title(f"Channel {chan}")
    ax.grid(True, alpha=0.3) 
    fig.colorbar(c, ax=ax)

    plt.tight_layout(rect=[0, 0.1, 1, 1])
    plt.close(fig)

    return fig
