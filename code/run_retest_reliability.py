"""
重测信度检验脚本（使用阿里云百炼API）
对50条评论重新提取信念，计算e_i一致率、b_i ICC、ATT Pearson r

API: 阿里云百炼 (OpenAI兼容接口)
Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1
Model: qwen-plus
"""

import json
import sys
import os
import random
import csv
import math
import time
import re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"E:\bi_ye_she_ji\data"
RESULTS_DIR = r"E:\bi_ye_she_ji\results"
ANALYSIS_CSV = os.path.join(DATA_DIR, "final_analysis_data_complete.csv")
CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_reviews.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "reliability_retest_sample.csv")
OUTPUT_TXT = os.path.join(RESULTS_DIR, "retest_reliability_results.txt")

# ---- API配置 ----
API_KEY = "sk-87c58597f63d4001949476d28bc9c553"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-plus"
API_TIMEOUT = 60
API_DELAY = 0.5


def call_api(prompt: str, max_retries: int = 3) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a consumer psychology expert specializing in multi-attribute attitude theory."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                timeout=API_TIMEOUT
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 2
                print(f"  API失败（尝试{attempt+1}/{max_retries}），{wait}s后重试: {e}")
                time.sleep(wait)
            else:
                print(f"  API最终失败: {e}")
                raise
    return ""


def extract_beliefs(full_text: str):
    """提取信念和e_i（与原始提取逻辑一致）"""
    review_length = len(full_text)
    if review_length < 50:
        num_beliefs = "1"
    elif review_length < 500:
        num_beliefs = "1-3"
    else:
        num_beliefs = "3-5"

    prompt = f"""You are a consumer psychology expert specializing in multi-attribute attitude theory.

IMPORTANT CONSTRAINT: ONLY extract beliefs that are EXPLICITLY stated or clearly implied in the review text below. Do NOT infer, fabricate, or add beliefs that are not present in the original text.

Task: Extract user beliefs from the following review and score the emotional polarity (e_i) for each belief.

Extraction Strategy:
1. PRIORITY: Extract beliefs about specific product attributes (e.g., texture, efficacy, packaging, price, brand)
2. FALLBACK: If no clear attributes are expressed, extract overall evaluation beliefs and mark with "type": "general_belief"
3. Quantity: Extract approximately {num_beliefs} key belief(s) based on review length ({review_length} characters)
4. Score the emotional polarity for each belief:
   - +1: Clearly positive
   - 0: Neutral or mixed
   - -1: Clearly negative

Output Format: Strictly follow this JSON format (do not add any other text):
{{"beliefs": [{{"text": "belief1", "e_i": 1, "type": "attribute"}}, {{"text": "belief2", "e_i": -1, "type": "general_belief"}}]}}

Review:
{full_text}

Output JSON only, no other text."""

    try:
        response = call_api(prompt)
        json_match = re.search(r'\{[^{}]*"beliefs"[^{}]*\[.*?\]\s*\}', response, re.DOTALL)
        json_str = json_match.group(0) if json_match else response
        result = json.loads(json_str)
        beliefs = result.get("beliefs", [])
        valid = []
        for b in beliefs:
            if isinstance(b, dict) and "text" in b and "e_i" in b:
                if b["e_i"] in [-1, 0, 1]:
                    valid.append({"text": str(b["text"]).strip(), "e_i": int(b["e_i"])})
        return valid
    except Exception as e:
        print(f"  解析失败: {e}")
        return []


def assess_belief_strength(belief_text: str, review_context: str = "") -> float:
    """评估信念强度b_i（0.4-1.0）"""
    prompt = f"""Rate the certainty/strength of the following belief statement on a scale from 0.4 to 1.0.

Scoring criteria:
- 1.0: Absolutely certain ("absolutely love it", "definitely the best")
- 0.9: Very certain ("very good", "extremely effective", "highly recommend")
- 0.8: Fairly certain ("good", "works well", "nice")
- 0.7: Moderately certain ("seems good", "appears to work", "I think")
- 0.6: Somewhat uncertain ("might be", "could be", "not sure but")
- 0.5: Uncertain ("maybe", "possibly", "hard to tell")
- 0.4: Very uncertain ("not sure", "can't really tell")

Belief: {belief_text}
Review context: {review_context[:200] if review_context else ""}

Output ONLY a single number between 0.4 and 1.0, nothing else."""

    try:
        response = call_api(prompt)
        # 提取数字
        match = re.search(r'(0\.\d+|1\.0)', response.strip())
        if match:
            val = float(match.group(1))
            return max(0.4, min(1.0, val))
        return 0.7
    except Exception:
        return 0.7


def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    return cov / (sx * sy) if sx * sy > 0 else 0.0


def icc_two_way_mixed(orig, retest):
    """ICC(2,1) 双向混合模型（绝对一致性）"""
    n = len(orig)
    if n < 3:
        return 0.0
    grand_mean = (sum(orig) + sum(retest)) / (2 * n)
    # 行均值（每个评论的均值）
    row_means = [(orig[i] + retest[i]) / 2 for i in range(n)]
    # SS_between (subjects)
    ss_r = 2 * sum((m - grand_mean) ** 2 for m in row_means)
    # SS_within
    ss_w = sum((orig[i] - row_means[i]) ** 2 + (retest[i] - row_means[i]) ** 2 for i in range(n))
    # MS
    ms_r = ss_r / (n - 1)
    ms_w = ss_w / n  # df_within = n*(k-1) = n*1 = n for k=2
    # ICC(2,1) absolute agreement
    k = 2
    icc = (ms_r - ms_w) / (ms_r + (k - 1) * ms_w)
    return icc


def main():
    print("=" * 60)
    print("重测信度检验（阿里云百炼 qwen-plus）")
    print("=" * 60)

    # 读取原始评论文本
    review_texts = {}
    with open(CLEANED_CSV, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            review_texts[row["review_id"]] = row["full_text"]
    print(f"加载评论文本: {len(review_texts)} 条")

    # 读取原始提取结果
    valid_rows = []
    with open(ANALYSIS_CSV, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row.get("beliefs") and row.get("ATT") and row["review_id"] in review_texts:
                try:
                    beliefs = json.loads(row["beliefs"])
                    if beliefs and any(b.get("b_i") is not None for b in beliefs):
                        valid_rows.append(row)
                except Exception:
                    pass
    print(f"有效原始提取行: {len(valid_rows)} 条")

    random.seed(123)
    sample = random.sample(valid_rows, min(50, len(valid_rows)))
    print(f"抽取重测样本: {len(sample)} 条\n")

    results = []
    for i, row in enumerate(sample):
        rid = row["review_id"]
        full_text = review_texts[rid]
        att_original = float(row["ATT"])
        orig_beliefs = json.loads(row["beliefs"])

        print(f"[{i+1:2d}/{len(sample)}] {rid} (原ATT={att_original:.2f})", end=" ... ")

        try:
            # 重新提取信念
            new_beliefs_raw = extract_beliefs(full_text)
            time.sleep(API_DELAY)

            if not new_beliefs_raw:
                print("跳过（无信念）")
                continue

            # 重新评估信念强度
            new_att = 0.0
            new_beliefs_full = []
            for b in new_beliefs_raw:
                b_i_new = assess_belief_strength(b["text"], full_text)
                time.sleep(API_DELAY)
                att_component = b_i_new * b["e_i"]
                new_att += att_component
                new_beliefs_full.append({
                    "belief_text": b["text"],
                    "e_i_new": b["e_i"],
                    "b_i_new": b_i_new
                })

            orig_e_i_list = [b.get("e_i") for b in orig_beliefs if b.get("e_i") is not None]
            orig_b_i_list = [float(b.get("b_i", 0.7)) for b in orig_beliefs if b.get("b_i") is not None]
            new_e_i_list = [b["e_i_new"] for b in new_beliefs_full]
            new_b_i_list = [b["b_i_new"] for b in new_beliefs_full]

            results.append({
                "review_id": rid,
                "att_original": att_original,
                "att_retest": new_att,
                "n_beliefs_original": len(orig_beliefs),
                "n_beliefs_retest": len(new_beliefs_full),
                "orig_e_i": json.dumps(orig_e_i_list),
                "new_e_i": json.dumps(new_e_i_list),
                "orig_b_i": json.dumps(orig_b_i_list),
                "new_b_i": json.dumps(new_b_i_list),
            })
            print(f"重测ATT={new_att:.2f}")

        except Exception as e:
            print(f"错误: {e}")
            continue

    if not results:
        print("无有效重测结果，退出")
        return

    n = len(results)
    print(f"\n成功重测: {n} 条")

    # ---- ATT重测信度（Pearson r）----
    atts_orig = [r["att_original"] for r in results]
    atts_new = [r["att_retest"] for r in results]
    r_att = pearson_r(atts_orig, atts_new)
    print(f"\nATT重测信度（Pearson r）: {r_att:.3f}（N={n}）")
    print(f"结论: {'通过 (r>0.90)' if r_att > 0.90 else '未通过 (r≤0.90)'}")

    # ---- e_i一致率 ----
    # 对每条评论，比较原始和重测的e_i列表（按位置匹配，取最短长度）
    ei_match = 0
    ei_total = 0
    for r in results:
        orig_ei = json.loads(r["orig_e_i"])
        new_ei = json.loads(r["new_e_i"])
        min_len = min(len(orig_ei), len(new_ei))
        for j in range(min_len):
            ei_total += 1
            if orig_ei[j] == new_ei[j]:
                ei_match += 1
    ei_rate = ei_match / ei_total if ei_total > 0 else 0.0
    print(f"\ne_i一致率: {ei_match}/{ei_total} = {ei_rate*100:.1f}%")
    print(f"结论: {'通过 (>90%)' if ei_rate > 0.90 else '未通过 (≤90%)'}")

    # ---- b_i ICC ----
    # 对每条评论，取原始和重测的b_i均值（评论级别）
    b_orig_means = []
    b_new_means = []
    for r in results:
        orig_bi = json.loads(r["orig_b_i"])
        new_bi = json.loads(r["new_b_i"])
        if orig_bi and new_bi:
            b_orig_means.append(sum(orig_bi) / len(orig_bi))
            b_new_means.append(sum(new_bi) / len(new_bi))
    icc_val = icc_two_way_mixed(b_orig_means, b_new_means) if len(b_orig_means) >= 3 else 0.0
    print(f"\nb_i ICC（评论级均值，N={len(b_orig_means)}）: {icc_val:.3f}")
    print(f"结论: {'通过 (ICC>0.70)' if icc_val > 0.70 else '未通过 (ICC≤0.70)'}")

    # ---- 保存CSV ----
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\n重测数据已保存: {OUTPUT_CSV}")

    # ---- 保存结果文本 ----
    os.makedirs(RESULTS_DIR, exist_ok=True)
    lines = [
        "重测信度检验结果",
        "=" * 60,
        f"重测样本量: N={n}",
        f"API: 阿里云百炼 qwen-plus",
        "",
        f"ATT重测信度（Pearson r）: {r_att:.3f}",
        f"  阈值: r>0.90",
        f"  结论: {'通过' if r_att > 0.90 else '未通过'}",
        "",
        f"e_i一致率: {ei_match}/{ei_total} = {ei_rate*100:.1f}%",
        f"  阈值: >90%",
        f"  结论: {'通过' if ei_rate > 0.90 else '未通过'}",
        "",
        f"b_i ICC（评论级均值）: {icc_val:.3f}",
        f"  阈值: ICC>0.70",
        f"  结论: {'通过' if icc_val > 0.70 else '未通过'}",
    ]
    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"结果已保存: {OUTPUT_TXT}")


if __name__ == "__main__":
    main()
