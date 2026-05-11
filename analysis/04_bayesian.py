import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv("data/cookie_cats.csv")
np.random.seed(42)
N_SAMPLES = 100_000

def bayesian_ab(df, metric):
    g30 = df[df["version"] == "gate_30"][metric]
    g40 = df[df["version"] == "gate_40"][metric]

    # 成功数 / 失败数
    s30, f30 = g30.sum(), len(g30) - g30.sum()
    s40, f40 = g40.sum(), len(g40) - g40.sum()

    # posterior: Beta(1 + 成功, 1 + 失败)
    post30 = stats.beta(1 + s30, 1 + f30)
    post40 = stats.beta(1 + s40, 1 + f40)

    # 抽样
    samples30 = post30.rvs(N_SAMPLES)
    samples40 = post40.rvs(N_SAMPLES)

    # P(gate_30 > gate_40)
    prob = (samples30 > samples40).mean()

    # 期望提升
    lift = (samples30 - samples40).mean()
    lift_ci_low = np.percentile(samples30 - samples40, 2.5)
    lift_ci_high = np.percentile(samples30 - samples40, 97.5)

    print(f"\n=== {metric} ===")
    print(f"gate_30 posterior 均值: {post30.mean():.4f}")
    print(f"gate_40 posterior 均值: {post40.mean():.4f}")
    print(f"P(gate_30 > gate_40): {prob:.4f}")
    print(f"期望提升: {lift:.4f}  95% CI: [{lift_ci_low:.4f}, {lift_ci_high:.4f}]")

    # 可视化
    x = np.linspace(
        min(post30.ppf(0.001), post40.ppf(0.001)),
        max(post30.ppf(0.999), post40.ppf(0.999)),
        1000
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, post30.pdf(x), color="#4C72B0", label="gate_30")
    ax.plot(x, post40.pdf(x), color="#DD8452", label="gate_40")
    ax.fill_between(x, post30.pdf(x), alpha=0.2, color="#4C72B0")
    ax.fill_between(x, post40.pdf(x), alpha=0.2, color="#DD8452")
    ax.axvline(post30.mean(), color="#4C72B0", linestyle="--", alpha=0.7)
    ax.axvline(post40.mean(), color="#DD8452", linestyle="--", alpha=0.7)
    ax.set_title(f"{metric} — Posterior Distribution\nP(gate_30 > gate_40) = {prob:.4f}")
    ax.set_xlabel("retention rate")
    ax.set_ylabel("density")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"outputs/04_bayesian_{metric}.png", dpi=150)
    plt.show()
    print(f"图已保存：outputs/04_bayesian_{metric}.png")

bayesian_ab(df, "retention_1")
bayesian_ab(df, "retention_7")