#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文献引用一致性检查脚本
检查论文中的文献引用是否与参考文献列表匹配
"""

import re
from collections import defaultdict

def extract_references(file_path):
    """提取参考文献列表"""
    references = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到参考文献部分
    ref_section = re.search(r'十、参考文献\n\n(.*?)(?=\n============)', content, re.DOTALL)
    if not ref_section:
        print("未找到参考文献部分")
        return references

    ref_text = ref_section.group(1)

    # 提取每条参考文献
    pattern = r'\[(\d+)\]\s+([^\n]+)'
    matches = re.findall(pattern, ref_text)

    for num, citation in matches:
        # 提取第一作者姓氏和年份
        author_match = re.match(r'([A-Z][a-z]+)', citation)
        year_match = re.search(r'\((\d{4})\)', citation)

        if author_match and year_match:
            author = author_match.group(1)
            year = year_match.group(1)
            references[num] = {
                'author': author,
                'year': year,
                'full': citation
            }

    return references

def check_citations(file_path, references):
    """检查正文中的文献引用"""
    errors = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 匹配格式：Author et al., YYYY[N] 或 Author & Author, YYYY[N]
    pattern1 = r'([A-Z][a-z]+)\s+et al\.,?\s+(\d{4})\[(\d+)\]'
    pattern2 = r'([A-Z][a-z]+)\s+&\s+[A-Z][a-z]+,?\s+(\d{4})\[(\d+)\]'
    pattern3 = r'([A-Z][a-z]+)\s+et al\.\s+\((\d{4})\)\s*\[(\d+)\]'

    for line_num, line in enumerate(lines, 1):
        # 检查 "Author et al., YYYY[N]" 格式
        for match in re.finditer(pattern1, line):
            author, year, ref_num = match.groups()
            if ref_num in references:
                ref = references[ref_num]
                if ref['author'] != author or ref['year'] != year:
                    errors.append({
                        'line': line_num,
                        'text': match.group(0),
                        'expected_author': ref['author'],
                        'expected_year': ref['year'],
                        'found_author': author,
                        'found_year': year,
                        'ref_num': ref_num
                    })

        # 检查 "Author & Author, YYYY[N]" 格式
        for match in re.finditer(pattern2, line):
            author, year, ref_num = match.groups()
            if ref_num in references:
                ref = references[ref_num]
                if ref['author'] != author or ref['year'] != year:
                    errors.append({
                        'line': line_num,
                        'text': match.group(0),
                        'expected_author': ref['author'],
                        'expected_year': ref['year'],
                        'found_author': author,
                        'found_year': year,
                        'ref_num': ref_num
                    })

        # 检查 "Author et al. (YYYY) [N]" 格式
        for match in re.finditer(pattern3, line):
            author, year, ref_num = match.groups()
            if ref_num in references:
                ref = references[ref_num]
                if ref['author'] != author or ref['year'] != year:
                    errors.append({
                        'line': line_num,
                        'text': match.group(0),
                        'expected_author': ref['author'],
                        'expected_year': ref['year'],
                        'found_author': author,
                        'found_year': year,
                        'ref_num': ref_num
                    })

    return errors

def main():
    file_path = r'E:\bi_ye_she_ji\bi_ye_lun_wen.txt'

    print("正在提取参考文献列表...")
    references = extract_references(file_path)
    print(f"找到 {len(references)} 篇参考文献\n")

    print("正在检查文献引用一致性...")
    errors = check_citations(file_path, references)

    if errors:
        print(f"\n发现 {len(errors)} 处文献引用不匹配：\n")
        for i, error in enumerate(errors, 1):
            print(f"{i}. 第 {error['line']} 行")
            print(f"   引用文本: {error['text']}")
            print(f"   正文中: {error['found_author']} ({error['found_year']})")
            print(f"   参考文献[{error['ref_num']}]: {error['expected_author']} ({error['expected_year']})")
            print()
    else:
        print("\n✓ 所有文献引用与参考文献列表匹配！")

if __name__ == '__main__':
    main()
