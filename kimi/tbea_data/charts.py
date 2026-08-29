import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
try:
    from daimon_runtime import setup_plot
    setup_plot()
except Exception:
    plt.rcParams["font.family"] = ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS", "sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False

out = Path("/Users/zendu/Documents/invest/医药/tbea_data")

# 图1: 营收与归母净利
years = ["2023", "2024", "2025", "2026H1"]
rev = [982.06, 978.67, 973.18, 565.85]
np_ = [107.03, 41.35, 59.54, 25.52]
ocf = [258.12, 129.49, 93.31, 62.20]
x = np.arange(len(years)); w = 0.35
fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.bar(x - w/2, rev, w, label="营业总收入(亿元)", color="#2E5E8C")
ax1.bar(x + w/2, ocf, w, label="经营现金流净额(亿元)", color="#7FB3D5")
ax1.set_xticks(x); ax1.set_xticklabels(years)
ax1.set_ylabel("亿元")
ax2 = ax1.twinx()
ax2.plot(x, np_, "o-", color="#C0392B", lw=2, label="归母净利润(亿元)")
for xi, v in zip(x, np_):
    ax2.annotate(f"{v}", (xi, v), textcoords="offset points", xytext=(0, 8), ha="center", color="#C0392B", fontsize=10)
ax2.set_ylabel("归母净利润(亿元)", color="#C0392B")
ax2.set_ylim(0, 130)
h1,l1 = ax1.get_legend_handles_labels(); h2,l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc="upper right", fontsize=9)
ax1.set_title("特变电工：收入、经营现金流与归母净利润（2023–2026H1）")
fig.savefig(out/"fin_trend.png", bbox_inches="tight", dpi=150)
plt.close(fig)

# 图2: 业务分部收入结构 2024 vs 2025 vs 2026H1
segs = ["变压器", "电线电缆", "煤炭产品", "光伏(硅片/系统工程)", "电费", "铝电子新材料"]
v2025 = [267.60, 155.69, 169.66, 135.55, 71.83, 0]
v2024 = [223.64, 156.92, 192.64, 185.31, 0, 56.05]
v2026h1 = [149.68, 108.41, 79.02, 95.45, 0, 35.09]
fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))
for ax, vals, title in zip(axes, [v2024, v2025, v2026h1], ["2024年报", "2025年报", "2026中报"]):
    vals2 = [v for v in vals]
    labels = [f"{s}\n{v:.0f}亿" if v > 0 else "" for s, v in zip(segs, vals2)]
    plot_vals = [v if v > 0 else 0.0001 for v in vals2]
    wedges, _ = ax.pie(plot_vals, colors=plt.cm.Set3.colors[:6], startangle=90,
                       wedgeprops=dict(width=0.55, edgecolor="w"))
    ax.legend(wedges, [f"{s} {v:.1f}亿" if v>0 else f"{s} —" for s, v in zip(segs, vals2)],
              loc="center left", bbox_to_anchor=(0.96, 0.5), fontsize=8)
    ax.set_title(title)
fig.suptitle("特变电工业务分部收入结构（按产品，亿元）")
fig.savefig(out/"segments.png", bbox_inches="tight", dpi=150)
plt.close(fig)

# 图3: 分部毛利率变化
gm = {
    "变压器": [17.58, 19.81, 19.55],
    "电线电缆": [7.62, 8.34, 8.80],
    "煤炭产品": [32.42, 22.39, 25.65],
    "光伏": [1.41, 0.59, 9.73],
    "铝电子新材料": [11.61, None, 18.14],
}
periods = ["2024年报", "2025年报", "2026中报"]
fig, ax = plt.subplots(figsize=(9, 5))
for name, vals in gm.items():
    xs = [i for i, v in enumerate(vals) if v is not None]
    ys = [v for v in vals if v is not None]
    ax.plot(xs, ys, "o-", label=name, lw=2)
    for xi, yi in zip(xs, ys):
        ax.annotate(f"{yi:.1f}", (xi, yi), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
ax.set_xticks(range(3)); ax.set_xticklabels(periods)
ax.set_ylabel("毛利率(%)")
ax.set_title("特变电工分产品毛利率变化")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
fig.savefig(out/"gross_margin.png", bbox_inches="tight", dpi=150)
plt.close(fig)
print("charts done")
