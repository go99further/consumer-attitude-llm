# Predictive Validity of Consumer Multi-Attribute Attitude from Online Reviews

> Undergraduate thesis, Dalian University of Technology (DUT), 2026.

This repository contains the LaTeX source and analysis code for an undergraduate
thesis applying Large Language Models (LLMs) to extract consumer multi-attribute
attitudes from Amazon product reviews, grounded in Fishbein's Multi-Attribute
Attitude Theory: **ATT = Σ (b_i × e_i)**.

## Overview

The study validates the predictive validity of LLM-extracted attitudes through
four hypotheses:

| H | Statement | Result | Key Statistic |
|---|---|---|---|
| H1 | ATT predicts Rating | Supported | β = 1.867, p < 0.001, R² = 0.560 |
| H2 | Reviewer Experience moderates ATT–Rating | Supported (exploratory) | β = −0.008, p = 0.001 |
| H3 | ATT predicts Behavioral Intention (BI) | Supported | β = 0.167, p = 0.004 |
| H4 | ATT shows incremental validity beyond Rating | Supported | ΔR² = 0.018, p = 0.004 |

A central methodological contribution is the **three-data-source design**
(LLM text extraction / platform structured ratings / cross-category behavioral
data) that eliminates Common Method Variance (CMV) at its root for H1 and H2.
Section 8.5.1 of the thesis further documents two failed attempts to construct
an external behavioral proxy for BI, demonstrating the irreplaceability of the
three-source design.

## Repository Layout

```
.
├── latex_new/                 # Thesis LaTeX source (Chinese, ctexart)
│   ├── main.tex
│   ├── preamble.tex
│   ├── build.bat              # Windows build script (xelatex + biber)
│   ├── chapters/              # Chapter 1–9, abstract, cover, appendix
│   ├── refs/                  # Bibliography (refs01.bib – refs05.bib)
│   ├── figures/               # PNG figures and TikZ source
│   └── code/                  # Figure-generation Python scripts
├── code/                      # Analysis pipeline
│   ├── config.py.template     # API config template (copy to config.py)
│   ├── variable_extraction.py # LLM-based ATT/BI/PV extraction
│   ├── compute_reviewer_experience.py
│   ├── llm_reliability_check.py
│   ├── run_retest_reliability.py
│   ├── study1_analysis.py     # H1/H2 (N = 1,157)
│   ├── study2_analysis.py     # H3/H4 (N = 298)
│   └── ...
├── data/                      # Processed datasets (CSV)
│   ├── cleaned_reviews.csv
│   ├── final_analysis_data_complete.csv
│   ├── reviewer_experience.csv
│   └── ...
├── requirements.txt
├── .gitignore
└── README.md
```

## Building the Thesis

### Prerequisites
- TeX Live 2024+ or MiKTeX with **XeLaTeX** and **Biber**
- Chinese fonts: SimSun, SimHei, KaiTi, FangSong, STXihei (Windows built-in)

### Compile
```bash
cd latex_new
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

On Windows you can also run `build.bat`.

## Running the Analysis

```bash
# 1. Set up API access
cp code/config.py.template code/config.py
# Edit code/config.py and insert your own LLM API key

# 2. Install dependencies
pip install -r requirements.txt

# 3. Variable extraction (uses LLM API; slow)
python code/variable_extraction.py

# 4. Statistical analysis
python code/study1_analysis.py    # H1, H2
python code/study2_analysis.py    # H3, H4

# 5. Reliability checks
python code/llm_reliability_check.py
python code/run_retest_reliability.py
```

## Data

The analysis is based on **1,331 reviews** of Burt's Bees Hand Cream Gift Set
(ASIN: `B004EDYQX6`) from Amazon Reviews 2023 (McAuley Lab). Raw review JSONL
files are excluded from this repository due to size; processed CSV datasets
sufficient to reproduce all reported analyses are provided in `data/`.

**Reviewer Experience** is derived from the full Amazon Beauty & Personal Care
category (≈ 23.9M reviews) by counting each reviewer's category-level history.
The full source dataset is publicly available from the McAuley Lab; this repo
contains only the per-reviewer aggregated values used in the analysis.

## Privacy Note

This is a redacted public version of the thesis. Author name, advisor name,
student ID, college, major, and acknowledgments have been removed. The
research content, methodology, results, and figures are unchanged.

## Citation

If you find the methodology useful, please cite the corresponding arXiv
preprint (forthcoming) rather than this thesis directly.

## License

Released under the MIT License for the source code; the thesis text itself
is provided under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
for academic reference.
