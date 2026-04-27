#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 7-2  评论者经验对 ATT-Rating 关系的调节效应（简单斜率分析）
两条线：黑色实线（低经验）、黑色虚线（高经验）
斜率注释放右侧，显著性放图注，Y轴标签正确
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
ATT_range  = np.linspace(-2.5, 2.5, 200)
intercept  = 3.85

slope_low  = 0.741   # 低经验组（-1SD）
slope_high = 0.573   # 高经验组（+1SD）

y_low  = intercept + slope_low  * ATT_range
y_high = intercept + slope_high * ATT_range

# ── 画布（留右侧空间放斜率注释）
fig, ax = plt.subplots(figsize=(9, 5.5))
plt.subplots_adjust(right=0.72)

# 两条线
ax.plot(ATT_range, y_low,
        color=C_BLACK, lw=2.0, ls='-',
        label='低经验组（-1SD）')
ax.plot(ATT_range, y_high,
        color=C_BLACK, lw=2.0, ls='--',
        label='高经验组（+1SD）')

# ATT=0 参考竖线（浅灰）
ax.axvline(x=0, color=C_PALE, lw=0.9, ls=':', zorder=1)

# ── 坐标轴
ax.set_xlabel('多属性态度（ATT，均值中心化）',
              fontsize=FS_LABEL, fontweight='normal')
ax.set_ylabel('评论评分（Rating）',
              fontsize=FS_LABEL, fontweight='normal')
ax.set_xlim(-2.6, 2.6)
ax.set_ylim(1.5, 5.8)
ax.tick_params(labelsize=FS_LABEL)
ax.yaxis.set_major_locator(plt.MultipleLocator(0.5))

# 轻微 y 轴网格线
ax.yaxis.grid(True, linestyle=':', linewidth=0.7, alpha=0.5, color=C_PALE)
ax.set_axisbelow(True)

# ── 图例（左上，无边框加粗）
leg = ax.legend(loc='upper left',
                fontsize=FS_LABEL,
                frameon=True,
                framealpha=0.95,
                edgecolor=C_PALE,
                prop={'weight': 'normal'})

# ── 右侧斜率注释（axes坐标之外，用 figure text）
x_note = 2.65   # 数据坐标，略超右轴

# 低经验
y_low_end  = intercept + slope_low  * 2.5
y_high_end = intercept + slope_high * 2.5

ax.annotate('低经验\n斜率 = 0.741',
            xy=(2.5, y_low_end),
            xytext=(2.68, y_low_end),
            fontsize=FS_LABEL,
            fontweight='normal',
            va='center',
            annotation_clip=False)

ax.annotate('高经验\n斜率 = 0.573',
            xy=(2.5, y_high_end),
            xytext=(2.68, y_high_end),
            fontsize=FS_LABEL,
            fontweight='normal',
            va='center',
            annotation_clip=False)

# ── 图注（图下方，正文字号-1）
note = ('注: 低经验组 (RE = 均值-1SD), 高经验组 (RE = 均值+1SD); 两组斜率均 p < 0.001.\n'
        '交互项 ATT_c x RE_c: beta = -0.008, t = -3.34, p = 0.001; R2 = 0.564, N = 1,157.')
fig.text(0.5, -0.06, note,
         ha='center', va='top',
         fontsize=FS_LABEL,
         fontweight='normal',
         color=C_DARK,
         linespacing=1.8,
         transform=fig.transFigure)

plt.savefig('E:/bi_ye_she_ji/latex_new/figures/fig7_2_moderation.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figure 7-2 done")
plt.close()
