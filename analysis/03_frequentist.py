import pandas as pd
import numpy as np
from scipy import stats
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv("data/cookie_cats.csv")

def ztest_proportions(df, metric):
    g30 = df[df["version"] == "gate_30"][metric]
    g40 = df[df["version"] == "gate_40"][metric]

    n30, n40 = len(g30), len(g40)
    p30, p40 = g30.mean(), g40.mean()

    # Z-test
    p_pool = (g30.sum() + g40.sum()) / (n30 + n40)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n30 + 1/n40))
    z = (p30 - p40) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # 95% 置信区间（gate_30 - gate_40 的差值）
    diff = p30 - p40
    se_diff = np.sqrt(p30*(1-p30)/n30 + p40*(1-p40)/n40)
    ci_low = diff - 1.96 * se_diff
    ci_high = diff + 1.96 * se_diff

    print(f"\n=== {metric} ===")
    print(f"gate_30: {p30:.4f}  gate_40: {p40:.4f}")
    print(f"差值 (gate_30 - gate_40): {diff:.4f}")
    print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
    print(f"Z 统计量: {z:.4f}")
    print(f"p 值: {p_value:.4f}")
    if p_value < 0.05:
        print(f"✅  显著：gate_30 {'高于' if diff > 0 else '低于'} gate_40")
    else:
        print("—  不显著：两组无统计差异")

ztest_proportions(df, "retention_1")
ztest_proportions(df, "retention_7")