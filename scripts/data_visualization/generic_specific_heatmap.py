import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.ticker import ScalarFormatter


plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "DejaVu Serif", "Times New Roman"],
    "mathtext.fontset": "stix",
    "font.size": 8,
    "axes.labelsize": 9,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
})

sns.set_theme(
    style="white",
    rc={
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif", "Times New Roman"],
    }
)



def format_generic_label(label: str) -> str:
    """
    Remove underscores for x-axis labels and optionally wrap long labels.
    """
    mapping = {
        "AVIATION": "AVIATION",
        "SMART_DEVICE": "SMART_\nDEVICE",
        "AUTOMOTIVE": "AUTOMOTIVE",
        "SMART_BUILDING": "SMART_\nBUILDING",
        "SECURITY": "SECURITY",
        "DRONES": "DRONES",
        "AUTONOMOUS_PASSENGER_SHIP": "AUTONOMOUS_\nPASSENGER_SHIP",
    }
    return mapping.get(label, label.replace("_", " "))


def plot_domain_problem_heatmap(
    generic_csv_path: str,
    specific_csv_path: str,
    output_path: str = "generic_specific_heatmap.pdf",
    figsize=(8.8, 5.8),
    min_problem_count: int = 3,
    top_k: int = 15,
    use_log_scale: bool = True,
):
    ignore_labels = {"BENCHMARK", "TESTING"}


    generic_df = pd.read_csv(generic_csv_path)[["Model", "CLUSTERS"]].copy()
    specific_df = pd.read_csv(specific_csv_path)[["Model", "CLUSTERS"]].copy()

    generic_df.columns = ["Model", "GenericDomain"]
    specific_df.columns = ["Model", "SpecificProblem"]

    generic_df = generic_df[~generic_df["GenericDomain"].isin(ignore_labels)]
    specific_df = specific_df[~specific_df["SpecificProblem"].isin(ignore_labels)]

    merged_df = pd.merge(generic_df, specific_df, on="Model", how="inner")

    if merged_df.empty:
        raise ValueError("No overlapping models found after filtering.")

    if min_problem_count > 1:
        valid_problems = (
            merged_df["SpecificProblem"]
            .value_counts()
            .loc[lambda s: s >= min_problem_count]
            .index
        )
        merged_df = merged_df[merged_df["SpecificProblem"].isin(valid_problems)]

    if merged_df.empty:
        raise ValueError("No models remain after applying min_problem_count.")

    top_problems = (
        merged_df["SpecificProblem"]
        .value_counts()
        .head(top_k)
        .index
    )

    merged_df["SpecificProblem"] = merged_df["SpecificProblem"].apply(
        lambda x: x if x in top_problems else "OTHER_PROBLEMS"
    )

    # Crosstab
    heatmap_df = pd.crosstab(
        merged_df["SpecificProblem"],
        merged_df["GenericDomain"]
    )

    # Sort columns and rows
    col_order = heatmap_df.sum(axis=0).sort_values(ascending=False).index.tolist()
    row_order = heatmap_df.sum(axis=1).sort_values(ascending=False).index.tolist()

    if "OTHER_PROBLEMS" in row_order:
        row_order.remove("OTHER_PROBLEMS")
        row_order.append("OTHER_PROBLEMS")

    heatmap_df = heatmap_df.loc[row_order, col_order]

    x_labels = [format_generic_label(c) for c in heatmap_df.columns]

    y_labels = heatmap_df.index.tolist()
    fig, ax = plt.subplots(figsize=figsize)

    if use_log_scale:
        plot_df = heatmap_df.astype(float).replace(0, np.nan)
        vmax = np.nanmax(plot_df.values)

        sns.heatmap(
            plot_df,
            annot=False,
            cmap="YlGnBu",
            linewidths=0.3,
            linecolor="white",
            norm=LogNorm(vmin=1, vmax=vmax),
            cbar_kws={
                "label": "Number of Models",
                "shrink": 0.92,
                "pad": 0.02
            },
            ax=ax
        )

        cbar = ax.collections[0].colorbar
        ticks = [t for t in [1, 10, 100] if t <= vmax]
        if not ticks:
            ticks = [1]
        cbar.set_ticks(ticks)
        cbar.formatter = ScalarFormatter()
        cbar.update_ticks()

    else:
        sns.heatmap(
            heatmap_df,
            annot=False,
            cmap="YlGnBu",
            linewidths=0.3,
            linecolor="white",
            cbar_kws={
                "label": "Number of Models",
                "shrink": 0.92,
                "pad": 0.02
            },
            ax=ax
        )

    ax.set_xlabel("Generic Application Domain")
    ax.set_ylabel("Specific Problem Cluster")

    # Apply labels
    ax.set_xticklabels(x_labels, rotation=0, ha="center", fontsize=7)
    ax.set_yticklabels(y_labels, rotation=0, fontsize=8)

    ax.tick_params(axis="x", labelsize=7, pad=1)
    ax.tick_params(axis="y", labelsize=8, pad=1)
    ax.xaxis.label.set_weight("medium")
    ax.yaxis.label.set_weight("medium")

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=7)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.show()

    return heatmap_df


if __name__ == "__main__":
    generic_csv = "annotations/generic_domain_clusters.csv"
    specific_csv = "annotations/specific_domain_clusters.csv"

    heatmap_table = plot_domain_problem_heatmap(
        generic_csv_path=generic_csv,
        specific_csv_path=specific_csv,
        output_path="generic_specific_heatmap.png",
        figsize=(8.8, 5.8),
        min_problem_count=3,
        top_k=10,
        use_log_scale=True,
    )

    print(heatmap_table)