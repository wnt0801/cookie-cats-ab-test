# Cookie Cats A/B Test Analysis

Mobile game retention experiment analysis using Frequentist and Bayesian frameworks.

## 项目背景

Cookie Cats 是一款移动消除游戏。本实验测试将强制等待关卡从第 30 关移至第 40 关（gate_30 vs gate_40）对用户留存的影响。数据来源：[Kaggle - Mobile Games A/B Testing](https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing)

- 样本量：90,189 名用户
- 核心指标：次日留存（retention_1）、7日留存（retention_7）

## 分析流程

| 模块 | 文件 | 内容 |
|---|---|---|
| 01 | `analysis/01_eda.py` | 数据探索、分布可视化、指标均值对比 |
| 02 | `analysis/02_srm_check.py` | Sample Ratio Mismatch 检验 |
| 03 | `analysis/03_frequentist.py` | Z-test + 95% 置信区间 |
| 04 | `analysis/04_bayesian.py` | Bayesian Beta-Binomial 模型 |
| 05 | `analysis/05_business_summary.py` | ROI 换算 + 业务建议 |

## 核心结论

**建议保留 gate_30，不上线 gate_40。**

| 指标 | gate_30 | gate_40 | P(gate_30 > gate_40) |
|---|---|---|---|
| retention_1 | 44.82% | 44.23% | 96.3% |
| retention_7 | 19.02% | 18.20% | **99.9%** |

- 7日留存差值 0.82%，按 DAU 100万估算，gate_40 每天减少约 **8,200 名长期活跃用户**
- 频率派与 Bayesian 结论一致，两项指标信号均指向 gate_30 更优
- SRM 检验偏差 0.87%，大样本敏感性问题，工程上可接受

## 方法说明

**为什么同时使用两种框架？**

频率派（Z-test）给出 p 值，是工业界标准基线；Bayesian 框架输出"gate_30 更好的概率"，对业务方更直观。retention_1 在频率派下不显著（p=0.074），但 Bayesian 显示 96.3% 概率 gate_30 更优——两种框架的差异本身就是分析洞察。

## 技术栈

- Python 3.13
- pandas / numpy / scipy
- matplotlib / seaborn
- Bayesian 建模：scipy.stats.beta（Beta-Binomial 解析解）

## 复现步骤

```bash
git clone https://github.com/wnt0801/cookie-cats-ab-test.git
cd cookie-cats-ab-test
pip install -r requirements.txt
python analysis/01_eda.py
python analysis/02_srm_check.py
python analysis/03_frequentist.py
python analysis/04_bayesian.py
python analysis/05_business_summary.py
```

输出图表保存至 `outputs/` 目录。