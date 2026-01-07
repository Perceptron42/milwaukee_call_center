"""
Phase 2: Category Analysis
Milwaukee Call Center Data - Deep Dive into Case Types

Focus Areas:
- Top case categories (OBJECTDESC)
- Closure rates by category
- Resolution time by category
- Backlog drivers
- Closure reason patterns
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set style for professional visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Create output directory
os.makedirs('output/phase2_category', exist_ok=True)

print("=" * 80)
print("PHASE 2: CATEGORY ANALYSIS")
print("=" * 80)

# Load cleaned data
print("\n[1/7] Loading cleaned data...")
df_historical = pd.read_csv('cleaned_data/callcenterdatahistorical_cleaned.csv',
                            parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])
df_current = pd.read_csv('cleaned_data/callcenterdatacurrent_cleaned.csv',
                         parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])

# Combine datasets
df = pd.concat([df_historical, df_current], ignore_index=True)
print(f"   Total records: {len(df):,}")

# Calculate derived fields
df['RESOLUTION_TIME_HOURS'] = (df['CLOSEDDATETIME'] - df['CREATIONDATE']).dt.total_seconds() / 3600
df['RESOLUTION_TIME_DAYS'] = df['RESOLUTION_TIME_HOURS'] / 24
df['IS_CLOSED'] = df['CLOSEDDATETIME'].notna()
df['YEAR'] = df['CREATIONDATE'].dt.year

# Clean category field - TITLE contains the case type, OBJECTDESC contains addresses
df['CATEGORY'] = df['TITLE'].fillna('Unknown/Missing')
df['CATEGORY'] = df['CATEGORY'].str.strip()
df['ADDRESS'] = df['OBJECTDESC'].fillna('No Address')

print(f"   Unique categories: {df['CATEGORY'].nunique():,}")
print(f"   Missing categories: {(df['CATEGORY'] == 'Unknown/Missing').sum():,} ({(df['CATEGORY'] == 'Unknown/Missing').sum()/len(df)*100:.1f}%)")

print("\n[2/7] Analyzing Top Categories...")
print("-" * 80)

# Top 20 categories by volume
top_categories = df['CATEGORY'].value_counts().head(20)
print(f"\n📊 TOP 20 CASE CATEGORIES (by volume)")
print(f"{'Rank':<6} {'Category':<50} {'Count':>10} {'% of Total':>12}")
print("-" * 80)
for rank, (category, count) in enumerate(top_categories.items(), 1):
    pct = (count / len(df)) * 100
    # Truncate long category names
    cat_display = category[:47] + "..." if len(category) > 50 else category
    print(f"{rank:<6} {cat_display:<50} {count:>10,} {pct:>11.1f}%")

# Calculate category statistics
category_stats = df.groupby('CATEGORY').agg({
    'CREATIONDATE': 'count',
    'IS_CLOSED': ['sum', 'mean'],
    'RESOLUTION_TIME_DAYS': ['median', 'mean']
}).round(2)

category_stats.columns = ['Total_Cases', 'Closed_Cases', 'Closure_Rate', 'Median_Resolution_Days', 'Mean_Resolution_Days']
category_stats['Closure_Rate_Pct'] = (category_stats['Closure_Rate'] * 100).round(1)
category_stats['Open_Cases'] = category_stats['Total_Cases'] - category_stats['Closed_Cases']
category_stats = category_stats.sort_values('Total_Cases', ascending=False)

print("\n[3/7] Identifying Problematic Categories...")
print("-" * 80)

# Categories with worst closure rates (min 100 cases)
min_cases = 100
significant_cats = category_stats[category_stats['Total_Cases'] >= min_cases]

worst_closure = significant_cats.nsmallest(10, 'Closure_Rate_Pct')
print(f"\n🚨 WORST CLOSURE RATES (min {min_cases} cases)")
print(f"{'Category':<50} {'Total':>8} {'Closed':>8} {'Rate':>8}")
print("-" * 80)
for category, row in worst_closure.iterrows():
    cat_display = category[:47] + "..." if len(category) > 50 else category
    print(f"{cat_display:<50} {int(row['Total_Cases']):>8,} {int(row['Closed_Cases']):>8,} {row['Closure_Rate_Pct']:>7.1f}%")

# Categories with longest resolution times
longest_resolution = significant_cats[significant_cats['Median_Resolution_Days'] > 0].nlargest(10, 'Median_Resolution_Days')
print(f"\n⏱️  LONGEST RESOLUTION TIMES (min {min_cases} cases)")
print(f"{'Category':<50} {'Total':>8} {'Median Days':>12}")
print("-" * 80)
for category, row in longest_resolution.iterrows():
    cat_display = category[:47] + "..." if len(category) > 50 else category
    print(f"{cat_display:<50} {int(row['Total_Cases']):>8,} {row['Median_Resolution_Days']:>12.1f}")

# Biggest backlog contributors
biggest_backlog = significant_cats.nlargest(10, 'Open_Cases')
print(f"\n📦 BIGGEST BACKLOG CONTRIBUTORS (min {min_cases} cases)")
print(f"{'Category':<50} {'Open':>8} {'Total':>8} {'% Open':>8}")
print("-" * 80)
for category, row in biggest_backlog.iterrows():
    cat_display = category[:47] + "..." if len(category) > 50 else category
    pct_open = (row['Open_Cases'] / row['Total_Cases']) * 100
    print(f"{cat_display:<50} {int(row['Open_Cases']):>8,} {int(row['Total_Cases']):>8,} {pct_open:>7.1f}%")

print("\n[4/7] Analyzing Closure Reasons...")
print("-" * 80)

# Top closure reasons
df['CLOSURE_REASON'] = df['CASECLOSUREREASONDESCRIPTION'].fillna('Not Closed/Missing')
df['CLOSURE_REASON'] = df['CLOSURE_REASON'].str.strip()

top_closure_reasons = df[df['IS_CLOSED']]['CLOSURE_REASON'].value_counts().head(15)
print(f"\n📝 TOP 15 CLOSURE REASONS")
print(f"{'Rank':<6} {'Closure Reason':<50} {'Count':>10} {'% of Closed':>12}")
print("-" * 80)
total_closed = df['IS_CLOSED'].sum()
for rank, (reason, count) in enumerate(top_closure_reasons.items(), 1):
    pct = (count / total_closed) * 100
    reason_display = reason[:47] + "..." if len(reason) > 50 else reason
    print(f"{rank:<6} {reason_display:<50} {count:>10,} {pct:>11.1f}%")

print("\n[5/7] Creating Visualizations...")

# ============================================================================
# VISUALIZATION 1: Top 15 Categories by Volume
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

top_15_cats = category_stats.head(15)
categories = [cat[:40] + "..." if len(cat) > 40 else cat for cat in top_15_cats.index]
values = top_15_cats['Total_Cases'].values

colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(categories)))
bars = ax.barh(range(len(categories)), values, color=colors, alpha=0.8, edgecolor='black')

ax.set_yticks(range(len(categories)))
ax.set_yticklabels(categories, fontsize=10)
ax.set_xlabel('Number of Cases', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Case Categories by Volume', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(val + max(values)*0.01, i, f'{val:,}', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('output/phase2_category/1_top_categories_volume.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 1_top_categories_volume.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Closure Rate by Top Categories
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

top_15_cats_sorted = category_stats.head(15).sort_values('Closure_Rate_Pct')
categories = [cat[:40] + "..." if len(cat) > 40 else cat for cat in top_15_cats_sorted.index]
closure_rates = top_15_cats_sorted['Closure_Rate_Pct'].values

# Color code: red for low (<30%), yellow for medium (30-50%), green for high (>50%)
colors = ['red' if rate < 30 else 'orange' if rate < 50 else 'green' for rate in closure_rates]
bars = ax.barh(range(len(categories)), closure_rates, color=colors, alpha=0.7, edgecolor='black')

ax.set_yticks(range(len(categories)))
ax.set_yticklabels(categories, fontsize=10)
ax.set_xlabel('Closure Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Closure Rate by Top 15 Categories', fontsize=14, fontweight='bold', pad=20)
ax.axvline(41.9, color='blue', linestyle='--', linewidth=2, alpha=0.7, label='Overall Average (41.9%)')
ax.grid(True, alpha=0.3, axis='x')
ax.legend(loc='lower right')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, closure_rates)):
    ax.text(val + 1, i, f'{val:.1f}%', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('output/phase2_category/2_closure_rate_by_category.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 2_closure_rate_by_category.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Open vs Closed Cases (Top 10 Categories)
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

top_10_cats = category_stats.head(10)
categories = [cat[:35] + "..." if len(cat) > 35 else cat for cat in top_10_cats.index]
open_cases = top_10_cats['Open_Cases'].values
closed_cases = top_10_cats['Closed_Cases'].values

y_pos = np.arange(len(categories))
ax.barh(y_pos, closed_cases, label='Closed', color='green', alpha=0.7, edgecolor='black')
ax.barh(y_pos, open_cases, left=closed_cases, label='Open', color='red', alpha=0.7, edgecolor='black')

ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=10)
ax.set_xlabel('Number of Cases', fontsize=12, fontweight='bold')
ax.set_title('Open vs Closed Cases - Top 10 Categories', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='lower right', fontsize=11)
ax.grid(True, alpha=0.3, axis='x')

# Add total labels
for i, (open_val, closed_val) in enumerate(zip(open_cases, closed_cases)):
    total = open_val + closed_val
    ax.text(total + max(top_10_cats['Total_Cases'])*0.01, i, f'{total:,}', 
            va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('output/phase2_category/3_open_vs_closed_top10.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 3_open_vs_closed_top10.png")
plt.close()

# ============================================================================
# VISUALIZATION 4: Resolution Time by Category (Top 10 with data)
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

# Get top categories with resolution time data
top_with_resolution = category_stats[
    (category_stats['Median_Resolution_Days'] > 0) & 
    (category_stats['Total_Cases'] >= 100)
].head(10).sort_values('Median_Resolution_Days')

categories = [cat[:35] + "..." if len(cat) > 35 else cat for cat in top_with_resolution.index]
median_days = top_with_resolution['Median_Resolution_Days'].values

colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(categories)))
bars = ax.barh(range(len(categories)), median_days, color=colors, alpha=0.8, edgecolor='black')

ax.set_yticks(range(len(categories)))
ax.set_yticklabels(categories, fontsize=10)
ax.set_xlabel('Median Resolution Time (Days)', fontsize=12, fontweight='bold')
ax.set_title('Median Resolution Time by Category (Top 10)', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, median_days)):
    ax.text(val + max(median_days)*0.01, i, f'{val:.1f}d', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('output/phase2_category/4_resolution_time_by_category.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 4_resolution_time_by_category.png")
plt.close()

# ============================================================================
# VISUALIZATION 5: Top 20 Closure Reasons (Excluding "Not Closed/Missing")
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 10))

# Exclude "Not Closed/Missing" to see actual closure reasons - show top 20
top_20_reasons = top_closure_reasons[top_closure_reasons.index != 'Not Closed/Missing'].head(20)
reasons = [r[:50] + "..." if len(r) > 50 else r for r in top_20_reasons.index]
counts = top_20_reasons.values

colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(reasons)))
bars = ax.barh(range(len(reasons)), counts, color=colors, alpha=0.8, edgecolor='black')

ax.set_yticks(range(len(reasons)))
ax.set_yticklabels(reasons, fontsize=9)
ax.set_xlabel('Number of Cases', fontsize=12, fontweight='bold')
ax.set_title('Top 20 Case Closure Reasons (Excluding "Not Closed/Missing")', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels with percentages
for i, (bar, val) in enumerate(zip(bars, counts)):
    pct = (val / total_closed) * 100
    ax.text(val + max(counts)*0.01, i, f'{val:,} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=8)

plt.tight_layout()
plt.savefig('output/phase2_category/5_top_closure_reasons.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 5_top_closure_reasons.png")
plt.close()

# ============================================================================
# VISUALIZATION 6: Category Trends Over Time (Top 5)
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 8))

top_5_categories = category_stats.head(5).index
df['YEAR_MONTH'] = df['CREATIONDATE'].dt.to_period('M')

for category in top_5_categories:
    cat_data = df[df['CATEGORY'] == category]
    monthly_counts = cat_data.groupby('YEAR_MONTH').size()
    monthly_counts.index = monthly_counts.index.to_timestamp()
    
    label = category[:30] + "..." if len(category) > 30 else category
    ax.plot(monthly_counts.index, monthly_counts.values, marker='o', linewidth=2, 
            markersize=4, label=label, alpha=0.8)

ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Cases', fontsize=12, fontweight='bold')
ax.set_title('Monthly Trends - Top 5 Categories', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('output/phase2_category/6_category_trends_over_time.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 6_category_trends_over_time.png")
plt.close()

# ============================================================================
# VISUALIZATION 7: Backlog Composition (Pie Chart)
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Top 10 categories for open cases
open_cases_by_cat = df[~df['IS_CLOSED']].groupby('CATEGORY').size().nlargest(10)
other_open = df[~df['IS_CLOSED']].groupby('CATEGORY').size().sum() - open_cases_by_cat.sum()

# Prepare data for pie chart
pie_data = list(open_cases_by_cat.values) + [other_open]
pie_labels = [cat[:25] + "..." if len(cat) > 25 else cat for cat in open_cases_by_cat.index] + ['Other']

colors = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
wedges, texts, autotexts = ax1.pie(pie_data, labels=pie_labels, autopct='%1.1f%%',
                                     colors=colors, startangle=90, textprops={'fontsize': 9})

for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')

ax1.set_title('Backlog Composition - Top 10 Categories', fontsize=13, fontweight='bold', pad=20)

# Top 10 closure reasons (excluding "Not Closed/Missing")
closure_reason_counts = df[df['IS_CLOSED']].groupby('CLOSURE_REASON').size()
closure_reason_counts = closure_reason_counts[closure_reason_counts.index != 'Not Closed/Missing'].nlargest(10)
other_closure = df[df['IS_CLOSED']].groupby('CLOSURE_REASON').size().sum() - closure_reason_counts.sum() - df[df['IS_CLOSED'] & (df['CLOSURE_REASON'] == 'Not Closed/Missing')].shape[0]

pie_data2 = list(closure_reason_counts.values) + [other_closure]
pie_labels2 = [r[:25] + "..." if len(r) > 25 else r for r in closure_reason_counts.index] + ['Other']

colors2 = plt.cm.Pastel1(np.linspace(0, 1, len(pie_data2)))
wedges2, texts2, autotexts2 = ax2.pie(pie_data2, labels=pie_labels2, autopct='%1.1f%%',
                                        colors=colors2, startangle=90, textprops={'fontsize': 9})

for autotext in autotexts2:
    autotext.set_color('black')
    autotext.set_fontweight('bold')

ax2.set_title('Closure Reason Distribution', fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('output/phase2_category/7_backlog_and_closure_composition.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 7_backlog_and_closure_composition.png")
plt.close()

print("\n[6/7] Generating Category Statistics CSV...")

# Save detailed category statistics
category_stats_export = category_stats.copy()
category_stats_export = category_stats_export.reset_index()
category_stats_export.columns = ['Category', 'Total_Cases', 'Closed_Cases', 'Closure_Rate_Decimal', 
                                  'Median_Resolution_Days', 'Mean_Resolution_Days', 'Closure_Rate_Pct', 'Open_Cases']
category_stats_export = category_stats_export[['Category', 'Total_Cases', 'Open_Cases', 'Closed_Cases', 
                                                'Closure_Rate_Pct', 'Median_Resolution_Days', 'Mean_Resolution_Days']]
category_stats_export.to_csv('output/phase2_category/category_statistics.csv', index=False)
print("   ✓ Saved: category_statistics.csv")

# Save top insights
insights = {
    'Insight_Type': [
        'Top Category by Volume',
        'Category with Worst Closure Rate',
        'Category with Longest Resolution',
        'Biggest Backlog Contributor',
        'Most Common Closure Reason',
        'Total Unique Categories',
        'Categories with >1000 cases',
        'Categories with <30% closure rate'
    ],
    'Value': [
        top_categories.index[0],
        worst_closure.index[0],
        longest_resolution.index[0] if len(longest_resolution) > 0 else 'N/A',
        biggest_backlog.index[0],
        top_closure_reasons.index[0],
        df['CATEGORY'].nunique(),
        len(category_stats[category_stats['Total_Cases'] > 1000]),
        len(significant_cats[significant_cats['Closure_Rate_Pct'] < 30])
    ],
    'Details': [
        f"{top_categories.iloc[0]:,} cases",
        f"{worst_closure.iloc[0]['Closure_Rate_Pct']:.1f}% closure rate",
        f"{longest_resolution.iloc[0]['Median_Resolution_Days']:.1f} days median" if len(longest_resolution) > 0 else 'N/A',
        f"{biggest_backlog.iloc[0]['Open_Cases']:,.0f} open cases",
        f"{top_closure_reasons.iloc[0]:,} cases ({top_closure_reasons.iloc[0]/total_closed*100:.1f}%)",
        f"{(df['CATEGORY'] == 'Unknown/Missing').sum():,} missing ({(df['CATEGORY'] == 'Unknown/Missing').sum()/len(df)*100:.1f}%)",
        f"{category_stats[category_stats['Total_Cases'] > 1000]['Total_Cases'].sum():,} total cases",
        f"{significant_cats[significant_cats['Closure_Rate_Pct'] < 30]['Total_Cases'].sum():,} total cases"
    ]
}

insights_df = pd.DataFrame(insights)
insights_df.to_csv('output/phase2_category/key_insights.csv', index=False)
print("   ✓ Saved: key_insights.csv")

print("\n[7/7] Phase 2 Complete!")
print("=" * 80)
print("\n✅ KEY CATEGORY INSIGHTS:")
print(f"   1. Top category: '{top_categories.index[0][:60]}' ({top_categories.iloc[0]:,} cases)")
print(f"   2. Worst closure rate: '{worst_closure.index[0][:60]}' ({worst_closure.iloc[0]['Closure_Rate_Pct']:.1f}%)")
print(f"   3. Biggest backlog: '{biggest_backlog.index[0][:60]}' ({biggest_backlog.iloc[0]['Open_Cases']:,.0f} open)")
print(f"   4. Most common closure: '{top_closure_reasons.index[0][:60]}' ({top_closure_reasons.iloc[0]:,} cases)")
print(f"   5. {df['CATEGORY'].nunique():,} unique categories identified")

print(f"\n📁 All outputs saved to: output/phase2_category/")
print("=" * 80)
