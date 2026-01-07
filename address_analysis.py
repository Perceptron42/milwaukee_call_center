"""
Address Analysis
Identifies problematic addresses with frequent complaints
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output directory
os.makedirs('output/phase3_address', exist_ok=True)

print("=" * 80)
print("ADDRESS ANALYSIS - FREQUENT COMPLAINERS")
print("=" * 80)

# Load cleaned data
print("\n[1/5] Loading data...")
df_historical = pd.read_csv('cleaned_data/callcenterdatahistorical_cleaned.csv',
                            parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])
df_current = pd.read_csv('cleaned_data/callcenterdatacurrent_cleaned.csv',
                         parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])

df = pd.concat([df_historical, df_current], ignore_index=True)

# Add derived fields
df['ADDRESS'] = df['OBJECTDESC'].fillna('No Address').str.strip()
df['CATEGORY'] = df['TITLE'].fillna('Unknown').str.strip()
df['YEAR'] = df['CREATIONDATE'].dt.year
df['IS_CLOSED'] = df['CLOSEDDATETIME'].notna()

# Filter out missing addresses
df_with_address = df[df['ADDRESS'] != 'No Address']
print(f"   Total records: {len(df):,}")
print(f"   Records with address: {len(df_with_address):,}")
print(f"   Unique addresses: {df_with_address['ADDRESS'].nunique():,}")

print("\n[2/5] Finding Top Complaining Addresses...")
print("-" * 80)

# Top addresses by complaint count
address_counts = df_with_address.groupby('ADDRESS').agg({
    'CREATIONDATE': 'count',
    'IS_CLOSED': 'sum',
    'CATEGORY': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Various'
}).rename(columns={'CREATIONDATE': 'Total_Cases', 'IS_CLOSED': 'Closed_Cases', 'CATEGORY': 'Top_Category'})

address_counts['Closure_Rate'] = (address_counts['Closed_Cases'] / address_counts['Total_Cases'] * 100).round(1)
address_counts['Open_Cases'] = address_counts['Total_Cases'] - address_counts['Closed_Cases']
address_counts = address_counts.sort_values('Total_Cases', ascending=False)

# Top 25 addresses
top_25 = address_counts.head(25)
print(f"\n📍 TOP 25 ADDRESSES BY COMPLAINT VOLUME")
print(f"{'Rank':<6} {'Address':<55} {'Cases':>8} {'Open':>8} {'Top Issue':<30}")
print("-" * 110)
for rank, (address, row) in enumerate(top_25.iterrows(), 1):
    addr_display = address[:52] + "..." if len(address) > 55 else address
    cat_display = row['Top_Category'][:27] + "..." if len(str(row['Top_Category'])) > 30 else row['Top_Category']
    print(f"{rank:<6} {addr_display:<55} {int(row['Total_Cases']):>8} {int(row['Open_Cases']):>8} {cat_display:<30}")

print("\n[3/5] Analyzing Repeat Offenders...")
print("-" * 80)

# Addresses with 10+ complaints
repeat_offenders = address_counts[address_counts['Total_Cases'] >= 10]
print(f"\n🔴 REPEAT OFFENDERS (10+ complaints)")
print(f"   Total addresses with 10+ complaints: {len(repeat_offenders):,}")
print(f"   Total cases from these addresses: {repeat_offenders['Total_Cases'].sum():,}")
print(f"   Percentage of all cases: {repeat_offenders['Total_Cases'].sum()/len(df_with_address)*100:.1f}%")

# Addresses with 20+ complaints
high_volume = address_counts[address_counts['Total_Cases'] >= 20]
print(f"\n⚠️  HIGH VOLUME (20+ complaints)")
print(f"   Total addresses: {len(high_volume):,}")
print(f"   Total cases: {high_volume['Total_Cases'].sum():,}")

# Addresses with 50+ complaints
chronic = address_counts[address_counts['Total_Cases'] >= 50]
print(f"\n🚨 CHRONIC LOCATIONS (50+ complaints)")
print(f"   Total addresses: {len(chronic):,}")
print(f"   Total cases: {chronic['Total_Cases'].sum():,}")

# Analyze categories for top addresses
print("\n[4/5] Category Breakdown for Top Addresses...")
print("-" * 80)

top_10_addresses = address_counts.head(10).index

for address in top_10_addresses[:5]:
    addr_data = df_with_address[df_with_address['ADDRESS'] == address]
    top_cats = addr_data['CATEGORY'].value_counts().head(3)
    addr_display = address[:60] if len(address) <= 60 else address[:57] + "..."
    print(f"\n📍 {addr_display} ({len(addr_data)} cases)")
    for cat, count in top_cats.items():
        cat_display = cat[:50] if len(cat) <= 50 else cat[:47] + "..."
        print(f"   - {cat_display}: {count}")

print("\n[5/5] Creating Visualizations...")

# ============================================================================
# VISUALIZATION 1: Top 20 Addresses by Complaint Volume
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 10))

top_20 = address_counts.head(20)
addresses = [addr[:40] + "..." if len(addr) > 40 else addr for addr in top_20.index]
values = top_20['Total_Cases'].values

colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(addresses)))
bars = ax.barh(range(len(addresses)), values, color=colors, alpha=0.8, edgecolor='black')

ax.set_yticks(range(len(addresses)))
ax.set_yticklabels(addresses, fontsize=9)
ax.set_xlabel('Number of Cases', fontsize=12, fontweight='bold')
ax.set_title('Top 20 Addresses by Complaint Volume', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(val + max(values)*0.01, i, f'{val:,}', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('output/phase3_address/1_top_addresses_volume.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 1_top_addresses_volume.png")
plt.close()

# ============================================================================
# VISUALIZATION 2: Distribution of Complaints per Address
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

bins = [1, 2, 3, 5, 10, 20, 50, 100]
hist_data = np.histogram(address_counts['Total_Cases'], bins=bins)

labels = ['1', '2', '3-4', '5-9', '10-19', '20-49', '50+']
ax.bar(labels, hist_data[0], color='steelblue', alpha=0.7, edgecolor='black')
ax.set_xlabel('Number of Complaints per Address', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Addresses', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Complaints per Address', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y')

for i, val in enumerate(hist_data[0]):
    ax.text(i, val + max(hist_data[0])*0.01, f'{val:,}', ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('output/phase3_address/2_complaint_distribution.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 2_complaint_distribution.png")
plt.close()

# ============================================================================
# VISUALIZATION 3: Closure Rate by Complaint Volume
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

# Group addresses by complaint volume
volume_bins = pd.cut(address_counts['Total_Cases'], bins=[0, 1, 2, 5, 10, 20, 50, 1000], 
                     labels=['1', '2', '3-5', '6-10', '11-20', '21-50', '50+'])
closure_by_volume = address_counts.groupby(volume_bins).agg({
    'Total_Cases': 'sum',
    'Closed_Cases': 'sum'
})
closure_by_volume['Closure_Rate'] = (closure_by_volume['Closed_Cases'] / closure_by_volume['Total_Cases'] * 100)

bars = ax.bar(closure_by_volume.index.astype(str), closure_by_volume['Closure_Rate'], 
              color='teal', alpha=0.7, edgecolor='black')
ax.axhline(41.9, color='red', linestyle='--', linewidth=2, label='Overall Average (41.9%)')
ax.set_xlabel('Complaints per Address', fontsize=12, fontweight='bold')
ax.set_ylabel('Closure Rate (%)', fontsize=12, fontweight='bold')
ax.set_title('Closure Rate by Address Complaint Volume', fontsize=14, fontweight='bold', pad=20)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('output/phase3_address/3_closure_rate_by_volume.png', dpi=300, bbox_inches='tight')
print("   ✓ Saved: 3_closure_rate_by_volume.png")
plt.close()

# Save top addresses to CSV
address_counts.head(100).to_csv('output/phase3_address/top_100_addresses.csv')
print("   ✓ Saved: top_100_addresses.csv")

print("\n" + "=" * 80)
print("✅ ADDRESS ANALYSIS COMPLETE!")
print("=" * 80)
print(f"\n📊 KEY FINDINGS:")
print(f"   1. Top address: {address_counts.index[0][:60]} ({int(address_counts.iloc[0]['Total_Cases'])} cases)")
print(f"   2. Addresses with 10+ complaints: {len(repeat_offenders):,}")
print(f"   3. Addresses with 50+ complaints: {len(chronic):,}")
print(f"   4. {repeat_offenders['Total_Cases'].sum():,} cases ({repeat_offenders['Total_Cases'].sum()/len(df_with_address)*100:.1f}%) from repeat addresses")

print(f"\n📁 All outputs saved to: output/phase3_address/")
print("=" * 80)
