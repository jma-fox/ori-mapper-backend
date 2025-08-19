import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def plot_ori_curve(chan_result):
    chan = chan_result['chan']
    x_vals = chan_result['x_vals']
    y_vals = chan_result['y_vals']

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(x_vals, y_vals, 'ko', markersize=8)
    ax.set_title(f"Channel {chan}")
    ax.set_xlabel('Orientation (degrees)')
    ax.set_ylabel('Spike Count')
    ax.set_xlim(min(x_vals) - 10, max(x_vals) + 10)
    ax.set_ylim(0, 5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.close(fig)

    return fig
