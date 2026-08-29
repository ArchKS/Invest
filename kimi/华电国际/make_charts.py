from pathlib import Path
import sys
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
setup_plot()

# 图1: 业绩趋势
years = ['2023', '2024', '2025']
rev = [1171.8, 1129.9, 1260.1]      # iFinD 原始披露口径
np_ = [45.2, 57.0, 60.7]            # 归母净利润
fig, ax1 = plt.subplots(figsize=(9, 5))
x = range(3)
b = ax1.bar([i-0.2 for i in x], rev, width=0.38, label='营业收入(亿元)', color='#4878d0')
ax1.bar_label(b, fmt='%.0f')
ax2 = ax1.twinx()
b2 = ax2.bar([i+0.2 for i in x], np_, width=0.38, label='归母净利润(亿元)', color='#ee854a')
ax2.bar_label(b2, fmt='%.1f')
ax1.set_xticks(list(x)); ax1.set_xticklabels(years)
ax1.set_ylabel('营业收入 (亿元)'); ax2.set_ylabel('归母净利润 (亿元)')
ax1.set_ylim(0, 1500); ax2.set_ylim(0, 150)
ax1.set_title('华电国际 2023–2025 业绩趋势（iFinD，原始披露口径）')
h1,l1 = ax1.get_legend_handles_labels(); h2,l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left')
fig.savefig('chart_profit.png', dpi=200, bbox_inches='tight'); plt.close(fig)

# 图2: 近一年股价周线
p = pd.read_csv('data/price1y.csv')
p['date'] = pd.to_datetime(p['time'], format='%Y%m%d')
fig, ax = plt.subplots(figsize=(10, 4.5))
sns.lineplot(data=p, x='date', y='close', ax=ax, color='#4878d0', linewidth=1.8)
ax.axhline(p['close'].iloc[-1], ls='--', color='#d65f5f', lw=1)
ax.text(p['date'].iloc[0], p['close'].iloc[-1]+0.03, f"最新收盘 {p['close'].iloc[-1]:.2f} 元", color='#d65f5f')
ax.set_title('华电国际（600027.SH）近一年周收盘价（前复权，元）— iFinD')
ax.set_ylabel('收盘价 (元)'); ax.set_xlabel('')
fig.savefig('chart_price.png', dpi=200, bbox_inches='tight'); plt.close(fig)
print('done')
