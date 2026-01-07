# Call Center Data Exploration & Cleaning

## Overview
This walkthrough documents the exploration and cleaning of two call center CSV files: `callcenterdatacurrent.csv` and `callcenterdatahistorical.csv`.

---

## 1. Data Exploration

### Files Created
- [main.py](file:///c:/Users/Desk/PycharmProjects/gladly_data_project/main.py) - Comprehensive data exploration script

### Key Findings

#### Current Data (`callcenterdatacurrent.csv`)
- **Rows**: 93
- **Date Range**: January 1-4, 2026 (4 days)
- **Null Values**:
  - `CLOSEDDATETIME`: 77.42% (most cases still open)
  - `CASECLOSUREREASONDESCRIPTION`: 33.33%
- **Data Quality Issues**:
  - Non-ASCII character: curly apostrophe (`'`)
  - 248 commas in addresses

#### Historical Data (`callcenterdatahistorical.csv`)
- **Rows**: 175,840
- **Date Range**: March 21, 2020 - December 31, 2025 (~5.8 years)
- **Null Values**:
  - `CLOSEDDATETIME`: 58.12%
  - `OBJECTDESC`: 27.95%
  - `CASECLOSUREREASONDESCRIPTION`: 30.14%
- **Data Quality Issues**:
  - **42 unique non-ASCII characters** including:
    - Emojis: 🏻, 👮
    - Special quotes: ", ", ', '
    - Accented letters: é, œ
  - **5,152 newlines** in text fields
  - **1,573 carriage returns**
  - **88 tabs**
  - **44,310 commas** in descriptions

---

## 2. Data Cleaning

### Files Created
- [clean.py](file:///c:/Users/Desk/PycharmProjects/gladly_data_project/clean.py) - Data cleaning script

### Cleaning Operations

#### Text Column Cleaning (`OBJECTDESC`, `TITLE`, `CASECLOSUREREASONDESCRIPTION`)
1. **Character Normalization**:
   - Replaced curly quotes (`'`, `'`, `"`, `"`) with standard ASCII quotes
   - Replaced em-dash (`—`) and en-dash (`–`) with hyphens
   - Replaced bullet points (`•`, `·`) with hyphens
   - Removed all emojis and non-ASCII characters

2. **Whitespace Normalization**:
   - Replaced newlines (`\n`, `\r\n`, `\r`) with spaces
   - Replaced tabs with spaces
   - Collapsed multiple spaces into single spaces
   - Trimmed leading/trailing whitespace

#### Date Column Conversion (`CREATIONDATE`, `CLOSEDDATETIME`)
- Converted all date strings to Python `datetime` objects
- Invalid dates converted to `NaT` (Not a Time)

### Results

#### Current Data (Cleaned)
- **File**: `cleaned_data/callcenterdatacurrent_cleaned.csv`
- **Size**: 12.6 KB
- **Valid Dates**:
  - `CREATIONDATE`: 93/93 (100%)
  - `CLOSEDDATETIME`: 21/93 (22.58%)
- **Non-empty Text**:
  - `OBJECTDESC`: 93/93 (100%)
  - `TITLE`: 93/93 (100%)
  - `CASECLOSUREREASONDESCRIPTION`: 62/93 (66.67%)

#### Historical Data (Cleaned)
- **File**: `cleaned_data/callcenterdatahistorical_cleaned.csv`
- **Size**: 25 MB
- **Valid Dates**:
  - `CREATIONDATE`: 175,840/175,840 (100%)
  - `CLOSEDDATETIME`: 73,647/175,840 (41.88%)
- **Non-empty Text**:
  - `OBJECTDESC`: 126,684/175,840 (72.05%)
  - `TITLE`: 175,840/175,840 (100%)
  - `CASECLOSUREREASONDESCRIPTION`: 122,841/175,840 (69.86%)

---

## 3. Next Steps

The cleaned data is now ready for analysis with:
- ✅ All problematic characters removed
- ✅ Dates in proper Python datetime format
- ✅ Normalized whitespace
- ✅ CSV-safe text fields (no embedded newlines)

### Recommended Usage
```python
import pandas as pd

# Load cleaned data
df_current = pd.read_csv('cleaned_data/callcenterdatacurrent_cleaned.csv', 
                         parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])

df_historical = pd.read_csv('cleaned_data/callcenterdatahistorical_cleaned.csv',
                            parse_dates=['CREATIONDATE', 'CLOSEDDATETIME'])
```

---

## Summary

✅ **Exploration Complete**: Identified null values, date ranges, and 42 types of problematic characters  
✅ **Cleaning Complete**: Processed 175,933 total rows across both files  
✅ **Output**: Clean, analysis-ready CSV files in `cleaned_data/` directory
