import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
import textwrap #Added for long text

BASE_DIR = Path(__file__).parent.parent
filepathpatrons = BASE_DIR / 'data' / 'patrons_clean.csv'
filepathsurveys = BASE_DIR / 'data' / 'exit_surveys_clean.csv'

plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'monospace'

print('Libraries OK')

# Loading datasets
patrons = pd.read_csv(filepathpatrons)

surveys = pd.read_csv(filepathsurveys, parse_dates=['churned_at'])

print(f'Patrons: {patrons.shape}')
print(f'Surveys: {surveys.shape}')
print()
surveys.head()

# How many patrons that churned left a survey?
churned_patrons = patrons['patron_status'].isin(['Former patron', 'Declined patron']).sum()
survey_responses = len(surveys)

coverage = round(survey_responses/churned_patrons * 100, 1)
silent = round(100 - coverage, 1)

print(f'Total churned patrons:     {churned_patrons}')
print(f'Exit survey responses:     {survey_responses}')
print(f'Survey coverage:           {coverage}%')
print(f'Churned silently:          {silent}%')
print()
print('Note: This means our churn reason analysis covers only a portion of actual churn since surveys are optional.')
print()

reason_cols = [c for c in surveys.columns if c.startswith('reason_')]

# Clean up labels for display for the churn resons
reason_labels = {
    'reason_financial':         'Financial situation changed',
    'reason_overcharged':       'Felt overcharged',
    'reason_got_benefit':       'Got what they came for',
    'reason_amount_limit':      'Reached intended spend limit',
    'reason_low_activity':      'Creator not active enough',
    'reason_missing_rewards':   'Rewards not as described',
    'reason_hard_access':       'Hard to access rewards',
    'reason_disliked_rewards':  'Disliked the rewards',
    'reason_patreon_platform':  'Unhappy with Patreon',
    'reason_tax':               'Tax concerns',
    'reason_other':             'Other reason',
}

reason_counts = surveys[reason_cols].sum().sort_values(ascending=False)
reason_counts.index = [reason_labels.get(i, i) for i in reason_counts.index]
reason_pct = round((reason_counts/len(surveys) * 100), 1)

summary = pd.DataFrame({'count': reason_counts, 'pct_if_churners': reason_pct})
print('Churn Reasons: Mainly their own financial situation since this is not a necessary spend')
print()
print(summary.to_string())
print()

# Churn reasons visual
fig, ax = plt.subplots(figsize=(10,6))

bars = ax.barh(
    reason_counts.index,
    reason_counts.values,
    color='#ef4444',
    edgecolor='none',
    height=0.6
)

for bar, val in zip(bars, reason_counts.values):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            f'{val} ({val/len(surveys):.0f}%',
            va='center', fontsize=9, color='#6b7280')

ax.set_xlabel('Number of patrons who selected this reason', fontsize=10)
ax.set_title('Why Patrons Cancelled — Exit Survey Results', fontsize=13, fontweight='bold', pad=14)
ax.set_xlim(0, reason_counts.max() + 4)
ax.invert_yaxis()  # highest count at top
ax.grid(axis='x', alpha=0.3)
ax.set_facecolor('#f9fafb')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(BASE_DIR / 'outputs' / 'churn_reasons.png', bbox_inches='tight')
plt.show()
print('Saved to outputs/churn_reasons.png')

# Churn by pledge amount, low vs high values patrons
print('Pledge amounts in survey data:')
print(surveys['pledge_usd'].value_counts().sort_index())
print()

low_value = surveys[surveys['pledge_usd'].values <= 5]

high_value = surveys[surveys['pledge_usd'].values > 5]

print(f'Low value churners ($5):     {len(low_value)}')
print(f'High value churners (>$5):   {len(high_value)}')

#Comparing the churn reason by values
low_pct  = (low_value[reason_cols].sum()  / len(low_value)  * 100).round(1)
high_pct = (high_value[reason_cols].sum() / len(high_value) * 100).round(1)

comparison = pd.DataFrame({
    'Low value ($5)':   low_pct,
    'High value (>$5)': high_pct,
})
comparison.index = [reason_labels.get(i, i) for i in comparison.index]
comparison = comparison[comparison.sum(axis=1) > 0]  # hide zero rows

print('Churn reasons by pledge segment (% of each group):')
print(comparison.to_string())

# Chrun over time, group the responses by month and plot them as a timeline
churn_by_month = surveys.groupby(surveys['churned_at'].dt.to_period('M')).size()
churn_by_month.index = churn_by_month.index.astype(str)

print('Survey responses per month:')
print(churn_by_month.to_string())

# Plot
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(churn_by_month.index, churn_by_month.values, color='#f97316', edgecolor='none')
ax.set_xlabel('Month', fontsize=10)
ax.set_ylabel('Number of exit surveys', fontsize=10)
ax.set_title('Exit Survey Responses Over Time', fontsize=13, fontweight='bold', pad=14)
plt.xticks(rotation=45, ha='right', fontsize=8)
ax.grid(axis='y', alpha=0.3)
ax.set_facecolor('#f9fafb')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(BASE_DIR / 'outputs' / 'churn_over_time.png', bbox_inches='tight')
plt.show()


# Whale patrons
whale = surveys[surveys['pledge_usd'] == surveys['pledge_usd'].max()]

print('=== Highest Value Churner ===')
print(f"Pledge amount: ${whale['pledge_usd'].values[0]:,.2f}")
print(f"Churned:       {whale['churned_at'].values[0]}")
print()
print('Reasons selected:')
for col in reason_cols:
    if whale[col].values[0] == 1:
        print(f'  - {reason_labels.get(col, col)}')
print()
print('Free text feedback:')
feedback = whale['feedback_text'].values[0]
if pd.isna(feedback):
    print('  (no feedback left)')
else:
    print(textwrap.fill(str(feedback), width=80))

"""
Some patrons go want to spend the extra money to receive personalized content, like private assessments and plans,
this is why some of them have the big spike from the usual 5$, the plan is to attract low value patrons, then promote
the personalized plans, this is where the big money comes in.
"""
feedback_responses = surveys[surveys['feedback_text'].notna()][['churned_at', 'pledge_usd', 'feedback_text']]

print(f'{len(feedback_responses)} patrons left written feedback:\n')
print('─' * 60)

for _, row in feedback_responses.iterrows():
    print(f"Date: {row['churned_at'].date()}  |  Pledge: ${row['pledge_usd']}")
    print(textwrap.fill(str(row['feedback_text']), width=70))
    print('─' * 60)

# ALso some survey can be personalized, giving more insights to the creator.

insights = """
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
"""

print(insights)

churn_summary = pd.DataFrame({
    'reason': reason_counts.index,
    'count': reason_counts.values,
    'pct_of_churners': reason_pct.values
})

churn_summary.to_csv(BASE_DIR / 'data' / 'churn_reasons.csv', index=False)
print(f'Saved {len(churn_summary)} rows to data/processed/churn_reasons.csv')
print()
print(churn_summary.to_string(index=False))