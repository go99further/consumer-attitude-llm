#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 7-2  评论者经验对 ATT-Rating 关系的调节效应（简单斜率分析）
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

fp_song = FontProperties(family='SimSun', size=9)
fp_tnr  = FontProperties(family='Times New Roman', size=9)

plt.rcParams.update({
    'font.family':        'serif',
    'font.serif':         ['SimSun', 'Times New Roman'],
    'font.size':          10,
    'axes.unicode_minus': False,
    'mathtext.fontset':   'stix',
})

ATT_range   = np.linspace(-2.5, 2.5, 100)
intercept   = 3.85

slope_low   = 0.741
slope_high  = 0.573

rating_low  = intercept + slope_low  * ATT_range
rating_high = intercept + slope_high * ATT_range

fig, ax = plt.subplots(figsize=(8, 5.8))

ax.plot(ATT_range, rating_low,
        color='#000000', lw=2.2, ls='-',
        label='低经验组（$-$1SD）')

ax.plot(ATT_range, rating_high,
        color='#000000', lw=2.2, ls='--',
        label='高经验组（$+$1SD）')

ax.axvline(x=0, color='#AAAAAA', lw=0.8, ls=':', zorder=1)

# slope annotations on right side
x_ann = 2.1
ax.text(x_ann + 0.15, intercept + slope_low * x_ann,
        '低经验\n斜率 = 0.741', ha='left', va='center',
        fontproperties=fp_song, fontsize=9, color='#222222', linespacing=1.3)
ax.text(x_ann + 0.15, intercept + slope_high * x_ann - 0.15,
        '高经验\n斜率 = 0.573', ha='left', va='center',
        fontproperties=fp_song, fontsize=9, color='#555555', linespacing=1.3)

ax.set_xlabel('多属性态度（ATT，均值中心化）', fontsize=10)
ax.set_ylabel('评论评分（Rating）', fontsize=10)

ax.set_xlim(-2.8, 3.2)
ax.set_ylim(1.8, 5.7)
ax.tick_params(labelsize=9)

legend = ax.legend(loc='upper left', fontsize=9,
                   frameon=True, framealpha=0.95, edgecolor='#888888')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

note_lines = (
    '注：低经验组（RE = 均值$-$1SD），高经验组（RE = 均值$+$1SD）；两组斜率均 $p < 0.001$。\n'
    '交互项 ATT_c $\\times$ RE_c：$\\beta = -0.008$，$t = -3.34$，$p = 0.001$；'
    '$R^2 = 0.564$，$N = 1{,}157$。'
)
fig.text(0.12, 0.02, note_lines,
         fontsize=9, fontfamily='serif',
         ha='left', va='bottom',
         linespacing=1.4, color='#333333')

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.savefig('E:/bi_ye_she_ji/latex_new/figures/fig7_2_moderation.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figure 7-2 done")
plt.close()
