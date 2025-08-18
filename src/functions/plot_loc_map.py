import matplotlib.pyplot as plt
import streamlit as st


def plot_loc_map(chan, chan_res):
    if chan_res is not None:
        grid_x, grid_y, grid_z = chan_res['grid_x'], chan_res['grid_y'], chan_res['grid_z']

        fig, ax = plt.subplots(figsize=(6, 5))
        extent = [grid_x.min(), grid_x.max(), grid_y.min(), grid_y.max()]
        c = ax.imshow(grid_z, extent=extent, origin='lower', cmap="viridis", aspect='auto')
        ax.set_title(f"Channel {chan} - RF Map (2D Gaussian Fit)")
        ax.set_xlabel("X position (deg)")
        ax.set_ylabel("Y position (deg)")
        ax.grid(True, alpha=0.3) 
        fig.colorbar(c, ax=ax)

        plt.tight_layout(rect=[0, 0.1, 1, 1])
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning(f'No data available for channel {chan}')
