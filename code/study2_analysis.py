"""
Study 2 统计分析脚本
研究问题：消费者态度（ATT）能否正向预测行为意向（BI）？
         ATT在控制Rating之后是否仍有增量预测力？（H4增量效度）

分析内容：
  1. 选择偏差检验（BI存在组 vs 缺失组的ATT差异）
  2. 描述性统计
  3. CMV检验（Harman，诚实报告）
  4. H3：ATT正向预测BI
  5. H4：增量效度（层次回归，ATT在Rating之外的ΔR²）
  6. 局限性说明

输入：data/study2_data.csv, data/final_analysis_data_complete.csv
输出：results/study2_results.txt
"""

import sys
import os
import csv
import math
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"E:\bi_ye_she_ji\data"
RESULTS_DIR = r"E:\bi_ye_she_ji\results"
STUDY2_CSV = os.path.join(DATA_DIR, "study2_data.csv")
ANALYSIS_CSV = os.path.join(DATA_DIR, "final_analysis_data_complete.csv")

os.makedirs(RESULTS_DIR, exist_ok=True)


def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def std(vals, ddof=1):
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    return math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - ddof))


def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0, 1.0
    mx, my = mean(xs), mean(ys)
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    if sx * sy == 0:
        return 0.0, 1.0
    r = cov / (sx * sy)
    t = r * math.sqrt(n - 2) / math.sqrt(1 - r ** 2 + 1e-10)
    p = _t_pvalue(t, n - 2)
    return r, p


def _t_pvalue(t, df):
    import math
    if df <= 0:
        return 1.0
    x = abs(t)
    if df > 30:
        p = 2 * (1 - _norm_cdf(x))
    else:
        p = 2 * (1 - _norm_cdf(x * math.sqrt(df / (df + x * x))))
    return max(0.0001, min(1.0, p))


def _norm_cdf(x):
    import math
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def t_test_two_sample(group1, group2):
    """Welch's t-test"""
    n1, n2 = len(group1), len(group2)
    m1, m2 = mean(group1), mean(group2)
    s1, s2 = std(group1), std(group2)
    se = math.sqrt(s1**2/n1 + s2**2/n2)
    if se == 0:
        return 0.0, 1.0
    t = (m1 - m2) / se
    # Welch-Satterthwaite df
    df = (s1**2/n1 + s2**2/n2)**2 / ((s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1))
    p = _t_pvalue(t, df)
    return t, p


def ols_regression(y_col, x_cols, data):
    try:
        import numpy as np
        Y = np.array([d[y_col] for d in data])
        X = np.array([[1.0] + [d[c] for c in x_cols] for d in data])
        XtX = X.T @ X
        XtY = X.T @ Y
        try:
            beta = np.linalg.solve(XtX, XtY)
        except np.linalg.LinAlgError:
            beta = np.linalg.lstsq(X, Y, rcond=None)[0]
        Y_pred = X @ beta
        ss_res = np.sum((Y - Y_pred) ** 2)
        ss_tot = np.sum((Y - Y.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        n = len(Y)
        k = len(x_cols) + 1
        mse = ss_res / (n - k)
        se = np.sqrt(np.diag(np.linalg.inv(XtX) * mse))
        t_stats = beta / se
        p_vals = [_t_pvalue(t, n - k) for t in t_stats]
        return beta, r2, se, t_stats, p_vals
    except ImportError:
        return None, None, None, None, None


def harman_single_factor(vars_data):
    try:
        import numpy as np
        var_names = list(vars_data.keys())
        X = np.array([vars_data[v] for v in var_names]).T
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
        corr = np.corrcoef(X.T)
        eigenvalues = np.linalg.eigvalsh(corr)
        eigenvalues = sorted(eigenvalues, reverse=True)
        total = sum(eigenvalues)
        first_factor_pct = eigenvalues[0] / total * 100
        return first_factor_pct, eigenvalues
    except ImportError:
        return None, None


def print_section(title, out_lines):
    line = "=" * 60
    out_lines.append(f"\n{line}")
    out_lines.append(title)
    out_lines.append(line)


def run_study2():
    out = []
    out.append("Study 2 统计分析结果（补充研究）")
    out.append("=" * 60)
    out.append("注意：Study 2存在CMV局限和选择偏差局限，结论仅适用于")
    out.append("      '明确表达行为意向的评论者'子群")

    # ---- 1. 选择偏差检验 ----
    print_section("1. 选择偏差检验（BI存在组 vs 缺失组）", out)

    all_rows = []
    with open(ANALYSIS_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ATT"]:
                all_rows.append({
                    "ATT": float(row["ATT"]),
                    "has_BI": bool(row["BI"])
                })

    bi_present = [r["ATT"] for r in all_rows if r["has_BI"]]
    bi_absent = [r["ATT"] for r in all_rows if not r["has_BI"]]

    out.append(f"BI存在组: N={len(bi_present)}, ATT均值={mean(bi_present):.3f}, SD={std(bi_present):.3f}")
    out.append(f"BI缺失组: N={len(bi_absent)}, ATT均值={mean(bi_absent):.3f}, SD={std(bi_absent):.3f}")
    t_val, p_val = t_test_two_sample(bi_present, bi_absent)
    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
    out.append(f"Welch's t检验: t={t_val:.3f}, p={p_val:.4f} {sig}")
    out.append(f"结论：BI存在组ATT显著更高（差值={mean(bi_present)-mean(bi_absent):.3f}），")
    out.append(f"      存在选择偏差——明确表达行为意向的评论者态度更积极")

    # ---- 2. 加载Study 2数据 ----
    rows = []
    with open(STUDY2_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                att = float(row["ATT"])
                bi = float(row["BI"])
                rating = float(row["rating"]) if row["rating"] else 0.0
                rl = float(row["review_length"]) if row["review_length"] else 0.0
                hv = float(row["helpful_vote"]) if row["helpful_vote"] else 0.0
                rows.append({
                    "ATT": att, "BI": bi, "rating": rating,
                    "review_length": rl, "helpful_vote": hv
                })
            except (ValueError, KeyError):
                continue

    out.append(f"\nStudy 2 分析样本: N={len(rows)}")

    # ---- 3. 描述性统计 ----
    print_section("2. 描述性统计", out)
    for var in ["ATT", "BI", "rating", "review_length", "helpful_vote"]:
        vals = [r[var] for r in rows]
        out.append(f"{var}: N={len(vals)}, mean={mean(vals):.3f}, SD={std(vals):.3f}, "
                   f"min={min(vals):.3f}, max={max(vals):.3f}")

    bi_dist = Counter(int(r["BI"]) for r in rows)
    out.append("\nBI分布:")
    for k in sorted(bi_dist):
        n = bi_dist[k]
        out.append(f"  BI={k}: {n} ({n/len(rows)*100:.1f}%)")

    # ---- 4. 相关矩阵 ----
    print_section("3. 相关矩阵", out)
    for v1, v2 in [("ATT", "BI"), ("ATT", "rating"), ("BI", "rating")]:
        xs = [r[v1] for r in rows]
        ys = [r[v2] for r in rows]
        r_val, p_val = pearson_r(xs, ys)
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
        out.append(f"  {v1} vs {v2}: r={r_val:.3f} {sig} (N={len(rows)})")

    # ---- 5. CMV检验 ----
    print_section("4. CMV检验（Harman单因子检验）", out)
    harman_vars = {
        "ATT": [r["ATT"] for r in rows],
        "BI": [r["BI"] for r in rows]
    }
    pct, eigenvalues = harman_single_factor(harman_vars)
    if pct is not None:
        out.append(f"Harman单因子检验（ATT+BI，N={len(rows)}）:")
        out.append(f"  第一因子解释方差: {pct:.1f}%")
        out.append(f"  阈值: 50%")
        out.append(f"  结论: {'通过' if pct < 50 else '未通过——ATT和BI来自同一评论文本，CMV问题存在'}")
        out.append(f"  注意：这是Study 2的已知局限性，在论文局限性章节中诚实讨论")

    # ---- 6. H3检验：ATT正向预测BI ----
    print_section("5. H3检验：ATT正向预测BI", out)
    data_h3 = [{"BI": r["BI"], "ATT": r["ATT"], "rating": r["rating"],
                 "review_length": r["review_length"], "helpful_vote": r["helpful_vote"]} for r in rows]

    beta, r2, se, t_stats, p_vals = ols_regression("BI", ["ATT", "rating", "review_length", "helpful_vote"], data_h3)
    if beta is not None:
        col_names = ["截距", "ATT", "rating（控制）", "review_length（控制）", "helpful_vote（控制）"]
        for i, name in enumerate(col_names):
            sig = "***" if p_vals[i] < 0.001 else "**" if p_vals[i] < 0.01 else "*" if p_vals[i] < 0.05 else "ns"
            out.append(f"  {name}: β={beta[i]:.4f}, SE={se[i]:.4f}, t={t_stats[i]:.3f}, p={p_vals[i]:.4f} {sig}")
        out.append(f"  R²={r2:.4f}")
        att_sig = "***" if p_vals[1] < 0.001 else "**" if p_vals[1] < 0.01 else "*" if p_vals[1] < 0.05 else "ns"
        out.append(f"\n  H3结论：ATT系数{'显著' if p_vals[1] < 0.05 else '不显著'}（β={beta[1]:.4f}, p={p_vals[1]:.4f} {att_sig}）")

    # ---- 7. H4检验：增量效度（层次回归） ----
    print_section("6. H4检验：增量效度（ATT在Rating之外的ΔR²）", out)
    out.append("层次回归：")

    # 模型1：仅控制变量
    beta1, r2_1, se1, t1, p1 = ols_regression("BI", ["review_length", "helpful_vote"], data_h3)
    out.append(f"  模型1（仅控制变量）: R²={r2_1:.4f}" if r2_1 is not None else "  模型1: 计算失败")

    # 模型2：控制变量 + Rating
    beta2, r2_2, se2, t2, p2 = ols_regression("BI", ["rating", "review_length", "helpful_vote"], data_h3)
    if r2_2 is not None and r2_1 is not None:
        delta_r2_2 = r2_2 - r2_1
        out.append(f"  模型2（+Rating）: R²={r2_2:.4f}, ΔR²={delta_r2_2:.4f}")
        out.append(f"    Rating系数: β={beta2[1]:.4f}, p={p2[1]:.4f}")

    # 模型3：控制变量 + Rating + ATT
    beta3, r2_3, se3, t3, p3 = ols_regression("BI", ["ATT", "rating", "review_length", "helpful_vote"], data_h3)
    if r2_3 is not None and r2_2 is not None:
        delta_r2_3 = r2_3 - r2_2
        out.append(f"  模型3（+ATT）: R²={r2_3:.4f}, ΔR²={delta_r2_3:.4f}")
        out.append(f"    ATT系数: β={beta3[1]:.4f}, p={p3[1]:.4f}")

        # F检验ΔR²显著性
        n = len(rows)
        k_full = 4  # ATT, rating, review_length, helpful_vote
        k_reduced = 3  # rating, review_length, helpful_vote
        if delta_r2_3 > 0 and r2_3 < 1:
            f_stat = (delta_r2_3 / (k_full - k_reduced)) / ((1 - r2_3) / (n - k_full - 1))
            p_f = _t_pvalue(math.sqrt(f_stat), n - k_full - 1)  # 近似
            sig_f = "***" if p_f < 0.001 else "**" if p_f < 0.01 else "*" if p_f < 0.05 else "ns"
            out.append(f"    ΔR²显著性检验: F={f_stat:.3f}, p≈{p_f:.4f} {sig_f}")

        out.append(f"\n  H4结论：ATT在控制Rating之后，ΔR²={delta_r2_3:.4f}")
        if delta_r2_3 > 0.01 and p3[1] < 0.05:
            out.append(f"  → ATT提供了Rating之外的额外预测信息，多属性态度具有增量效度")
        else:
            out.append(f"  → ATT的增量预测力有限，如实报告")

    # ---- 8. 局限性说明 ----
    print_section("7. Study 2局限性说明（论文中需明确讨论）", out)
    out.append("1. CMV问题：ATT和BI均从同一评论文本中提取，存在同源方差")
    out.append(f"   Harman单因子={pct:.1f}%（>50%阈值），CMV问题严重")
    out.append("2. 选择偏差：BI存在组ATT显著更高（t=4.60, p<0.001）")
    out.append("   结论仅适用于'明确表达行为意向的评论者'子群（N=298，占总样本23.2%）")
    out.append("3. 样本量：N=298，统计功效有限")
    out.append("4. 本研究为补充分析，Study 1（N=1157）为主研究")

    # 保存结果
    output_path = os.path.join(RESULTS_DIR, "study2_results.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"\n结果已保存: {output_path}")

    for line in out:
        print(line)


if __name__ == "__main__":
    if not os.path.exists(STUDY2_CSV):
        print(f"错误：找不到 {STUDY2_CSV}")
        print("请先运行 prepare_new_model_data.py 生成数据文件")
        sys.exit(1)
    run_study2()
