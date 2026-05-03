# Changelog

All notable changes to this project are documented here.  
Format: `[YYYY-MM-DD] — type: description`

Types: `feat` · `analysis` · `fix` · `docs` · `refactor` · `data`

---

## [2026-04-24]

### analysis: tier revenue, retention and upsell opportunity

- Loaded patron data and filtered to 150 paying patrons across 3 tiers
- Built crosstab of tier vs patron status with active rate per tier
- Computed revenue breakdown: Full Rewards $4,881 (68.2%), Commission $1,465 (20.5%), VIP $814 (11.4%)
- Calculated avg LTV per tier: Commission $488, VIP $116, Full Rewards $35
- Identified VIP Rewards as longest tenure tier at 12.5 avg months
- Noted $1,557 outlier patron classified under VIP Rewards skewing avg pledge — excluded from upsell calculation
- Upsell scenario: 10 Full Rewards → VIP upgrades generates ~$500/year additional recurring revenue
- Generated outputs/tier_revenue.png — total revenue and avg LTV side by side bar charts
- Generated outputs/tier_retention.png — active rate by tier
- Exported data/processed/tier_summary.csv for PowerBI dashboard use
- Updated README with tier analysis findings

### feat: project initialization and data anonymization
- Set up project folder structure (`data/`, `scripts/`, `dashboard/`, `outputs/`)
- Exported raw Patreon member data (359 patrons, Apr 2024 – Apr 2026)
- Normalized date columns, renamed all columns to snake_case
- Derived additional columns: `tenure_days`, `cohort_month`, `is_active`, `is_paying`
- Cleaned and normalized `exit_surveys_clean.csv` (42 churn survey responses)

### analysis: cohort retention matrix
- Built `cohort_retention_matrix.py` — computes monthly retention for 25 cohorts across 150 paying patrons
- Calculated patron end dates using right-censoring (active patrons use today's date)
- Computed `tenure_months` per patron using floor division of elapsed days
- Pivoted long retention table into cohort × month matrix
- Generated cohort retention heatmap (`outputs/Patron_Cohort_Retention.png`)
- Generated average retention curve across all cohorts
- Exported `data/processed/cohort_retention.csv` for downstream use

### docs: project README
- Documented business questions, dataset description, project structure
- Added key findings from cohort retention analysis
- Placeholder sections for upcoming churn, tier, and MRR analyses

---

[2026-04-27]
analysis: churn reason breakdown and high-value patron case study

- Loaded and merged exit survey data (42 responses) with patron dataset
- Calculated survey coverage: ~51% of churned patrons left a response, 49% churned silently
- Computed churn reason frequency — financial situation #1 at 50% of respondents
- Segmented churn reasons by pledge amount (low value ≤$5 vs high value >$5)
- Identified high-value patron churn pattern: transactional intent (join for specific content, leave after receiving it)
- Investigated November 2025 churn spike — not confirmed in survey data, likely silent churn with seasonal factor
- Case study on $1,557 lifetime value churner — illustrates Pareto dynamic in creator monetization
- Generated outputs/churn_reasons.png — horizontal bar chart of churn reasons
- Generated outputs/churn_over_time.png — monthly churn survey timeline
- Exported data/processed/churn_reasons.csv for PowerBI dashboard use

*Upcoming:*
- `02_churn_analysis` — cross exit survey reasons with cohort and pledge data
- `03_tier_analysis` — retention and LTV comparison across tiers
- `04_mrr_timeline` — reconstruct monthly recurring revenue
- PowerBI dashboard layer on top of processed CSVs
