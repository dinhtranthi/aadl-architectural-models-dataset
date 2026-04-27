import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_cluster_distribution(
    csv_path,
    output_dir="figures",
    column_name="CLUSTERS",
    figsize=(10, 7),
    dpi=600
):
    df = pd.read_csv(csv_path)

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found.")

    df = df.dropna(subset=[column_name])

    counts = df[column_name].value_counts().sort_values(ascending=True)
    percentages = counts / counts.sum() * 100

    plot_df = pd.DataFrame({
        "label": counts.index,
        "percentage": percentages.values
    })

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 12,
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none"
    })

    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.barh(
        plot_df["label"],
        plot_df["percentage"],
        edgecolor="black",
        linewidth=1.0,
        color="#4C8C4A"
    )

    ax.set_xlabel("Percentage of Models (%)")
    ax.set_ylabel("Architecture Domain")

    # Grid
    ax.grid(axis="x", linestyle="--", linewidth=0.7, alpha=0.5)
    ax.set_axisbelow(True)

    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))

    max_pct = plot_df["percentage"].max()
    offset = max_pct * 0.01

    for bar, pct in zip(bars, plot_df["percentage"]):
        ax.text(
            bar.get_width() + offset,
            bar.get_y() + bar.get_height() / 2,
            f"{pct:.1f}%",
            va="center",
            ha="left",
            fontsize=10
        )

    ax.set_xlim(0, max_pct * 1.15)

    fig.tight_layout()

    base_name = f"{column_name.lower()}_distribution"


    fig.savefig(os.path.join(output_dir, base_name + ".pdf"), bbox_inches="tight")

    plt.close(fig)

    print("Saved professional figures to:", output_dir)


if __name__ == "__main__":
    plot_cluster_distribution(
        csv_path="annotations/generic_domain_clusters.csv",
        output_dir="figures",
        column_name="CLUSTERS"
    )