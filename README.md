# Patreon Subscriber Analytics

A end-to-end data analytics project built on real, anonymized subscription data 
from my content creator Patreon page (2024–2026).

The goal is to answer the same questions any SaaS or subscription business faces: 
who stays, who leaves, when do they leave, and why? Also to showcase my skills in
Python, Excel, PowerBI, SQL and how I analyze, interpret and draw actions from the data.

---

## Business Questions

- What % of subscribers are still active after 1, 3, 6, and 12 months?
- Which signup cohorts retain best, and which drop off fastest?
- What are the primary reasons patrons cancel their subscriptions?
- Does pledge amount or tier correlate with churn behavior?
- How has monthly recurring revenue trended over time?

---

## Dataset

Anonymized export from a content creator's Patreon page.

| File | Description |
|------|-------------|
| `data/processed/patrons_clean.csv` | 359 patrons, 18 columns. All PII replaced with anonymous IDs. |
| `data/processed/exit_surveys_clean.csv` | 42 exit survey responses from churned patrons (Sept 2024 – Apr 2026). |
| `data/processed/cohort_retention.csv` | Computed retention matrix, output of the analysis pipeline. |

**Tiers:** Free · Full Rewards · VIP Rewards · Commission  
**Date range:** April 2024 – April 2026  
**Paying patrons:** 150 (69 active, 76 former, 5 declined)

## Analysis

### 1. Cohort Retention
*Script:* `scripts/cohort_retention_matrix.py`  
*Output:* `outputs/Patron_Cohort_Retention.png`

Grouped 150 paying patrons into monthly cohorts and tracked what percentage remained subscribed at each month from M0 to M12.

**Key findings:**
- Early cohorts (Apr–Oct 2024) show near-perfect retention through 12 months, these are core long-term fans who joined at the page's relaunch.
- The largest single-cohort drop occurred in the **2025-06 cohort**, which went from 100% to 0% between M4 and M5 (November 2025), coinciding with  content output decline during that month.
- The **2025-01 cohort** (10 patrons) dropped sharply from 100% to 20% at M10, suggesting a cluster of patrons with similar subscription intent who left around the same time.
- Recent cohorts (2026) show early churn in M1–M2, which is normal with the current economic pressure on "random" spending.
- Average retention stabilizes around **50–60%** for cohorts that survive past month 6.

---

### 2. Churn Analysis
*Coming soon*

---

### 3. Tier & Lifetime Value Analysis
*Coming soon*

---

### 4. MRR Timeline
*Coming soon*

---

## Dashboard

An interactive cohort retention heatmap built in React. Color-coded cells show retention 
% at each month for each cohort, with tooltips showing exact patron counts.

*Link: coming soon 
---

## Tools & Stack

| Layer | Tools |
|-------|-------|
| Data cleaning | Python, Pandas, Pathlib |
| Analysis | Python, Pandas, NumPy |
| Visualization | Matplotlib, PowerBI *(in progress)* |
| Dashboard | React |
| Data storage | CSV → PostgreSQL *(planned)* |

## About

This project was built as part of a portfolio targeting **Data Analyst** and 
**Product /Business Analyst** roles. The dataset comes from a real subscription page, 
anonymized, and reflects genuine business patterns rather than synthetic data.
