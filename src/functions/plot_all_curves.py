import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_all_curves(ori_result):
    all_curves = pd.DataFrame(ori_result).explode(['x_vals', 'y_vals'])

    fig, ax = plt.subplots(figsize=(6.5, 4.15))
    sns.scatterplot(
        data=all_curves,
        x='x_vals', 
        y='y_vals',
        hue='chan',
        palette='tab20',
        s=50,
        ax=ax,
    )

    ax.set_xlabel('Orientation (degrees)')
    ax.set_ylabel('Spike Count')
    ax.grid(True, alpha=0.3)

    ax.legend(
        title='Channel', 
        bbox_to_anchor=(1.01, 1),
        loc='upper left',
        borderaxespad=0., 
        frameon=True, 
        fontsize='small'
    )

    plt.tight_layout()
    plt.close(fig)

    return fig
