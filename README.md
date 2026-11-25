# EU CBAM Impact Modeling & Decision Support for Vietnam Exports (2019–2034)

> **End-to-End Quantitative Trade & Carbon Liability Analysis, 100% Vietnam Scope Audit, and Interactive Decision-Support Dashboard**

[![Report](https://img.shields.io/badge/Report-English%20(Word)-blue)](docs/CBAM_Report_EN.docx)
[![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20HTML-brightgreen)](dashboard/index.html)
[![Notebooks](https://img.shields.io/badge/Notebooks-ETL%20%26%2015%20Audits-orange)](02_cbam_live_verification_and_methodology_audit.ipynb)
[![Data](https://img.shields.io/badge/Coverage-275%20CN8%20Codes-lightgrey)](data/processed/cbam_vn_exposure_master_by_cn8.csv)

---

## 📌 Project Overview

The European Union's **Carbon Border Adjustment Mechanism (CBAM)** introduces carbon-price parity on carbon-intensive imports entering the EU market, shifting from its transitional phase to definitive financial enforcement (2026–2034).

This project builds a reproducible data pipeline, methodology audit suite, and interactive decision-support dashboard to quantify Vietnam's export exposure across **275 CN8 product codes (54 HS4 groups, 4 CBAM-covered sectors)** using official trade, carbon-price, and emissions benchmark datasets (**Eurostat**, **EEX EUA**, **ECB**, and **European Commission**).

---

## 🔍 Key Quantitative Findings

1. **Super-Pareto Risk Concentration:**
   * Just **20 out of 275 CN8 codes** (7.3% of product lines) account for **89.5% of Vietnam's total CBAM liability in 2026**, rising to **90.1% in 2029**.
   * Exposure is led by coated flat-rolled steel `72104900` (\$71.7M) and semi-finished steel `72071210` (\$68.9M).

2. **Default-Value Mark-Up Penalty Escalation (2028–2029):**
   * Failing to report verified actual emissions (MRV) triggers EU default-value mark-up penalties that jump from **+10% (2026)** to **+30% (from 2028 onward)**.
   * Additional penalty costs surge from **\$69.0M (2026)** to **\$207.0M/year (2029)** — representing **34.9%** of the total CBAM bill.

3. **Counter-Intuitive Margin Stress-Test Results:**
   * **Cement (`25232900`):** Despite modest export value (\$12.6M), effective CBAM burden reaches **112.5% of export price by 2029**, creating severe negative-margin risk without MRV decarbonization.
   * **Aluminum (`7616`, `7604`, `7601`):** Despite large export volume, effective CBAM burden remains low (**1.4% – 4.7% of export price**) due to high unit prices (\$2,673–\$7,545/ton) and exclusion of indirect electricity emissions under current rules.

4. **Value-Chain Trap & Downstream Steel Paradox:**
   * Downstream steel (`7209`, `7210`, `7219`, `73xx`) accounts for **63.7% of total CBAM liability (\$240.5M)** while relying heavily on imported HRC/billets.
   * Because embedded emissions from imported precursors cannot be offset through Vietnam's domestic carbon exchange (HNX), exporters require end-to-end supply-chain traceability and upstream localization.

---

## 🚀 Quick Start & Reviewer Guide

Explore the project deliverables in recommended order:

1. **Comprehensive Academic & Policy Report (English):**
   * Open [`docs/CBAM_Report_EN.docx`](docs/CBAM_Report_EN.docx) for the Executive Summary, Methodology, Quantitative Analysis, 2026–2034 Scenario Simulations, and Policy Recommendations.
2. **Interactive Web Dashboard:**
   * Open [`dashboard/index.html`](dashboard/index.html) directly in any modern browser (Chrome, Edge, Firefox, Safari) — no web server or backend setup required (all datasets and Chart.js visualizations are self-contained; Vietnamese UI).
3. **Data Dictionary & Presentation Workbook (Excel):**
   * Open [`CBAM_Dataset_Data_Dictionary_Presentation.xlsx`](CBAM_Dataset_Data_Dictionary_Presentation.xlsx) containing 5 structured sheets (12-dataset catalog, 30+ attribute dictionary, Top 20 Super-Pareto breakdown, 4-sector summary, and quality audit).
4. **Methodology & Live Data Verification Notebook:**
   * Review [`02_cbam_live_verification_and_methodology_audit.ipynb`](02_cbam_live_verification_and_methodology_audit.ipynb) for 15 independent checks covering data integrity, mark-up penalty formulas, and counter-intuitive findings.
5. **ETL & Preprocessing Pipeline Notebook:**
   * Review [`01_cbam_preprocessing_pipeline.ipynb`](01_cbam_preprocessing_pipeline.ipynb) for the end-to-end transformation from raw Eurostat/EEX/EU Commission sources into the 275-CN8 master dataset.
6. **Policy Notes, Data Catalog & AI Reproduction Prompts:**
   * [`docs/CBAM_CARBON_POLICY_OUTLINE.md`](docs/CBAM_CARBON_POLICY_OUTLINE.md) — Policy framework & domestic HNX carbon market strategy.
   * [`docs/DATA_CATALOG_AND_QUALITY_REPORT.md`](docs/DATA_CATALOG_AND_QUALITY_REPORT.md) — Source catalog, download links & quality verification.
   * [`prompt.md`](prompt.md) — 12-step modular prompt sequence for reproducing the project with AI agents.

---

## 🛠️ Tech Stack & Methodology

* **Data Engineering & Analytics:** Python, Pandas, Jupyter Notebooks (`01_cbam_preprocessing_pipeline.ipynb`, `02_cbam_live_verification_and_methodology_audit.ipynb`)
* **Data Sources:** Eurostat EU-27 imports (monthly & annual CN8), EEX EUA carbon futures (2020–2026), ECB FX rates, EU Commission CBAM Default Values & Benchmarks
* **Scenario & Shock Modeling:** 9M 2026 Price–Volume decomposition (`cbam_vn_yoy_2026_shock.csv`), 2026–2034 phase-in & mark-up simulation
* **Visualization & Reporting:** Self-contained HTML/CSS/JavaScript + Chart.js dashboard, Excel Data Dictionary, Academic Word Report

---

## 📁 Repository Structure

```text
.
├── README.md                                             # Project overview & reviewer guide
├── 01_cbam_preprocessing_pipeline.ipynb                  # ETL pipeline: Eurostat, EEX, EU Commission -> 275 CN8
├── 02_cbam_live_verification_and_methodology_audit.ipynb # 15 independent methodology & integrity audits
├── CBAM_Dataset_Data_Dictionary_Presentation.xlsx         # 5-tab data dictionary & presentation workbook
├── prompt.md                                             # 12 modular prompts to reproduce the project
│
├── dashboard/                                            # Self-contained interactive web dashboards
│   ├── index.html                                        # Primary interactive dashboard (Chart.js)
│   ├── index_vi.html                                     # Backup copy of interactive dashboard
│   └── cbam_dashboards_updated.html                      # Standalone 3-dashboard UI extract
│
├── data/                                                 # Standardized research datasets
│   ├── processed/                                        # Clean analytical & dashboard-ready datasets
│   │   ├── cbam_vn_exposure_master_by_cn8.csv            # Master 275 CN8 Vietnam-to-EU exports (2025 base)
│   │   ├── cbam_vn_exposure_master_by_hs4.csv            # Aggregated 54 HS4 product groups
│   │   ├── cbam_vn_exposure_summary_by_sector.csv        # 4 CBAM-covered sector summary
│   │   ├── cbam_vn_yoy_2026_shock.csv                    # 9M 2026 Price–Volume shock decomposition
│   │   ├── eex_eua_prices_monthly_2020_2026.csv          # Monthly EEX EUA carbon price series
│   │   └── eurostat_eu27_imports_vn_cbam_cn8_*.csv       # Monthly & annual Eurostat trade series
│   └── raw/                                              # Raw reference tables (EU Default Values, Benchmarks)
│
├── docs/                                                 # Reports & technical documentation
│   ├── CBAM_Report_EN.docx                               # Comprehensive Academic & Policy Report (English)
│   ├── CBAM_CARBON_POLICY_OUTLINE.md                     # Policy framework & HNX carbon market strategy
│   ├── DATA_CATALOG_AND_QUALITY_REPORT.md                # Data catalog, direct links & quality report
│   ├── CBAM_Dataset_Data_Dictionary_Presentation.xlsx    # Copy of presentation data dictionary
│   ├── prompt.md                                         # AI reproduction prompt framework
│   └── paste_tutorial.md                                 # Integration guide for developers / AI agents
│
├── scripts/                                              # Reproducible Python automation scripts
│   ├── fetch_cbam_datasets.py                            # Automated API ingestion (Eurostat, ECB, EEX)
│   ├── build_master_and_audit.py                         # Master dataset builder & audit runner
│   ├── build_dashboard.py                                # Dashboard generator v1
│   ├── build_dashboard_v2.py                             # Dashboard generator v2
│   ├── build_notebook.py                                 # Notebook 01 generator
│   └── generate_live_test_notebook.py                    # Notebook 02 generator
│
└── _archive/                                             # Initial archive & safe backups
```
