# 基于在线评论的消费者多属性态度预测效度研究

**大连理工大学本科毕业论文，2026 届**

[![PDF](https://img.shields.io/badge/PDF-下载论文-red?logo=adobe)](thesis_pdf/thesis_redacted.pdf) [![LaTeX](https://img.shields.io/badge/LaTeX-源码-green?logo=latex)](latex_new/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**[下载完整论文 PDF（49 页，909KB）](thesis_pdf/thesis_redacted.pdf)**

> 本 README 图片通过 GitHub Pages 加载，国内可直接访问，无需翻墙。

---

## 研究概述

本论文以 **Fishbein 多属性态度理论** 为基础，运用 **大语言模型（LLM）** 从亚马逊商品评论中抽取消费者的多属性态度：

$$\text{ATT} = \sum_{i=1}^{n} b_i \times e_i$$

其中 `b_i` 为信念强度（0.4–1.0，LLM 评估），`e_i` 为评价方向（−1 / 0 / +1），ATT 为整体态度指数。

研究以 Burt's Bees 护手霜礼盒（ASIN：B004EDYQX6）的 **1,331 条亚马逊评论** 为样本，通过四个假设系统检验 LLM 抽取态度的 **预测效度**。

---

## 研究范式定位

在线评论研究存在两类范式：第一类关注评论对潜在购买者决策的影响（评论 → 他人），第二类关注评论者自身的态度–行为关系（评论者 → 自身）。本研究属于第二类，将评论文本视为评论者态度的自然表达，而非影响他人的信息载体。

<div align="center">
<b>表 1　在线评论研究两类范式对比</b>

<table>
<thead>
<tr style="border-top: 2px solid black; border-bottom: 1px solid black;">
<th style="border: none; padding: 6px 12px; text-align: left;">对比维度</th>
<th style="border: none; padding: 6px 12px; text-align: left;">第一类：评论 → 他人决策</th>
<th style="border: none; padding: 6px 12px; text-align: left;">第二类：本研究定位</th>
</tr>
</thead>
<tbody>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">研究对象</td><td style="border: none; padding: 4px 12px;">潜在购买者</td><td style="border: none; padding: 4px 12px;">评论者自身</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">核心变量关系</td><td style="border: none; padding: 4px 12px;">评论特征 → 消费者采纳/购买</td><td style="border: none; padding: 4px 12px;">信念 → 态度 → 评分/行为意向</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">数据来源</td><td style="border: none; padding: 4px 12px;">问卷、实验、平台聚合数据</td><td style="border: none; padding: 4px 12px;">评论文本（自然发生数据）</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">方法论工具</td><td style="border: none; padding: 4px 12px;">传统实证方法</td><td style="border: none; padding: 4px 12px;">LLM 文本提取 + 平台客观数据</td></tr>
<tr style="border: none; border-bottom: 2px solid black;"><td style="border: none; padding: 4px 12px;">CMV 控制</td><td style="border: none; padding: 4px 12px;">依赖程序控制或实验设计</td><td style="border: none; padding: 4px 12px;">三独立数据源从设计层面消除</td></tr>
</tbody>
</table>

注：CMV = Common Method Variance，同源方差。
</div>

---

## 研究框架

本研究采用三套独立数据源的设计，将 ATT（LLM 文本抽取）、Rating（平台结构化字段）和 Reviewer Experience（跨品类行为数据）分离至不同来源，从设计层面消除 H1/H2 的共同方法偏差。H3/H4 中 ATT 与 BI 均来自同一评论文本，存在 CMV 局限，在论文中诚实报告。

<div align="center">

![研究框架与假设检验路径图](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig5_1_framework.png)

图 1　研究框架与假设检验路径图
</div>

<div align="center">
<b>表 2　三数据源设计</b>

<table>
<thead>
<tr style="border-top: 2px solid black; border-bottom: 1px solid black;">
<th style="border: none; padding: 6px 12px; text-align: left;">数据源</th>
<th style="border: none; padding: 6px 12px; text-align: left;">变量</th>
<th style="border: none; padding: 6px 12px; text-align: left;">来源</th>
<th style="border: none; padding: 6px 12px; text-align: left;">作用</th>
</tr>
</thead>
<tbody>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">数据源 ①</td><td style="border: none; padding: 4px 12px;">ATT（多属性态度）</td><td style="border: none; padding: 4px 12px;">LLM 文本抽取</td><td style="border: none; padding: 4px 12px;">核心预测变量</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">数据源 ②</td><td style="border: none; padding: 4px 12px;">评分（1–5 星）</td><td style="border: none; padding: 4px 12px;">平台结构化字段</td><td style="border: none; padding: 4px 12px;">外部效标（H1）</td></tr>
<tr style="border: none; border-bottom: 2px solid black;"><td style="border: none; padding: 4px 12px;">数据源 ③</td><td style="border: none; padding: 4px 12px;">评论者经验</td><td style="border: none; padding: 4px 12px;">跨品类行为数据</td><td style="border: none; padding: 4px 12px;">调节变量（H2）</td></tr>
</tbody>
</table>
</div>

---

## 主要研究发现

四个假设全部获得支持。H1 表明 LLM 抽取的多属性态度能够有效预测消费者评分（解释 56% 的方差）；H2 发现评论者经验显著调节该关系；H3 证实 ATT 对行为意向的预测力；H4 进一步表明 ATT 在控制评分后仍具有增量预测效度。

<div align="center">
<b>表 3　假设检验结果汇总</b>

<table>
<thead>
<tr style="border-top: 2px solid black; border-bottom: 1px solid black;">
<th style="border: none; padding: 6px 12px; text-align: center;">假设</th>
<th style="border: none; padding: 6px 12px; text-align: left;">内容</th>
<th style="border: none; padding: 6px 12px; text-align: center;">结论</th>
<th style="border: none; padding: 6px 12px; text-align: left;">关键统计量</th>
</tr>
</thead>
<tbody>
<tr style="border: none;"><td style="border: none; padding: 4px 12px; text-align: center;">H1</td><td style="border: none; padding: 4px 12px;">ATT 正向预测评分</td><td style="border: none; padding: 4px 12px; text-align: center;">支持</td><td style="border: none; padding: 4px 12px;">β = 1.867，<i>p</i> &lt; 0.001，<i>R</i>² = 0.560</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px; text-align: center;">H2</td><td style="border: none; padding: 4px 12px;">评论者经验调节 ATT–评分关系</td><td style="border: none; padding: 4px 12px; text-align: center;">支持</td><td style="border: none; padding: 4px 12px;">β = −0.008，<i>p</i> = 0.001</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px; text-align: center;">H3</td><td style="border: none; padding: 4px 12px;">ATT 正向预测行为意向（BI）</td><td style="border: none; padding: 4px 12px; text-align: center;">支持</td><td style="border: none; padding: 4px 12px;">β = 0.167，<i>p</i> = 0.004</td></tr>
<tr style="border: none; border-bottom: 2px solid black;"><td style="border: none; padding: 4px 12px; text-align: center;">H4</td><td style="border: none; padding: 4px 12px;">ATT 在评分之上具有增量效度</td><td style="border: none; padding: 4px 12px; text-align: center;">支持</td><td style="border: none; padding: 4px 12px;">Δ<i>R</i>² = 0.018，<i>p</i> = 0.004</td></tr>
</tbody>
</table>
</div>

### H2：调节效应

简单斜率分析显示，低经验评论者（−1SD）的 ATT–评分斜率为 0.741，高经验评论者（+1SD）为 0.573，差异显著。这表明经验较少的评论者在给出评分时，更多地依赖对各属性的逐一评价；而经验丰富的评论者可能形成了更整体化的判断模式，其评分与多属性分解的对应关系相对较弱。

<div align="center">

![H2 调节效应简单斜率图](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig7_2_moderation.png)

图 2　评论者经验对 ATT–Rating 关系的调节效应（简单斜率分析）
</div>

### H4：增量效度

层次回归分析中，模型 1 仅含控制变量，模型 2 加入 Rating，模型 3 在模型 2 基础上加入 ATT。结果显示 ATT 在控制 Rating 后仍贡献 Δ*R*² = 0.018（*F* = 8.32，*p* = 0.004），说明多属性态度分解捕获了评分所不能反映的额外信息——消费者对具体产品属性的细粒度评价。

<div align="center">

![H4 增量效度层次回归图](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig7_3_incremental.png)

图 3　ATT 增量效度的层次回归分析（三模型 <i>R</i>² 对比）
</div>

---

## 方法亮点

本研究使用 DeepSeek-V3.2 通过 API 对全部 1,331 条评论进行信念抽取与态度计算。为验证 LLM 抽取的可靠性，从计算准确率、幻觉率、重测信度和评价方向一致性四个维度进行了系统检验。

<div align="center">
<b>表 4　LLM 变量抽取质量指标</b>

<table>
<thead>
<tr style="border-top: 2px solid black; border-bottom: 1px solid black;">
<th style="border: none; padding: 6px 12px; text-align: left;">指标</th>
<th style="border: none; padding: 6px 12px; text-align: left;">数值</th>
<th style="border: none; padding: 6px 12px; text-align: left;">说明</th>
</tr>
</thead>
<tbody>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">抽取成功率</td><td style="border: none; padding: 4px 12px;">100%</td><td style="border: none; padding: 4px 12px;">1,087 / 1,087 个有效 ATT</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">幻觉率</td><td style="border: none; padding: 4px 12px;">4.2%</td><td style="border: none; padding: 4px 12px;">抽样 214 条信念中 9 条无法溯源至原文</td></tr>
<tr style="border: none;"><td style="border: none; padding: 4px 12px;">重测信度</td><td style="border: none; padding: 4px 12px;"><i>r</i> = 0.892</td><td style="border: none; padding: 4px 12px;">DeepSeek-V3.2 与 qwen-plus 独立抽取对比</td></tr>
<tr style="border: none; border-bottom: 2px solid black;"><td style="border: none; padding: 4px 12px;">评价方向一致性</td><td style="border: none; padding: 4px 12px;">97.2%</td><td style="border: none; padding: 4px 12px;">108 条信念中 105 条极性判断一致</td></tr>
</tbody>
</table>
</div>

### 消除 CMV 的失败尝试

论文 8.5.1 节记录了为 BI 构建外部行为代理变量的两次失败尝试：（1）重复购买行为——仅 7 个用户（1.1%）在同一商品下留过多条评论，样本量不足；（2）有用投票代理——89% 的评论 0 票（极端零膨胀），且有用投票衡量的是信息质量而非评论者意图（构念错配）。这两次失败以反证形式证明了三数据源设计的不可替代性。

---

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
