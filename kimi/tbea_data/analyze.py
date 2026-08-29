# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))

import pandas as pd
import numpy as np

BASE = "/Users/zendu/Documents/invest/医药/tbea_data"

px = pd.read_csv(f"{BASE}/price_3y.csv", parse_dates=["time"], date_format="%Y%m%d")
ix = pd.read_csv(f"{BASE}/sh_index_3y.csv", parse_dates=["time"], date_format="%Y%m%d")
px = px.sort_values("time").reset_index(drop=True)
ix = ix.sort_values("time").reset_index(drop=True)

last = px.iloc[-1]
prev = px.iloc[-2]
latest_date = last["time"].date()
latest_close = last["close"]
prev_close = prev["close"]
pct_chg = (latest_close / prev_close - 1) * 100

# 52周最高/最低（近252个交易日）
one_yr = px[px["time"] >= px["time"].max() - pd.Timedelta(days=365)]
high_52w = one_yr["close"].max()
low_52w = one_yr["close"].min()
high_52w_d = one_yr.loc[one_yr["close"].idxmax(), "time"].date()
low_52w_d = one_yr.loc[one_yr["close"].idxmin(), "time"].date()

# 涨跌幅
ret_1y = (latest_close / one_yr.iloc[0]["close"] - 1) * 100
ret_3y = (latest_close / px.iloc[0]["close"] - 1) * 100

# 年化波动率（日收益，252交易日）
ret = px["close"].pct_change().dropna()
ann_vol = ret.std() * np.sqrt(252) * 100

# 最大回撤
cummax = px["close"].cummax()
dd = px["close"] / cummax - 1
mdd = dd.min() * 100
mdd_trough_date = px.loc[dd.idxmin(), "time"].date()

# 指数同期
ix_one_yr = ix[ix["time"] >= ix["time"].max() - pd.Timedelta(days=365)]
ix_ret_1y = (ix.iloc[-1]["close"] / ix_one_yr.iloc[0]["close"] - 1) * 100
ix_ret_3y = (ix.iloc[-1]["close"] / ix.iloc[0]["close"] - 1) * 100

# 区间基值日期
print(f"股票区间: {px['time'].min().date()} ~ {latest_date}, 共{len(px)}个交易日")
print(f"指数区间: {ix['time'].min().date()} ~ {ix['time'].max().date()}, 共{len(ix)}个交易日")
print(f"1年基准日(股): {one_yr.iloc[0]['time'].date()}, (指): {ix_one_yr.iloc[0]['time'].date()}")
print()
print(f"最新收盘价({latest_date}): {latest_close} 元, 较前日({prev['time'].date()}) {prev_close} 涨跌 {pct_chg:+.2f}%")
print(f"52周最高: {high_52w} ({high_52w_d}), 52周最低: {low_52w} ({low_52w_d})")
print(f"近1年涨跌幅: {ret_1y:+.2f}%")
print(f"近3年涨跌幅: {ret_3y:+.2f}%")
print(f"年化波动率: {ann_vol:.2f}%")
print(f"最大回撤: {mdd:.2f}% (谷底日 {mdd_trough_date})")
print(f"上证指数近1年: {ix_ret_1y:+.2f}%, 近3年: {ix_ret_3y:+.2f}%")
print(f"超额收益 近1年: {ret_1y - ix_ret_1y:+.2f}pct, 近3年: {ret_3y - ix_ret_3y:+.2f}pct")

# ---- 绘图 ----
from daimon_runtime import setup_plot
setup_plot()
import matplotlib.pyplot as plt

merged = px[["time", "close"]].rename(columns={"close": "tbea"}).merge(
    ix[["time", "close"]].rename(columns={"close": "sse"}), on="time", how="inner")
merged["tbea_norm"] = merged["tbea"] / merged["tbea"].iloc[0] * 100
merged["sse_norm"] = merged["sse"] / merged["sse"].iloc[0] * 100

fig, ax = plt.subplots(figsize=(11, 6))
ax.plot(merged["time"], merged["tbea_norm"], label="特变电工 (600089.SH)", lw=1.6, color="#d62728")
ax.plot(merged["time"], merged["sse_norm"], label="上证指数 (000001.SH)", lw=1.4, color="#1f77b4")
ax.axhline(100, color="gray", ls="--", lw=0.8, alpha=0.6)
ax.set_title("特变电工 vs 上证指数 · 近三年归一化走势 (2023-08-30 = 100)")
ax.set_ylabel("归一化净值")
ax.legend()
ax.grid(alpha=0.3)
fig.autofmt_xdate()
out = f"{BASE}/price_vs_index.png"
fig.savefig(out, bbox_inches="tight", dpi=150)
print(f"\n图已保存: {out}")
