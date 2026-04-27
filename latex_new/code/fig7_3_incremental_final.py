#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 7-3  多属性态度（ATT）的增量效度分析（层次回归 ΔR²）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family':        'serif',
    'font.serif':         ['SimSun', 'Times New Roman'],
    'font.size':          10,
    'axes.unicode_minus': False,
    'mathtext.fontset':   'stix',
})

model_labels = [
    'Model 1\n（控制变量）',
    'Model 2\n（+Rating）',
    'Model 3\n（+ATT）'
]
R2_vals    = [0.022, 0.336, 0.354]
delta_R2   = [0.022, 0.314, 0.018]
delta_sig  = ['',    '***', '**' ]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
x = np.arange(len(model_labels))

# ── Left: R² cumulative line
ax1.plot(x, R2_vals,
         marker='o', markersize=10,
         lw=2.2, color='#222222',
         markerfacecolor='white', markeredgewidth=2,
         markeredgecolor='#222222', zorder=3)

ax1.fill_between([x[0], x[1]], [R2_vals[0]]*2, [R2_vals[1]]*2,
                 alpha=0.12, color='#555555')
ax1.fill_between([x[1], x[2]], [R2_vals[1]]*2, [R2_vals[2]]*2,
                 alpha=0.22, color='#222222')

for i, (xi, yi) in enumerate(zip(x, R2_vals)):
    ax1.text(xi, yi + 0.018,
             f'$R^2 = {yi:.3f}$',
             ha='center', va='bottom',
             fontsize=9, fontweight='bold')

ax1.set_xticks(x)
ax1.set_xticklabels(model_labels, fontsize=8.5)
ax1.set_ylabel(r'决定系数（$R^2$）', fontsize=10)
ax1.set_ylim(0, 0.42)
ax1.set_yticks(np.arange(0, 0.45, 0.05))
ax1.tick_params(labelsize=8.5)
ax1.grid(True, axis='y', ls=':', lw=0.8, alpha=0.4)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ── Right: ΔR² bar chart
bar_colors = ['#BBBBBB', '#666666', '#333333']

for i, (xi, dv, bc) in enumerate(zip(x, delta_R2, bar_colors)):
    ax2.bar(xi, dv, width=0.55,
            color=bc, edgecolor='#222222', linewidth=1.2, alpha=0.85)

    label_text = f'$\\Delta R^2 = {dv:.3f}$'
    ax2.text(xi, dv + 0.006,
             label_text,
             ha='center', va='bottom',
             fontsize=9, fontweight='bold')

ax2.set_xticks(x)
ax2.set_xticklabels(model_labels, fontsize=8.5)
ax2.set_ylabel(r'$R^2$ 增量（$\Delta R^2$）', fontsize=10)
ax2.set_ylim(0, 0.38)
ax2.set_yticks(np.arange(0, 0.40, 0.05))
ax2.tick_params(labelsize=8.5)
ax2.grid(True, axis='y', ls=':', lw=0.8, alpha=0.4)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ── Bottom note — tight, left-aligned, 9pt serif
note = (
    '注：Model 1 仅含控制变量；'
    'Model 2 加入 Rating（$\\Delta R^2 = 0.314$，$F = 139.8$，$p < 0.001$）；\n'
    'Model 3 加入 ATT（$\\Delta R^2 = 0.018$，$F = 8.32$，$p = 0.004$）。'
    '$^{**}\\! p < 0.01$，$^{***}\\! p < 0.001$。'
)
fig.text(0.06, 0.02, note,
         fontsize=9, fontfamily='serif',
         ha='left', va='bottom',
         linespacing=1.4, color='#333333')

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.savefig('E:/bi_ye_she_ji/latex_new/figures/fig7_3_incremental.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figure 7-3 done")
plt.close()
