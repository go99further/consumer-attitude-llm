#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 7-3  多属性态度（ATT）的增量效度分析（层次回归 ΔR²）
左：R² 累积折线图  右：ΔR² 柱状图
统一深灰色，p值放图注，左右等宽对齐
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family']        = 'serif'
plt.rcParams['font.serif']         = ['SimSun', 'STSong', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

FS_TITLE = 10.5
FS_LABEL = 9.0

C_BLACK = '#000000'
C_DARK  = '#444444'
C_MID   = '#777777'
C_PALE  = '#BBBBBB'
C_WHITE = '#FFFFFF'

# ── 数据
model_labels = ['Model 1\n（控制变量）', 'Model 2\n（+Rating）', 'Model 3\n（+ATT）']
R2     = [0.022, 0.336, 0.354]
dR2    = [0.022, 0.314, 0.018]
x      = np.array([0, 1, 2])

# ── 画布：左右等宽，统一纵轴范围
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5),
                                gridspec_kw={'width_ratios': [1, 1]})
plt.subplots_adjust(wspace=0.38, bottom=0.28)

# ════════════════════════════════════════
# 左图：R² 累积折线
# ════════════════════════════════════════
ax1.plot(x, R2,
         marker='o', markersize=8,
         lw=2.0, color=C_BLACK,
         markerfacecolor=C_WHITE,
         markeredgewidth=1.8,
         markeredgecolor=C_BLACK,
         zorder=3)

# 增量阴影
ax1.fill_between([0, 1], [R2[0]]*2, [R2[1]]*2, alpha=0.10, color=C_MID)
ax1.fill_between([1, 2], [R2[1]]*2, [R2[2]]*2, alpha=0.20, color=C_DARK)

# R² 数值标注（点上方）
for i, (xi, yi) in enumerate(zip(x, R2)):
    ax1.text(xi, yi + 0.016,
             f'R² = {yi:.3f}',
             ha='center', va='bottom',
             fontsize=FS_LABEL, fontweight='normal')

ax1.set_xticks(x)
ax1.set_xticklabels(model_labels, fontsize=FS_LABEL)
ax1.set_ylabel('决定系数（R²）', fontsize=FS_LABEL, fontweight='normal')
ax1.set_ylim(0, 0.42)
ax1.set_yticks(np.arange(0, 0.45, 0.05))
ax1.tick_params(axis='y', labelsize=FS_LABEL)
ax1.tick_params(axis='x', labelsize=FS_LABEL)
ax1.yaxis.grid(True, linestyle=':', linewidth=0.7, alpha=0.5, color=C_PALE)
ax1.set_axisbelow(True)

# ════════════════════════════════════════
# 右图：ΔR² 柱状图（统一深灰，无彩色）
# ════════════════════════════════════════
bar_colors  = ['#AAAAAA', '#666666', '#333333']
bar_hatches = ['', '', '']

bars = ax2.bar(x, dR2, width=0.5,
               color=bar_colors,
               edgecolor=C_BLACK,
               linewidth=1.0)

# ΔR² 数值（柱顶上方）
for i, (xi, dv) in enumerate(zip(x, dR2)):
    ax2.text(xi, dv + 0.008,
             f'ΔR² = {dv:.3f}',
             ha='center', va='bottom',
             fontsize=FS_LABEL, fontweight='normal')

ax2.set_xticks(x)
ax2.set_xticklabels(model_labels, fontsize=FS_LABEL)
ax2.set_ylabel('R² 增量（ΔR²）', fontsize=FS_LABEL, fontweight='normal')
ax2.set_ylim(0, 0.38)
ax2.set_yticks(np.arange(0, 0.40, 0.05))
ax2.tick_params(axis='y', labelsize=FS_LABEL)
ax2.tick_params(axis='x', labelsize=FS_LABEL)
ax2.yaxis.grid(True, linestyle=':', linewidth=0.7, alpha=0.5, color=C_PALE)
ax2.set_axisbelow(True)

# ── 图注（图下方统一放显著性）
note = ('注: Model 1 仅含控制变量; Model 2 加入 Rating (DeltaR2 = 0.314, F = 139.8, p < 0.001);\n'
        'Model 3 加入 ATT (DeltaR2 = 0.018, F = 8.32, p = 0.004). ** p < 0.01, *** p < 0.001.')
fig.text(0.5, -0.04, note,
         ha='center', va='top',
         fontsize=FS_LABEL,
         fontweight='normal',
         color=C_DARK,
         linespacing=1.8,
         transform=fig.transFigure)

plt.savefig('E:/bi_ye_she_ji/latex_new/figures/fig7_3_incremental.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figure 7-3 done")
plt.close()
