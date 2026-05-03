import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

plt.rcParams['figure.dpi'] = 120
plt.rcParams['font.family'] = 'monospace'

print('Libraries OK')

BASE_DIR = Path(__file__).parent.parent
filepathpatrons = BASE_DIR / 'data' / 'patrons_clean.csv'
filepathsurveys = BASE_DIR / 'data' / 'exit_surveys_clean.csv'

# Load the data and filter by paying patrons
patrons = pd.read_csv(filepathpatrons, parse_dates=['started_at'])

paying = patrons[patrons['is_paying'] == True]

print(f'Total patrons: {len(patrons)}')
print(f'Paying patrons: {len(paying)}')
print()
print('Tier breakdown:')
print(paying['tier'].value_counts())

crosstab = pd.crosstab(paying['tier'], paying['patron_status'])
crosstab['total'] = crosstab.sum(axis=1)

# Add retention rate column
if 'Active patron' in crosstab.columns:
    crosstab['active_rate_%'] = (crosstab['Active patron'] / crosstab['total'] * 100).round(1)

print('Patron count by tier and status:')
print(crosstab.to_string())

# Lifetime value by tier, grouping by tier and aggregating
ltv = paying.groupby('tier')['lifetime_usd'].agg(
    total_revenue = 'sum',
    avg_ltv       = 'mean',
    median_ltv    = 'median',
    patron_count  = 'count',
).round(2)

ltv['revenue_share_%'] = (ltv['total_revenue'] / ltv['total_revenue'].sum() * 100).round(1)

print('Lifetime value by tier:')
print(ltv.to_string())
print()
print(f"Total revenue across all tiers: ${ltv['total_revenue'].sum():,.2f}")

# Revenenue by tier visual
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
colors = ['#3b82f6', '#8b5cf6', '#f59e0b']
tiers = ltv.index.tolist()

# Left: total revenue
bars1 = ax1.bar(tiers, ltv['total_revenue'], color=colors, edgecolor='none', width=0.5)
for bar, val in zip(bars1, ltv['total_revenue']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'${val:,.0f}', ha='center', fontsize=9, color='#374151')
ax1.set_title('Total Revenue by Tier', fontsize=12, fontweight='bold', pad=12)
ax1.set_ylabel('Total Lifetime Revenue ($)', fontsize=10)
ax1.set_facecolor('#f9fafb')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', alpha=0.3)

# Right: average LTV
bars2 = ax2.bar(tiers, ltv['avg_ltv'], color=colors, edgecolor='none', width=0.5)
for bar, val in zip(bars2, ltv['avg_ltv']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'${val:,.0f}', ha='center', fontsize=9, color='#374151')
ax2.set_title('Average Lifetime Value per Patron', fontsize=12, fontweight='bold', pad=12)
ax2.set_ylabel('Avg LTV ($)', fontsize=10)
ax2.set_facecolor('#f9fafb')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('Tier Revenue Analysis', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(BASE_DIR / 'outputs' / 'tier_revenue.png', bbox_inches='tight')
plt.show()

# Avg pledge by tier
avg_pledge = paying.groupby('tier')['pledge_usd'].mean().round(2)

print('Average pledge amount by tier:')
print(avg_pledge.to_string())

# VIP Rewards has a higher avg pledge than Commission, which is a tier only richer or big fans subscribe to,
# and they tend to stay subscribed, this is a step further that a real fan will take to support.

# Retention rate by tier (mean of is_active, grouped by tier)
retention_by_tier = (paying.groupby('tier')['is_active'].mean() * 100).round(1)

print('Active patron rate by tier (%):')
print(retention_by_tier.to_string())

# Plot
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(retention_by_tier.index, retention_by_tier.values,
              color=['#3b82f6', '#8b5cf6', '#f59e0b'], edgecolor='none', width=0.5)
for bar, val in zip(bars, retention_by_tier.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val}%', ha='center', fontsize=10, fontweight='bold', color='#374151')
ax.axhline(y=50, color='#ef4444', linestyle='--', linewidth=1, alpha=0.5, label='50% line')
ax.set_title('Current Active Rate by Tier', fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel('% of patrons still active', fontsize=10)
ax.set_ylim(0, 100)
ax.set_facecolor('#f9fafb')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig(BASE_DIR / 'outputs' / 'tier_retention.png', bbox_inches='tight')
plt.show()

# Group by tier, get mean and median of tenure_days
tenure = paying.groupby('tier')['tenure_days'].agg(['mean', 'median']).round(0)
tenure.columns = ['avg_days', 'median_days']
tenure['avg_months']    = (tenure['avg_days'] / 30.44).round(1)
tenure['median_months'] = (tenure['median_days'] / 30.44).round(1)

print('Tenure by tier:')
print(tenure.to_string())

# Which tier has the longest average tenure? As I've mentioned previously, VIP Rewards is where the tryhard fans are.

vip_patrons = paying[paying['tier'] == 'VIP Rewards']
vip_avg_pledge = vip_patrons[vip_patrons['pledge_usd'] < 100]['pledge_usd'].mean()

full_rewards_avg_pledge = paying[paying['tier'] == 'Full Rewards']['pledge_usd'].mean()

# How many Full Rewards patrons would need to upgrade to VIP to be meaningful?
upsell_count = 10  # CHANGE THIS

monthly_gain = upsell_count * (vip_avg_pledge - full_rewards_avg_pledge)
annual_gain  = monthly_gain * 12

print(f'Full Rewards avg pledge:  ${full_rewards_avg_pledge:.2f}/month')
print(f'VIP Rewards avg pledge:   ${vip_avg_pledge:.2f}/month')
print(f'Difference per patron:    ${vip_avg_pledge - full_rewards_avg_pledge:.2f}/month')
print()
print(f'If {upsell_count} Full Rewards patrons upgraded to VIP:')
print(f'  Monthly revenue gain:   ${monthly_gain:,.2f}')
print(f'  Annual revenue gain:    ${annual_gain:,.2f}')

# Is upselling realistic given what you know about your audience? Upselling is hard, it depends entirely on how
# the patrons see you and even how much they like your personality, along with the content.

insights = """
1. Which tier generates the most total revenue and why:
Full rewards tier generates the most since it's the most accessible one, VIP generates extra money for no extra work,
Commissions is where a big boost of money comes, but it requires the most work.

2. Which tier is most valuable per patron and what that means:
Commission tier is the most valuable, people are willing to pay way extra for personalized content and insights, 
especially from someone they respect, enjoy etc.

3. Which tier retains best and which retains worst:
Full rewards retains the best since again, it's the most accessible (cheapest), so people don't mind that much a coffee
per month, also VIP is not that behind also. Full Rewards has the most active patrons, but VIP shows longer average 
tenure.

4. What the upsell calculation reveals about revenue growth potential:
Upselling can bring extra revenue at to extra work, but again, patron deciding to upgrade is based entirely on their
decisions, it's very hard to influence that directly, maybe in the long run, since they will be part of the journey
themselves. Even a small upsell of 10 patron will generate around 500$ per year extra.

5. Top recommendation: where should the creator focus — more patrons, higher tiers, or better retention?
The recomandation is to increase the funnel itself, Free patrons > Full Rewards > VIP > Commission, the more the better,
since even the free patrons can subscribe with upgrade coupons.
"""
print(insights)

tier_summary = ltv.copy()
tier_summary['avg_pledge_usd']    = paying.groupby('tier')['pledge_usd'].mean().round(2)
tier_summary['active_rate_%']     = (paying.groupby('tier')['is_active'].mean() * 100).round(1)
tier_summary['avg_tenure_months'] = (paying.groupby('tier')['tenure_days'].mean() / 30.44).round(1)

tier_summary.to_csv(BASE_DIR / 'data' / 'tier_summary.csv')
print('Saved tier_summary.csv')
print()
print(tier_summary.to_string())

