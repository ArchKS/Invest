# -*- coding: utf-8 -*-
"""新氧(SY)研究报告配图：收入/利润趋势 + 收入结构转型"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style="whitegrid")
setup_plot()

OUT = Path("/Users/zendu/Documents/invest/医药/data")

# ---------- 图1：年度营收与归母净利润 ----------
years = ["2022", "2023", "2024", "2025"]
revenue = [12.58, 14.98, 14.67, 15.23]      # 亿元
net_income = [-0.66, 0.21, -5.90, -2.42]     # 亿元

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(years, revenue, color="#4C9AFF", width=0.5, label="营业收入（亿元）")
ax1.set_ylabel("营业收入（亿元）")
ax1.set_ylim(0, 18)
for b, v in zip(bars, revenue):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.3, f"{v:.2f}", ha="center", fontsize=10)
ax2 = ax1.twinx()
ax2.plot(years, net_income, color="#E5484D", marker="o", linewidth=2.2, label="归母净利润（亿元）")
ax2.axhline(0, color="#888888", linewidth=0.8, linestyle="--")
ax2.set_ylabel("归母净利润（亿元）")
ax2.set_ylim(-8, 4)
for x, v in zip(years, net_income):
    ax2.annotate(f"{v:.2f}", (x, v), textcoords="offset points",
                 xytext=(0, -16 if v < 0 else 8), ha="center", color="#E5484D", fontsize=10)
ax1.set_title("新氧（SY）年度营收与归母净利润（2022–2025）")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left")
fig.text(0.99, 0.01, "数据来源：SEC XBRL / 公司20-F，单位：人民币亿元", ha="right", fontsize=8, color="#666666")
fig.savefig(OUT / "sy_annual_revenue_profit.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ---------- 图2：收入结构转型（2024 vs 2025） ----------
mix = pd.DataFrame({
    "年份": ["2024", "2025"],
    "信息及预约服务（线上平台）": [9.30, 5.00],
    "医美诊疗服务（自营诊所）": [1.70, 6.75],
    "产品及其他（估算）": [3.67, 3.48],
})
fig, ax = plt.subplots(figsize=(9, 5))
bottom = np.zeros(2)
colors = ["#9BB7D4", "#E5484D", "#B8B8B8"]
for col, c in zip(mix.columns[1:], colors):
    vals = mix[col].values
    ax.bar(mix["年份"], vals, bottom=bottom, color=c, width=0.45, label=col)
    for i, (v, b) in enumerate(zip(vals, bottom)):
        if v > 0.8:
            ax.text(i, b + v / 2, f"{v:.1f}", ha="center", va="center", fontsize=10, color="white")
    bottom += vals
ax.set_ylabel("收入（亿元）")
ax.set_title("新氧收入结构：从线上平台到自营医美连锁（2024 vs 2025）")
ax.legend(loc="upper right", fontsize=9)
fig.text(0.99, 0.01, "数据来源：公司财报及公开报道；2024线上收入按63.4%占比推算，余项为估算", ha="right", fontsize=8, color="#666666")
fig.savefig(OUT / "sy_revenue_mix.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ---------- 图3：季度营收与净利润（2025Q1–2026Q1） ----------
qs = ["25Q1", "25Q2", "25Q3", "25Q4", "26Q1"]
qrev = [2.97, 3.79, 3.87, 4.61, 4.33]
qni = [-0.33, -0.36, -0.64, -1.09, -0.49]

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(qs, qrev, color="#66C2A5", width=0.5, label="季度营收（亿元）")
ax1.set_ylabel("营收（亿元）")
ax1.set_ylim(0, 6)
for b, v in zip(bars, qrev):
    ax1.text(b.get_x() + b.get_width() / 2, v + 0.12, f"{v:.2f}", ha="center", fontsize=10)
ax2 = ax1.twinx()
ax2.plot(qs, qni, color="#E5484D", marker="o", linewidth=2.2, label="季度净利润（亿元）")
ax2.axhline(0, color="#888888", linewidth=0.8, linestyle="--")
ax2.set_ylabel("净利润（亿元）")
ax2.set_ylim(-1.6, 0.6)
for i, (x, v) in enumerate(zip(qs, qni)):
    xytext = (20, -4) if i == 0 else (0, -15)
    ax2.annotate(f"{v:.2f}", (x, v), textcoords="offset points", xytext=xytext,
                 ha="center", color="#E5484D", fontsize=10)
ax1.set_title("新氧季度营收与净利润（2025Q1–2026Q1）")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left")
fig.text(0.99, 0.01, "数据来源：公司季度财报（6-K），单位：人民币亿元", ha="right", fontsize=8, color="#666666")
fig.savefig(OUT / "sy_quarterly_trend.png", dpi=200, bbox_inches="tight")
plt.close(fig)

print("saved:", [p.name for p in OUT.glob("sy_*.png")])
