"""
This code was writen to reproduce a cohort retention matrix - similarly with how Saas companies use
to analyze how good they keep subscribers over time

This analysis will answer to these questions:
What % of patrons from each signup month are still subscribed after 1, 3, 6, 12 months?
Which cohort retains best? Which retains worst?
At what month does the biggest drop-off typically happen?
Are newer cohorts improving or declining compared to older ones?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
from pandas.io.sas.sas_constants import column_name_offset_length

BASE_DIR = Path(__file__).parent.parent

plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.size'] = 12

# Check if all libraries loaded correctly
print('Libraries loaded')

# Load the data from the .csv file
df = pd.read_csv(
    r'/data/patrons_clean.csv',
    parse_dates=['started_at','last_updated_at','last_charge_at'],
)

print(f'Shape: {df.shape}')
print(f'Columns: {list(df.columns)}')
df.head(10)

# Filter for paying patrons only, since free users can't churn, so we only want patrons where pledge_uds > 0
paying = df[df['pledge_usd'] > 0]

print(f'Total paying patrons: {len(paying)}')
print()
print('Patrons Status Breakdown')
print(paying['patron_status'].value_counts())
print()
print('Tier Breakdown: ')
print(paying['tier'].value_counts())

# Determine each patron's end date
# If active, end date = today
# If former, end date = last updated at
TODAY = pd.Timestamp('2026-04-24')
paying = paying.copy()

paying['end_date'] = paying.apply(
    lambda row: TODAY if row['is_active'] else row['last_updated_at'],
    axis=1
)

print('Active patron end_date')
print(paying[~paying['is_active']]['end_date'].value_counts().head())
print()
print('Former patron end_date')
print(paying[~paying['is_active']]['end_date'].sort_values().tail(10).values)

# Calculate tenure in months, which is how many complete months a patron was subscribed
# Formula: floor((end_date - started_at).days / 30.44 (avg days in a month per year))

paying['tenure_months'] = np.floor(
    (paying['end_date'] - paying['started_at']).dt.days / 30.44
)

print('Tenure stats (months): ')
print(paying['tenure_months'].describe())
print()
print('Distribution:')
print(paying['tenure_months'].value_counts().sort_index().head(20))

# Assign each patron a cohort. A cohort is a group of patrons that joined in the same calendar month, so November
# patrons will be assigned the 2024-11 cohort.

paying['cohort'] = paying['started_at'].dt.to_period('M')

cohort_sizes = paying.groupby('cohort')['patron_id'].count().rename('size')

print('Patrons per cohort: ')
print(cohort_sizes.to_string)
print()
print(f'Total cohorts: {len(cohort_sizes)}')
print(f'Largers cohort: {cohort_sizes.idxmax()}) ({cohort_sizes.max()} patrons)')

"""
Retention Matrix
For each cohort and each month, we want to know what % of patrons from this cohort are still subscribed at M month.
So it will loop over each cohort, count how many patrons in that cohort have tenure_months >= month, then divide
by cohort size. 
"""

MAX_MONTHS = 12

retention_rows = []

for cohort, group in paying.groupby('cohort'):
    size = len(group)
    cohort_age_months = (TODAY - cohort.to_timestamp()). days / 30.44

    for month in range(MAX_MONTHS + 1):
        if cohort_age_months < month:
            continue

        survived = (group['tenure_months'] >= month).sum()
        retention_pct = round(survived / size * 100, 1)

        retention_rows.append({
            'cohort': str(cohort),
            'month': month,
            'retention_pct': retention_pct,
            'patron_retained': int(survived),
            'cohort_size': size,
        })

retention = pd.DataFrame(retention_rows)

print(f'Retention table shape: {retention.shape}')
print()
print('First 15 rows:')
print(retention.head(15).to_string(index=False))

# Pivot into a matrix, for the heatmap I need cohorts x months using pd.pivot_table()

matrix = retention.pivot_table(
    index='cohort',
    columns='month',
    values ='retention_pct',
)

matrix.columns = [f'M{m}' for m in matrix.columns]

print(f'Matrix shape: {matrix.shape} (cohort x months)')
print()
matrix

# Heatmap visual
fig, ax = plt.subplots(figsize=(16, 9))

cohort_size_map = paying.groupby(paying['cohort'].astype(str))['patron_id'].count()
matrix_labeled = matrix.copy()

cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=0, vmax=100)

im = ax.imshow(
    matrix_labeled.values,
    aspect='auto',
    cmap=cmap,
    norm=norm,
)

for i in range(matrix_labeled.shape[0]):
    for j in range(matrix_labeled.shape[1]):
        val = matrix_labeled.iloc[i, j]
        if not np.isnan(val):
            ax.text(j, i, f'{val:.0f}%', ha='center', va='center',
                    fontsize=7, color='black' if 30 < val < 80 else 'white',
                    fontweight='bold')

ax.set_xticks(range(len(matrix_labeled.columns)))
ax.set_xticklabels(matrix_labeled.columns, fontsize=9)
ax.set_yticks(range(len(matrix_labeled.index)))
ax.set_yticklabels(
    [f"{c}  (n={cohort_size_map.get(c, '?')})" for c in matrix_labeled.index],
    fontsize=8
)

ax.set_title('Patron Cohort Retention — Paying Members Only', fontsize=14, pad=16, fontweight='bold')
ax.set_xlabel('Months Since First Payment', fontsize=10)
ax.set_ylabel('Cohort (Signup Month)', fontsize=10)

plt.colorbar(im, ax=ax, label='Retention %', shrink=0.6)
plt.tight_layout()
plt.savefig(BASE_DIR / 'processed' / 'cohort_retention_heatmap.png', bbox_inches='tight')
plt.show()
print("chart saved to data/processed/cohort_retention_heatmap.png")

# Average retention curve
avg_retention = retention.groupby('month')['retention_pct'].mean().round(1)

print("Average retention by month:")
print(avg_retention.to_string())

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(avg_retention.index, avg_retention.values, marker='o', linewidth=2,
        color='#3b82f6', markerfacecolor='white', markeredgewidth=2, markersize=7)
ax.fill_between(avg_retention.index, avg_retention.values, alpha=0.1, color='#3b82f6')

for x, y in zip(avg_retention.index, avg_retention.values):
    ax.annotate(f'{y:.0f}%', (x, y), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=8, color='#6b7280')

ax.set_xlabel('Month Since First Payment', fontsize=10)
ax.set_ylabel('Avg Retention %', fontsize=10)
ax.set_title('Average Patron Retention Curve', fontsize=13, fontweight='bold')
ax.set_ylim(0, 110)
ax.set_xticks(avg_retention.index)
ax.grid(axis='y', alpha=0.3)
ax.set_facecolor('#f9fafb')
plt.tight_layout()
plt.savefig(BASE_DIR / 'processed' / 'cohort_retention_heatmap.png', bbox_inches='tight')
plt.show()

insights = """

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
"""

print(insights)

retention.to_csv(BASE_DIR / 'processed' / 'cohort_retention.csv', index=False)
print(f'Saved {len(retention)} rows to data/processed/cohort_retention.csv')
print()
print('Preview:')
print(retention.head(10).to_string(index=False))