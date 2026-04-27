import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

def log_tick_formatter(val, pos=None):
    return f"{int(val)}" if val >= 1 else ""


df = pd.read_csv("metadata.csv")


nodes_min = 0
nodes_max = 2000

edges_min = 0
edges_max = 2000

# Common ticks for log scale
ticks = [1, 10, 100, 1000]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
})


fig, axes = plt.subplots(1, 2, figsize=(10, 4))
bins = np.logspace(np.log10(1), np.log10(2000), 30)

# Nodes (gray)
axes[0].hist(
    df['num_components'],
    bins=bins,
    color="#6E6E6E",
    edgecolor="black",
    linewidth=0.5
)
axes[0].set_xscale('log')
axes[0].set_xlim(nodes_min, nodes_max)
axes[0].set_xticks(ticks)
axes[0].xaxis.set_major_formatter(FuncFormatter(log_tick_formatter))
axes[0].set_title("Nodes (Components)")
axes[0].set_xlabel("Number of Nodes")
axes[0].set_ylabel("Number of Models")
axes[0].grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.5)

# Edges (muted orange)
axes[1].hist(
    df['num_connections'],
    bins=bins,
    color="#D28E2A",
    edgecolor="black",
    linewidth=0.5
)
axes[1].set_xscale('log')
axes[1].set_xlim(edges_min, edges_max)
axes[1].set_xticks(ticks)
axes[1].xaxis.set_major_formatter(FuncFormatter(log_tick_formatter))
axes[1].set_title("Edges (Connections)")
axes[1].set_xlabel("Number of Edges")
axes[1].set_ylabel("Number of Models")
axes[1].grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.5)

plt.tight_layout()
plt.rcParams.update({
    "text.usetex": True,
})
plt.savefig("model_size_distribution_combined.pdf", bbox_inches="tight")
plt.show()


