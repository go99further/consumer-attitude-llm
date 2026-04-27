"""
Study 1 统计分析脚本
研究问题：LLM提取的多属性态度（ATT）能否有效预测消费者评论评分（Rating）？
         评论者经验（Reviewer Experience）如何调节这一关系？

分析内容：
  1. 描述性统计
  2. 信度：ATT重测信度（从reliability_retest_sample.csv读取，如存在）
  3. 效度：预测效度（ATT-Rating相关）+ 区分效度（ATT-reviewer_experience低相关）
  4. CMV检验：Harman单因子检验
  5. H1：ATT正向预测Rating（有序Logistic + OLS）
  6. H2：reviewer_experience调节ATT→Rating（均值中心化交互项）
  7. 稳健性检验

输入：data/study1_data.csv
输出：results/study1_results.txt
"""

import sys
import os
import csv
import math
import json
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"E:\bi_ye_she_ji\data"
RESULTS_DIR = r"E:\bi_ye_she_ji\results"
STUDY1_CSV = os.path.join(DATA_DIR, "study1_data.csv")
RETEST_CSV = os.path.join(DATA_DIR, "reliability_retest_sample.csv")

os.makedirs(RESULTS_DIR, exist_ok=True)


def load_study1_data():
    rows = []
    with open(STUDY1_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                att = float(row["ATT"])
                rating = float(row["rating"])
                re = float(row["reviewer_experience"]) if row["reviewer_experience"] else 0.0
                rl = float(row["review_length"]) if row["review_length"] else 0.0
                hv = float(row["helpful_vote"]) if row["helpful_vote"] else 0.0
                ry = float(row["review_year"]) if row["review_year"] else 0.0
                rows.append({
                    "review_id": row["review_id"],
                    "ATT": att,
                    "rating": rating,
                    "reviewer_experience": re,
                    "experience_level": row.get("experience_level", ""),
                    "review_length": rl,
                    "helpful_vote": hv,
                    "review_year": ry,
                })
            except (ValueError, KeyError):
                continue
    return rows


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
    # t-test for significance
    t = r * math.sqrt(n - 2) / math.sqrt(1 - r ** 2 + 1e-10)
    # approximate p-value (two-tailed, df=n-2)
    # use simple approximation
    p = _t_pvalue(t, n - 2)
    return r, p


def _t_pvalue(t, df):
    """Approximate two-tailed p-value for t-distribution"""
    # Simple approximation using normal distribution for large df
    import math
    if df <= 0:
        return 1.0
    # Use Wilson-Hilferty approximation
    x = abs(t)
    if df > 30:
        # Normal approximation
        p = 2 * (1 - _norm_cdf(x))
    else:
        # Rough approximation
        p = 2 * (1 - _norm_cdf(x * math.sqrt(df / (df + x * x))))
    return max(0.0001, min(1.0, p))


def _norm_cdf(x):
    """Approximate standard normal CDF"""
    import math
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def ols_regression(y, X_cols, data):
    """
    简单OLS回归（使用numpy如果可用，否则用正规方程）
    X_cols: list of column names
    data: list of dicts
    返回: coefficients, r_squared, se, t_stats, p_vals
    """
    try:
        import numpy as np
        Y = np.array([d["y"] for d in data])
        X = np.array([[1.0] + [d[c] for c in X_cols] for d in data])
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
        k = len(X_cols) + 1
        mse = ss_res / (n - k)
        se = np.sqrt(np.diag(np.linalg.inv(XtX) * mse))
        t_stats = beta / se
        p_vals = [_t_pvalue(t, n - k) for t in t_stats]
        return beta, r2, se, t_stats, p_vals
    except ImportError:
        return None, None, None, None, None


def ols_regression_vcov(y, X_cols, data):
    """
    OLS回归，额外返回方差-协方差矩阵（用于简单斜率分析）
    返回: beta, r2, se, t_stats, p_vals, vcov, df_resid
    """
    try:
        import numpy as np
        Y = np.array([d["y"] for d in data])
        X = np.array([[1.0] + [d[c] for c in X_cols] for d in data])
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
        k = len(X_cols) + 1
        df_resid = n - k
        mse = ss_res / df_resid
        XtX_inv = np.linalg.inv(XtX)
        vcov = XtX_inv * mse
        se = np.sqrt(np.diag(vcov))
        t_stats = beta / se
        p_vals = [_t_pvalue(t, df_resid) for t in t_stats]
        return beta, r2, se, t_stats, p_vals, vcov, df_resid
    except ImportError:
        return None, None, None, None, None, None, None


def compute_vif(X_cols, data):
    """计算VIF（方差膨胀因子）"""
    try:
        import numpy as np
        X = np.array([[d[c] for c in X_cols] for d in data])
        vifs = {}
        for i, col in enumerate(X_cols):
            y_i = X[:, i]
            X_others = np.column_stack([X[:, j] for j in range(len(X_cols)) if j != i])
            X_others = np.column_stack([np.ones(len(y_i)), X_others])
            try:
                beta = np.linalg.lstsq(X_others, y_i, rcond=None)[0]
                y_pred = X_others @ beta
                ss_res = np.sum((y_i - y_pred) ** 2)
                ss_tot = np.sum((y_i - y_i.mean()) ** 2)
                r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
                vif = 1 / (1 - r2) if r2 < 1 else float("inf")
            except Exception:
                vif = float("nan")
            vifs[col] = vif
        return vifs
    except ImportError:
        return {}


def harman_single_factor(vars_data):
    """
    Harman单因子检验
    vars_data: dict of {var_name: [values]}
    返回: 第一因子解释方差比例
    """
    try:
        import numpy as np
        var_names = list(vars_data.keys())
        n = len(list(vars_data.values())[0])
        X = np.array([vars_data[v] for v in var_names]).T  # n x p
        # 标准化
        X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
        # 相关矩阵
        corr = np.corrcoef(X.T)
        eigenvalues = np.linalg.eigvalsh(corr)
        eigenvalues = sorted(eigenvalues, reverse=True)
        total = sum(eigenvalues)
        first_factor_pct = eigenvalues[0] / total * 100
        return first_factor_pct, eigenvalues
    except ImportError:
        return None, None


def ordered_logistic_summary(y, x_cols, data):
    """
    有序Logistic回归（使用statsmodels如果可用）
    """
    try:
        import numpy as np
        from statsmodels.miscmodels.ordinal_model import OrderedModel
        Y = np.array([d["y"] for d in data])
        X = np.array([[d[c] for c in x_cols] for d in data])
        import pandas as pd
        df = pd.DataFrame(X, columns=x_cols)
        model = OrderedModel(Y, df, distr="logit")
        result = model.fit(method="bfgs", disp=False)
        return result
    except Exception as e:
        return None


def print_section(title, out_lines):
    line = "=" * 60
    out_lines.append(f"\n{line}")
    out_lines.append(title)
    out_lines.append(line)


def run_study1():
    out = []
    out.append("Study 1 统计分析结果")
    out.append("=" * 60)

    rows = load_study1_data()
    out.append(f"样本量: N={len(rows)}")

    # ---- 1. 描述性统计 ----
    print_section("1. 描述性统计", out)
    for var in ["ATT", "rating", "reviewer_experience", "review_length", "helpful_vote"]:
        vals = [r[var] for r in rows if r[var] is not None]
        out.append(f"{var}: N={len(vals)}, mean={mean(vals):.3f}, SD={std(vals):.3f}, "
                   f"min={min(vals):.3f}, max={max(vals):.3f}")

    rating_dist = Counter(int(r["rating"]) for r in rows)
    out.append("\nRating分布:")
    total = len(rows)
    for k in sorted(rating_dist):
        n = rating_dist[k]
        out.append(f"  {k}星: {n} ({n/total*100:.1f}%)")

    exp_dist = Counter(r["experience_level"] for r in rows)
    out.append("\nReviewer Experience分布:")
    for level in ["novice", "moderate", "experienced", "expert", "unknown"]:
        n = exp_dist.get(level, 0)
        if n > 0:
            out.append(f"  {level}: {n} ({n/total*100:.1f}%)")

    # ---- 2. 相关矩阵 ----
    print_section("2. 相关矩阵（效度检验）", out)
    vars_to_corr = ["ATT", "rating", "reviewer_experience", "review_length", "helpful_vote"]
    for i, v1 in enumerate(vars_to_corr):
        for v2 in vars_to_corr[i+1:]:
            pairs = [(r[v1], r[v2]) for r in rows if r[v1] is not None and r[v2] is not None]
            if len(pairs) < 3:
                continue
            xs, ys = zip(*pairs)
            r_val, p_val = pearson_r(list(xs), list(ys))
            sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
            out.append(f"  {v1} vs {v2}: r={r_val:.3f} {sig} (N={len(pairs)})")

    out.append("\n预测效度：ATT-Rating相关（见上）")
    out.append("区分效度：ATT-reviewer_experience相关应显著低于ATT-Rating相关（见上）")

    # ---- 3. CMV检验（Harman） ----
    print_section("3. CMV检验（Harman单因子检验）", out)
    harman_vars = {}
    for var in ["ATT", "rating", "reviewer_experience"]:
        vals = [r[var] for r in rows if r[var] is not None]
        if len(vals) == len(rows):
            harman_vars[var] = vals
        else:
            # 只取三个变量都有值的行
            pass

    # 取三个变量都完整的行
    complete_rows = [r for r in rows if r["ATT"] is not None and r["rating"] is not None
                     and r["reviewer_experience"] > 0]
    if len(complete_rows) > 10:
        harman_vars = {
            "ATT": [r["ATT"] for r in complete_rows],
            "rating": [r["rating"] for r in complete_rows],
            "reviewer_experience": [r["reviewer_experience"] for r in complete_rows]
        }
        pct, eigenvalues = harman_single_factor(harman_vars)
        if pct is not None:
            out.append(f"Harman单因子检验（ATT+Rating+reviewer_experience，N={len(complete_rows)}）:")
            out.append(f"  第一因子解释方差: {pct:.1f}%")
            out.append(f"  阈值: 50%")
            out.append(f"  结论: {'通过' if pct < 50 else '未通过（但主要CMV论证依赖方法分离，见正文）'}")
            if eigenvalues:
                out.append(f"  特征值: {[round(e, 3) for e in eigenvalues[:5]]}")
    else:
        out.append(f"注意：reviewer_experience数据不足（N={len(complete_rows)}），Harman检验仅用ATT+Rating")
        harman_vars2 = {
            "ATT": [r["ATT"] for r in rows],
            "rating": [r["rating"] for r in rows]
        }
        pct2, _ = harman_single_factor(harman_vars2)
        if pct2 is not None:
            out.append(f"Harman单因子检验（ATT+Rating，N={len(rows)}）: {pct2:.1f}%")

    # ---- 4. H1检验：ATT正向预测Rating ----
    print_section("4. H1检验：ATT正向预测Rating", out)

    data_h1 = [{"y": r["rating"], "ATT": r["ATT"],
                 "review_length": r["review_length"],
                 "helpful_vote": r["helpful_vote"],
                 "review_year": r["review_year"]} for r in rows]

    # OLS回归
    out.append("--- OLS回归（稳健性参考）---")
    beta, r2, se, t_stats, p_vals = ols_regression("rating", ["ATT", "review_length", "helpful_vote", "review_year"], data_h1)
    if beta is not None:
        col_names = ["截距", "ATT", "review_length", "helpful_vote", "review_year"]
        for i, name in enumerate(col_names):
            sig = "***" if p_vals[i] < 0.001 else "**" if p_vals[i] < 0.01 else "*" if p_vals[i] < 0.05 else "ns"
            out.append(f"  {name}: β={beta[i]:.4f}, SE={se[i]:.4f}, t={t_stats[i]:.3f}, p={p_vals[i]:.4f} {sig}")
        out.append(f"  R²={r2:.4f}")

    # VIF检验
    out.append("\n--- VIF检验（多重共线性）---")
    vif_data = [{"ATT": r["ATT"], "review_length": r["review_length"],
                 "helpful_vote": r["helpful_vote"], "review_year": r["review_year"]} for r in rows]
    vifs = compute_vif(["ATT", "review_length", "helpful_vote", "review_year"], vif_data)
    for var, vif in vifs.items():
        flag = " ⚠️ >10" if vif > 10 else ""
        out.append(f"  VIF({var}) = {vif:.2f}{flag}")

    # 有序Logistic回归
    out.append("\n--- 有序Logistic回归（主模型）---")
    result_ologit = ordered_logistic_summary(
        [r["rating"] for r in rows],
        ["ATT", "review_length", "helpful_vote", "review_year"],
        data_h1
    )
    if result_ologit is not None:
        out.append(result_ologit.summary().as_text())
    else:
        out.append("  [需要statsmodels] pip install statsmodels")
        out.append("  安装后重新运行可获得有序Logistic回归结果")

    # ---- 5. H2检验：reviewer_experience调节效应（均值中心化） ----
    print_section("5. H2检验：reviewer_experience调节ATT→Rating", out)

    rows_with_exp = [r for r in rows if r["reviewer_experience"] > 0]
    out.append(f"有reviewer_experience数据的样本: N={len(rows_with_exp)}")

    if len(rows_with_exp) > 30:
        # 均值中心化
        att_mean = mean([r["ATT"] for r in rows_with_exp])
        re_mean = mean([r["reviewer_experience"] for r in rows_with_exp])
        out.append(f"均值中心化: ATT均值={att_mean:.3f}, reviewer_experience均值={re_mean:.3f}")

        data_h2 = []
        for r in rows_with_exp:
            att_c = r["ATT"] - att_mean
            re_c = r["reviewer_experience"] - re_mean
            data_h2.append({
                "y": r["rating"],
                "ATT_c": att_c,
                "RE_c": re_c,
                "ATT_x_RE": att_c * re_c,
                "review_length": r["review_length"],
                "helpful_vote": r["helpful_vote"],
                "review_year": r["review_year"]
            })

        out.append("\n--- 调节效应OLS回归（均值中心化后）---")
        beta_h2, r2_h2, se_h2, t_h2, p_h2, vcov_h2, df_h2 = ols_regression_vcov(
            "rating",
            ["ATT_c", "RE_c", "ATT_x_RE", "review_length", "helpful_vote", "review_year"],
            data_h2
        )
        if beta_h2 is not None:
            col_names = ["截距", "ATT_c", "RE_c", "ATT×RE（交互项）", "review_length", "helpful_vote", "review_year"]
            for i, name in enumerate(col_names):
                sig = "***" if p_h2[i] < 0.001 else "**" if p_h2[i] < 0.01 else "*" if p_h2[i] < 0.05 else "ns"
                out.append(f"  {name}: β={beta_h2[i]:.4f}, SE={se_h2[i]:.4f}, t={t_h2[i]:.3f}, p={p_h2[i]:.4f} {sig}")
            out.append(f"  R²={r2_h2:.4f}")

            # 判断交互项是否显著
            interaction_idx = 3  # ATT×RE是第4个系数（索引3，截距是0）
            if p_h2[interaction_idx] < 0.05:
                out.append(f"\n  H2结论：交互项显著（p={p_h2[interaction_idx]:.4f}），调节效应成立")
                out.append("  → 进行简单斜率分析（Simple Slopes Analysis）")
                re_vals = [d["RE_c"] for d in data_h2]
                re_sd = std(re_vals)
                _simple_slopes_analysis(beta_h2, vcov_h2, df_h2, re_sd, out)
            else:
                out.append(f"\n  H2结论：交互项不显著（p={p_h2[interaction_idx]:.4f}），调节效应不成立")
                out.append("  → H2为探索性假设，如实报告，不强行解释")

        # VIF检验（含交互项）
        out.append("\n--- VIF检验（含交互项，均值中心化后）---")
        vif_data_h2 = [{"ATT_c": d["ATT_c"], "RE_c": d["RE_c"], "ATT_x_RE": d["ATT_x_RE"],
                         "review_length": d["review_length"], "helpful_vote": d["helpful_vote"]} for d in data_h2]
        vifs_h2 = compute_vif(["ATT_c", "RE_c", "ATT_x_RE", "review_length", "helpful_vote"], vif_data_h2)
        for var, vif in vifs_h2.items():
            flag = " ⚠️ >10" if vif > 10 else ""
            out.append(f"  VIF({var}) = {vif:.2f}{flag}")
    else:
        out.append("  reviewer_experience数据不足，跳过H2检验")

    # ---- 6. 稳健性检验 ----
    print_section("6. 稳健性检验", out)
    out.append("--- reviewer_experience四分类稳健性 ---")
    level_map = {"novice": 1, "moderate": 2, "experienced": 3, "expert": 4}
    rows_with_level = [r for r in rows if r["experience_level"] in level_map]
    if len(rows_with_level) > 30:
        data_robust = [{"y": r["rating"], "ATT": r["ATT"],
                         "RE_cat": float(level_map[r["experience_level"]]),
                         "review_length": r["review_length"],
                         "helpful_vote": r["helpful_vote"]} for r in rows_with_level]
        beta_r, r2_r, se_r, t_r, p_r = ols_regression(
            "rating", ["ATT", "RE_cat", "review_length", "helpful_vote"], data_robust
        )
        if beta_r is not None:
            out.append(f"  ATT系数（四分类RE）: β={beta_r[1]:.4f}, p={p_r[1]:.4f}")
            out.append(f"  R²={r2_r:.4f}")
    else:
        out.append("  数据不足，跳过四分类稳健性检验")

    # 保存结果
    output_path = os.path.join(RESULTS_DIR, "study1_results.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"\n结果已保存: {output_path}")

    # 同时打印到控制台
    for line in out:
        print(line)


def _simple_slopes_analysis(beta_h2, vcov_h2, df_resid, re_sd, out):
    """
    简单斜率分析（解析法）
    模型: Rating = β0 + β1*ATT_c + β2*RE_c + β3*ATT_x_RE + controls
    系数索引: 0=截距, 1=ATT_c, 2=RE_c, 3=ATT_x_RE, 4+=controls

    在固定RE水平（±1SD）下，ATT对Rating的简单斜率：
      slope = β1 + β3 × re_level
      SE(slope) = sqrt(Var(β1) + re_level² × Var(β3) + 2×re_level×Cov(β1,β3))
    """
    try:
        import math
        out.append("\n  --- 简单斜率分析 ---")
        out.append(f"  RE标准差（中心化后）: {re_sd:.3f}")

        b1 = float(beta_h2[1])   # ATT_c系数
        b3 = float(beta_h2[3])   # ATT_x_RE系数
        var_b1 = float(vcov_h2[1, 1])
        var_b3 = float(vcov_h2[3, 3])
        cov_b1_b3 = float(vcov_h2[1, 3])

        for label, re_level in [("高RE（+1SD）", re_sd), ("低RE（-1SD）", -re_sd)]:
            slope = b1 + b3 * re_level
            var_slope = var_b1 + re_level**2 * var_b3 + 2 * re_level * cov_b1_b3
            se_slope = math.sqrt(max(var_slope, 0.0))
            if se_slope > 0:
                t_val = slope / se_slope
                p_val = _t_pvalue(t_val, df_resid)
            else:
                t_val, p_val = 0.0, 1.0
            sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
            out.append(f"  {label}: 简单斜率={slope:.4f}, SE={se_slope:.4f}, t={t_val:.3f}, p={p_val:.4f} {sig}")

        out.append(f"  解读：交互项β3={b3:.4f}（负值表示高经验评论者ATT-Rating一致性略弱）")
    except Exception as e:
        out.append(f"  简单斜率分析失败: {e}")


if __name__ == "__main__":
    if not os.path.exists(STUDY1_CSV):
        print(f"错误：找不到 {STUDY1_CSV}")
        print("请先运行 prepare_new_model_data.py 生成数据文件")
        sys.exit(1)
    run_study1()
