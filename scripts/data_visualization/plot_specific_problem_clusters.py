import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_top_problem_clusters(
    csv_path,
    output_path="figures/top10_problem_clusters.png",
    column_name="CLUSTERS",
    top_k=10,
    figsize=(11, 8),
    dpi=600
):

    df = pd.read_csv(csv_path)

    if column_name not in df.columns:
        raise ValueError(
            f"Column '{column_name}' not found in CSV. Available columns: {list(df.columns)}"
        )

    df = df.dropna(subset=[column_name]).copy()

    if df.empty:
        raise ValueError(f"No valid rows found in column '{column_name}'.")

    counts = df[column_name].value_counts()

    top_counts = counts.iloc[:top_k].copy()
    others_count = counts.iloc[top_k:].sum()

    if others_count > 0:
        top_counts.loc["Others"] = others_count

    # Sort ascending
    plot_counts = top_counts.sort_values(ascending=True)
    total = plot_counts.sum()
    percentages = plot_counts / total * 100

    plot_df = pd.DataFrame({
        "label": plot_counts.index,
        "percentage": percentages.values
    })

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 12,
        "axes.labelsize": 14,
        "axes.titlesize": 15,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "pdf.fonttype": 42,
        "ps.fonttype": 42
    })

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=figsize)

    bars = ax.barh(
        plot_df["label"],
        plot_df["percentage"],
        edgecolor="black",
        linewidth=1.0
    )

    ax.set_xlabel("Percentage of Models (%)")
    ax.set_ylabel("Specific Problem Cluster")

    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.grid(axis="x", linestyle="--", linewidth=0.7, alpha=0.5)
    ax.set_axisbelow(True)

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
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    plot_top_problem_clusters(
        csv_path="annotations/specific_domain_clusters.csv",
        output_path="figures/top10_specific_problem_clusters.pdf",
        column_name="CLUSTERS",
        top_k=10,
        figsize=(11, 8),
        dpi=600
    )