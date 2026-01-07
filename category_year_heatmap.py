"""
Category vs Year Heatmap
Shows which categories are growing/shrinking over time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
print("Loading data...")
df_historical = pd.read_csv('cleaned_data/callcenterdatahistorical_cleaned.csv',
                            parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])
df_current = pd.read_csv('cleaned_data/callcenterdatacurrent_cleaned.csv',
                         parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])

df = pd.concat([df_historical, df_current], ignore_index=True)

# Extract year and category
df['YEAR'] = df['CREATIONDATE'].dt.year
df['CATEGORY'] = df['TITLE'].fillna('Unknown/Missing').str.strip()

# Get top 15 categories overall
top_categories = df['CATEGORY'].value_counts().head(15).index

# Create pivot table: categories vs years
pivot_data = df[df['CATEGORY'].isin(top_categories)].groupby(['CATEGORY', 'YEAR']).size().unstack(fill_value=0)

# Exclude 2026 (only 4 days of data)
pivot_data = pivot_data.drop(columns=[2026], errors='ignore')

# Sort by total volume
pivot_data['Total'] = pivot_data.sum(axis=1)
pivot_data = pivot_data.sort_values('Total', ascending=False).drop(columns='Total')

# Create heatmap
fig, ax = plt.subplots(figsize=(12, 10))

# Shorten category names for display
category_labels = [cat[:45] + "..." if len(cat) > 45 else cat for cat in pivot_data.index]

sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlOrRd', 
            linewidths=0.5, cbar_kws={'label': 'Number of Cases'},
            yticklabels=category_labels, ax=ax)

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Category', fontsize=12, fontweight='bold')
ax.set_title('Case Volume by Category and Year (Top 15 Categories)', 
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('output/phase2_category/8_category_year_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: output/phase2_category/8_category_year_heatmap.png")
plt.close()

# Print insights
print("\n" + "="*80)
print("KEY INSIGHTS FROM HEATMAP:")
print("="*80)

# Find categories with biggest growth
growth = pivot_data[2025] - pivot_data[2020]
print("\n📈 BIGGEST GROWTH (2020 → 2025):")
for cat, val in growth.nlargest(5).items():
    print(f"   {cat[:60]}: +{val:,} cases")

print("\n📉 BIGGEST DECLINE (2020 → 2025):")
for cat, val in growth.nsmallest(5).items():
    print(f"   {cat[:60]}: {val:,} cases")

# Find most consistent categories
std_dev = pivot_data.std(axis=1)
print("\n📊 MOST VOLATILE (high variation):")
for cat, val in std_dev.nlargest(5).items():
    print(f"   {cat[:60]}: σ={val:.1f}")

print("\n" + "="*80)
