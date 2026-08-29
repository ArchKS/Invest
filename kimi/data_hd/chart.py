from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

setup_plot()

OUT = Path("/Users/zendu/Documents/invest/医药/data_hd/huadian_analysis.png")

df = pd.DataFrame({
    "年份": ["2023", "2024", "2025"],
    "营业总收入(亿元)": [1171.76, 1129.94, 1260.13],
    "归母净利润(亿元)": [45.22, 57.03, 60.70],
    "经营净现金流(亿元)": [132.52, 163.36, 272.21],
    "资产负债率(%)": [62.63, 61.55, 61.37],
})

fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

ax = axes[0]
x = range(len(df))
w = 0.28
ax.bar([i - w for i in x], df["营业总收入(亿元)"], width=w, label="营业总收入", color="#4C72B0")
ax.bar(x, df["归母净利润(亿元)"], width=w, label="归母净利润", color="#DD8452")
ax.bar([i + w for i in x], df["经营净现金流(亿元)"], width=w, label="经营净现金流", color="#55A868")
ax.set_xticks(list(x), df["年份"])
ax.set_ylabel("亿元")
ax.set_title("华电国际：收入、利润与经营现金流（2023-2025）")
ax.legend(frameon=False, fontsize=9)
for i, v in enumerate(df["归母净利润(亿元)"]):
    ax.text(i, v + 18, f"{v:.1f}", ha="center", fontsize=9)

ax2 = axes[1]
sns.lineplot(data=df, x="年份", y="资产负债率(%)", ax=ax2, marker="o", color="#C44E52", linewidth=2)
for i, v in enumerate(df["资产负债率(%)"]):
    ax2.text(i, v + 0.12, f"{v:.1f}%", ha="center", fontsize=10)
ax2.set_ylim(60, 64)
ax2.set_title("资产负债率走势")
ax2.set_ylabel("%")

fig.savefig(OUT, dpi=200, bbox_inches="tight")
print(OUT)
