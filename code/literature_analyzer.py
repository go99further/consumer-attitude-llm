#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献分析器 - 提取并分析参考文献年份
从bi_ye_lun_wen.txt中提取参考文献，识别旧文献，生成待替换清单
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

# 高引经典文献白名单（保留这些文献，即使年份较旧）
CLASSIC_WHITELIST = [
    "Fishbein",
    "Ajzen, I. (1991)",
    "Mudambi & Schuff (2010)",
    "Campbell & Fiske (1959)",
    "Fornell & Larcker (1981)",
    "Harman (1976)",
    "Podsakoff"
]

def extract_references(thesis_file):
    """从论文中提取参考文献列表"""
    print(f"正在读取论文文件: {thesis_file}")

    with open(thesis_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到参考文献章节
    ref_start = content.find("十、参考文献")
    ref_end = content.find("十一、附录")

    if ref_start == -1:
        print("❌ 未找到参考文献章节")
        return []

    ref_section = content[ref_start:ref_end if ref_end != -1 else None]

    # 提取每条文献（格式：[数字] 文献内容）
    pattern = r'\[(\d+)\]\s+(.+?)(?=\n\[|\n\n|$)'
    matches = re.findall(pattern, ref_section, re.DOTALL)

    references = []
    for ref_id, ref_text in matches:
        ref_text = ref_text.strip()
        references.append({
            'id': int(ref_id),
            'text': ref_text,
            'original_text': f"[{ref_id}] {ref_text}"
        })

    print(f"✓ 提取到 {len(references)} 条参考文献")
    return references

def extract_year(ref_text):
    """从文献文本中提取年份"""
    # 匹配各种年份格式
    patterns = [
        r'\((\d{4})\)',      # (2024)
        r'\[(\d{4})\]',      # [2024]
        r'\.?\s*(\d{4})\.',  # . 2024.
        r',\s*(\d{4})',      # , 2024
    ]

    for pattern in patterns:
        match = re.search(pattern, ref_text)
        if match:
            year = int(match.group(1))
            # 合理性检查（1950-2026）
            if 1950 <= year <= 2026:
                return year

    return None

def is_classic(ref_text):
    """判断是否为高引经典文献"""
    for classic in CLASSIC_WHITELIST:
        if classic in ref_text:
            return True
    return False

def analyze_references(references):
    """分析文献年份分布"""
    print("\n开始分析文献年份...")

    current_year = 2026
    recent_threshold = current_year - 5  # 2022-2026为近五年

    analysis = {
        'total': len(references),
        'with_year': 0,
        'without_year': 0,
        'recent_5years': 0,  # 2022-2026
        'old': 0,            # 2021及以前
        'classic': 0,        # 高引经典
        'to_replace': [],    # 待替换文献
        'year_distribution': {},
        'references_detail': []
    }

    for ref in references:
        year = extract_year(ref['text'])
        is_classic_lit = is_classic(ref['text'])

        ref_detail = {
            'id': ref['id'],
            'text': ref['text'],
            'year': year,
            'is_classic': is_classic_lit,
            'is_recent': False,
            'should_replace': False
        }

        if year:
            analysis['with_year'] += 1

            # 年份分布统计
            if year not in analysis['year_distribution']:
                analysis['year_distribution'][year] = 0
            analysis['year_distribution'][year] += 1

            # 近五年判断
            if year >= recent_threshold:
                analysis['recent_5years'] += 1
                ref_detail['is_recent'] = True
            else:
                analysis['old'] += 1

                # 判断是否需要替换
                if is_classic_lit:
                    analysis['classic'] += 1
                    ref_detail['should_replace'] = False
                else:
                    ref_detail['should_replace'] = True
                    analysis['to_replace'].append({
                        'id': ref['id'],
                        'text': ref['text'],
                        'year': year,
                        'reason': f'年份过旧（{year}），非高引经典'
                    })
        else:
            analysis['without_year'] += 1
            print(f"⚠ 文献[{ref['id']}]未识别到年份: {ref['text'][:80]}...")

        analysis['references_detail'].append(ref_detail)

    return analysis

def generate_report(analysis, output_file):
    """生成分析报告"""
    print("\n生成分析报告...")

    report = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'summary': {
            'total_references': analysis['total'],
            'with_year': analysis['with_year'],
            'without_year': analysis['without_year'],
            'recent_5years_count': analysis['recent_5years'],
            'recent_5years_percentage': round(analysis['recent_5years'] / analysis['total'] * 100, 2),
            'old_count': analysis['old'],
            'classic_count': analysis['classic'],
            'to_replace_count': len(analysis['to_replace']),
            'target_recent_percentage': 60.0,
            'gap_to_target': round(60.0 - (analysis['recent_5years'] / analysis['total'] * 100), 2)
        },
        'year_distribution': dict(sorted(analysis['year_distribution'].items())),
        'to_replace': analysis['to_replace'],
        'all_references': analysis['references_detail']
    }

    # 保存JSON报告
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✓ 报告已保存: {output_file}")

    # 打印摘要
    print("\n" + "="*60)
    print("文献分析摘要")
    print("="*60)
    print(f"总文献数: {analysis['total']}")
    print(f"识别到年份: {analysis['with_year']}")
    print(f"未识别年份: {analysis['without_year']}")
    print(f"\n近五年文献(2022-2026): {analysis['recent_5years']} ({report['summary']['recent_5years_percentage']}%)")
    print(f"旧文献(≤2021): {analysis['old']}")
    print(f"  - 其中高引经典(保留): {analysis['classic']}")
    print(f"  - 待替换: {len(analysis['to_replace'])}")
    print(f"\n目标: 近五年文献占比≥60%")
    print(f"当前差距: {report['summary']['gap_to_target']}%")
    print(f"需要替换: 至少 {len(analysis['to_replace'])} 篇旧文献")
    print("="*60)

    # 打印年份分布
    print("\n年份分布:")
    for year in sorted(report['year_distribution'].keys(), reverse=True):
        count = report['year_distribution'][year]
        bar = "█" * count
        marker = " ← 近五年" if year >= 2022 else ""
        print(f"  {year}: {bar} ({count}){marker}")

    # 打印待替换文献清单
    if report['to_replace']:
        print(f"\n待替换文献清单 (共{len(report['to_replace'])}篇):")
        for item in report['to_replace'][:10]:  # 只显示前10篇
            print(f"  [{item['id']}] ({item['year']}) {item['text'][:60]}...")
        if len(report['to_replace']) > 10:
            print(f"  ... 还有 {len(report['to_replace']) - 10} 篇（详见JSON报告）")

    return report

def main():
    """主函数"""
    print("="*60)
    print("文献分析器 v1.0")
    print("="*60)

    # 文件路径
    base_dir = Path(__file__).parent.parent
    thesis_file = base_dir / "bi_ye_lun_wen.txt"
    output_file = base_dir / "data" / "literature_analysis.json"

    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 提取文献
    references = extract_references(thesis_file)

    if not references:
        print("❌ 未提取到任何文献，程序退出")
        return

    # 分析文献
    analysis = analyze_references(references)

    # 生成报告
    report = generate_report(analysis, output_file)

    print(f"\n✓ 文献分析完成！")
    print(f"详细报告: {output_file}")

if __name__ == "__main__":
    main()
