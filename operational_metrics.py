"""
Phase 1: Operational Metrics Analysis
Milwaukee Call Center Data - Quick Wins Analysis

Focus Areas:
- Volume & Trends
- COVID-19 Impact
- Seasonal Patterns
- Key Performance Metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set style for professional visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Create output directory
os.makedirs('output/phase1_operational', exist_ok=True)

print("=" * 80)
print("PHASE 1: OPERATIONAL METRICS ANALYSIS")
print("=" * 80)

# Load cleaned data
print("\n[1/6] Loading cleaned data...")
df_historical = pd.read_csv('cleaned_data/callcenterdatahistorical_cleaned.csv',
                            parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])
df_current = pd.read_csv('cleaned_data/callcenterdatacurrent_cleaned.csv',
                         parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])

# Combine datasets
df = pd.concat([df_historical, df_current], ignore_index=True)
print(f"   Total records: {len(df):,}")
print(f"   Date range: {df['CREATIONDATE'].min()} to {df['CREATIONDATE'].max()}")

# Calculate resolution time
df['RESOLUTION_TIME_HOURS'] = (df['CLOSEDDATETIME'] - df['CREATIONDATE']).dt.total_seconds() / 3600
df['IS_CLOSED'] = df['CLOSEDDATETIME'].notna()

# Extract time features
df['YEAR'] = df['CREATIONDATE'].dt.year
df['MONTH'] = df['CREATIONDATE'].dt.month
df['YEAR_MONTH'] = df['CREATIONDATE'].dt.to_period('M')
df['DAY_OF_WEEK'] = df['CREATIONDATE'].dt.day_name()
df['DATE'] = df['CREATIONDATE'].dt.date

# Data collection start marker (actual operational data begins April 25, 2020)
data_start = pd.to_datetime('2020-04-25')
df['IS_POST_START'] = df['CREATIONDATE'] >= data_start

print("\n[2/6] Calculating Key Metrics...")
print("-" * 80)

# Overall metrics
total_cases = len(df)
closed_cases = df['IS_CLOSED'].sum()
closure_rate = (closed_cases / total_cases) * 100
avg_resolution_hours = df[df['IS_CLOSED']]['RESOLUTION_TIME_HOURS'].median()
avg_resolution_days = avg_resolution_hours / 24

print(f"\n📊 OVERALL METRICS")
print(f"   Total Cases: {total_cases:,}")
print(f"   Closed Cases: {closed_cases:,} ({closure_rate:.1f}%)")
print(f"   Open Cases: {total_cases - closed_cases:,} ({100-closure_rate:.1f}%)")
print(f"   Median Resolution Time: {avg_resolution_days:.1f} days ({avg_resolution_hours:.1f} hours)")

# Pre/Post data collection start comparison
pre_start = df[~df['IS_POST_START']]
post_start = df[df['IS_POST_START']]

print(f"\n📅 DATA COLLECTION TIMELINE")
print(f"   Initial Cases (Mar 21 - Apr 24, 2020): {len(pre_start):,}")
print(f"   Full Operations (Apr 25, 2020+): {len(post_start):,}")
if len(post_start[post_start['IS_CLOSED']]) > 0:
    post_start_res = post_start[post_start['IS_CLOSED']]['RESOLUTION_TIME_HOURS'].median() / 24
    print(f"   Closure Rate (Full Operations): {(post_start['IS_CLOSED'].sum()/len(post_start)*100):.1f}%")
    print(f"   Median Resolution (Full Operations): {post_start_res:.1f} days")

# Yearly breakdown
print(f"\n📅 YEARLY BREAKDOWN (Note: 2026 only has 4 days of data)")
yearly_stats = df.groupby('YEAR').agg({
    'CREATIONDATE': 'count',
    'IS_CLOSED': ['sum', 'mean']
}).round(3)
yearly_stats.columns = ['Total_Cases', 'Closed_Cases', 'Closure_Rate']
yearly_stats['Closure_Rate'] = (yearly_stats['Closure_Rate'] * 100).round(1)
print(yearly_stats.to_string())

# Recent trends (last 6 months)
six_months_ago = df['CREATIONDATE'].max() - timedelta(days=180)
recent_df = df[df['CREATIONDATE'] >= six_months_ago]
print(f"\n📈 RECENT TRENDS (Last 6 Months)")
print(f"   Cases Created: {len(recent_df):,}")
print(f"   Closure Rate: {(recent_df['IS_CLOSED'].sum()/len(recent_df)*100):.1f}%")
print(f"   Avg Daily Volume: {len(recent_df)/180:.1f} cases/day")

print("\n[3/6] Creating Visualizations...")

# ============================================================================
# VISUALIZATION 1: Call Volume Over Time with COVID Annotation
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 6))

# Daily volume
daily_volume = df.groupby('DATE').size().reset_index(name='count')
daily_volume['DATE'] = pd.to_datetime(daily_volume['DATE'])

ax.plot(daily_volume['DATE'], daily_volume['count'], linewidth=1, alpha=0.6, color='steelblue')

# 7-day moving average
daily_volume['MA7'] = daily_volume['count'].rolling(window=7, center=True).mean()
ax.plot(daily_volume['DATE'], daily_volume['MA7'], linewidth=2.5, color='darkblue', label='7-Day Moving Average')

# Data collection start annotation
ax.axvline(data_start, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Full Operations Start (Apr 25, 2020)')

ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Daily Call Volume', fontsize=12, fontweight='bold')
ax.set_title('Milwaukee Call Center: Daily Volume Trends (2020-2026)', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/phase1_operational/1_daily_volume_trend.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 1_daily_volume_trend.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Monthly Volume Comparison
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Monthly volume
monthly_volume = df.groupby('YEAR_MONTH').size().reset_index(name='count')
monthly_volume['YEAR_MONTH_STR'] = monthly_volume['YEAR_MONTH'].astype(str)

colors = ['green' if pd.to_datetime(str(ym)) >= data_start else 'lightgray' 
          for ym in monthly_volume['YEAR_MONTH']]

ax1.bar(range(len(monthly_volume)), monthly_volume['count'], color=colors, alpha=0.7)
ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
ax1.set_ylabel('Total Cases', fontsize=12, fontweight='bold')
ax1.set_title('Monthly Call Volume', fontsize=13, fontweight='bold')
ax1.set_xticks(range(0, len(monthly_volume), 6))
ax1.set_xticklabels(monthly_volume['YEAR_MONTH_STR'].iloc[::6], rotation=45, ha='right')
ax1.grid(True, alpha=0.3, axis='y')

# Yearly comparison
yearly_volume = df.groupby('YEAR').size()
colors_year = ['lightgray' if year == 2020 else 'steelblue' if year < 2026 else 'orange' for year in yearly_volume.index]
ax2.bar(yearly_volume.index, yearly_volume.values, color=colors_year, alpha=0.7, edgecolor='black')
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Cases', fontsize=12, fontweight='bold')
ax2.set_title('Yearly Call Volume', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (year, count) in enumerate(yearly_volume.items()):
    label = f'{count:,}' if year != 2026 else f'{count:,}*'
    ax2.text(year, count + 1000, label, ha='center', va='bottom', fontweight='bold')

# Add note for 2026
ax2.text(0.98, 0.02, '* 2026: Only 4 days of data (Jan 1-4)', 
         transform=ax2.transAxes, ha='right', va='bottom', fontsize=9, style='italic', color='gray')

plt.tight_layout()
plt.savefig('output/phase1_operational/2_monthly_yearly_volume.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 2_monthly_yearly_volume.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Resolution Time Distribution
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Filter to reasonable resolution times (< 365 days)
resolved_df = df[df['IS_CLOSED'] & (df['RESOLUTION_TIME_HOURS'] < 365*24)]

# Histogram
ax1.hist(resolved_df['RESOLUTION_TIME_HOURS'] / 24, bins=50, color='green', alpha=0.7, edgecolor='black')
ax1.axvline(avg_resolution_days, color='red', linestyle='--', linewidth=2, label=f'Median: {avg_resolution_days:.1f} days')
ax1.set_xlabel('Resolution Time (Days)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Cases', fontsize=12, fontweight='bold')
ax1.set_title('Resolution Time Distribution (Closed Cases < 1 Year)', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Box plot by year
resolved_by_year = df[df['IS_CLOSED'] & (df['RESOLUTION_TIME_HOURS'] < 365*24)].copy()
resolved_by_year['RESOLUTION_DAYS'] = resolved_by_year['RESOLUTION_TIME_HOURS'] / 24

box_data = [resolved_by_year[resolved_by_year['YEAR'] == year]['RESOLUTION_DAYS'].values 
            for year in sorted(resolved_by_year['YEAR'].unique())]
positions = sorted(resolved_by_year['YEAR'].unique())

bp = ax2.boxplot(box_data, positions=positions, widths=0.6, patch_artist=True,
                 boxprops=dict(facecolor='lightblue', alpha=0.7),
                 medianprops=dict(color='red', linewidth=2))

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Resolution Time (Days)', fontsize=12, fontweight='bold')
ax2.set_title('Resolution Time by Year', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('output/phase1_operational/3_resolution_time_distribution.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 3_resolution_time_distribution.png")
plt.close()

# ============================================================================
# VISUALIZATION 3b: Resolution Time for Recent Years (2022-2026)
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Filter to recent years only (2022-2026) and reasonable resolution times
recent_resolved = df[df['IS_CLOSED'] & 
                     (df['YEAR'] >= 2022) & 
                     (df['RESOLUTION_TIME_HOURS'] < 365*24)].copy()
recent_resolved['RESOLUTION_DAYS'] = recent_resolved['RESOLUTION_TIME_HOURS'] / 24

# Histogram for recent years
ax1.hist(recent_resolved['RESOLUTION_DAYS'], bins=50, color='teal', alpha=0.7, edgecolor='black')
recent_median = recent_resolved['RESOLUTION_DAYS'].median()
ax1.axvline(recent_median, color='red', linestyle='--', linewidth=2, 
            label=f'Median: {recent_median:.1f} days')
ax1.set_xlabel('Resolution Time (Days)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Cases', fontsize=12, fontweight='bold')
ax1.set_title('Resolution Time Distribution (2022-2026 Only)', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Box plot by year for recent years
box_data_recent = [recent_resolved[recent_resolved['YEAR'] == year]['RESOLUTION_DAYS'].values 
                   for year in sorted(recent_resolved['YEAR'].unique())]
positions_recent = sorted(recent_resolved['YEAR'].unique())

bp = ax2.boxplot(box_data_recent, positions=positions_recent, widths=0.6, patch_artist=True,
                 boxprops=dict(facecolor='lightgreen', alpha=0.7),
                 medianprops=dict(color='red', linewidth=2))

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Resolution Time (Days)', fontsize=12, fontweight='bold')
ax2.set_title('Resolution Time by Year (2022-2026)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Add median values as text
for i, year in enumerate(positions_recent):
    median_val = recent_resolved[recent_resolved['YEAR'] == year]['RESOLUTION_DAYS'].median()
    ax2.text(year, median_val, f'{median_val:.1f}d', ha='center', va='bottom', 
             fontweight='bold', fontsize=9, color='darkred')

plt.tight_layout()
plt.savefig('output/phase1_operational/3b_resolution_time_recent_years.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 3b_resolution_time_recent_years.png")
plt.close()

# ============================================================================
# VISUALIZATION 4: Closure Rate Trends
# ============================================================================
fig, ax = plt.subplots(figsize=(16, 6))

# Monthly closure rate
monthly_closure = df.groupby('YEAR_MONTH').agg({
    'IS_CLOSED': ['sum', 'count', 'mean']
}).reset_index()
monthly_closure.columns = ['YEAR_MONTH', 'Closed', 'Total', 'Rate']
monthly_closure['Rate_Pct'] = monthly_closure['Rate'] * 100
monthly_closure['YEAR_MONTH_DT'] = monthly_closure['YEAR_MONTH'].apply(lambda x: x.to_timestamp())

ax.plot(monthly_closure['YEAR_MONTH_DT'], monthly_closure['Rate_Pct'], 
        linewidth=2.5, color='green', marker='o', markersize=4)
ax.axhline(closure_rate, color='red', linestyle='--', linewidth=2, alpha=0.7, 
           label=f'Overall Average: {closure_rate:.1f}%')
ax.axvline(data_start, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Full Operations Start')

ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Closure Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Case Closure Rate Over Time', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output/phase1_operational/4_closure_rate_trend.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 4_closure_rate_trend.png")
plt.close()

# ============================================================================
# VISUALIZATION 5: Day of Week Pattern
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 6))

# Day of week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_volume = df.groupby('DAY_OF_WEEK').size().reindex(day_order)

colors_dow = ['steelblue' if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] 
              else 'coral' for day in day_order]
ax.bar(range(len(day_volume)), day_volume.values, color=colors_dow, alpha=0.7, edgecolor='black')
ax.set_xticks(range(len(day_order)))
ax.set_xticklabels(day_order, rotation=45, ha='right')
ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Cases', fontsize=12, fontweight='bold')
ax.set_title('Call Volume by Day of Week', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, count in enumerate(day_volume.values):
    ax.text(i, count + 1000, f'{count:,}', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('output/phase1_operational/5_day_of_week_pattern.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 5_day_of_week_pattern.png")
plt.close()

# ============================================================================
# VISUALIZATION 6: Key Metrics Dashboard
# ============================================================================
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# Metric boxes
metrics = [
    ("Total Cases", f"{total_cases:,}", "steelblue"),
    ("Closed Cases", f"{closed_cases:,}", "green"),
    ("Open Cases", f"{total_cases - closed_cases:,}", "red"),
    ("Closure Rate", f"{closure_rate:.1f}%", "purple"),
    ("Median Resolution", f"{avg_resolution_days:.1f} days", "orange"),
    ("Avg Daily Volume", f"{len(df)/len(df['DATE'].unique()):.1f}", "teal"),
]

for idx, (label, value, color) in enumerate(metrics):
    row = idx // 3
    col = idx % 3
    ax = fig.add_subplot(gs[row, col])
    ax.text(0.5, 0.6, value, ha='center', va='center', fontsize=32, fontweight='bold', color=color)
    ax.text(0.5, 0.3, label, ha='center', va='center', fontsize=14, color='gray')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor=color, linewidth=3))

fig.suptitle('Milwaukee Call Center - Key Operational Metrics', fontsize=18, fontweight='bold', y=0.98)
plt.savefig('output/phase1_operational/6_metrics_dashboard.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 6_metrics_dashboard.png")
plt.close()

print("\n[4/6] Analyzing Peak Times...")
print("-" * 80)

# Peak analysis
peak_day = day_volume.idxmax()
peak_day_count = day_volume.max()

print(f"\n⏰ PEAK DAY")
print(f"   Busiest Day: {peak_day} ({peak_day_count:,} cases)")
print(f"   Note: Hourly data not available (all timestamps at midnight)")

# Identify unusual spikes
daily_volume['Z_SCORE'] = (daily_volume['count'] - daily_volume['count'].mean()) / daily_volume['count'].std()
spikes = daily_volume[daily_volume['Z_SCORE'] > 3].sort_values('count', ascending=False).head(5)

if len(spikes) > 0:
    print(f"\n🚨 UNUSUAL SPIKES (Top 5 Days)")
    for idx, row in spikes.iterrows():
        print(f"   {row['DATE']}: {row['count']} cases (Z-score: {row['Z_SCORE']:.2f})")

print("\n[5/6] Generating Summary Statistics...")

# Create summary CSV
summary_stats = {
    'Metric': [
        'Total Cases',
        'Closed Cases',
        'Open Cases',
        'Overall Closure Rate (%)',
        'Median Resolution Time (days)',
        'Mean Resolution Time (days)',
        'Initial Period Cases (Mar 21 - Apr 24, 2020)',
        'Full Operations Cases (Apr 25, 2020+)',
        'Full Operations Closure Rate (%)',
        'Date Range Start',
        'Date Range End',
        'Total Days Covered',
        'Average Daily Volume',
        'Peak Day',
        '2026 Data Coverage'
    ],
    'Value': [
        total_cases,
        closed_cases,
        total_cases - closed_cases,
        f"{closure_rate:.2f}",
        f"{avg_resolution_days:.2f}",
        f"{df[df['IS_CLOSED']]['RESOLUTION_TIME_HOURS'].mean() / 24:.2f}" if df['IS_CLOSED'].sum() > 0 else "N/A",
        len(pre_start),
        len(post_start),
        f"{(post_start['IS_CLOSED'].sum()/len(post_start)*100):.2f}" if len(post_start) > 0 else "N/A",
        str(df['CREATIONDATE'].min()),
        str(df['CREATIONDATE'].max()),
        (df['CREATIONDATE'].max() - df['CREATIONDATE'].min()).days,
        f"{len(df)/len(df['DATE'].unique()):.2f}",
        peak_day,
        'Jan 1-4 only (4 days)'
    ]
}

summary_df = pd.DataFrame(summary_stats)
summary_df.to_csv('output/phase1_operational/summary_statistics.csv', index=False)
print("   ✓ Saved: summary_statistics.csv")

print("\n[6/6] Phase 1 Complete!")
print("=" * 80)
print("\n✅ KEY FINDINGS:")
print(f"   1. {closure_rate:.1f}% closure rate suggests potential backlog issues")
print(f"   2. Data collection started Apr 25, 2020 with {len(post_start):,} cases since then")
print(f"   3. Median resolution time is {avg_resolution_days:.1f} days")
print(f"   4. Peak activity: {peak_day}s ({peak_day_count:,} cases)")
print(f"   5. Average {len(df)/len(df['DATE'].unique()):.1f} cases per day")
print(f"   6. 2026 data is incomplete (only Jan 1-4)")

print(f"\n📁 All outputs saved to: output/phase1_operational/")
print("=" * 80)
