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

1. Biggest drop-off month:
    The biggest drop happened in Nov 2025, content output dropped in this period where I couldn't post as much as
    I wanted so it correlates with the high churn spike.

2. Best cohort and possible reason:
    Best cohort is the one from the beginning of the page, it was the second time that I launched the page and some
    people who were fans before joined in and some still remain to this day.

3. Worst cohort and possible explanation:
    Worst cohort is from June 2025, basically people who joined in that months and left in Nov, all of them from the
    base tier, from the exit surveys, most of them in that period are marked with "My financial situation changed".

4. Early vs recent cohort comparison:
    Earlies cohorts are better since it was before the economy shifted drastically in the past months, so keeping
    subscribers becomes harder and harder, even for external reasons.

5. Recommendation:
    Increase the content quality and include patrons in FAQ, votes etc, making them feel more connected with the page,
    that will help out with the churn rate. So at least one engagement post per month should be able to improve the
    retention.

---

### 2. Churn Analysis
*Script:* scripts/churn_analysis.py
*Outputs:* outputs/churn_reasons.png · outputs/churn_over_time.png

**Key findings:**

1. Primary churn reason and what the creator can/cannot control:
Can control: quality and quantity of content, Can't control: The wallets of the patreons, but with the can control
aspects, you can try to balance the chances in your favor, at least to make them think twice before churning, including
cancelling coupons, life 50% discount for the next month if you don't cancel. Even if they churn, they can be targeted
again with coupons for rejoining.

2. How high-value patrons differ from low-value patrons in churn behaviour:
Usually they get their personalized content and leave, depends on how much they want or if they come back for more
at a later time.

3. Does the November 2025 spike appear in the survey data? What reason dominated that month?
No, so in the end, it's hard to find the exact reasons why so many people left, the only thing that they would have in
common is the Chrismas coming.

4. What the $1,557 churner case study reveals:
This is the final objective of the page, 20% of clients generate 80% of the revenue, the more people come to the page,
the bigger the chances that one of them will be a whale, spending more than 99% of patrons, this also creates a
division between passive and active income from the page.

5. Top recommendation based on churn analysis:
Focus on the things that I can control, more involvement with the patrons, and cancellations and returning offers.

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
