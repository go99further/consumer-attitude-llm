# Predictive Validity of Consumer Multi-Attribute Attitude from Online Reviews

**Undergraduate Thesis, Dalian University of Technology (DUT), 2026**

[![PDF](https://img.shields.io/badge/PDF-Download-red?logo=adobe)](thesis_pdf/thesis_redacted.pdf) [![LaTeX](https://img.shields.io/badge/LaTeX-Source-green?logo=latex)](latex_new/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**📥 [Download Full Thesis (PDF, 49 pages, 911KB)](thesis_pdf/thesis_redacted.pdf)**

---

## 🎯 Research Overview

This thesis applies **Large Language Models (LLMs)** to extract consumer **multi-attribute attitudes** from Amazon product reviews, grounded in **Fishbein's Multi-Attribute Attitude Theory**:

$$\text{ATT} = \sum_{i=1}^{n} b_i \times e_i$$

where:
- **b_i** = belief strength (0.4–1.0, LLM-assessed)
- **e_i** = evaluative aspect (−1 / 0 / +1, sentiment polarity)
- **ATT** = overall attitude index

The study validates the **predictive validity** of LLM-extracted attitudes through four hypotheses tested on **1,331 Amazon reviews** of Burt's Bees Hand Cream Gift Set (ASIN: B004EDYQX6).

---

## 🔬 Research Framework

![Research Framework](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/latex_new/figures/fig5_1_framework.png)

**Key Design Feature: Three Independent Data Sources**

| Data Source | Variable | Origin | Purpose |
|---|---|---|---|
| 🤖 **Source 1** | ATT (Multi-Attribute Attitude) | LLM text extraction | Core predictor |
| ⭐ **Source 2** | Rating (1–5 stars) | Platform structured data | External criterion (H1) |
| 📊 **Source 3** | Reviewer Experience | Cross-category behavioral data | Moderator (H2) |

This design **eliminates Common Method Variance (CMV)** at its root for H1 and H2 by ensuring ATT, Rating, and Reviewer Experience originate from completely independent sources.

---

## 📊 Key Findings

### Hypothesis Testing Results

| Hypothesis | Statement | Result | Key Statistic |
|:---:|---|:---:|---|
| **H1** | ATT predicts Rating | ✅ **Supported** | β = 1.867, *p* < 0.001, *R*² = 0.560 |
| **H2** | Reviewer Experience moderates ATT–Rating | ✅ **Supported** | β = −0.008, *p* = 0.001 |
| **H3** | ATT predicts Behavioral Intention (BI) | ✅ **Supported** | β = 0.167, *p* = 0.004 |
| **H4** | ATT shows incremental validity beyond Rating | ✅ **Supported** | Δ*R*² = 0.018, *p* = 0.004 |

### H2: Moderation Effect (Simple Slopes Analysis)

![Moderation Effect](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/latex_new/figures/fig7_2_moderation.png)

**Finding**: Low-experience reviewers show **stronger ATT–Rating consistency** (slope = 0.741) than high-experience reviewers (slope = 0.573). The interaction term is significant (β = −0.008, *p* = 0.001), suggesting experienced reviewers rely less on multi-attribute decomposition when forming overall ratings.

### H4: Incremental Validity

![Incremental Validity](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/latex_new/figures/fig7_3_incremental.png)

**Finding**: After controlling for Rating, ATT still contributes **Δ*R*² = 0.018** (*F* = 8.32, *p* = 0.004) to predicting Behavioral Intention. This demonstrates that multi-attribute decomposition captures information **beyond** simple summary ratings.

---

## 🛠️ Methodology Highlights

### LLM-Based Variable Extraction

- **Model**: DeepSeek-V3.2 via API
- **Extraction Accuracy**: 100% (1,087/1,087 valid ATT values)
- **Hallucination Rate**: 4.2% (9/214 sampled beliefs)
- **Test-Retest Reliability**: *r* = 0.892 (DeepSeek vs. qwen-plus)
- **Evaluative Aspect Consistency**: 97.2% (105/108 beliefs)

### Methodological Contribution: Failed Attempts to Eliminate CMV

Section 8.5.1 of the thesis documents two **failed attempts** to construct an external behavioral proxy for BI:

1. **Repeat Purchase Behavior**: Only 7 users (1.1%) left multiple reviews for the same product — insufficient sample size.
2. **Helpful Vote Proxy**: 89% of reviews received zero helpful votes (extreme zero-inflation), and helpful votes measure *information quality*, not reviewer intention (construct mismatch).

These failures **prove by contradiction** the **irreplaceability** of the three-data-source design.

---

## 📁 Repository Structure

```
.
├── thesis_pdf/
│   ├── thesis_redacted.pdf    # 📥 Full thesis (49 pages, redacted)
│   └── preview_pages/         # PDF preview images (page_01.png - page_49.png)
├── latex_new/                 # LaTeX source (Chinese, ctexart)
│   ├── main.tex
│   ├── preamble.tex
│   ├── build.bat              # Windows build script (xelatex + biber)
│   ├── chapters/              # Chapter 1–9, abstract, cover, appendix
│   ├── refs/                  # Bibliography (refs01.bib – refs05.bib)
│   ├── figures/               # PNG figures and TikZ source
│   └── code/                  # Figure-generation Python scripts
├── code/                      # Analysis pipeline
│   ├── config.py.template     # API config template
│   ├── variable_extraction.py # LLM-based ATT/BI extraction
│   ├── study1_analysis.py     # H1/H2 (N = 1,157)
│   ├── study2_analysis.py     # H3/H4 (N = 298)
│   └── ...
├── data/                      # Processed datasets (CSV, ~1.3MB total)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start

**Prerequisites**: TeX Live 2024+ or MiKTeX with XeLaTeX and Biber, Chinese fonts (SimSun, SimHei, KaiTi, FangSong, STXihei).

### Build the Thesis

```bash
cd latex_new
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Or run `build.bat` on Windows.

### Run the Analysis

```bash
# 1. Set up API access
cp code/config.py.template code/config.py
# Edit code/config.py and insert your LLM API key

# 2. Install dependencies
pip install -r requirements.txt

# 3. Variable extraction (uses LLM API; slow)
python code/variable_extraction.py

# 4. Statistical analysis
python code/study1_analysis.py    # H1, H2
python code/study2_analysis.py    # H3, H4
```

### Data

The analysis uses **1,331 reviews** of Burt's Bees Hand Cream Gift Set (ASIN: `B004EDYQX6`) from the **Amazon Reviews 2023** dataset (McAuley Lab). Processed CSV datasets are in `data/`. Raw JSONL files are excluded due to size; the full source dataset is publicly available from the [McAuley Lab](https://amazon-reviews-2023.github.io/).

---

## 📖 Full Thesis (49 Pages)

Scroll down to read the complete thesis below. No download or click required.

![Page 1](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_01.png)

![Page 2](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_02.png)

![Page 3](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_03.png)

![Page 4](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_04.png)

![Page 5](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_05.png)

![Page 6](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_06.png)

![Page 7](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_07.png)

![Page 8](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_08.png)

![Page 9](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_09.png)

![Page 10](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_10.png)

![Page 11](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_11.png)

![Page 12](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_12.png)

![Page 13](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_13.png)

![Page 14](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_14.png)

![Page 15](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_15.png)

![Page 16](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_16.png)

![Page 17](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_17.png)

![Page 18](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_18.png)

![Page 19](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_19.png)

![Page 20](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_20.png)

![Page 21](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_21.png)

![Page 22](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_22.png)

![Page 23](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_23.png)

![Page 24](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_24.png)

![Page 25](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_25.png)

![Page 26](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_26.png)

![Page 27](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_27.png)

![Page 28](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_28.png)

![Page 29](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_29.png)

![Page 30](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_30.png)

![Page 31](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_31.png)

![Page 32](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_32.png)

![Page 33](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_33.png)

![Page 34](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_34.png)

![Page 35](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_35.png)

![Page 36](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_36.png)

![Page 37](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_37.png)

![Page 38](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_38.png)

![Page 39](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_39.png)

![Page 40](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_40.png)

![Page 41](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_41.png)

![Page 42](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_42.png)

![Page 43](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_43.png)

![Page 44](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_44.png)

![Page 45](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_45.png)

![Page 46](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_46.png)

![Page 47](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_47.png)

![Page 48](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_48.png)

![Page 49](https://raw.githubusercontent.com/go99further/consumer-attitude-llm/main/thesis_pdf/preview_pages/page_49.png)

---

## 🔐 Privacy Note

This is a **redacted public version** of the thesis. The following information has been removed: author name, advisor name, student ID, college and major, and acknowledgments. The research content, methodology, results, and figures are **unchanged**.

---

## 📜 License

- **Source code**: [MIT License](LICENSE)
- **Thesis text**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for academic reference

---

## 🙏 Acknowledgments

This research was conducted at **Dalian University of Technology (DUT)** as an undergraduate thesis project in 2026.

Special thanks to the open-source community: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/) (McAuley Lab), [DeepSeek](https://www.deepseek.com/) for LLM API access, and the LaTeX/Python scientific computing ecosystem.
