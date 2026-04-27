#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure 5-1 研究框架与假设检验路径图
规范：统一字体、灰度配色、无重叠、清晰分层
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib
matplotlib.use('Agg')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

FONT_TITLE   = 11   # 模块标题
FONT_VAR     = 9    # 变量框内文字
FONT_LABEL   = 8.5  # 箭头标注
FONT_NOTE    = 8    # 注释说明

# ── 颜色系统（灰度）
C_BOX_DARK   = '#333333'  # 深色边框
C_BOX_MID    = '#666666'  # 中灰边框
C_BOX_LIGHT  = '#999999'  # 浅灰边框
C_FILL_1     = '#F0F0F0'  # 数据源框填充
C_FILL_VAR   = '#FFFFFF'  # 变量框填充（白色）
C_FILL_HEAD  = '#DEDEDE'  # 模块标题背景
C_ARROW      = '#000000'  # 主效应箭头
C_MOD        = '#555555'  # 调节效应箭头
C_INC        = '#222222'  # 增量效度箭头

def draw_box(ax, cx, cy, w, h, text, edgecolor, facecolor, fontsize, bold=False):
    """绘制圆角矩形框 + 居中文字"""
    box = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                         boxstyle="round,pad=0.06",
                         edgecolor=edgecolor, facecolor=facecolor,
                         linewidth=1.8, zorder=3)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(cx, cy, text, ha='center', va='center',
            fontsize=fontsize, fontweight=weight,
            linespacing=1.4, zorder=4)

def draw_arrow_solid(ax, x1, y1, x2, y2, label='', label_side='top', lw=2.2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=lw,
                                color=C_ARROW, connectionstyle='arc3,rad=0'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        dy = 0.25 if label_side == 'top' else -0.28
        ax.text(mx, my+dy, label, ha='center', va='center',
                fontsize=FONT_LABEL, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='black', lw=1))

def draw_arrow_dashed(ax, x1, y1, x2, y2, label='', label_side='bottom', lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=lw,
                                color=C_MOD,
                                linestyle='dashed',
                                connectionstyle='arc3,rad=0'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        dy = -0.28 if label_side == 'bottom' else 0.25
        ax.text(mx, my+dy, label, ha='center', va='center',
                fontsize=FONT_LABEL, fontweight='bold', color=C_MOD,
                bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=C_MOD, lw=1))

# ──────────────────────────────────────────────
# 上半部分：H1/H2 全样本模型
# ──────────────────────────────────────────────
# 模块标题背景
ax.add_patch(FancyBboxPatch((0.3, 7.75), 13.4, 0.55,
             boxstyle="round,pad=0.05",
             edgecolor=C_BOX_DARK, facecolor=C_FILL_HEAD, lw=1.5, zorder=2))
ax.text(7, 8.02, '全样本分析  H1/H2  (N = 1,157)',
        ha='center', va='center', fontsize=FONT_TITLE, fontweight='bold')

# 数据源框（顶行）
ds_y = 7.05
draw_box(ax, 2.5, ds_y, 2.8, 0.55, '数据源 1\nLLM 评论文本提取',
         C_BOX_MID, C_FILL_1, FONT_VAR)
draw_box(ax, 7,   ds_y, 2.8, 0.55, '数据源 2\n平台结构化字段',
         C_BOX_MID, C_FILL_1, FONT_VAR)
draw_box(ax, 11.5,ds_y, 2.8, 0.55, '数据源 3\n全品类行为数据',
         C_BOX_MID, C_FILL_1, FONT_VAR)

# 数据源→变量 细点线
var_y = 5.9
for sx, vx in [(2.5, 2.5), (7, 7), (11.5, 11.5)]:
    ax.plot([sx, vx], [ds_y-0.28, var_y+0.30],
            color='#AAAAAA', lw=1, ls='dotted', zorder=1)

# 变量框（第二行）
draw_box(ax, 2.5, var_y, 2.8, 0.60, '多属性态度\nATT',
         C_BOX_DARK, C_FILL_VAR, FONT_VAR, bold=True)
draw_box(ax, 7,   var_y, 2.8, 0.60, '评论评分\nRating (1–5 星)',
         C_BOX_DARK, C_FILL_VAR, FONT_VAR, bold=True)
draw_box(ax, 11.5,var_y, 2.8, 0.60, '评论者经验\nReviewer Experience',
         C_BOX_DARK, C_FILL_VAR, FONT_VAR, bold=True)

# H1 主效应箭头 ATT → Rating
draw_arrow_solid(ax, 3.9, var_y, 5.6, var_y, 'H1', label_side='top')

# H2 调节效应：Reviewer Exp. → 中点 ↓（折线形式）
mx_h2 = 7.0
ax.plot([11.5, mx_h2], [var_y-0.30, var_y-0.30],
        color=C_MOD, lw=1.8, ls='--', zorder=3)
ax.annotate('', xy=(mx_h2, var_y-0.01), xytext=(mx_h2, var_y-0.30),
            arrowprops=dict(arrowstyle='->', lw=1.8, color=C_MOD))
ax.text(9.25, var_y-0.55, 'H2（调节效应）',
        ha='center', va='center', fontsize=FONT_LABEL,
        fontweight='bold', color=C_MOD,
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=C_MOD, lw=1))

# 分隔线
ax.plot([0.5, 13.5], [4.90, 4.90], color='#444444', lw=1.8, ls='--')

# ──────────────────────────────────────────────
# 下半部分：H3/H4 子样本模型
# ──────────────────────────────────────────────
ax.add_patch(FancyBboxPatch((0.3, 4.35), 13.4, 0.50,
             boxstyle="round,pad=0.05",
             edgecolor=C_BOX_DARK, facecolor=C_FILL_HEAD, lw=1.5, zorder=2))
ax.text(7, 4.60, '子样本分析  H3/H4  (N = 298)',
        ha='center', va='center', fontsize=FONT_TITLE, fontweight='bold')

# 变量框（第三行）- 三个节点左中右对齐
v2_y = 3.40
draw_box(ax, 2.5, v2_y, 2.8, 0.60, '多属性态度\nATT',
         C_BOX_DARK, C_FILL_VAR, FONT_VAR, bold=True)
draw_box(ax, 7,   v2_y, 2.8, 0.60, '评论评分\nRating（控制变量）',
         C_BOX_MID, '#F5F5F5', FONT_VAR, bold=False)
draw_box(ax, 11.5,v2_y, 2.8, 0.60, '行为意向\nBI（0–3 量表）',
         C_BOX_DARK, C_FILL_VAR, FONT_VAR, bold=True)

# H3 主效应：ATT → BI（上弧，避开Rating框）
ax.annotate('', xy=(10.1, v2_y+0.30), xytext=(3.9, v2_y+0.30),
            arrowprops=dict(arrowstyle='->', lw=2.2, color=C_ARROW,
                            connectionstyle='arc3,rad=-0.35'))
ax.text(7, v2_y+1.05, 'H3（主效应）',
        ha='center', va='center', fontsize=FONT_LABEL, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='black', lw=1))

# Rating → BI 控制路径（水平直线）
draw_arrow_solid(ax, 8.4, v2_y, 10.1, v2_y, '', lw=1.5)
ax.text(9.25, v2_y+0.22, '控制',
        ha='center', va='bottom', fontsize=FONT_NOTE, color='#555555')

# H4 增量效度：ATT → BI（下弧，标注ΔR²）
ax.annotate('', xy=(10.1, v2_y-0.30), xytext=(3.9, v2_y-0.30),
            arrowprops=dict(arrowstyle='->', lw=2.0, color=C_INC,
                            linestyle='dashed',
                            connectionstyle='arc3,rad=0.35'))
ax.text(7, v2_y-1.05,
        r'H4：$\Delta R^2$ 增量效度（控制 Rating 后）',
        ha='center', va='center', fontsize=FONT_LABEL, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.30', fc='white', ec='#333333', lw=1.2))

# 注释说明
ax.text(7, 1.80,
        '注：ATT 与 Rating 来自独立数据源，无同源方差（CMV）问题；\n'
        'ATT 与 BI 均来自同一评论文本，存在 CMV 局限（Harman 单因子 = 76.8%）。',
        ha='center', va='center', fontsize=FONT_NOTE, style='italic', color='#444444',
        linespacing=1.5)

# ──────────────────────────────────────────────
# 图例
# ──────────────────────────────────────────────
leg_x, leg_y = 0.6, 1.10
ax.text(leg_x, leg_y, '图例：', ha='left', va='center',
        fontsize=FONT_NOTE, fontweight='bold')

# 实线
ax.annotate('', xy=(leg_x+1.2, leg_y-0.30), xytext=(leg_x+0.05, leg_y-0.30),
            arrowprops=dict(arrowstyle='->', lw=2.2, color=C_ARROW))
ax.text(leg_x+1.35, leg_y-0.30, '主效应 / 预测关系',
        ha='left', va='center', fontsize=FONT_NOTE)

# 虚线（调节）
ax.plot([leg_x+0.05, leg_x+1.2], [leg_y-0.62, leg_y-0.62],
        color=C_MOD, lw=1.8, ls='--')
ax.annotate('', xy=(leg_x+1.2, leg_y-0.62), xytext=(leg_x+1.05, leg_y-0.62),
            arrowprops=dict(arrowstyle='->', lw=1.8, color=C_MOD))
ax.text(leg_x+1.35, leg_y-0.62, '调节效应',
        ha='left', va='center', fontsize=FONT_NOTE)

# 虚线（增量效度）
ax.plot([leg_x+4.5, leg_x+5.65], [leg_y-0.30, leg_y-0.30],
        color=C_INC, lw=2.0, ls='--')
ax.annotate('', xy=(leg_x+5.65, leg_y-0.30), xytext=(leg_x+5.50, leg_y-0.30),
            arrowprops=dict(arrowstyle='->', lw=2.0, color=C_INC))
ax.text(leg_x+5.80, leg_y-0.30, r'$\Delta R^2$ 增量效度',
        ha='left', va='center', fontsize=FONT_NOTE)

# 点线（数据源连接）
ax.plot([leg_x+4.5, leg_x+5.65], [leg_y-0.62, leg_y-0.62],
        color='#AAAAAA', lw=1, ls='dotted')
ax.text(leg_x+5.80, leg_y-0.62, '数据源连接',
        ha='left', va='center', fontsize=FONT_NOTE)

plt.tight_layout(pad=0.3)
plt.savefig('E:/bi_ye_she_ji/latex_new/figures/fig5_1_framework.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Figure 5-1 done")
plt.close()
