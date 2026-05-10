import pandas as pd
import os
os.chdir(r"C:\Users\Lenovo\PycharmProjects\cookie-cats-ab-test")
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 读取数据 ──────────────────────────────────────────
df = pd.read_csv("data/cookie_cats.csv")

print("=== 基本信息 ===")
print(df.shape)
print(df.dtypes)
print(df.head())

print("\n=== 缺失值 ===")
print(df.isnull().sum())

print("\n=== 各组样本量 ===")
print(df["version"].value_counts())

# ── 核心指标均值对比 ──────────────────────────────────
print("\n=== 留存率对比 ===")
summary = df.groupby("version")[["retention_1", "retention_7"]].mean().round(4)
print(summary)

print("\n=== 游戏局数描述统计 ===")
print(df.groupby("version")["sum_gamerounds"].describe().round(2))

# ── 图1：sum_gamerounds 分布（去掉极端值方便看） ────────
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, version in zip(axes, ["gate_30", "gate_40"]):
    data = df[df["version"] == version]["sum_gamerounds"]
    data_clipped = data[data <= data.quantile(0.95)]  # 截掉 top 5% 极端值
    ax.hist(data_clipped, bins=40, color="#4C72B0", edgecolor="white", alpha=0.85)
    ax.set_title(f"{version} — sum_gamerounds 分布 (p95截断)")
    ax.set_xlabel("game rounds")
    ax.set_ylabel("用户数")

plt.tight_layout()
plt.savefig("outputs/01_gamerounds_dist.png", dpi=150)
plt.show()
print("图1已保存：outputs/01_gamerounds_dist.png")

# ── 图2：留存率对比柱状图 ────────────────────────────
retention_df = summary.reset_index().melt(
    id_vars="version",
    value_vars=["retention_1", "retention_7"],
    var_name="metric",
    value_name="rate"
)

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=retention_df, x="metric", y="rate", hue="version",
            palette=["#4C72B0", "#DD8452"], ax=ax)
ax.set_title("Retention Rate: gate_30 vs gate_40")
ax.set_ylabel("retention rate")
ax.set_xlabel("")
ax.set_ylim(0, max(retention_df["rate"]) * 1.2)

for container in ax.containers:
    ax.bar_label(container, fmt="%.4f", padding=3, fontsize=9)

plt.tight_layout()
plt.savefig("outputs/01_retention_compare.png", dpi=150)
plt.show()
print("图2已保存：outputs/01_retention_compare.png")