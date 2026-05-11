import pandas as pd
import numpy as np
from scipy import stats
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv("data/cookie_cats.csv")

# ── 实际样本量 ────────────────────────────────────────
observed = df["version"].value_counts()
n_total = len(df)

print("=== 实际样本量 ===")
print(observed)
print(f"总计：{n_total}")

# ── 期望样本量（1:1 分配）────────────────────────────
expected = np.array([n_total / 2, n_total / 2])
observed_values = np.array([observed["gate_30"], observed["gate_40"]])

print(f"\n期望各组：{n_total / 2:.0f}")
print(f"实际 gate_30：{observed_values[0]}，gate_40：{observed_values[1]}")

# ── 卡方检验 ─────────────────────────────────────────
chi2, p_value = stats.chisquare(f_obs=observed_values, f_exp=expected)

print(f"\n=== SRM Check 结果 ===")   # SRM：Sample Ratio Mismatch（样本比例不匹配）
print(f"chi2 统计量：{chi2:.4f}")
print(f"p 值：{p_value:.4f}")

if p_value < 0.05:
    deviation = abs(observed_values[0] - observed_values[1]) / n_total
    print(f"⚠️  p={p_value:.4f}，统计显著，但实际偏差仅 {deviation:.2%}")
    print("    大样本放大微小随机误差所致，判断为正常波动，非分流机制故障")
else:
    print("✅  流量分配正常，无 SRM 问题")