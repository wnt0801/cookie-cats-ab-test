import pandas as pd
import numpy as np
from scipy import stats
import os

os.chdir(r"C:\Users\Lenovo\PycharmProjects\cookie-cats-ab-test")

df = pd.read_csv("data/cookie_cats.csv")

# ── 基础数据 ──────────────────────────────────────────
g30 = df[df["version"] == "gate_30"]
g40 = df[df["version"] == "gate_40"]

r1_30, r1_40 = g30["retention_1"].mean(), g40["retention_1"].mean()
r7_30, r7_40 = g30["retention_7"].mean(), g40["retention_7"].mean()

# ── ROI 换算 ─────────────────────────────────────────
# 假设 DAU = 1,000,000（互联网产品常用估算基数）
DAU = 1_000_000

loss_r1 = (r1_30 - r1_40) * DAU
loss_r7 = (r7_30 - r7_40) * DAU

print("=== 业务影响估算（基于 DAU=100万）===")
print(f"retention_1 差值: {r1_30 - r1_40:.4f} → 每天少留存 {loss_r1:,.0f} 名用户")
print(f"retention_7 差值: {r7_30 - r7_40:.4f} → 每天少留存 {loss_r7:,.0f} 名用户")

# ── 结论汇总 ─────────────────────────────────────────
print("""
=== 实验结论汇总 ===

实验设计：
  - 对照组 gate_30（n=44,700）vs 实验组 gate_40（n=45,489）
  - SRM 检验：p=0.0086，偏差 0.87%，大样本敏感性问题，工程上可接受

频率派结果：
  - retention_1：p=0.074，不显著，CI 跨零
  - retention_7：p=0.0016，显著，CI=[0.0031, 0.0133]，gate_30 更高

Bayesian 结果：
  - retention_1：P(gate_30 > gate_40) = 96.3%，期望提升 +0.59%
  - retention_7：P(gate_30 > gate_40) = 99.9%，期望提升 +0.82%

业务建议：
  强烈建议保留 gate_30。
  7日留存下降概率 99.9%，按 DAU 100万估算每天减少约 8,200 名长期活跃用户。
  次日留存虽频率派不显著，但 Bayesian 显示 96% 概率 gate_30 更优，方向一致。
  两项指标信号均指向同一结论，gate_40 上线风险明显大于收益。
""")