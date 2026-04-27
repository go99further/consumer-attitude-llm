#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献替换助手 - 生成替换建议（需人工审核）
为每篇待替换文献生成搜索关键词和替换建议
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

def load_analysis(analysis_file):
    """加载文献分析结果"""
    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_topic_and_keywords(ref_text):
    """从文献中提取主题和关键词"""
    # 移除作者和年份
    text = re.sub(r'^[^(]+\(\d{4}\)\.?\s*', '', ref_text)

    # 提取标题
    title_match = re.search(r'^([^.]+)', text)
    title = title_match.group(1).strip() if title_match else ""

    # 提取期刊名
    journal_match = re.search(r'\.\s*([A-Z][^,]+),', text)
    journal = journal_match.group(1).strip() if journal_match else ""

    # 生成搜索关键词
    stopwords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from']
    words = title.lower().split()
    keywords = [w for w in words if w not in stopwords and len(w) > 3]

    return {
        'title': title,
        'journal': journal,
        'keywords': keywords[:5],
        'search_query': ' '.join(keywords[:5]) + ' 2022-2026'
    }

def categorize_literature(ref_text):
    """对文献进行分类"""
    text_lower = ref_text.lower()

    categories = []

    # 主题分类
    if any(word in text_lower for word in ['review', 'ewom', 'word-of-mouth', 'online review']):
        categories.append('在线评论')

    if any(word in text_lower for word in ['attitude', 'belief', 'intention', 'behavior']):
        categories.append('态度行为')

    if any(word in text_lower for word in ['sentiment', 'opinion', 'emotion']):
        categories.append('情感分析')

    if any(word in text_lower for word in ['llm', 'language model', 'gpt', 'nlp', 'text mining']):
        categories.append('LLM/NLP')

    if any(word in text_lower for word in ['consumer', 'customer', 'purchase', 'buying']):
        categories.append('消费者行为')

    if any(word in text_lower for word in ['helpfulness', 'usefulness', 'quality']):
        categories.append('评论质量')

    if not categories:
        categories.append('其他')

    return categories

def generate_replacement_suggestions(to_replace):
    """生成替换建议"""
    suggestions = []

    for ref in to_replace:
        info = extract_topic_and_keywords(ref['text'])
        categories = categorize_literature(ref['text'])

        suggestion = {
            'id': ref['id'],
            'old_year': ref['year'],
            'old_text': ref['text'],
            'categories': categories,
            'title': info['title'],
            'journal': info['journal'],
            'keywords': info['keywords'],
            'search_query': info['search_query'],
            'search_urls': {
                'google_scholar': f"https://scholar.google.com/scholar?q={'+'.join(info['keywords'])}+2022..2026",
                'semantic_scholar': f"https://www.semanticscholar.org/search?q={'+'.join(info['keywords'])}&year%5B0%5D=2022&year%5B1%5D=2026",
                'cnki': f"https://kns.cnki.net/kns8/defaultresult/index?kw={'+'.join(info['keywords'])}&korder=SU"
            },
            'replacement_strategy': get_replacement_strategy(categories, ref['year'])
        }

        suggestions.append(suggestion)

    return suggestions

def get_replacement_strategy(categories, old_year):
    """根据分类给出替换策略"""
    strategies = []

    if 'LLM/NLP' in categories:
        strategies.append("优先搜索2023-2024年LLM应用文献（ChatGPT后时代）")

    if 'attitude' in ' '.join(categories).lower():
        strategies.append("搜索'2022-2026年应用Fishbein/TPB理论的实证研究'")

    if '在线评论' in categories:
        strategies.append("搜索'online review + consumer behavior + 2022-2026'")

    if old_year < 2010:
        strategies.append("经典理论文献，搜索'近期引用该理论的综述或元分析'")

    if not strategies:
        strategies.append("搜索相同主题的近五年文献")

    return strategies

def generate_markdown_report(suggestions, output_file):
    """生成Markdown格式的替换建议报告"""
    md = ["# 文献替换建议报告\n"]
    md.append(f"生成时间: {Path(output_file).stem}\n")
    md.append(f"待替换文献数: {len(suggestions)}\n")
    md.append("---\n\n")

    for i, sug in enumerate(suggestions, 1):
        md.append(f"## {i}. 文献 [{sug['id']}] ({sug['old_year']})\n\n")

        md.append(f"**原文献:**\n")
        md.append(f"> {sug['old_text']}\n\n")

        md.append(f"**分类:** {', '.join(sug['categories'])}\n\n")

        md.append(f"**标题:** {sug['title']}\n\n")

        if sug['journal']:
            md.append(f"**期刊:** {sug['journal']}\n\n")

        md.append(f"**关键词:** {', '.join(sug['keywords'])}\n\n")

        md.append(f"**替换策略:**\n")
        for strategy in sug['replacement_strategy']:
            md.append(f"- {strategy}\n")
        md.append("\n")

        md.append(f"**搜索链接:**\n")
        md.append(f"- [Google Scholar]({sug['search_urls']['google_scholar']})\n")
        md.append(f"- [Semantic Scholar]({sug['search_urls']['semantic_scholar']})\n")
        md.append(f"- [CNKI]({sug['search_urls']['cnki']})\n\n")

        md.append(f"**替换文献:** (请手动填写)\n")
        md.append(f"```\n")
        md.append(f"[{sug['id']}] \n")
        md.append(f"```\n\n")

        md.append("---\n\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(md)

    print(f"✓ Markdown报告已生成: {output_file}")

def main():
    """主函数"""
    print("="*60)
    print("文献替换助手 v1.0")
    print("="*60)

    # 文件路径
    base_dir = Path(__file__).parent.parent
    analysis_file = base_dir / "data" / "literature_analysis.json"
    output_json = base_dir / "data" / "replacement_suggestions.json"
    output_md = base_dir / "data" / "replacement_suggestions.md"

    # 加载分析结果
    analysis = load_analysis(analysis_file)
    to_replace = analysis['to_replace']

    print(f"待替换文献: {len(to_replace)} 篇\n")

    # 生成替换建议
    print("正在生成替换建议...")
    suggestions = generate_replacement_suggestions(to_replace)

    # 保存JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON报告已保存: {output_json}")

    # 生成Markdown报告
    generate_markdown_report(suggestions, output_md)

    print("\n" + "="*60)
    print("下一步操作:")
    print("="*60)
    print(f"1. 打开文件: {output_md}")
    print(f"2. 点击每个文献的搜索链接")
    print(f"3. 找到合适的替换文献后，填写到对应位置")
    print(f"4. 完成后运行 apply_replacements.py 应用替换")
    print("="*60)

if __name__ == "__main__":
    main()
