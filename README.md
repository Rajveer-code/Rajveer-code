<div align="center">

# Rajveer Singh Pall

**Researcher · Causal Inference & Machine Learning**

B.Tech Computer Science & Business Systems · Gyan Ganga Institute of Technology and Sciences, Jabalpur, India

*6th Semester · MSc Applicant 2027 · ETH Zurich · Cambridge · Oxford*

[![Email](https://img.shields.io/badge/Email-rajveerpall04%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:rajveerpall04@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rajveer%20Singh%20Pall-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rajveer-singh-pall)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--6763--6124-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0001-6763-6124)

</div>

---

## Research

I build machine learning systems that work **equitably and reliably** in the real world — and measure precisely when they don't. My work sits at the intersection of causal inference, algorithmic fairness, and applied ML in high-stakes domains: healthcare and financial markets.

Three ongoing research lines:

- **Algorithmic fairness in clinical ML** — when a diabetes screening model underperforms by 13.5 AUC points for elderly adults (the highest-risk group), that is not a technical curiosity. It is a deployment hazard. I measure it, attribute it, and build tools to prevent it.

- **Causal inference in financial markets** — documenting a 10.6 percentage point racial mortgage approval gap across 42 million applications, then mapping *who* within that population bears the largest share of harm using Causal Forests and Double Machine Learning.

- **Privacy-preserving ML for healthcare** — federated learning addresses the barrier that prevents multi-institutional clinical models from being deployed in practice.

---

## Publications

### Accepted

**Comprehensive Evaluation of Machine Learning for Type 2 Diabetes Risk Prediction: Large-Scale External Validation and Fairness Analysis**
*Rajveer Singh Pall, Sameer Yadav, Siddharth Bhalerao, Sourabh Sahu, Ritu Ahluwalia, Bhaskar Awadhiya*
📍 **IEEE Conference** — Accepted

> Trained XGBoost on NHANES 2015–2020 (n=15,685), externally validated on BRFSS 2020–2022 (n=1,285,783). Internal AUC 0.794 degraded to 0.717 on external validation. Fairness analysis revealed a **13.5 AUC-point gap** between young and elderly adults — the population at highest absolute diabetes risk receives the worst algorithmic performance. SHAP analysis confirmed age, BMI, and physical activity as primary risk drivers.

`XGBoost` `SHAP` `Algorithmic Fairness` `DeLong CI` `External Validation` `TRIPOD-AI`

---

### Under Review

**Persistent Racial Disparities in U.S. Mortgage Approval: Evidence from 42 Million Applications**
📍 **Journal of Housing Economics** — Under Review

> Analyses 5,500 lenders across 2020–2024 HMDA data. Documents a **within-lender racial approval penalty of 10.6 percentage points** using regression discontinuity (PMI 80% LTV threshold), difference-in-differences (2022 Fed tightening cycle), and DFL decomposition. The gap persists after controlling for all observable financial characteristics — income, LTV, loan purpose, property type — and is largest at the PMI boundary, implicating institutional discretion rather than risk-based underwriting.

`Regression Discontinuity` `Difference-in-Differences` `DFL Decomposition` `HMDA` `Causal Inference`

---

**[FinSight] Financial Sentiment and Market Signal Extraction from Earnings Call Transcripts**
📍 **Quantitative Finance and Economics** — Under Review

> Processes 14,584 earnings call transcripts using FinBERT and VADER sentiment pipelines. LightGBM model with walk-forward validation and SHAP attribution. Includes entity-level signals: CEO sentiment, competitor mentions, analyst Q&A negativity ratio. Production Next.js dashboard at [finsight-web-rust.vercel.app](https://finsight-web-rust.vercel.app).

`FinBERT` `LightGBM` `NLP` `Walk-forward Validation` `SHAP`

---

## Active Research Projects

> A coherent five-project programme built around a single question: *how do we build ML systems that work equitably and reliably in the real world?*

---

### P1 — Heterogeneous Treatment Effects in Mortgage Lending
`Months 1–5` · **In Progress**

Extending the HMDA paper from Average Treatment Effects to **Conditional Average Treatment Effects** using Causal Forests (Wager & Athey, 2018) and Double Machine Learning (Chernozhukov et al., 2018). The core question: for which borrower types is racial discrimination most severe — high-income applicants (animus) or PMI-boundary applicants (structural)? SHAP on the Causal Forest maps heterogeneity drivers across the full 42M applicant distribution.

**Target:** arXiv preprint · FAccT 2026 · JASA Applications

`econml` `Causal Forests` `Double ML` `SHAP` `Dask` `42M observations`

📂 [`CATE-HMDA-Heterogeneous-Effects`](https://github.com/Rajveer-code/CATE-HMDA-Heterogeneous-Effects)

---

### P2 — Federated Learning for Diabetes Prediction
`Months 2–6` · Planned

Closes the limitation my IEEE paper explicitly identifies: patient data cannot be shared across institutions. Uses **Flower (flwr)** — the FL framework developed at Cambridge — to train across three demographically heterogeneous hospital nodes without centralising raw data. Compares FedAvg, FedProx, and FedNova aggregation strategies. Key question: does training on distributed demographic variation reduce the **13.5 AUC-point age gap** my centralised model produced?

**Target:** CHIL 2026 · ML4H @ NeurIPS 2026 · JAMIA

`Flower (flwr)` `PyTorch` `FedAvg` `FedProx` `Differential Privacy` `Opacus`

📂 [`diabetes-xai-research`](https://github.com/Rajveer-code/diabetes-xai-research)

---

### P3 — LLM Evaluation Benchmark for Indian Financial Regulatory Text
`Months 3–7` · Planned

**The benchmark no Western university can build.** 700–800 expert-annotated QA pairs drawn from SEBI circulars, RBI monetary policy documents, and NSE/BSE compliance filings — across five task types: regulatory interpretation, numerical reasoning, entity extraction, contradiction detection, and Hindi-English mixed text. Evaluates GPT-4o, Gemini 1.5 Pro, LLaMA-3-70B, Mistral, and Krutrim. Error taxonomy classifies failures as domain knowledge gaps vs. numerical reasoning failures vs. multilingual failures.

**Target:** HuggingFace Dataset release · ACL Findings / EMNLP 2026

`Label Studio` `HuggingFace Datasets` `Gradio` `BERTScore` `Ollama` `OpenAI API`

---

### P4 — FinSight v3: Production MLOps System
`Months 3–8` · Planned

Re-architecting FinSight from a research system into a **live, monitored, auto-updating production pipeline**: Airflow DAG fetches transcripts weekly → FinBERT NLP → PostgreSQL (Supabase) → FastAPI serving → Evidently AI drift detection → MLflow model versioning → Next.js dashboard (live updates). Automatic retraining triggers on distribution shift. The distinction between a student who built a model and an engineer who operates one.

`Apache Airflow` `FastAPI` `Docker` `PostgreSQL` `Evidently AI` `MLflow` `Railway`

📂 [`Finsight`](https://github.com/Rajveer-code/Finsight) · [`finsight-web`](https://github.com/Rajveer-code/finsight-web)

---

### P5 — FairAudit: Open-Source ML Fairness Auditing Library
`Months 6–9` · Planned

Packaging two years of fairness research into **`pip install fairaudit`**. Five modules: (1) subgroup AUC with DeLong 95% CIs and Bonferroni correction, (2) calibration by demographic group (ECE per subgroup — a gap in both AIF360 and Fairlearn), (3) SHAP-based disparity attribution (which features drive the gap for a specific group), (4) distribution shift robustness per subgroup, (5) automated PDF audit report via ReportLab. CI/CD via GitHub Actions, ReadTheDocs documentation.

**AIF360 measures bias mitigation. Fairlearn measures constraint training. FairAudit produces the external validation + calibration + SHAP attribution report.**

**Target:** PyPI · ReadTheDocs · 100+ downloads post-v1.0

`scikit-learn API` `DeLong method` `SHAP` `ReportLab` `Sphinx` `pytest 85%+`

---

## Methods & Stack

```
Causal Inference     Causal Forests · Double Machine Learning · RDD · DiD · DFL Decomposition
Fairness             Subgroup AUC · DeLong CI · ECE · Equalised Odds · Disparate Impact
ML                   XGBoost · LightGBM · PyTorch · scikit-learn · Random Forest
NLP                  FinBERT · VADER · HuggingFace Transformers · SHAP
Federated Learning   Flower (flwr) · FedAvg · FedProx · FedNova · Opacus (DP)
MLOps                Apache Airflow · FastAPI · Docker · MLflow · Evidently AI · PostgreSQL
Data                 HMDA (42M) · BRFSS (1.28M) · NHANES · 14,584 earnings transcripts
Languages            Python · R · SQL
Viz                  Plotly · Matplotlib · Seaborn · Next.js
Libraries            econml · shap · statsmodels · Dask · pandas · numpy
```

---

## The Research Narrative

| # | Project | Contribution |
|---|---------|-------------|
| 1 | IEEE Diabetes Paper | Found a 13.5 AUC-point fairness failure in clinical ML |
| 2 | HMDA Paper | Found a 10.6 pp racial gap in mortgage lending at scale |
| 3 | CATE Extension | Maps *who* bears the largest share of that gap, and why |
| 4 | Federated Learning | Solves the privacy barrier blocking clinical deployment |
| 5 | LLM Benchmark | Tests whether current AI understands the Indian domains I work in |
| 6 | FinSight v3 | Proves I can build systems that run in production, not just notebooks |
| 7 | FairAudit | Builds the tool I wish had existed when I started all of this |

> This is not a collection of unrelated projects. It is a research programme about building ML systems that work equitably and reliably in the real world. Every project motivates the next.

---

<div align="center">

*B.Tech Computer Science & Business Systems · Gyan Ganga Institute of Technology and Sciences*
*Jabalpur, India · Targeting MSc Data Science / AI — ETH Zurich · Cambridge · Oxford · 2027*

</div>
