"""
H2调节效应图（简单斜率图）- 修正版
展示评论者经验对ATT-Rating关系的调节作用
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib import font_manager

# 设置中文字体和数学字体
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['mathtext.fontset'] = 'stix'  # 使用STIX字体显示数学符号

# 数据来自论文第6.2.5节
# 简单斜率分析结果
high_re_slope = 0.573  # 高经验组（+1SD）
low_re_slope = 0.741   # 低经验组（-1SD）

# ATT均值和标准差（来自表5.1）
att_mean = 1.054
att_sd = 1.208

# Rating均值（来自表5.1）
rating_mean = 4.440

# 创建ATT的范围（-1SD到+1SD）
att_range = np.array([att_mean - att_sd, att_mean + att_sd])

# 计算对应的Rating预测值
# 高经验组的预测线
high_re_rating = rating_mean + high_re_slope * (att_range - att_mean)

# 低经验组的预测线
low_re_rating = rating_mean + low_re_slope * (att_range - att_mean)

# 创建图形
fig, ax = plt.subplots(figsize=(10, 7))

# 绘制两条简单斜率线
ax.plot(att_range, high_re_rating,
        linewidth=2.5,
        color='#E74C3C',  # 红色
        marker='o',
        markersize=8,
        label='高经验组 (+1SD)\n斜率 = 0.573***',
        linestyle='-')

ax.plot(att_range, low_re_rating,
        linewidth=2.5,
        color='#3498DB',  # 蓝色
        marker='s',
        markersize=8,
        label='低经验组 (-1SD)\n斜率 = 0.741***',
        linestyle='--')

# 设置坐标轴标签
ax.set_xlabel('多属性态度 (ATT)', fontsize=14, fontweight='bold')
ax.set_ylabel('评论评分 (Rating)', fontsize=14, fontweight='bold')

# 设置坐标轴范围
ax.set_xlim(att_range[0] - 0.2, att_range[1] + 0.2)
ax.set_ylim(2.5, 5.5)

# 添加网格
ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)

# 添加图例
legend = ax.legend(loc='upper left', fontsize=12, frameon=True,
                   shadow=True, fancybox=True)
legend.get_frame().set_alpha(0.9)

# 添加注释说明（使用希腊字母beta的unicode）
textstr = '注：***p < 0.001\n交互项 β = -0.008, p = 0.001\n低经验组态度-评分一致性更强'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

# 美化图形
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)

plt.tight_layout()

# 保存图形
output_path = 'E:/bi_ye_she_ji/output/figures/h2_moderation_plot.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"H2图形已保存至: {output_path}")

plt.close()
