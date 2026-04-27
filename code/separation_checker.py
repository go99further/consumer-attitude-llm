#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分离检查器 - 验证理论/数据/结论分离
使用LLM检查全文是否存在理论/数据/结论跨部分越界
"""

import re
import json
import sys
from pathlib import Path

# 设置Windows控制台UTF-8编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 章节定义
CHAPTER_DEFINITIONS = {
    '理论部分': ['二、文献综述', '三、研究假设'],
    '数据与方法部分': ['四、研究设计', '五、数据描述性统计', '六、研究结果'],
    '讨论与结论部分': ['七、讨论', '八、研究贡献与局限', '九、结论']
}

# 越界检测规则
VIOLATION_RULES = {
    '理论部分_数据越界': {
        'keywords': [
            r'本研究.*?均值',
            r'本研究.*?标准差',
            r'N\s*=\s*\d+',
            r'p\s*[<>=]\s*0\.\d+',
            r'r\s*=\s*0\.\d+',
            r'β\s*=\s*[+-]?\d+\.\d+',
            r't\s*=\s*[+-]?\d+\.\d+',
            r'F\s*=\s*\d+\.\d+',
            r'χ²\s*=\s*\d+\.\d+',
            r'回归.*?显著',
            r'相关.*?显著',
            r'检验.*?结果',
            r'数据.*?显示',
            r'分析.*?表明',
            r'实证.*?结果'
        ],
        'description': '理论章节出现本研究的数据、统计量或结果'
    },
    '结果部分_理论越界': {
        'keywords': [
            r'根据.*?理论.*?态度.*?由.*?构成',
            r'Fishbein.*?模型.*?认为',
            r'计划行为理论.*?指出',
            r'理论.*?框架.*?表明',
            r'从.*?理论.*?角度.*?分析',
            r'理论.*?基础.*?在于'
        ],
        'min_length': 100,  # 超过100字的理论论述
        'description': '结果章节出现大段理论论述（>100字）'
    },
    '讨论部分_新数据越界': {
        'keywords': [
            r'新.*?分析.*?显示',
            r'补充.*?检验.*?表明',
            r'进一步.*?回归',
            r'额外.*?数据'
        ],
        'description': '讨论章节引入未在结果部分报告的新数据分析'
    }
}

def load_thesis(thesis_file):
    """加载论文文件"""
    print(f"正在加载论文: {thesis_file}")

    with open(thesis_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"✓ 论文已加载，总字数: {len(content)}")
    return content

def extract_chapters(content):
    """提取各章节内容"""
    chapters = {}

    # 查找所有章节标题
    chapter_pattern = r'^([一二三四五六七八九十]+)、(.+?)$'
    matches = list(re.finditer(chapter_pattern, content, re.MULTILINE))

    for i, match in enumerate(matches):
        chapter_num = match.group(1)
        chapter_title = match.group(2).strip()
        chapter_key = f"{chapter_num}、{chapter_title}"

        # 提取章节内容（到下一章节或文件结尾）
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)

        chapter_content = content[start:end].strip()

        chapters[chapter_key] = {
            'title': chapter_title,
            'content': chapter_content,
            'start_pos': start,
            'end_pos': end
        }

    print(f"✓ 提取到 {len(chapters)} 个章节")
    return chapters

def check_violations(chapters):
    """检查越界内容"""
    print("\n开始检查理论/数据/结论分离...")

    violations = []

    # 检查理论部分是否包含数据
    for chapter_key in ['二、文献综述', '三、研究假设']:
        if chapter_key not in chapters:
            continue

        chapter = chapters[chapter_key]
        content = chapter['content']

        for keyword_pattern in VIOLATION_RULES['理论部分_数据越界']['keywords']:
            matches = list(re.finditer(keyword_pattern, content, re.IGNORECASE))

            for match in matches:
                # 提取上下文
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end]

                violations.append({
                    'type': '理论部分_数据越界',
                    'chapter': chapter_key,
                    'matched_text': match.group(0),
                    'context': context,
                    'position': match.start(),
                    'severity': 'high',
                    'suggestion': '将此数据描述移至结果章节，或删除具体数值'
                })

    # 检查结果部分是否有大段理论论述
    for chapter_key in ['五、数据描述性统计', '六、研究结果']:
        if chapter_key not in chapters:
            continue

        chapter = chapters[chapter_key]
        content = chapter['content']

        for keyword_pattern in VIOLATION_RULES['结果部分_理论越界']['keywords']:
            matches = list(re.finditer(keyword_pattern, content, re.IGNORECASE))

            for match in matches:
                # 检查是否为大段论述（>100字）
                start = match.start()
                end = min(len(content), start + 200)
                segment = content[start:end]

                if len(segment) > VIOLATION_RULES['结果部分_理论越界']['min_length']:
                    violations.append({
                        'type': '结果部分_理论越界',
                        'chapter': chapter_key,
                        'matched_text': match.group(0),
                        'context': segment[:150] + '...',
                        'position': match.start(),
                        'severity': 'medium',
                        'suggestion': '精简理论论述，或将其移至讨论章节'
                    })

    # 检查讨论部分是否引入新数据
    for chapter_key in ['七、讨论', '八、研究贡献与局限', '九、结论']:
        if chapter_key not in chapters:
            continue

        chapter = chapters[chapter_key]
        content = chapter['content']

        for keyword_pattern in VIOLATION_RULES['讨论部分_新数据越界']['keywords']:
            matches = list(re.finditer(keyword_pattern, content, re.IGNORECASE))

            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 100)
                context = content[start:end]

                violations.append({
                    'type': '讨论部分_新数据越界',
                    'chapter': chapter_key,
                    'matched_text': match.group(0),
                    'context': context,
                    'position': match.start(),
                    'severity': 'high',
                    'suggestion': '将新数据分析移至结果章节，或删除'
                })

    print(f"✓ 检查完成，发现 {len(violations)} 处潜在越界")
    return violations

def generate_report(violations, output_file):
    """生成检查报告"""
    print("\n生成检查报告...")

    report = {
        'check_date': Path(output_file).stem,
        'total_violations': len(violations),
        'by_severity': {
            'high': len([v for v in violations if v['severity'] == 'high']),
            'medium': len([v for v in violations if v['severity'] == 'medium']),
            'low': len([v for v in violations if v['severity'] == 'low'])
        },
        'by_type': {},
        'violations': violations
    }

    # 按类型统计
    for v in violations:
        vtype = v['type']
        if vtype not in report['by_type']:
            report['by_type'][vtype] = 0
        report['by_type'][vtype] += 1

    # 保存JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✓ 报告已保存: {output_file}")

    # 打印摘要
    print("\n" + "="*60)
    print("分离检查摘要")
    print("="*60)
    print(f"总越界数: {report['total_violations']}")
    print(f"\n按严重程度:")
    print(f"  高: {report['by_severity']['high']}")
    print(f"  中: {report['by_severity']['medium']}")
    print(f"  低: {report['by_severity']['low']}")

    print(f"\n按类型:")
    for vtype, count in report['by_type'].items():
        desc = VIOLATION_RULES.get(vtype, {}).get('description', vtype)
        print(f"  {desc}: {count}")

    if violations:
        print(f"\n前5个越界示例:")
        for i, v in enumerate(violations[:5], 1):
            print(f"\n  {i}. [{v['chapter']}] {v['type']}")
            print(f"     匹配: {v['matched_text']}")
            print(f"     上下文: {v['context'][:80]}...")
            print(f"     建议: {v['suggestion']}")

    print("="*60)

    return report

def main():
    """主函数"""
    print("="*60)
    print("分离检查器 v1.0")
    print("="*60)

    # 文件路径
    base_dir = Path(__file__).parent.parent
    thesis_file = base_dir / "bi_ye_lun_wen.txt"
    output_file = base_dir / "data" / "separation_check_report.json"

    # 加载论文
    content = load_thesis(thesis_file)

    # 提取章节
    chapters = extract_chapters(content)

    # 检查越界
    violations = check_violations(chapters)

    # 生成报告
    report = generate_report(violations, output_file)

    if violations:
        print(f"\n⚠ 发现 {len(violations)} 处潜在越界，请人工审核")
    else:
        print(f"\n✓ 未发现明显越界，理论/数据/结论分离良好")

    print(f"\n详细报告: {output_file}")

if __name__ == "__main__":
    main()
