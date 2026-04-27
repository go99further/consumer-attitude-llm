# 基于在线评论的消费者多属性态度预测效度研究

**大连理工大学本科毕业论文，2026 届**

[![PDF](https://img.shields.io/badge/PDF-下载论文-red?logo=adobe)](thesis_pdf/thesis_redacted.pdf) [![LaTeX](https://img.shields.io/badge/LaTeX-源码-green?logo=latex)](latex_new/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**📥 [下载完整论文 PDF（49 页，909KB）](thesis_pdf/thesis_redacted.pdf)**

> 📌 本 README 图片通过 GitHub Pages 加载，国内可直接访问，无需翻墙。

---

## 研究概述

本论文以 **Fishbein 多属性态度理论** 为基础，运用 **大语言模型（LLM）** 从亚马逊商品评论中抽取消费者的多属性态度：

$$\text{ATT} = \sum_{i=1}^{n} b_i \times e_i$$

其中 $b_i$ 为信念强度（0.4–1.0，LLM 评估），$e_i$ 为评价方向（−1 / 0 / +1），ATT 为整体态度指数。

研究以 Burt's Bees 护手霜礼盒（ASIN：B004EDYQX6）的 **1,331 条亚马逊评论** 为样本，通过四个假设系统检验 LLM 抽取态度的 **预测效度**。

---

## 研究范式定位

本研究属于在线评论研究的第二类范式——关注评论者自身的态度–行为关系，而非评论对他人决策的影响。

<div align="center">

<table>
<caption><b>表 1　在线评论研究两类范式对比</b></caption>
<thead>
<tr><th>对比维度</th><th>第一类：评论 → 他人决策</th><th>第二类：本研究定位</th></tr>
</thead>
<tbody>
<tr><td>研究对象</td><td>潜在购买者</td><td>评论者自身</td></tr>
<tr><td>核心变量关系</td><td>评论特征 → 消费者采纳/购买</td><td>信念 → 态度 → 评分/行为意向</td></tr>
<tr><td>数据来源</td><td>问卷、实验、平台聚合数据</td><td>评论文本（自然发生数据）</td></tr>
<tr><td>方法论工具</td><td>传统实证方法</td><td>LLM 文本提取 + 平台客观数据</td></tr>
<tr><td>CMV 控制</td><td>依赖程序控制或实验设计</td><td>三独立数据源从设计层面消除</td></tr>
</tbody>
</table>

<sub>注：CMV = Common Method Variance，同源方差。</sub>

</div>

---

## 研究框架

<div align="center">

![研究框架](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig5_1_framework.png)

</div>

**核心设计：三套独立数据源**

<div align="center">

<table>
<caption><b>表 2　三数据源设计</b></caption>
<thead>
<tr><th>数据源</th><th>变量</th><th>来源</th><th>作用</th></tr>
</thead>
<tbody>
<tr><td>数据源 ①</td><td>ATT（多属性态度）</td><td>LLM 文本抽取</td><td>核心预测变量</td></tr>
<tr><td>数据源 ②</td><td>评分（1–5 星）</td><td>平台结构化字段</td><td>外部效标（H1）</td></tr>
<tr><td>数据源 ③</td><td>评论者经验</td><td>跨品类行为数据</td><td>调节变量（H2）</td></tr>
</tbody>
</table>

</div>

该设计在 H1 与 H2 上从源头消除了共同方法偏差（CMV）：ATT、评分、评论者经验来自完全独立的数据源。

---

## 主要研究发现

<div align="center">

<table>
<caption><b>表 3　假设检验结果汇总</b></caption>
<thead>
<tr><th>假设</th><th>内容</th><th>结论</th><th>关键统计量</th></tr>
</thead>
<tbody>
<tr><td><b>H1</b></td><td>ATT 正向预测评分</td><td>✅ 成立</td><td>β = 1.867，<i>p</i> &lt; 0.001，<i>R</i>² = 0.560</td></tr>
<tr><td><b>H2</b></td><td>评论者经验调节 ATT–评分关系</td><td>✅ 成立</td><td>β = −0.008，<i>p</i> = 0.001</td></tr>
<tr><td><b>H3</b></td><td>ATT 正向预测行为意向（BI）</td><td>✅ 成立</td><td>β = 0.167，<i>p</i> = 0.004</td></tr>
<tr><td><b>H4</b></td><td>ATT 在评分之上具有增量效度</td><td>✅ 成立</td><td>Δ<i>R</i>² = 0.018，<i>p</i> = 0.004</td></tr>
</tbody>
</table>

</div>

### H2：调节效应（简单斜率分析）

<div align="center">

![调节效应](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig7_2_moderation.png)

</div>

低经验评论者的 ATT–评分一致性更强（斜率 = 0.741），高经验评论者较弱（斜率 = 0.573）。交互项显著（β = −0.008，*p* = 0.001），说明经验丰富的评论者在形成总体评分时较少依赖多属性分解。

### H4：增量效度

<div align="center">

![增量效度](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig7_3_incremental.png)

</div>

在控制评分之后，ATT 对行为意向仍贡献 Δ*R*² = 0.018（*F* = 8.32，*p* = 0.004），表明多属性分解所携带的信息超越了简单的总体评分。

---

## 方法亮点

<div align="center">

<table>
<caption><b>表 4　LLM 变量抽取质量指标</b></caption>
<thead>
<tr><th>指标</th><th>数值</th><th>说明</th></tr>
</thead>
<tbody>
<tr><td>抽取成功率</td><td>100%</td><td>1,087 / 1,087 个有效 ATT</td></tr>
<tr><td>幻觉率</td><td>4.2%</td><td>抽样 214 条信念中 9 条</td></tr>
<tr><td>重测信度</td><td><i>r</i> = 0.892</td><td>DeepSeek-V3.2 vs. qwen-plus</td></tr>
<tr><td>评价方向一致性</td><td>97.2%</td><td>105 / 108 条信念</td></tr>
<tr><td>使用模型</td><td>DeepSeek-V3.2</td><td>API 调用</td></tr>
</tbody>
</table>

</div>

### 消除 CMV 的失败尝试

论文 8.5.1 节记录了为 BI 构建外部行为代理变量的两次失败尝试：（1）重复购买行为——仅 7 个用户（1.1%）在同一商品下留过多条评论，样本量不足；（2）有用投票代理——89% 的评论 0 票（极端零膨胀），且有用投票衡量的是信息质量而非评论者意图（构念错配）。这两次失败以反证形式证明了三数据源设计的不可替代性。

---

## 论文全文（49 页）

下方按顺序展示完整论文，无需点击或下载即可直接阅读。

![第 1 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_01.png)

![第 2 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_02.png)

![第 3 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_03.png)

![第 4 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_04.png)

![第 5 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_05.png)

![第 6 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_06.png)

![第 7 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_07.png)

![第 8 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_08.png)

![第 9 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_09.png)

![第 10 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_10.png)

![第 11 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_11.png)

![第 12 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_12.png)

![第 13 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_13.png)

![第 14 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_14.png)

![第 15 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_15.png)

![第 16 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_16.png)

![第 17 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_17.png)

![第 18 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_18.png)

![第 19 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_19.png)

![第 20 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_20.png)

![第 21 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_21.png)

![第 22 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_22.png)

![第 23 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_23.png)

![第 24 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_24.png)

![第 25 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_25.png)

![第 26 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_26.png)

![第 27 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_27.png)

![第 28 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_28.png)

![第 29 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_29.png)

![第 30 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_30.png)

![第 31 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_31.png)

![第 32 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_32.png)

![第 33 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_33.png)

![第 34 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_34.png)

![第 35 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_35.png)

![第 36 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_36.png)

![第 37 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_37.png)

![第 38 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_38.png)

![第 39 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_39.png)

![第 40 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_40.png)

![第 41 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_41.png)

![第 42 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_42.png)

![第 43 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_43.png)

![第 44 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_44.png)

![第 45 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_45.png)

![第 46 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_46.png)

![第 47 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_47.png)

![第 48 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_48.png)

![第 49 页](https://go99further.github.io/consumer-attitude-llm/thesis_pdf/preview_pages/page_49.png)

---

## 研究复现

```bash
# 1. 配置 API
cp code/config.py.template code/config.py
# 编辑 code/config.py，填入你的 LLM API key

# 2. 安装依赖
pip install -r requirements.txt

# 3. 变量抽取（调用 LLM API，耗时较长）
python code/variable_extraction.py

# 4. 统计分析
python code/study1_analysis.py    # H1, H2
python code/study2_analysis.py    # H3, H4
```

分析所用数据为 Burt's Bees 护手霜礼盒（ASIN：`B004EDYQX6`）在 [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)（McAuley Lab）中的 1,331 条评论。处理后的 CSV 位于 `data/`，原始 JSONL 因体积过大未上传。

---

## 仓库结构

```
.
├── thesis_pdf/
│   ├── thesis_redacted.pdf        # 完整论文（49 页，已脱敏）
│   └── preview_pages/             # PDF 预览图
├── latex_new/                     # LaTeX 源码（ctexart）
│   ├── main.tex
│   ├── preamble.tex
│   ├── build.bat                  # Windows 编译脚本
│   ├── chapters/                  # 第 1–9 章、摘要、封面、附录
│   ├── refs/                      # 参考文献
│   ├── figures/                   # 图片与 TikZ 源码
│   └── code/                      # 图表生成脚本
├── code/                          # 数据分析流程
│   ├── config.py.template         # API 配置模板
│   ├── variable_extraction.py     # LLM 变量抽取
│   ├── study1_analysis.py         # H1/H2（N = 1,157）
│   ├── study2_analysis.py         # H3/H4（N = 298）
│   └── ...
├── data/                          # 处理后数据集（CSV）
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 隐私声明

本仓库为脱敏后的公开版本。已删除：作者姓名、指导教师姓名、学号、学院与专业、致谢内容。研究内容、方法、结果与图表均未改动。

---

## 许可协议

- **源代码**：[MIT License](LICENSE)
- **论文文本**：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，可用于学术参考

---

## 致谢

本研究为大连理工大学 2026 届本科毕业论文项目。感谢 [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)（McAuley Lab）、[DeepSeek](https://www.deepseek.com/) 及 LaTeX/Python 开源生态。
