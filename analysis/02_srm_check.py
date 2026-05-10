import pandas as pd
import numpy as np
from scipy import stats
import os

os.chdir(r"C:\Users\Lenovo\PycharmProjects\cookie-cats-ab-test")

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
    print("⚠️  SRM 检测到异常：流量分配显著偏离 1:1，实验结论需谨慎")
else:
    print("✅  流量分配正常，无 SRM 问题，可继续分析")