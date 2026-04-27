"""
H4增量效度图（ΔR²柱状图）- 修正版
展示ATT在控制Rating后对BI的增量预测力
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib import font_manager

# 设置中文字体和数学字体
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['mathtext.fontset'] = 'stix'  # 使用STIX字体显示数学符号

# 数据来自论文表5.5（H4层次回归结果）
models = ['模型1\n(仅控制变量)', '模型2\n(+Rating)', '模型3\n(+ATT)']
r_squared = [0.022, 0.336, 0.354]
delta_r_squared = [0, 0.314, 0.018]

# 创建图形
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ========== 左图：R²累积柱状图 ==========
x_pos = np.arange(len(models))
colors = ['#95A5A6', '#3498DB', '#E74C3C']

bars = ax1.bar(x_pos, r_squared, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# 添加数值标签（使用$R^2$来正确显示上标）
for i, (bar, r2) in enumerate(zip(bars, r_squared)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'$R^2$ = {r2:.3f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylabel('$R^2$ (解释方差比例)', fontsize=13, fontweight='bold')
ax1.set_xlabel('层次回归模型', fontsize=13, fontweight='bold')
ax1.set_title('(a) 层次回归$R^2$变化', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(models, fontsize=10)
ax1.set_ylim(0, 0.4)
ax1.grid(axis='y', alpha=0.3, linestyle=':', linewidth=0.8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ========== 右图：ΔR²增量柱状图 ==========
delta_models = ['模型2 vs 模型1\n(Rating的贡献)', '模型3 vs 模型2\n(ATT的增量贡献)']
delta_values = [0.314, 0.018]
delta_colors = ['#3498DB', '#E74C3C']
significance = ['***', '**']

x_pos2 = np.arange(len(delta_models))
bars2 = ax2.bar(x_pos2, delta_values, color=delta_colors, alpha=0.8,
                edgecolor='black', linewidth=1.5)

# 添加数值标签和显著性标记（使用$\Delta R^2$来正确显示）
for i, (bar, delta, sig) in enumerate(zip(bars2, delta_values, significance)):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.005,
             r'$\Delta R^2$ = ' + f'{delta:.3f}{sig}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_ylabel(r'$\Delta R^2$ (增量解释方差)', fontsize=13, fontweight='bold')
ax2.set_xlabel('模型比较', fontsize=13, fontweight='bold')
ax2.set_title('(b) ATT的增量效度', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x_pos2)
ax2.set_xticklabels(delta_models, fontsize=10)
ax2.set_ylim(0, 0.35)
ax2.grid(axis='y', alpha=0.3, linestyle=':', linewidth=0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# 添加注释（使用$\Delta R^2$来正确显示）
textstr = r'注：**p < 0.01, ***p < 0.001' + '\n' + r'F($\Delta R^2$) = 8.32, p = 0.004' + '\nN = 298'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax2.text(0.98, 0.95, textstr, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right', bbox=props)

plt.tight_layout()

# 保存图形
output_path = 'E:/bi_ye_she_ji/output/figures/h4_incremental_validity_plot.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"H4图形已保存至: {output_path}")

plt.close()
