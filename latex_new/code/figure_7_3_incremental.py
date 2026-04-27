#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多属性态度(ATT)的增量效度分析
Figure 7-3: Incremental Validity Analysis of Multi-Attribute Attitude (ATT)
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

# 层次回归数据
models = ['Model 1\n(控制变量)', 'Model 2\n(+Rating)', 'Model 3\n(+ATT)']
R2_values = [0.022, 0.336, 0.354]
delta_R2 = [0.022, 0.314, 0.018]

# 创建图形（使用折线图+柱状图组合）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ========== 左图：R²累积变化（折线图） ==========
x_pos = np.arange(len(models))

# 绘制折线
line = ax1.plot(x_pos, R2_values, marker='o', markersize=12,
                linewidth=3, color='#2E86AB',
                markerfacecolor='white', markeredgewidth=2,
                markeredgecolor='#2E86AB')

# 添加数据标签
for i, (x, y) in enumerate(zip(x_pos, R2_values)):
    ax1.text(x, y + 0.02, f'$R^2 = {y:.3f}$',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

    # 添加显著性标注
    if i == 1:
        ax1.text(x, y - 0.03, '***', ha='center', va='top',
                 fontsize=14, color='red')
    elif i == 2:
        ax1.text(x, y - 0.03, '**', ha='center', va='top',
                 fontsize=14, color='red')

# 设置坐标轴
ax1.set_xlabel('层次回归模型', fontsize=12, fontweight='bold')
ax1.set_ylabel(r'决定系数 ($R^2$)', fontsize=12, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(models, fontsize=10)
ax1.set_ylim(0, 0.4)
ax1.set_yticks(np.arange(0, 0.41, 0.05))
ax1.grid(True, axis='y', linestyle=':', alpha=0.3)
ax1.set_title(r'(a) $R^2$ 累积变化', fontsize=12, fontweight='bold', pad=15)

# 添加阴影区域表示增量
for i in range(len(x_pos)-1):
    ax1.fill_between([x_pos[i], x_pos[i+1]],
                     [R2_values[i], R2_values[i]],
                     [R2_values[i+1], R2_values[i+1]],
                     alpha=0.2, color='lightblue')

# ========== 右图：ΔR²增量贡献（柱状图） ==========
colors = ['#95B8D1', '#2E86AB', '#A23B72']
bars = ax2.bar(x_pos, delta_R2, color=colors, alpha=0.8,
               edgecolor='black', linewidth=1.5, width=0.6)

# 添加数据标签
for i, (bar, value) in enumerate(zip(bars, delta_R2)):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'$\\Delta R^2 = {value:.3f}$',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

    # 添加显著性标注
    if i == 1:
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                 '***', ha='center', va='bottom',
                 fontsize=14, color='red')
    elif i == 2:
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                 '**', ha='center', va='bottom',
                 fontsize=14, color='red')

# 设置坐标轴
ax2.set_xlabel('层次回归模型', fontsize=12, fontweight='bold')
ax2.set_ylabel(r'$R^2$ 增量 ($\Delta R^2$)', fontsize=12, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(models, fontsize=10)
ax2.set_ylim(0, 0.35)
ax2.set_yticks(np.arange(0, 0.36, 0.05))
ax2.grid(True, axis='y', linestyle=':', alpha=0.3)
ax2.set_title(r'(b) $\Delta R^2$ 增量贡献', fontsize=12, fontweight='bold', pad=15)

# ========== 添加统计信息注释 ==========
stats_text = (
    '层次回归分析结果：\n'
    'Model 1: 控制变量 (review_length, helpful_vote, review_year)\n'
    r'Model 2: +Rating, $\Delta R^2 = 0.314$, $F = 139.8$***' + '\n'
    r'Model 3: +ATT, $\Delta R^2 = 0.018$, $F = 8.32$**' + '\n'
    r'样本量: $N = 298$' + '\n'
    r'**$p < 0.01$, ***$p < 0.001$'
)

fig.text(0.5, -0.05, stats_text,
         ha='center', va='top', fontsize=9,
         bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow',
                   edgecolor='gray', alpha=0.9))

# 添加解释说明
interpretation = (
    '结果解释：在控制Rating后，ATT对BI仍具有显著的增量预测力\n'
    r'($\Delta R^2 = 0.018$, $p = 0.004$)，证明多属性态度提供了超越单一评分的信息增量'
)
fig.text(0.5, -0.12, interpretation,
         ha='center', va='top', fontsize=9,
         style='italic', color='darkgreen',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                   edgecolor='darkgreen', alpha=0.7))

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('E:/bi_ye_she_ji/latex_new/figures/h4_incremental_validity_plot_new.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图7-3已生成: h4_incremental_validity_plot_new.png")
plt.close()
