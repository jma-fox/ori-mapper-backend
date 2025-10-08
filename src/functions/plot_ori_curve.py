import matplotlib.pyplot as plt


def plot_ori_curve(channel_result):
    channel = channel_result['channel']
    x_vals = channel_result['x_vals']
    y_vals = channel_result['y_vals']

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(x_vals, y_vals, 'ko', markersize=8)
    ax.set_title(f"Channel {channel}")
    ax.set_xlabel('Orientation (degrees)')
    ax.set_ylabel('Spike Count')
    ax.set_xlim(min(x_vals) - 10, max(x_vals) + 10)
    ax.set_ylim(0, 5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.close(fig)

    return fig
