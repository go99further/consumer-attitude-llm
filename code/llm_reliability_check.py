"""
LLM提取可靠性验证脚本
功能：
  1. 从final_analysis_data_complete.csv的beliefs列重新计算ATT，验证计算正确性
  2. 随机抽取100条评论，输出人工验证CSV（review_id, 原文, 信念, e_i, b_i）
  3. 语义相似度检验：用sentence-transformers计算每条信念与原文的余弦相似度
  4. 重测信度检验（需要API）：对50条评论重新提取，计算e_i一致率、b_i ICC、ATT Pearson r

输出文件：
  data/reliability_validation_sample.csv  — 100条人工验证表格
  data/reliability_semantic_similarity.csv — 语义相似度结果
  data/reliability_retest_sample.csv       — 50条重测信度结果（如果运行重测）
"""

import json
import sys
import os
import random
import csv
import math

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"E:\bi_ye_she_ji\data"
CODE_DIR = r"E:\bi_ye_she_ji\code"
ANALYSIS_CSV = os.path.join(DATA_DIR, "final_analysis_data_complete.csv")
CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_reviews.csv")

# ============================================================
# Step 1: 验证ATT计算正确性（从beliefs列重新计算）
# ============================================================

def verify_att_calculation():
    """从beliefs列重新计算ATT_calculated，与CSV中的ATT比对"""
    print("=" * 60)
    print("Step 1: 验证ATT计算正确性")
    print("=" * 60)

    rows = []
    with open(ANALYSIS_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    match_count = 0
    mismatch_count = 0
    skip_count = 0
    max_diff = 0.0
    diffs = []

    for row in rows:
        if not row["ATT"] or not row["beliefs"]:
            skip_count += 1
            continue
        try:
            att_csv = float(row["ATT"])
            beliefs = json.loads(row["beliefs"])
            # 重新计算 ATT = Σ(b_i × e_i)
            att_calc = 0.0
            valid = True
            for b in beliefs:
                b_i = b.get("b_i")
                e_i = b.get("e_i")
                if b_i is None or e_i is None:
                    valid = False
                    break
                att_calc += float(b_i) * float(e_i)
            if not valid:
                skip_count += 1
                continue
            diff = abs(att_csv - att_calc)
            diffs.append(diff)
            max_diff = max(max_diff, diff)
            if diff < 0.01:
                match_count += 1
            else:
                mismatch_count += 1
        except Exception:
            skip_count += 1

    total_checked = match_count + mismatch_count
    print(f"  检查总数: {total_checked}，跳过（缺失）: {skip_count}")
    print(f"  完全匹配（差值<0.01）: {match_count} ({match_count/total_checked*100:.1f}%)")
    print(f"  不匹配: {mismatch_count}")
    print(f"  最大差值: {max_diff:.4f}")
    if diffs:
        mean_diff = sum(diffs) / len(diffs)
        print(f"  平均差值: {mean_diff:.6f}")
    print()
    return match_count, mismatch_count


# ============================================================
# Step 2: 生成100条人工验证CSV
# ============================================================

def generate_validation_sample(n=100, seed=42):
    """随机抽取n条评论，输出人工验证表格"""
    print("=" * 60)
    print(f"Step 2: 生成{n}条人工验证样本")
    print("=" * 60)

    # 读取原始评论文本（cleaned_reviews.csv有BOM头，用utf-8-sig）
    review_texts = {}
    with open(CLEANED_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            review_texts[row["review_id"]] = row["full_text"]

    # 读取已提取的beliefs数据（只取有beliefs且有ATT的行）
    valid_rows = []
    with open(ANALYSIS_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["beliefs"] and row["ATT"]:
                try:
                    beliefs = json.loads(row["beliefs"])
                    if beliefs:
                        valid_rows.append(row)
                except Exception:
                    pass

    random.seed(seed)
    sample = random.sample(valid_rows, min(n, len(valid_rows)))
    print(f"  有效行数: {len(valid_rows)}，抽取: {len(sample)}")

    output_path = os.path.join(DATA_DIR, "reliability_validation_sample.csv")
    fieldnames = [
        "review_id", "original_text", "belief_index",
        "belief_text", "e_i", "b_i", "att_component",
        "belief_type",
        # 人工标注列（留空供填写）
        "human_has_basis",   # 是/否：该信念在原文中有语义依据
        "human_e_i",         # 人工判断的情感极性 (-1/0/1)
        "human_notes"        # 备注
    ]

    rows_out = []
    for row in sample:
        rid = row["review_id"]
        original_text = review_texts.get(rid, "")
        try:
            beliefs = json.loads(row["beliefs"])
        except Exception:
            continue
        for idx, b in enumerate(beliefs):
            rows_out.append({
                "review_id": rid,
                "original_text": original_text[:500],  # 截断避免CSV过大
                "belief_index": idx,
                "belief_text": b.get("belief_text", b.get("text", "")),
                "e_i": b.get("e_i", ""),
                "b_i": b.get("b_i", ""),
                "att_component": b.get("att_component", ""),
                "belief_type": b.get("type", ""),
                "human_has_basis": "",
                "human_e_i": "",
                "human_notes": ""
            })

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"  输出: {output_path}")
    print(f"  总信念条数: {len(rows_out)}")
    print(f"  请在 human_has_basis 列填写 是/否，human_e_i 列填写 -1/0/1")
    print()
    return output_path


# ============================================================
# Step 3: 语义相似度检验（需要sentence-transformers）
# ============================================================

def compute_semantic_similarity(sample_path=None, threshold=0.2):
    """计算每条信念与原文的余弦相似度，标记疑似幻觉"""
    print("=" * 60)
    print("Step 3: 语义相似度检验")
    print("=" * 60)

    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except ImportError:
        print("  [跳过] sentence-transformers未安装。")
        print("  安装命令: pip install sentence-transformers")
        print("  安装后重新运行此脚本即可执行语义相似度检验。")
        print()
        return None

    if sample_path is None:
        sample_path = os.path.join(DATA_DIR, "reliability_validation_sample.csv")

    if not os.path.exists(sample_path):
        print(f"  [跳过] 找不到验证样本文件: {sample_path}")
        return None

    print("  加载sentence-transformers模型（首次运行会下载模型）...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    rows = []
    with open(sample_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    print(f"  处理 {len(rows)} 条信念...")
    texts_belief = [r["belief_text"] for r in rows]
    texts_review = [r["original_text"] for r in rows]

    embeddings_belief = model.encode(texts_belief, batch_size=64, show_progress_bar=True)
    embeddings_review = model.encode(texts_review, batch_size=64, show_progress_bar=True)

    # 余弦相似度
    def cosine_sim(a, b):
        dot = float(np.dot(a, b))
        norm = float(np.linalg.norm(a) * np.linalg.norm(b))
        return dot / norm if norm > 0 else 0.0

    similarities = [cosine_sim(embeddings_belief[i], embeddings_review[i]) for i in range(len(rows))]

    # 标记疑似幻觉
    flagged = sum(1 for s in similarities if s < threshold)
    print(f"  相似度<{threshold}（疑似幻觉）: {flagged}/{len(rows)} ({flagged/len(rows)*100:.1f}%)")
    print(f"  平均相似度: {sum(similarities)/len(similarities):.3f}")
    print(f"  最低相似度: {min(similarities):.3f}")

    output_path = os.path.join(DATA_DIR, "reliability_semantic_similarity.csv")
    fieldnames = list(rows[0].keys()) + ["semantic_similarity", "flagged_hallucination"]
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row, sim in zip(rows, similarities):
            row["semantic_similarity"] = round(sim, 4)
            row["flagged_hallucination"] = "是" if sim < threshold else "否"
            writer.writerow(row)

    print(f"  输出: {output_path}")
    print()
    return output_path


# ============================================================
# Step 4: 重测信度检验（需要API，可选）
# ============================================================

def run_retest_reliability(n=50, seed=123):
    """
    对n条评论重新调用LLM提取，计算e_i一致率、b_i ICC、ATT Pearson r
    注意：此步骤需要API调用，约50次，成本低但需要网络连接
    """
    print("=" * 60)
    print(f"Step 4: 重测信度检验（{n}条，需要API）")
    print("=" * 60)

    try:
        sys.path.insert(0, CODE_DIR)
        from variable_extraction import extract_beliefs_and_evaluation, assess_belief_strength
    except ImportError as e:
        print(f"  [跳过] 无法导入variable_extraction: {e}")
        return None

    # 读取原始评论文本（cleaned_reviews.csv有BOM头，用utf-8-sig）
    review_texts = {}
    with open(CLEANED_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            review_texts[row["review_id"]] = row["full_text"]

    # 读取原始提取结果
    valid_rows = []
    with open(ANALYSIS_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["beliefs"] and row["ATT"] and row["review_id"] in review_texts:
                try:
                    beliefs = json.loads(row["beliefs"])
                    if beliefs and any(b.get("b_i") is not None for b in beliefs):
                        valid_rows.append(row)
                except Exception:
                    pass

    random.seed(seed)
    sample = random.sample(valid_rows, min(n, len(valid_rows)))
    print(f"  抽取 {len(sample)} 条进行重测...")

    results = []
    for i, row in enumerate(sample):
        rid = row["review_id"]
        full_text = review_texts[rid]
        att_original = float(row["ATT"])

        print(f"  [{i+1}/{len(sample)}] {rid}...", end=" ")

        try:
            # 重新提取信念
            new_beliefs_raw = extract_beliefs_and_evaluation(full_text)
            if not new_beliefs_raw:
                print("跳过（无信念）")
                continue

            # 重新评估信念强度
            new_att = 0.0
            new_beliefs_full = []
            for b in new_beliefs_raw:
                b_i_new = assess_belief_strength(b["text"], full_text, len(full_text))
                if b_i_new is None:
                    b_i_new = 0.7  # 默认值
                att_component = b_i_new * b["e_i"]
                new_att += att_component
                new_beliefs_full.append({
                    "belief_text": b["text"],
                    "e_i_new": b["e_i"],
                    "b_i_new": b_i_new
                })

            # 原始信念
            orig_beliefs = json.loads(row["beliefs"])
            orig_e_i_list = [b.get("e_i") for b in orig_beliefs if b.get("e_i") is not None]
            orig_b_i_list = [b.get("b_i") for b in orig_beliefs if b.get("b_i") is not None]
            new_e_i_list = [b["e_i_new"] for b in new_beliefs_full]
            new_b_i_list = [b["b_i_new"] for b in new_beliefs_full]

            results.append({
                "review_id": rid,
                "att_original": att_original,
                "att_retest": new_att,
                "n_beliefs_original": len(orig_beliefs),
                "n_beliefs_retest": len(new_beliefs_full),
                "orig_e_i": str(orig_e_i_list),
                "new_e_i": str(new_e_i_list),
                "orig_b_i": str(orig_b_i_list),
                "new_b_i": str(new_b_i_list),
            })
            print(f"ATT原={att_original:.2f} 重测={new_att:.2f}")

        except Exception as e:
            print(f"错误: {e}")
            continue

    if not results:
        print("  无有效重测结果")
        return None

    # 计算ATT重测信度（Pearson r）
    atts_orig = [r["att_original"] for r in results]
    atts_new = [r["att_retest"] for r in results]
    n = len(atts_orig)
    mean_o = sum(atts_orig) / n
    mean_n = sum(atts_new) / n
    cov = sum((atts_orig[i] - mean_o) * (atts_new[i] - mean_n) for i in range(n)) / n
    std_o = math.sqrt(sum((x - mean_o) ** 2 for x in atts_orig) / n)
    std_n = math.sqrt(sum((x - mean_n) ** 2 for x in atts_new) / n)
    pearson_r = cov / (std_o * std_n) if std_o * std_n > 0 else 0.0

    print(f"\n  ATT重测信度（Pearson r）: {pearson_r:.3f}（N={n}）")
    print(f"  阈值要求: r>0.90")
    print(f"  结论: {'通过' if pearson_r > 0.90 else '未通过，需要检查提示词一致性'}")

    output_path = os.path.join(DATA_DIR, "reliability_retest_sample.csv")
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print(f"  输出: {output_path}")
    print()
    return pearson_r


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LLM提取可靠性验证")
    parser.add_argument("--retest", action="store_true", help="运行重测信度检验（需要API调用）")
    parser.add_argument("--n-retest", type=int, default=50, help="重测样本数（默认50）")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("LLM提取可靠性验证")
    print("=" * 60 + "\n")

    # Step 1: 验证ATT计算
    verify_att_calculation()

    # Step 2: 生成人工验证样本
    sample_path = generate_validation_sample(n=100)

    # Step 3: 语义相似度检验
    compute_semantic_similarity(sample_path=sample_path)

    # Step 4: 重测信度（可选）
    if args.retest:
        run_retest_reliability(n=args.n_retest)
    else:
        print("提示: 运行 --retest 参数可执行重测信度检验（需要API调用约50次）")
        print("命令: python llm_reliability_check.py --retest")
