# Milwaukee Call Center - Operational Metrics Analysis

## Overview
Analysis of Milwaukee call center operational data from **April 25, 2020 to January 4, 2026** covering **175,933 total cases**.

---

## Executive Summary

### Key Metrics
- **Total Cases**: 175,933
- **Closure Rate**: 41.9% (73,668 closed, 102,265 open)
- **Median Resolution Time**: 0.0 days (instant closure when closed)
- **Average Daily Volume**: 85.3 cases/day
- **Peak Day**: Tuesday (33,180 total cases)

### Critical Findings
1. **58.1% of cases remain open** - significant backlog issue
2. **2020 dominated volume**: 138,267 cases (78.6% of all cases)
3. **Declining closure rates**: Recent 6 months only 29.9% (getting worse)
4. **Unusual spikes**: Nov 2-3, 2020 had ~1,900 cases/day (7.5x normal)

---

## Data Collection Timeline

- **Initial Period**: March 21 - April 24, 2020 (1 case - testing)
- **Full Operations**: April 25, 2020 onwards (175,932 cases)
- **Latest Data**: January 1-4, 2026 (93 cases in 4 days)

---

## Volume Trends

### Yearly Breakdown
| Year | Total Cases | Closed Cases | Closure Rate |
|------|------------|--------------|--------------|
| 2020 | 138,267 | 59,801 | 43.3% |
| 2021 | 4,043 | 870 | 21.5% |
| 2022 | 5,204 | 2,141 | 41.1% |
| 2023 | 10,446 | 3,959 | 37.9% |
| 2024 | 7,296 | 3,149 | 43.2% |
| 2025 | 10,584 | 3,727 | 35.2% |
| 2026* | 93 | 21 | 22.6% |

*2026 only has 4 days of data (Jan 1-4)

### Key Observations
- **2020 surge**: COVID-19 impact resulted in 34x more cases than typical years
- **Post-2020 stabilization**: Volume settled to ~5,000-10,000 cases/year
- **Declining performance**: Closure rates trending downward since 2020

---

## Operational Patterns

### Day of Week Distribution
- **Busiest Day**: Tuesday (33,180 cases)
- **Weekday vs Weekend**: Weekdays dominate (as expected for city services)

### Temporal Anomalies
**Unusual Spikes (Top 5 Days)**:
1. Nov 3, 2020: 1,898 cases (Z-score: 7.48)
2. Nov 2, 2020: 1,891 cases (Z-score: 7.45)
3. Nov 30, 2020: 1,388 cases (Z-score: 5.37)
4. Oct 20, 2020: 1,374 cases (Z-score: 5.32)
5. Nov 9, 2020: 1,267 cases (Z-score: 4.87)

*Note: November 2020 spikes likely related to election period*

---

## Resolution Performance

### Resolution Time Analysis
- **Median**: 0.0 days (instant when closed)
- **Mean**: 2.5 days
- **Distribution**: Most cases closed immediately or remain open indefinitely

### Recent Years (2022-2026)
Focused analysis shows resolution times vary by year, with median times generally under 1 day for cases that do get closed.

---

## Visualizations Generated

1. **Daily Volume Trend** - Shows 2020 surge and subsequent decline
2. **Monthly/Yearly Volume** - Comparison across time periods
3. **Resolution Time Distribution** - All years view
4. **Resolution Time (2022-2026)** - Recent years focused view
5. **Closure Rate Trends** - Declining performance over time
6. **Day of Week Pattern** - Tuesday peak clearly visible
7. **Metrics Dashboard** - Key numbers at a glance

---

## Critical Issues Identified

### 1. Massive Backlog (102,265 open cases)
- 58.1% of all cases remain unresolved
- Represents years of accumulated work
- Growing worse over time (recent 6 months: 70.1% open)

### 2. Declining Closure Rates
- Overall: 41.9%
- Recent 6 months: 29.9%
- 2026 (partial): 22.6%
- **Trend is deteriorating**

### 3. 2020 Legacy Impact
- 78,466 cases from 2020 still open (56.7% of 2020 volume)
- Old cases may never be resolved
- Skewing overall statistics

---

## Recommendations

### Immediate Actions (Week 1)
1. **Triage old cases**: Close all cases >2 years old with no activity
2. **Audit 2020 backlog**: Determine which cases are still relevant
3. **Investigate recent decline**: Why is 2026 closure rate so low?

### Short-term Improvements (1-3 months)
1. **Implement auto-closure rules** for certain case types
2. **Prioritize recent cases** over old backlog
3. **Analyze Nov 2020 spikes** to prevent future surges

### Long-term Strategy (6-12 months)
1. **Predictive triage system** to route cases efficiently
2. **Capacity planning** based on seasonal patterns
3. **Performance monitoring** to catch declining trends early

---

## Data Quality Notes

- **Hourly data**: Not available (all timestamps at midnight)
- **2026 data**: Incomplete (only 4 days)
- **Resolution times**: Many cases show 0 days (instant closure)

---

## Files Generated

All outputs saved to: `output/phase1_operational/`

- `summary_statistics.csv` - Detailed metrics
- 7 visualization PNG files
- This summary document

---

*Analysis completed: January 7, 2026*
