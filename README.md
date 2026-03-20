<meta name="google-site-verification" content="ulma8pVtPkxh6YRWcrvCQVg2ka8wKrE75kA-Pf2MDpU" />
<div align="center">

# Rajveer Singh Pall

**Researcher · Causal Inference & Machine Learning**

B.Tech Computer Science & Business Systems · 6th Semester
Gyan Ganga Institute of Technology and Sciences, Jabalpur, India

*MSc Applicant 2027 — ETH Zurich · Cambridge · Oxford*

[![Email](https://img.shields.io/badge/Email-rajveerpall04%40gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:rajveerpall04@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-rajveer--singh--pall-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rajveer-singh-pall)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0001--6763--6124-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0001-6763-6124)

</div>

---

## Research

I study two related questions: **when do ML systems fail the people they are meant to serve**, and **what does rigorous causal identification reveal about structural discrimination in financial markets**?

My published and submitted work spans three domains — healthcare ML fairness, racial disparities in mortgage lending, and market microstructure — all united by a commitment to external validity, honest negative results, and methods that hold up under scrutiny.

---

## Publications

### ✅ Accepted

**Comprehensive Evaluation of Machine Learning for Type 2 Diabetes Risk Prediction: Large-Scale External Validation and Fairness Analysis**
*Rajveer Singh Pall, Sameer Yadav, Siddharth Bhalerao, Sourabh Sahu, Ritu Ahluwalia, Bhaskar Awadhiya*
📍 **IEEE Conference** · Accepted

Trained XGBoost on NHANES 2015–2020 (n = 15,685). Externally validated on BRFSS 2020–2022 (n = 1,285,783). Internal AUC 0.794 degraded to 0.717 under distribution shift. Fairness analysis revealed a **13.5 AUC-point gap** between young adults (AUC 0.742) and elderly adults (AUC 0.607) — the population at highest absolute diabetes risk receives the weakest algorithmic performance. SHAP analysis confirmed age, BMI, and physical activity as primary risk drivers.

`XGBoost` `SHAP` `DeLong CI` `Algorithmic Fairness` `External Validation` `TRIPOD-AI`
📂 [`diabetes-xai-research`](https://github.com/Rajveer-code/diabetes-xai-research)

---

### 📬 Under Review

**Persistent Racial Disparities in U.S. Mortgage Approval: Evidence from 42 Million Applications, 2020–2024**
📍 **Journal of Housing Economics** · Under Review

42,323,519 mortgage applications across 5,500 lenders. Black applicants face a raw 14.95 pp approval gap. After DFL reweighting to equalise all observable financial characteristics, **98.6% of the gap remains unexplained**. Within-lender fixed effects show 74.6% of the gap arises within the same institution — growing monotonically from 66.8% (2020) to 78.3% (2024). Two quasi-experimental designs isolate specific channels: an RDD at the 80% LTV/PMI boundary (+2.0 pp differential, concentrated entirely in purchase loans, absent for refinancings) and a DiD exploiting the 2022 Fed tightening cycle (+1.5 pp widening, a structural break 2.4× the pre-existing trend).

`Regression Discontinuity` `Difference-in-Differences` `DFL Decomposition` `HMDA` `Within-Lender Fixed Effects`
📂 [`hmda-racial-disparities`](https://github.com/Rajveer-code/hmda-racial-disparities)

---

**The Transaction Cost Trap: Why Machine Learning Stock Prediction Fails Economically Under Realistic Market Frictions**
📍 **Quantitative Finance and Economics** · Under Review

A regime-filtered ensemble of CatBoost, Random Forest, and Deep Neural Networks on 7 large-cap technology stocks (17,773 stock-day observations, January 2015–April 2025) under strict walk-forward validation. The ensemble achieves up to **73.3% conditional directional accuracy** in bear-market regimes, yet generates **−42.49% annually** (Sharpe −2.83) after realistic 5 bps execution costs — while buy-and-hold earns 34.77% (Sharpe 1.21) over the same period. A closed-form breakeven accuracy formula shows that at 471 trades/year and 5 bps costs, profitable trading requires **88% accuracy**, 15 pp beyond the best conditional result. Magnitude asymmetry (winning trades +0.08% vs losing trades −0.31%, a 3.9× ratio) produces negative expected value per trade regardless of win rate. Results are consistent with weak-form market efficiency and make an explicit case against publication bias in financial ML.

`CatBoost` `DNN` `Walk-forward Validation` `Market Microstructure` `Ensemble Methods` `Market Efficiency`
📂 [`financial-sentiment-nlp`](https://github.com/Rajveer-code/financial-sentiment-nlp)

---

## Portfolio Project

**FinSight — LLM-Powered Earnings Intelligence System**
🌐 [finsight-web-rust.vercel.app](https://finsight-web-rust.vercel.app) · [HuggingFace Demo](https://huggingface.co/spaces/Rajveer234/finsight)

End-to-end ML system investigating whether NLP features from earnings call transcripts contain statistically significant alpha signals. Processes **14,584 S&P 500 earnings call transcripts (2018–2024)**, extracts 34 NLP features via FinBERT and RAG-based structured queries, trains 6 model architectures under strict walk-forward validation, and backtests a long-short quartile strategy at 5-day and 20-day holding periods. Key finding: Energy sector IC = +0.311 vs Technology IC = +0.004 — an 83× difference in signal strength across GICS sectors. Results served through a production Next.js dashboard and Streamlit demo.

`FinBERT` `RAG` `LightGBM` `Walk-forward Validation` `SHAP` `Next.js` `Streamlit`
📂 [`Finsight`](https://github.com/Rajveer-code/Finsight) · [`finsight-web`](https://github.com/Rajveer-code/finsight-web)

---

## Research Projects in Progress

> A five-project programme building directly on existing published work. Each project solves a problem the previous one exposed.

---

### P1 — Heterogeneous Treatment Effects in Mortgage Lending
`Months 1–5` · 🔄 **In Progress**

Extends the HMDA paper from Average Treatment Effects to **Conditional Average Treatment Effects**: for which borrowers is racial discrimination most severe? Uses Causal Forests (Wager & Athey, 2018) and Double Machine Learning (Chernozhukov et al., 2018) on the full 42M application sample. SHAP on the Causal Forest identifies which features drive heterogeneity in the treatment effect across the applicant distribution.

**Target:** arXiv preprint 2026 · FAccT 2026 · JASA Applications and Case Studies

`econml` `Causal Forests` `Double ML` `GRF` `Dask` `SHAP`
📂 [`CATE-HMDA-Heterogeneous-Effects`](https://github.com/Rajveer-code/CATE-HMDA-Heterogeneous-Effects)

---

### P2 — Federated Learning for Diabetes Prediction
`Months 2–6` · 📋 Planned

Closes the limitation my IEEE paper explicitly identifies: patient data cannot be pooled across institutions. Uses **Flower (flwr)** — developed at Cambridge, used by Google and Apple — across three demographically heterogeneous simulated hospital nodes without sharing raw data. Compares FedAvg, FedProx, and FedNova aggregation strategies. Core question: does training on distributed demographic variation reduce the **13.5 AUC-point age gap** the centralised model produced?

**Target:** CHIL 2026 · ML4H @ NeurIPS 2026 · JAMIA

`Flower (flwr)` `PyTorch` `FedAvg` `FedProx` `FedNova` `Differential Privacy` `Opacus`

---

### P3 — LLM Evaluation Benchmark for Indian Financial Regulatory Text
`Months 3–7` · 📋 Planned

700–800 expert-annotated QA pairs from SEBI circulars, RBI monetary policy documents, and NSE/BSE compliance filings. Five task types: regulatory interpretation, numerical reasoning, entity extraction, contradiction detection, Hindi-English mixed text. Evaluates GPT-4o, Gemini 1.5 Pro, LLaMA-3-70B, Mistral, and Krutrim. Error taxonomy distinguishes domain knowledge gaps from numerical reasoning failures from multilingual failures.

**Target:** HuggingFace Dataset release · ACL Findings / EMNLP 2026

`Label Studio` `HuggingFace Datasets` `Gradio Spaces` `BERTScore` `Ollama`

---

### P4 — FinSight v3: Production MLOps System
`Months 3–8` · 📋 Planned

Re-architecting FinSight into a live production system: weekly Airflow DAG for transcript ingestion → FinBERT NLP → PostgreSQL (Supabase) → FastAPI serving → Evidently AI drift detection → MLflow model versioning → Next.js dashboard with live updates. Automatic retraining triggered on detected distribution shift.

`Apache Airflow` `FastAPI` `Docker` `PostgreSQL` `Evidently AI` `MLflow` `Railway`

---

### P5 — FairAudit: Open-Source ML Fairness Auditing Library
`Months 6–9` · 📋 Planned

`pip install fairaudit` — packaging the fairness methodology developed across the diabetes and HMDA papers into a reusable tool. Five modules: (1) subgroup AUC with DeLong 95% CIs and Bonferroni correction, (2) calibration by demographic group (ECE per subgroup — a gap in AIF360 and Fairlearn both), (3) SHAP-based disparity attribution, (4) distribution shift robustness per subgroup, (5) automated PDF audit report.

**Target:** PyPI · ReadTheDocs · 85%+ test coverage · 100+ downloads post-v1.0

`scikit-learn API` `DeLong` `SHAP` `ReportLab` `Sphinx` `pytest` `GitHub Actions`

---

## Methods

```
Causal Inference     Causal Forests · Double ML · RDD · DiD · DFL Decomposition · Manski Bounds
Fairness             Subgroup AUC · DeLong CI · ECE · Equalised Odds · Disparate Impact
ML                   XGBoost · LightGBM · CatBoost · PyTorch · scikit-learn · Random Forest
NLP                  FinBERT · VADER · HuggingFace Transformers · RAG · SHAP
Federated Learning   Flower (flwr) · FedAvg · FedProx · FedNova · Opacus (DP)
Data at Scale        HMDA 42M · BRFSS 1.28M · NHANES · 17,773 stock-days · 14,584 transcripts
Languages            Python · R · SQL
```

---

## Other Projects

| Repository | Description |
|---|---|
| [`credit-scoring-app`](https://github.com/Rajveer-code/credit-scoring-app) | ML-based credit scoring web application |
| [`SereneSpace`](https://github.com/Rajveer-code/SereneSpace) | Mental wellness application |
| [`vaha-project`](https://github.com/Rajveer-code/vaha-project) | Full-stack web project |
| [`My-portfolio-using-html`](https://github.com/Rajveer-code/My-portfolio-using-html) | Personal portfolio site |

---

<div align="center">

*B.Tech Computer Science & Business Systems · 6th Semester*
*Gyan Ganga Institute of Technology and Sciences · Jabalpur, India*
*Targeting MSc Data Science / AI — ETH Zurich · Cambridge · Oxford · 2027 Intake*

</div>
