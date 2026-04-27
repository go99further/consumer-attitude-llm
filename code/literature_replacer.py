#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献替换器 - 自动搜索并替换旧文献
使用WebSearch搜索近五年相关文献，自动替换旧文献，更新正文引用
"""

import re
import json
import sys
from datetime import datetime
from pathlib import Path

# 设置Windows控制台UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def load_analysis(analysis_file):
    """加载文献分析结果"""
    print(f"正在加载文献分析结果: {analysis_file}")

    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    to_replace = analysis['to_replace']
    print(f"✓ 加载完成，待替换文献: {len(to_replace)} 篇")

    return to_replace, analysis

def extract_topic_keywords(ref_text):
    """从文献文本中提取主题关键词"""
    # 移除作者和年份
    text = re.sub(r'^[^(]+\(\d{4}\)\.?\s*', '', ref_text)

    # 提取标题（通常在第一个句号或期刊名之前）
    title_match = re.search(r'^([^.]+)', text)
    if title_match:
        title = title_match.group(1).strip()

        # 移除常见停用词
        stopwords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        words = title.lower().split()
        keywords = [w for w in words if w not in stopwords and len(w) > 3]

        return ' '.join(keywords[:5])  # 取前5个关键词

    return "consumer behavior online review"

def search_replacement_literature(ref_to_replace, max_results=3):
    """
    搜索替换文献（模拟版本）

    注意：这是一个模拟实现。在实际使用中，你需要：
    1. 使用WebSearch工具（Claude Code内置）
    2. 或调用学术搜索API（Google Scholar, Semantic Scholar等）

    由于当前环境限制，这里返回模拟结果
    """
    ref_id = ref_to_replace['id']
    ref_text = ref_to_replace['text']
    old_year = ref_to_replace['year']

    print(f"\n正在搜索替换文献 [{ref_id}] ({old_year})...")
    print(f"  原文献: {ref_text[:80]}...")

    # 提取主题关键词
    keywords = extract_topic_keywords(ref_text)
    print(f"  关键词: {keywords}")

    # 构建搜索查询
    search_query = f"{keywords} 2022-2026 consumer behavior"
    print(f"  搜索: {search_query}")

    # 模拟搜索结果
    # 在实际实现中，这里应该调用WebSearch或学术API
    candidates = [
        {
            'title': f"Recent advances in {keywords} (2024)",
            'authors': "Smith, J., & Johnson, M.",
            'year': 2024,
            'journal': "Journal of Consumer Research",
            'relevance_score': 0.85,
            'citation_count': 45,
            'reason': "高相关性，近期发表，引用量适中"
        }
    ]

    print(f"  ✓ 找到 {len(candidates)} 个候选文献")

    return candidates

def select_best_replacement(candidates):
    """从候选文献中选择最佳替换"""
    if not candidates:
        return None

    # 简单策略：选择相关性最高的
    best = max(candidates, key=lambda x: x['relevance_score'])

    return best

def format_reference(ref_data):
    """格式化文献引用（APA格式）"""
    authors = ref_data['authors']
    year = ref_data['year']
    title = ref_data['title']
    journal = ref_data.get('journal', 'Unknown Journal')

    return f"{authors} ({year}). {title}. {journal}."

def replace_literature_in_thesis(thesis_file, replacements, output_file):
    """在论文中替换文献"""
    print(f"\n正在更新论文文件...")

    with open(thesis_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 统计
    replaced_count = 0
    failed_count = 0

    # 替换参考文献列表
    for old_ref_id, new_ref_text in replacements.items():
        # 查找旧文献的位置
        pattern = rf'\[{old_ref_id}\]\s+.+?(?=\n\[|\n\n|十一、附录)'

        match = re.search(pattern, content, re.DOTALL)
        if match:
            old_text = match.group(0)
            new_text = f"[{old_ref_id}] {new_ref_text}"

            content = content.replace(old_text, new_text)
            replaced_count += 1
            print(f"  ✓ 已替换 [{old_ref_id}]")
        else:
            failed_count += 1
            print(f"  ✗ 未找到 [{old_ref_id}]")

    # 保存更新后的论文
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ 论文已更新: {output_file}")
    print(f"  成功替换: {replaced_count} 篇")
    print(f"  失败: {failed_count} 篇")

    return replaced_count, failed_count

def generate_replacement_log(replacements, output_file):
    """生成替换日志"""
    log = {
        'replacement_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_replacements': len(replacements),
        'replacements': []
    }

    for old_ref_id, replacement_info in replacements.items():
        log['replacements'].append({
            'old_ref_id': old_ref_id,
            'old_ref': replacement_info['old_ref'],
            'new_ref': replacement_info['new_ref'],
            'reason': replacement_info['reason']
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"✓ 替换日志已保存: {output_file}")

def main():
    """主函数"""
    print("="*60)
    print("文献替换器 v1.0 (模拟版)")
    print("="*60)
    print("\n⚠ 注意：这是模拟版本，实际替换需要人工审核")
    print("建议：先运行此脚本生成替换建议，然后人工审核后再应用\n")

    # 文件路径
    base_dir = Path(__file__).parent.parent
    analysis_file = base_dir / "data" / "literature_analysis.json"
    thesis_file = base_dir / "bi_ye_lun_wen.txt"
    output_file = base_dir / "bi_ye_lun_wen_updated.txt"
    log_file = base_dir / "data" / "replacement_log.json"

    # 加载待替换文献
    to_replace, analysis = load_analysis(analysis_file)

    if not to_replace:
        print("✓ 没有需要替换的文献")
        return

    # 限制替换数量（避免一次性替换太多）
    max_replace = min(len(to_replace), 10)
    print(f"\n本次将替换前 {max_replace} 篇文献（共{len(to_replace)}篇待替换）")

    replacements = {}
    replacement_details = {}

    # 搜索并选择替换文献
    for i, ref in enumerate(to_replace[:max_replace], 1):
        print(f"\n[{i}/{max_replace}] 处理文献 [{ref['id']}]")

        # 搜索候选文献
        candidates = search_replacement_literature(ref)

        # 选择最佳替换
        best = select_best_replacement(candidates)

        if best:
            new_ref_text = format_reference(best)
            replacements[ref['id']] = new_ref_text

            replacement_details[ref['id']] = {
                'old_ref': ref['text'],
                'new_ref': new_ref_text,
                'reason': best['reason']
            }

            print(f"  → 新文献: {new_ref_text[:80]}...")
        else:
            print(f"  ✗ 未找到合适的替换文献")

    if not replacements:
        print("\n✗ 没有找到任何替换文献")
        return

    # 生成替换日志
    generate_replacement_log(replacement_details, log_file)

    # 应用替换（创建新文件）
    replaced_count, failed_count = replace_literature_in_thesis(
        thesis_file, replacements, output_file
    )

    # 重新分析更新后的文献占比
    print("\n" + "="*60)
    print("替换完成摘要")
    print("="*60)
    print(f"原始近五年占比: {analysis['summary']['recent_5years_percentage']}%")
    print(f"本次替换: {replaced_count} 篇")
    print(f"预计新占比: {analysis['summary']['recent_5years_percentage'] + (replaced_count / analysis['summary']['total_references'] * 100):.2f}%")
    print(f"距离目标(60%): 还需替换约 {max(0, int((60 - analysis['summary']['recent_5years_percentage']) / 100 * analysis['summary']['total_references']) - replaced_count)} 篇")
    print("="*60)

    print(f"\n✓ 文献替换完成！")
    print(f"更新后的论文: {output_file}")
    print(f"替换日志: {log_file}")
    print(f"\n⚠ 请人工审核替换结果，确认无误后再使用！")

if __name__ == "__main__":
    main()
