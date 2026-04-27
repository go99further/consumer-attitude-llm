#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研究框架与假设检验路径图
Figure 5-1: Research Framework and Hypothesis Testing Path Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# 创建图形
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# ========== 第一部分：H1/H2 全样本模型 ==========

# 标题
ax.text(7, 9.5, 'H1/H2 全样本模型 (N=1,157)',
        ha='center', va='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.3))

# 数据源层（顶部）
datasrc_y = 8.5
datasrc_boxes = [
    (1.5, datasrc_y, '数据源1\nLLM评论文本提取', 'lightgreen'),
    (5.5, datasrc_y, '数据源2\n平台结构化字段', 'lightcoral'),
    (9.5, datasrc_y, '数据源3\n全品类行为数据', 'lightyellow')
]

for x, y, text, color in datasrc_boxes:
    box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6,
                          boxstyle="round,pad=0.05",
                          edgecolor='gray', facecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9)

# 变量层（中部）
var_y = 7.0
var_boxes = [
    (1.5, var_y, '多属性态度\nATT', 'white', 'green'),
    (5.5, var_y, '评论评分\nRating (1-5星)', 'white', 'orange'),
    (9.5, var_y, '评论者经验\nReviewer Experience', 'white', 'purple')
]

for x, y, text, facecolor, edgecolor in var_boxes:
    box = FancyBboxPatch((x-0.9, y-0.35), 1.8, 0.7,
                          boxstyle="round,pad=0.05",
                          edgecolor=edgecolor, facecolor=facecolor, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')

# 数据源到变量的连接线（细灰线）
for i in range(3):
    ax.plot([datasrc_boxes[i][0], var_boxes[i][0]],
            [datasrc_y-0.3, var_y+0.35],
            'gray', linewidth=1, linestyle='--', alpha=0.5)

# H1 主效应箭头（实线粗箭头）
arrow_h1 = FancyArrowPatch((2.4, var_y), (4.6, var_y),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2.5, color='black')
ax.add_patch(arrow_h1)
ax.text(3.5, var_y+0.25, 'H1', ha='center', va='bottom',
        fontsize=11, fontweight='bold', color='black')

# H2 调节效应箭头（虚线箭头）
# 从 Reviewer Experience 到 ATT-Rating 中点
arrow_h2 = FancyArrowPatch((9.5, var_y-0.35), (3.5, var_y-0.8),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='blue', linestyle='--')
ax.add_patch(arrow_h2)
ax.text(6.5, var_y-0.9, 'H2 (调节效应)', ha='center', va='top',
        fontsize=10, fontweight='bold', color='blue')

# 分隔线
ax.plot([0.5, 13.5], [5.8, 5.8], 'k--', linewidth=1.5, alpha=0.5)

# ========== 第二部分：H3/H4 子样本模型 ==========

# 标题
ax.text(7, 5.3, 'H3/H4 子样本模型 (N=298, 含CMV局限)',
        ha='center', va='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.3))

# 变量层（下部）
var2_y = 3.8
var2_boxes = [
    (1.5, var2_y, '多属性态度\nATT', 'white', 'green'),
    (5.5, var2_y, '评论评分\nRating\n(控制变量)', 'white', 'gray'),
    (11, var2_y, '行为意向\nBI (0-3量表)', 'white', 'red')
]

for x, y, text, facecolor, edgecolor in var2_boxes:
    width = 2.2 if x == 11 else 1.8
    box = FancyBboxPatch((x-width/2, y-0.35), width, 0.7,
                          boxstyle="round,pad=0.05",
                          edgecolor=edgecolor, facecolor=facecolor, linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')

# 数据源到变量的连接线（细灰线，从上方数据源延伸）
ax.plot([1.5, 1.5], [datasrc_y-0.3, var2_y+0.35],
        'gray', linewidth=1, linestyle='--', alpha=0.3)
ax.plot([5.5, 5.5], [datasrc_y-0.3, var2_y+0.35],
        'gray', linewidth=1, linestyle='--', alpha=0.3)

# H3 主效应箭头（实线）
arrow_h3 = FancyArrowPatch((2.4, var2_y), (9.9, var2_y),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2.5, color='black')
ax.add_patch(arrow_h3)
ax.text(6, var2_y+0.35, 'H3', ha='center', va='bottom',
        fontsize=11, fontweight='bold', color='black')

# Rating 控制变量箭头（实线，较细）
arrow_control = FancyArrowPatch((6.4, var2_y), (9.9, var2_y),
                                arrowstyle='->', mutation_scale=15,
                                linewidth=1.5, color='gray')
ax.add_patch(arrow_control)
ax.text(8, var2_y-0.35, '控制', ha='center', va='top',
        fontsize=9, color='gray')

# H4 增量效度箭头（弧形箭头）
from matplotlib.patches import Arc
arc = Arc((6, var2_y-1.2), 10, 2, angle=0, theta1=0, theta2=180,
          linewidth=2, color='darkgreen', linestyle='-')
ax.add_patch(arc)
arrow_h4_end = FancyArrowPatch((10.8, var2_y-0.5), (11, var2_y-0.35),
                               arrowstyle='->', mutation_scale=15,
                               linewidth=2, color='darkgreen')
ax.add_patch(arrow_h4_end)
ax.text(6, var2_y-1.5, r'H4 ($\Delta R^2$ 增量效度)', ha='center', va='top',
        fontsize=10, fontweight='bold', color='darkgreen')

# ========== 图例 ==========
legend_y = 1.5
legend_elements = [
    ('实线箭头', 'black', '-', '主效应/预测关系'),
    ('虚线箭头', 'blue', '--', '调节效应'),
    ('弧形箭头', 'darkgreen', '-', '增量效度')
]

ax.text(1, legend_y+0.5, '图例说明:', ha='left', va='center',
        fontsize=10, fontweight='bold')

for i, (label, color, style, desc) in enumerate(legend_elements):
    y_pos = legend_y - i*0.3
    ax.plot([1, 2], [y_pos, y_pos], color=color, linestyle=style, linewidth=2)
    ax.text(2.2, y_pos, f'{label}: {desc}', ha='left', va='center', fontsize=9)

# 注释说明
note_text = ('注：ATT与Rating来自独立数据源，无CMV问题；\n'
             'ATT与BI来自同一文本，存在CMV局限（Harman=76.8%）')
ax.text(7, 0.5, note_text, ha='center', va='center',
        fontsize=8, style='italic', color='gray',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                  edgecolor='gray', alpha=0.5))

plt.tight_layout()
plt.savefig('E:/bi_ye_she_ji/latex_new/figures/research_framework_new.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图5-1已生成: research_framework_new.png")
plt.close()
