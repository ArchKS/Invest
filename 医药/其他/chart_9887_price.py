from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

setup_plot()

csv = Path("/Users/zendu/Documents/invest/医药/ifind_9887_price_52w_daily.csv")
df = pd.read_csv(csv)
df["date"] = pd.to_datetime(df["time"], format="%Y%m%d")
df = df.sort_values("date")

fig, (ax, axv) = plt.subplots(
    2, 1, figsize=(11, 6.2), sharex=True,
    gridspec_kw={"height_ratios": [3, 1], "hspace": 0.06},
)
sns.lineplot(data=df, x="date", y="close", ax=ax, color="#c0392b", linewidth=1.8)
ax.fill_between(df["date"], df["close"], df["close"].min() * 0.9, color="#c0392b", alpha=0.08)
ax.axhline(35.0, color="#7f8c8d", linestyle="--", linewidth=1)
ax.text(df["date"].iloc[1], 36, "发行价 35.0 港元", color="#7f8c8d", fontsize=9)
ax.set_ylabel("收盘价（港元）")
ax.set_title("维立志博-B（9887.HK）股价走势 · 2026-04-27 至 2026-08-28（iFinD 数据可得区间）", fontsize=13)

colors = ["#c0392b" if c >= o else "#27ae60" for c, o in zip(df["close"], df["open"])]
axv.bar(df["date"], df["volume"] / 10000, color=colors, width=1.0)
axv.set_ylabel("成交量（万股）")
axv.set_xlabel("日期")

last = df.iloc[-1]
ax.annotate(
    f"{last['close']:.2f}",
    xy=(last["date"], last["close"]),
    xytext=(10, -12), textcoords="offset points", fontsize=10, color="#c0392b",
)

fig.savefig("/Users/zendu/Documents/invest/医药/chart_9887_price.png", dpi=200, bbox_inches="tight")
print("saved")
