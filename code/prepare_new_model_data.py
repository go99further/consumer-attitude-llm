"""
数据合并脚本
功能：合并所有数据源，输出study1_data.csv和study2_data.csv
输入：
  - data/final_analysis_data_complete.csv（ATT/BI/PV/Rating/beliefs）
  - data/reviews_B004EDYQX6.jsonl（user_id, helpful_vote, timestamp）
  - data/reviewer_experience.csv（user_id, review_count, experience_level）
输出：
  - data/study1_data.csv（N=ATT+Rating完整，含reviewer_experience）
  - data/study2_data.csv（N=ATT+BI完整）
"""

import json
import sys
import os
import csv
import math
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"E:\bi_ye_she_ji\data"
ANALYSIS_CSV = os.path.join(DATA_DIR, "final_analysis_data_complete.csv")
REVIEWS_JSONL = os.path.join(DATA_DIR, "reviews_B004EDYQX6.jsonl")
REVIEWER_EXP_CSV = os.path.join(DATA_DIR, "reviewer_experience.csv")
CLEANED_CSV = os.path.join(DATA_DIR, "cleaned_reviews.csv")
STUDY1_OUTPUT = os.path.join(DATA_DIR, "study1_data.csv")
STUDY2_OUTPUT = os.path.join(DATA_DIR, "study2_data.csv")


def load_reviews_metadata():
    """
    从reviews_B004EDYQX6.jsonl加载user_id, helpful_vote, timestamp
    jsonl中没有review_id字段，按行顺序生成R0001, R0002...与cleaned_reviews.csv对应
    """
    meta = {}
    with open(REVIEWS_JSONL, encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                rid = f"R{idx+1:04d}"
                uid = r.get("user_id", "")
                helpful = r.get("helpful_vote", 0) or 0
                ts = r.get("timestamp", 0) or 0
                meta[rid] = {
                    "user_id": uid,
                    "helpful_vote": int(helpful),
                    "timestamp": int(ts),
                    "verified_purchase": str(r.get("verified_purchase", "False")).lower() == "true"
                }
            except Exception:
                continue
    print(f"加载评论元数据: {len(meta)} 条")
    return meta


def load_reviewer_experience():
    """加载reviewer_experience.csv"""
    if not os.path.exists(REVIEWER_EXP_CSV):
        print(f"警告：reviewer_experience.csv不存在，请先运行compute_reviewer_experience.py")
        return {}
    exp = {}
    with open(REVIEWER_EXP_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp[row["user_id"]] = {
                "review_count": int(row["review_count"]),
                "experience_level": row["experience_level"]
            }
    print(f"加载评论者经验数据: {len(exp)} 条")
    return exp


def load_cleaned_reviews():
    """加载cleaned_reviews.csv，获取review_id到full_text的映射"""
    rid_to_meta = {}
    with open(CLEANED_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid_to_meta[row["review_id"]] = row
    print(f"加载清洗评论: {len(rid_to_meta)} 条")
    return rid_to_meta


def compute_review_length(text):
    """计算评论长度（字符数）"""
    return len(text) if text else 0


def merge_data():
    """合并所有数据源"""
    print("=" * 60)
    print("合并数据源")
    print("=" * 60)

    # 加载各数据源
    reviews_meta = load_reviews_metadata()
    reviewer_exp = load_reviewer_experience()
    cleaned = load_cleaned_reviews()

    # 读取主分析数据
    merged_rows = []
    with open(ANALYSIS_CSV, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid = row["review_id"]
            cleaned_row = cleaned.get(rid, {})
            full_text = cleaned_row.get("full_text", "")

            # 从jsonl按review_id顺序获取元数据
            meta = reviews_meta.get(rid, {})
            uid = meta.get("user_id", "")
            helpful_vote = meta.get("helpful_vote", 0)
            timestamp = meta.get("timestamp", 0)
            verified_purchase = meta.get("verified_purchase", False)

            review_count = 0
            experience_level = "unknown"
            if uid and uid in reviewer_exp:
                review_count = reviewer_exp[uid]["review_count"]
                experience_level = reviewer_exp[uid]["experience_level"]

            review_length = compute_review_length(full_text)

            # 时间戳转换为年份（用于控制变量）
            review_year = 0
            if timestamp > 0:
                try:
                    review_year = datetime.fromtimestamp(timestamp / 1000).year
                except Exception:
                    review_year = 0

            merged_rows.append({
                "review_id": rid,
                "ATT": row["ATT"],
                "BI": row["BI"],
                "PV": row["PV"],
                "rating": row["rating"],
                "user_id": uid,
                "helpful_vote": helpful_vote,
                "timestamp": timestamp,
                "review_year": review_year,
                "verified_purchase": 1 if verified_purchase else 0,
                "review_length": review_length,
                "reviewer_experience": review_count,
                "experience_level": experience_level,
            })

    print(f"合并完成: {len(merged_rows)} 行")
    return merged_rows


def save_study_datasets(merged_rows):
    """输出study1_data.csv和study2_data.csv"""

    # Study 1: ATT + Rating完整（reviewer_experience可能缺失，用0填充）
    study1_fields = [
        "review_id", "ATT", "rating", "reviewer_experience", "experience_level",
        "review_length", "helpful_vote", "review_year", "verified_purchase", "user_id"
    ]
    study1_rows = [r for r in merged_rows if r["ATT"] and r["rating"]]
    print(f"\nStudy 1 样本量: {len(study1_rows)}")

    # 检查reviewer_experience缺失情况
    exp_missing = sum(1 for r in study1_rows if r["reviewer_experience"] == 0 and r["experience_level"] == "unknown")
    print(f"  reviewer_experience缺失（未在全品类数据中找到）: {exp_missing} ({exp_missing/len(study1_rows)*100:.1f}%)")

    with open(STUDY1_OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=study1_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(study1_rows)
    print(f"  输出: {STUDY1_OUTPUT}")

    # Study 2: ATT + BI完整
    study2_fields = [
        "review_id", "ATT", "BI", "rating",
        "review_length", "helpful_vote", "review_year", "verified_purchase", "user_id"
    ]
    study2_rows = [r for r in merged_rows if r["ATT"] and r["BI"]]
    print(f"\nStudy 2 样本量: {len(study2_rows)}")

    with open(STUDY2_OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=study2_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(study2_rows)
    print(f"  输出: {STUDY2_OUTPUT}")

    # 计算reviewer_experience与review_length、helpful_vote的相关性（辅助效度证据）
    print("\n--- reviewer_experience辅助效度检验 ---")
    s1_with_exp = [r for r in study1_rows if r["reviewer_experience"] > 0]
    if len(s1_with_exp) > 10:
        _print_correlation(s1_with_exp, "reviewer_experience", "review_length")
        _print_correlation(s1_with_exp, "reviewer_experience", "helpful_vote")
    else:
        print("  reviewer_experience数据不足，跳过相关性检验")


def _print_correlation(rows, var1, var2):
    """计算并打印两个变量的Pearson相关系数"""
    pairs = [(float(r[var1]), float(r[var2])) for r in rows
             if r[var1] not in ("", None) and r[var2] not in ("", None)]
    if len(pairs) < 3:
        return
    n = len(pairs)
    m1 = sum(p[0] for p in pairs) / n
    m2 = sum(p[1] for p in pairs) / n
    cov = sum((p[0] - m1) * (p[1] - m2) for p in pairs) / n
    s1 = math.sqrt(sum((p[0] - m1) ** 2 for p in pairs) / n)
    s2 = math.sqrt(sum((p[1] - m2) ** 2 for p in pairs) / n)
    r = cov / (s1 * s2) if s1 * s2 > 0 else 0.0
    print(f"  {var1} vs {var2}: r={r:.3f} (N={n})")


if __name__ == "__main__":
    merged = merge_data()
    save_study_datasets(merged)
