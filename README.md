# 基于在线评论的消费者多属性态度预测效度研究

**大连理工大学本科毕业论文，2026 届**

[![PDF](https://img.shields.io/badge/PDF-下载-red?logo=adobe)](thesis_pdf/thesis_redacted.pdf) [![LaTeX](https://img.shields.io/badge/LaTeX-源码-green?logo=latex)](latex_new/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**📥 [下载完整论文 PDF（49 页，911KB）](thesis_pdf/thesis_redacted.pdf)**

> 📌 **国内访问说明**：本 README 中的图片均通过 **GitHub Pages**（`go99further.github.io`）加载，无需翻墙即可在大陆地区直接显示。

---

## 🎯 研究概述

本论文以 **Fishbein 多属性态度理论** 为基础，运用 **大语言模型（LLM）** 从亚马逊商品评论中抽取消费者的 **多属性态度**：

$$\text{ATT} = \sum_{i=1}^{n} b_i \times e_i$$

其中：
- **b_i** = 信念强度（0.4–1.0，由 LLM 评估）
- **e_i** = 评价方向（−1 / 0 / +1，情感极性）
- **ATT** = 整体态度指数

研究以 **Burt's Bees 护手霜礼盒**（ASIN：B004EDYQX6）的 **1,331 条亚马逊评论** 为样本，通过四个假设系统检验 LLM 抽取的多属性态度的 **预测效度**。

---

## 🔬 研究框架

![研究框架](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig5_1_framework.png)

**核心设计：三套独立数据源**

| 数据源 | 变量 | 来源 | 作用 |
|---|---|---|---|
| 🤖 **数据源 1** | ATT（多属性态度） | LLM 文本抽取 | 核心预测变量 |
| ⭐ **数据源 2** | 评分（1–5 星） | 平台结构化数据 | 外部效标（H1） |
| 📊 **数据源 3** | 评论者经验 | 跨品类行为数据 | 调节变量（H2） |

该设计在 H1 与 H2 上 **从源头消除了共同方法偏差（CMV）**：ATT、评分、评论者经验来自完全独立的数据源。

---

## 📊 主要研究发现

### 四个假设的检验结果

| 假设 | 内容 | 结论 | 关键统计量 |
|:---:|---|:---:|---|
| **H1** | ATT 正向预测评分 | ✅ **成立** | β = 1.867，*p* < 0.001，*R*² = 0.560 |
| **H2** | 评论者经验调节 ATT–评分关系 | ✅ **成立** | β = −0.008，*p* = 0.001 |
| **H3** | ATT 正向预测行为意向（BI） | ✅ **成立** | β = 0.167，*p* = 0.004 |
| **H4** | ATT 在评分之上具有增量效度 | ✅ **成立** | Δ*R*² = 0.018，*p* = 0.004 |

### H2：调节效应（简单斜率分析）

![调节效应](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig7_2_moderation.png)

**发现**：低经验评论者的 ATT–评分一致性更强（斜率 = 0.741），高经验评论者较弱（斜率 = 0.573）。交互项显著（β = −0.008，*p* = 0.001），说明经验丰富的评论者在形成总体评分时较少依赖多属性分解。

### H4：增量效度

![增量效度](https://go99further.github.io/consumer-attitude-llm/latex_new/figures/fig7_3_incremental.png)

**发现**：在控制评分之后，ATT 对行为意向仍贡献 **Δ*R*² = 0.018**（*F* = 8.32，*p* = 0.004）。这表明多属性分解所携带的信息 **超越了** 简单的总体评分。

---

## 🛠️ 方法亮点

### 基于 LLM 的变量抽取

- **模型**：DeepSeek-V3.2（API 调用）
- **抽取成功率**：100%（1,087/1,087 个有效 ATT）
- **幻觉率**：4.2%（抽样 214 条信念中 9 条）
- **重测信度**：*r* = 0.892（DeepSeek 与 qwen-plus 对比）
- **评价方向一致性**：97.2%（105/108 条信念）

### 方法论贡献：消除 CMV 的失败尝试

论文 8.5.1 节记录了为 BI 构建 **外部行为代理变量** 的两次 **失败尝试**：

1. **重复购买行为**：仅 7 个用户（1.1%）在同一商品下留过多条评论——样本量不足。
2. **有用投票代理**：89% 的评论 0 票（极端零膨胀），且有用投票衡量的是 *信息质量*，而非评论者意图（构念错配）。

这两次失败 **以反证形式** 证明了三数据源设计的 **不可替代性**。

---

## 📁 仓库结构

```
.
├── thesis_pdf/
│   ├── thesis_redacted.pdf    # 📥 完整论文（49 页，已脱敏）
│   └── preview_pages/         # PDF 预览图（page_01.png – page_49.png）
├── latex_new/                 # LaTeX 源码（中文，ctexart）
│   ├── main.tex
│   ├── preamble.tex
│   ├── build.bat              # Windows 编译脚本（xelatex + biber）
│   ├── chapters/              # 第 1–9 章、摘要、封面、附录
│   ├── refs/                  # 参考文献（refs01.bib – refs05.bib）
│   ├── figures/               # PNG 图片与 TikZ 源码
│   └── code/                  # 图表生成 Python 脚本
├── code/                      # 数据分析流程
│   ├── config.py.template     # API 配置模板
│   ├── variable_extraction.py # 基于 LLM 的 ATT/BI 抽取
│   ├── study1_analysis.py     # H1/H2 分析（N = 1,157）
│   ├── study2_analysis.py     # H3/H4 分析（N = 298）
│   └── ...
├── data/                      # 处理后数据集（CSV，约 1.3MB）
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 快速开始

**前置依赖**：TeX Live 2024+ 或 MiKTeX，需支持 XeLaTeX 与 Biber，以及中文字体（SimSun、SimHei、KaiTi、FangSong、STXihei）。

### 编译论文

```bash
cd latex_new
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Windows 用户可直接运行 `build.bat`。

### 运行分析

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

### 数据说明

分析所用数据为 Burt's Bees 护手霜礼盒（ASIN：`B004EDYQX6`）在 **Amazon Reviews 2023** 数据集（McAuley Lab）中的 **1,331 条评论**。处理后的 CSV 数据集位于 `data/`；原始 JSONL 文件因体积过大未上传，可从 [McAuley Lab 官网](https://amazon-reviews-2023.github.io/) 公开获取。

---

## 📖 论文全文（49 页）

下方按顺序展示完整论文内容，无需点击或下载即可直接阅读。

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

## 🔐 隐私声明

本仓库为 **脱敏后的公开版本**。已删除：作者姓名、指导教师姓名、学号、学院与专业、致谢部分。研究内容、方法、结果与图表 **均未改动**。

---

## 📜 许可协议

- **源代码**：[MIT License](LICENSE)
- **论文文本**：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，可用于学术参考

---

## 🙏 致谢

本研究为 **大连理工大学（DUT）** 2026 届本科毕业论文项目。

特别感谢开源社区：[Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)（McAuley Lab）、[DeepSeek](https://www.deepseek.com/) 提供的 LLM API，以及 LaTeX/Python 科学计算生态。
