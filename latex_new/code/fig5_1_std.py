#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 5-1  研究框架与假设检验路径图
上下两块布局：上=全样本H1/H2，下=子样本H3/H4
纯黑灰色，宋体+Times New Roman，无加粗斜体，无图名
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib import font_manager

_simsun_candidates = [f.fname for f in font_manager.fontManager.ttflist
                      if 'SimSun' in f.name or 'simsun' in f.fname.lower()]
if _simsun_candidates:
    _SIMSUN_PATH = _simsun_candidates[0]
else:
    _SIMSUN_PATH = None

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
C_BG    = '#F0F0F0'

fig, ax = plt.subplots(figsize=(11, 9))
ax.set_xlim(0, 11)
ax.set_ylim(0, 9)
ax.axis('off')

# ── 辅助函数
def rect(cx, cy, w, h, text, ec=C_BLACK, fc=C_WHITE, fs=FS_LABEL, lw=1.2):
    ax.add_patch(FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.05',
        edgecolor=ec, facecolor=fc, linewidth=lw, zorder=3))
    ax.text(cx, cy, text,
            ha='center', va='center',
            fontsize=fs, fontweight='normal',
            linespacing=1.5, zorder=4)

def solid_arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=1.4,
                                color=C_BLACK,
                                connectionstyle='arc3,rad=0'),
                zorder=3)

def label_box(x, y, text, fs=FS_LABEL):
    ax.text(x, y, text,
            ha='center', va='center',
            fontsize=fs, fontweight='normal',
            bbox=dict(boxstyle='round,pad=0.2',
                      fc=C_WHITE, ec=C_DARK, lw=0.8),
            zorder=5)

# ════════════════════════════════════════════════
# 上半部分：H1/H2  全样本 (N=1,157)
# ════════════════════════════════════════════════
TOP_Y = 7.0   # 变量框 Y 坐标

# 区域背景标题
ax.add_patch(FancyBboxPatch((0.3, 7.85), 10.4, 0.55,
    boxstyle='round,pad=0.04',
    edgecolor=C_DARK, facecolor=C_BG, lw=1.0, zorder=1))
ax.text(5.5, 8.12,
        '全样本分析  H1 / H2  (N = 1,157)',
        ha='center', va='center',
        fontsize=FS_LABEL, fontweight='normal')

BOX_W, BOX_H = 1.8, 0.70

# 三个变量框（等间距，水平居中）
X_ATT  = 2.2
X_RAT  = 5.5
X_EXP  = 8.8

rect(X_ATT, TOP_Y, BOX_W, BOX_H, 'ATT\n多属性态度')
rect(X_RAT, TOP_Y, BOX_W, BOX_H, 'Rating\n评论评分')
rect(X_EXP, TOP_Y, BOX_W, BOX_H, 'Reviewer\nExperience')

# H1 主效应：ATT → Rating
solid_arrow(X_ATT + BOX_W/2, TOP_Y, X_RAT - BOX_W/2, TOP_Y)
label_box((X_ATT + BOX_W/2 + X_RAT - BOX_W/2)/2, TOP_Y + 0.38, 'H1')

# H2 调节：Experience → ATT-Rating 路径中点（向下垂直箭头）
mid_x = (X_ATT + BOX_W/2 + X_RAT - BOX_W/2) / 2
line_y = TOP_Y - BOX_H/2 - 0.12
ax.plot([X_EXP, mid_x], [line_y, line_y],
        color=C_DARK, lw=1.2, ls='--', zorder=3)
ax.annotate('', xy=(mid_x, TOP_Y - BOX_H/2),
            xytext=(mid_x, line_y),
            arrowprops=dict(arrowstyle='->', lw=1.2, color=C_DARK),
            zorder=3)
label_box((mid_x + X_EXP)/2 + 0.3, line_y - 0.28, 'H2（调节）')

# 控制变量说明
ax.text(5.5, TOP_Y - BOX_H/2 - 0.75,
        '控制变量: review_length, helpful_vote, review_year',
        ha='center', va='center',
        fontsize=FS_LABEL - 0.5, fontweight='normal',
        color=C_MID)

# ════════════════════════════════════════════════
# 水平分隔线
# ════════════════════════════════════════════════
ax.plot([0.3, 10.7], [5.1, 5.1],
        color=C_PALE, lw=1.2, ls='--', zorder=1)

# ════════════════════════════════════════════════
# 下半部分：H3/H4  子样本 (N=298)
# ════════════════════════════════════════════════
BOT_Y = 3.6   # 变量框 Y 坐标

# 区域背景标题
ax.add_patch(FancyBboxPatch((0.3, 4.65), 10.4, 0.55,
    boxstyle='round,pad=0.04',
    edgecolor=C_DARK, facecolor=C_BG, lw=1.0, zorder=1))
ax.text(5.5, 4.92,
        '子样本分析  H3 / H4  (N = 298)',
        ha='center', va='center',
        fontsize=FS_LABEL, fontweight='normal')

XL = 2.2    # ATT 框
XM = 5.5    # Rating（控制）框
XR = 8.8    # BI 框

rect(XL, BOT_Y, BOX_W, BOX_H, 'ATT\n多属性态度')
rect(XM, BOT_Y, BOX_W, BOX_H, 'Rating\n（控制变量）', ec=C_PALE, fc='#F8F8F8')
rect(XR, BOT_Y, BOX_W, BOX_H, 'BI\n行为意向')

# H3 主效应：ATT → BI（上弧）
ax.annotate('',
            xy=(XR - BOX_W/2, BOT_Y + 0.08),
            xytext=(XL + BOX_W/2, BOT_Y + 0.08),
            arrowprops=dict(arrowstyle='->', lw=1.4,
                            color=C_BLACK,
                            connectionstyle='arc3,rad=-0.30'),
            zorder=3)
label_box(5.5, BOT_Y + 0.90, 'H3（主效应）')

# Rating → BI（控制路径，细实线）
solid_arrow(XM + BOX_W/2, BOT_Y, XR - BOX_W/2, BOT_Y)
ax.text((XM + BOX_W/2 + XR - BOX_W/2)/2, BOT_Y + 0.22,
        '控制', ha='center', va='bottom',
        fontsize=FS_LABEL - 0.5, color=C_MID)

# H4 增量效度：ATT → BI（下弧虚线）
ax.annotate('',
            xy=(XR - BOX_W/2, BOT_Y - 0.08),
            xytext=(XL + BOX_W/2, BOT_Y - 0.08),
            arrowprops=dict(arrowstyle='->', lw=1.2,
                            color=C_DARK, linestyle='dashed',
                            connectionstyle='arc3,rad=0.30'),
            zorder=3)
label_box(5.5, BOT_Y - 0.90, r'H4: $\Delta R^2$ 增量效度')

# ════════════════════════════════════════════════
# 图例（底部居中）
# ════════════════════════════════════════════════
LEG_Y = 1.55
ax.text(2.0, LEG_Y, '图例:', ha='left', va='center',
        fontsize=FS_LABEL, fontweight='normal')

ax.annotate('', xy=(3.2, LEG_Y), xytext=(2.5, LEG_Y),
            arrowprops=dict(arrowstyle='->', lw=1.4, color=C_BLACK))
ax.text(3.35, LEG_Y, '主效应路径',
        ha='left', va='center', fontsize=FS_LABEL)

ax.plot([5.8, 6.6], [LEG_Y, LEG_Y], color=C_DARK, lw=1.2, ls='--')
ax.annotate('', xy=(6.6, LEG_Y), xytext=(6.45, LEG_Y),
            arrowprops=dict(arrowstyle='->', lw=1.2, color=C_DARK))
ax.text(6.75, LEG_Y, '调节效应 / 增量效度',
        ha='left', va='center', fontsize=FS_LABEL)

# ════════════════════════════════════════════════
# 底部说明
# ════════════════════════════════════════════════
ax.text(5.5, 0.70,
        '注: ATT 与 Rating 来自独立数据源，不存在同源方差（CMV）问题；\n'
        'ATT 与 BI 均来自同一评论文本，存在 CMV 局限（Harman 单因子 = 76.8%）。',
        ha='center', va='center',
        fontsize=FS_LABEL, fontweight='normal',
        color=C_DARK, linespacing=1.6)

plt.tight_layout(pad=0.5)
plt.savefig('E:/bi_ye_she_ji/latex_new/figures/fig5_1_std.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figure 5-1 done")
plt.close()
