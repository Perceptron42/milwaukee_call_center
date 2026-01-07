# Milwaukee Call Center - Category Analysis

## Overview
Deep dive into **381 unique case categories** from Milwaukee call center data (April 2020 - January 2026).

---

## Executive Summary

### Top Findings
1. **Brush Pickup dominates**: 12,134 cases (6.9%) with 91.2% still open
2. **Potholes nearly never close**: 4,002 cases with only 2% closure rate
3. **Garbage cart issues**: 3,642 damaged carts (97.1% open), 2,673 missing (96.4% open)
4. **Street lighting problems**: 9,409 total cases (Street Light Out + Area Dark)

---

## Top 20 Case Categories (by Volume)

| Rank | Category | Total Cases | % of Total |
|------|----------|-------------|------------|
| 1 | Brush Pickup Request | 12,134 | 6.9% |
| 2 | Parking Violations Information | 7,296 | 4.1% |
| 3 | Street Light Out | 5,269 | 3.0% |
| 4 | Missed Collection: Garbage | 4,935 | 2.8% |
| 5 | Missed Collection: Recycling | 4,320 | 2.5% |
| 6 | Area Dark | 4,140 | 2.4% |
| 7 | Pothole | 4,002 | 2.3% |
| 8 | Weeds and Tall Grass Complaint | 3,993 | 2.3% |
| 9 | Miscellaneous Information Request | 3,745 | 2.1% |
| 10 | Scattered Litter and Debris | 3,643 | 2.1% |
| 11 | Garbage Cart: Damaged | 3,642 | 2.1% |
| 12 | Sanitation Inspector Notification | 3,504 | 2.0% |
| 13 | Drop-Off Centers Information | 3,414 | 1.9% |
| 14 | Garbage Collection Day Info | 3,061 | 1.7% |
| 15 | Election Commission Transfer | 2,800 | 1.6% |
| 16 | Garbage Cart: Missing | 2,673 | 1.5% |
| 17 | Dropped Call | 2,513 | 1.4% |
| 18 | Broken Branch Down | 2,369 | 1.3% |
| 19 | Clogged Catch Basin/Flooding | 2,333 | 1.3% |
| 20 | DNS Transfer | 2,246 | 1.3% |

---

## Worst Performing Categories

### Lowest Closure Rates (min 100 cases)

| Category | Total | Closed | Closure Rate |
|----------|-------|--------|--------------|
| No Mow May Registration | 298 | 0 | 0.0% |
| Sanitation Inspector Notification | 3,504 | 31 | 1.0% |
| All Other Signs | 667 | 10 | 1.0% |
| Special Services Callback | 498 | 7 | 1.0% |
| Traffic Signal Lamp Outages | 127 | 1 | 1.0% |
| **Pothole** | **4,002** | **62** | **2.0%** |
| Recycling Cart: Additional | 1,097 | 19 | 2.0% |
| Skid Referral | 1,058 | 24 | 2.0% |
| Stop Sign | 319 | 7 | 2.0% |
| Property Not Recorded Properly | 206 | 4 | 2.0% |

**Critical Issue**: Potholes have 3,940 open cases with virtually no resolution!

---

## Longest Resolution Times

| Category | Total Cases | Median Days |
|----------|-------------|-------------|
| Property Not Recorded Properly | 206 | 39.5 |
| Interior of Building in Disrepair | 1,804 | 8.0 |
| Rats or Rat Harborage | 941 | 8.0 |
| Graffiti | 895 | 8.0 |
| Junk Vehicle on Private Property | 176 | 8.0 |
| Fence in Disrepair | 151 | 8.0 |
| Dog Feces | 111 | 6.5 |
| Large Items Discarded | 1,289 | 6.0 |
| Nuisance Vehicle | 355 | 6.0 |
| Vacant Building | 329 | 6.0 |

---

## Biggest Backlog Contributors

| Category | Open Cases | Total Cases | % Open |
|----------|-----------|-------------|--------|
| **Brush Pickup Request** | **11,070** | **12,134** | **91.2%** |
| Missed Collection: Garbage | 4,166 | 4,935 | 84.4% |
| **Pothole** | **3,940** | **4,002** | **98.5%** |
| Street Light Out | 3,758 | 5,269 | 71.3% |
| Missed Collection: Recycling | 3,649 | 4,320 | 84.5% |
| Garbage Cart: Damaged | 3,535 | 3,642 | 97.1% |
| Sanitation Inspector | 3,473 | 3,504 | 99.1% |
| Area Dark | 3,140 | 4,140 | 75.8% |
| Garbage Cart: Missing | 2,576 | 2,673 | 96.4% |
| Garbage Cart: No Cart | 1,925 | 1,986 | 96.9% |

**Total backlog in top 10 categories**: 40,232 open cases (39% of all open cases)

---

## Closure Reason Analysis

### Top 20 Actual Closure Reasons
*(Excluding "Not Closed/Missing" which represents 55.1% of closed cases)*

| Rank | Closure Reason | Count | % of Closed |
|------|----------------|-------|-------------|
| 1 | Is night parking enforced? | 1,033 | 1.4% |
| 2 | NPP | 350 | 0.5% |
| 3 | Exception entered | 346 | 0.5% |
| 4 | Request follow up | 301 | 0.4% |
| 5 | Parking info | 151 | 0.2% |
| 6 | Grass and weeds over 7 inches | 99 | 0.1% |
| 7 | x3406 | 91 | 0.1% |
| 8 | night parking | 85 | 0.1% |
| 9 | *3406 | 82 | 0.1% |
| 10 | #2 | 79 | 0.1% |
| 11-20 | Various | <70 each | <0.1% each |

**Key Insight**: Most closure reasons are parking-related or generic codes, suggesting:
- Many cases closed without detailed resolution notes
- Parking violations are most commonly "resolved" cases
- Actual service delivery cases (potholes, garbage, etc.) rarely get closure reasons

---

## Category Trends Over Time

### Top 5 Categories Monthly Trends
1. **Brush Pickup**: Seasonal spikes (spring/fall)
2. **Parking Violations**: Relatively steady
3. **Street Light Out**: Increasing over time
4. **Missed Garbage Collection**: Consistent volume
5. **Missed Recycling Collection**: Consistent volume

---

## Critical Insights by Service Area

### 🚛 Sanitation Services (High Volume, Poor Performance)
- **Brush Pickup**: 12,134 cases, 91% open
- **Missed Garbage**: 4,935 cases, 84% open
- **Missed Recycling**: 4,320 cases, 85% open
- **Garbage Cart Issues**: 10,301 total cases (damaged/missing/no cart)
- **Total Sanitation**: ~35,000 cases

**Problem**: Service delivery issues dominate call volume but rarely get resolved in system

### 🚧 Infrastructure (High Volume, Terrible Closure Rates)
- **Potholes**: 4,002 cases, 98.5% open (only 62 closed!)
- **Street Lights**: 5,269 cases, 71% open
- **Area Dark**: 4,140 cases, 76% open
- **Clogged Basins**: 2,333 cases
- **Total Infrastructure**: ~15,000 cases

**Problem**: Physical infrastructure repairs have abysmal closure rates

### 🏘️ Property/Code Enforcement (Long Resolution Times)
- **Weeds/Grass**: 3,993 cases
- **Scattered Litter**: 3,643 cases
- **Building Disrepair**: 1,804 cases (8 day median)
- **Rats/Harborage**: 941 cases (8 day median)
- **Graffiti**: 895 cases (8 day median)

**Problem**: Code enforcement cases take longest to resolve when they do close

---

## Recommendations by Category

### Immediate Triage (Week 1)
1. **Brush Pickup**: Implement seasonal auto-closure after pickup window
2. **Potholes**: Audit 3,940 open cases - many likely already fixed
3. **Garbage Carts**: Auto-close after replacement confirmed

### Process Improvements (1-3 months)
1. **Sanitation**: Integrate with route completion data for auto-closure
2. **Street Lights**: Connect to We Energies work order system
3. **Parking**: Already working well - use as model for other categories

### System Integration (6-12 months)
1. **Field service integration**: Auto-close when work orders completed
2. **IoT sensors**: Street lights report status automatically
3. **Citizen feedback**: Allow residents to confirm resolution

---

## Data Quality Issues

### Missing Closure Reasons
- **55.1% of closed cases** have no meaningful closure reason
- Suggests cases closed administratively rather than through service delivery
- Need better closure reason enforcement

### Category Granularity
- 381 unique categories may be too many
- Consider consolidating similar categories
- Some categories are internal transfers (not resident-facing)

---

## Visualizations Generated

1. **Top 15 Categories by Volume** - Brush pickup dominates
2. **Closure Rate by Category** - Color-coded performance
3. **Open vs Closed (Top 10)** - Stacked bar showing backlog
4. **Resolution Time by Category** - Property issues take longest
5. **Top 20 Closure Reasons** - Parking-heavy distribution
6. **Category Trends Over Time** - Seasonal patterns visible
7. **Backlog Composition** - Pie charts of open cases and closures

---

## Files Generated

All outputs saved to: `output/phase2_category/`

- `category_statistics.csv` - Full stats for all 381 categories
- `key_insights.csv` - Summary metrics
- 7 visualization PNG files
- This summary document

---

*Analysis completed: January 7, 2026*
