"""
计算评论者经验（Reviewer Experience）
功能：逐行扫描Beauty_and_Personal_Care.jsonl（11GB），统计每个user_id的评论总数
输出：data/reviewer_experience.csv（user_id, review_count, experience_level）
"""

import json
import sys
import os
import csv
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = r"E:\bi_ye_she_ji\data"
FULL_DATASET = r"E:\bi_ye_she_ji\Beauty_and_Personal_Care.jsonl"
TARGET_REVIEWS = os.path.join(DATA_DIR, "reviews_B004EDYQX6.jsonl")
OUTPUT_PATH = os.path.join(DATA_DIR, "reviewer_experience.csv")


def get_target_user_ids():
    """获取目标产品评论中的所有user_id"""
    user_ids = set()
    with open(TARGET_REVIEWS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                review = json.loads(line)
                uid = review.get("user_id")
                if uid:
                    user_ids.add(uid)
            except json.JSONDecodeError:
                continue
    print(f"目标产品评论中的独立用户数: {len(user_ids)}")
    return user_ids


def compute_reviewer_experience(target_user_ids):
    """
    逐行扫描全品类数据，统计每个目标用户的评论总数
    使用逐行读取，不加载全部数据到内存
    """
    counts = {uid: 0 for uid in target_user_ids}
    total_lines = 0
    matched_lines = 0
    start_time = time.time()
    last_report = start_time

    print(f"开始扫描: {FULL_DATASET}")
    print("（11GB文件，预计2-5分钟）")

    with open(FULL_DATASET, encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                review = json.loads(line)
                uid = review.get("user_id")
                if uid and uid in counts:
                    counts[uid] += 1
                    matched_lines += 1
            except json.JSONDecodeError:
                continue

            # 每100万行报告一次进度
            if total_lines % 1_000_000 == 0:
                elapsed = time.time() - start_time
                print(f"  已处理 {total_lines:,} 行，匹配 {matched_lines:,} 条，耗时 {elapsed:.1f}s")

    elapsed = time.time() - start_time
    print(f"扫描完成: {total_lines:,} 行，匹配 {matched_lines:,} 条，耗时 {elapsed:.1f}s")
    return counts


def classify_experience(count):
    """将评论数量分为四个经验等级"""
    if count == 1:
        return "novice"       # 新手：仅1条评论
    elif count <= 5:
        return "moderate"     # 普通：2-5条
    elif count <= 20:
        return "experienced"  # 资深：6-20条
    else:
        return "expert"       # 专家：21+条


def save_results(counts):
    """保存结果到CSV"""
    rows = []
    for uid, count in counts.items():
        rows.append({
            "user_id": uid,
            "review_count": count,
            "experience_level": classify_experience(count)
        })

    # 按review_count降序排列
    rows.sort(key=lambda x: x["review_count"], reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "review_count", "experience_level"])
        writer.writeheader()
        writer.writerows(rows)

    # 统计分布
    from collections import Counter
    level_counts = Counter(r["experience_level"] for r in rows)
    total = len(rows)
    print(f"\n输出: {OUTPUT_PATH}")
    print(f"总用户数: {total}")
    print("经验等级分布:")
    for level in ["novice", "moderate", "experienced", "expert"]:
        n = level_counts.get(level, 0)
        print(f"  {level}: {n} ({n/total*100:.1f}%)")
    print(f"最大评论数: {max(r['review_count'] for r in rows)}")
    print(f"平均评论数: {sum(r['review_count'] for r in rows)/total:.1f}")
    print(f"中位数评论数: {sorted(r['review_count'] for r in rows)[total//2]}")

    return rows


if __name__ == "__main__":
    print("=" * 60)
    print("计算评论者经验（Reviewer Experience）")
    print("=" * 60)

    # 检查文件是否存在
    if not os.path.exists(FULL_DATASET):
        print(f"错误：找不到全品类数据文件: {FULL_DATASET}")
        sys.exit(1)

    # 获取目标用户ID
    target_user_ids = get_target_user_ids()

    # 扫描全品类数据
    counts = compute_reviewer_experience(target_user_ids)

    # 保存结果
    save_results(counts)
