"""
This module performs an initial exploration of the call center datasets.
It checks for data quality issues such as missing values, empty strings,
date range validity, and special character occurrences in text fields.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re


def explore_csv_file(filepath: str, filename: str):
    """
    Explore a CSV file for data quality issues.
    
    Args:
        filepath: Path to the CSV file
        filename: Name of the file for display purposes
    """
    print(f"\n{'='*80}")
    print(f"EXPLORING: {filename}")
    print(f"{'='*80}\n")
    
    # Load the data
    df = pd.read_csv(filepath, dtype=str)  # Load as strings to preserve all data
    
    # Basic Info
    print(f"📊 BASIC INFORMATION")
    print(f"-" * 80)
    print(f"Total Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"File Size: {filepath}")
    print(f"\nColumns: {list(df.columns)}")
    
    # Check for null/missing values
    print(f"\n🔍 NULL/MISSING VALUE ANALYSIS")
    print(f"-" * 80)
    null_counts = df.isnull().sum()
    null_percentages = (df.isnull().sum() / len(df) * 100).round(2)
    
    null_summary = pd.DataFrame({
        'Column': null_counts.index,
        'Null Count': null_counts.values,
        'Null %': null_percentages.values
    })
    print(null_summary.to_string(index=False))
    
    # Check for empty strings (different from null)
    print(f"\n📝 EMPTY STRING ANALYSIS")
    print(f"-" * 80)
    empty_counts = (df == '').sum()
    empty_percentages = ((df == '').sum() / len(df) * 100).round(2)
    
    empty_summary = pd.DataFrame({
        'Column': empty_counts.index,
        'Empty Count': empty_counts.values,
        'Empty %': empty_percentages.values
    })
    print(empty_summary.to_string(index=False))
    
    # Date column analysis
    date_columns = ['CREATIONDATE', 'CLOSEDDATETIME']
    print(f"\n📅 DATE RANGE ANALYSIS")
    print(f"-" * 80)
    
    for col in date_columns:
        if col in df.columns:
            print(f"\n{col}:")
            non_null_dates = df[col].dropna()
            non_empty_dates = non_null_dates[non_null_dates != '']
            
            if len(non_empty_dates) > 0:
                print(f"  Sample values (first 5):")
                for val in non_empty_dates.head(5):
                    print(f"    - {val}")
                
                # Try to parse dates to find min/max
                try:
                    # Try common date formats
                    parsed_dates = pd.to_datetime(non_empty_dates, errors='coerce')
                    valid_dates = parsed_dates.dropna()
                    
                    if len(valid_dates) > 0:
                        print(f"  Earliest Date: {valid_dates.min()}")
                        print(f"  Latest Date: {valid_dates.max()}")
                        print(f"  Date Range: {(valid_dates.max() - valid_dates.min()).days} days")
                        
                        # Check for unparseable dates
                        unparseable = len(non_empty_dates) - len(valid_dates)
                        if unparseable > 0:
                            print(f"  ⚠️  Unparseable dates: {unparseable} ({unparseable/len(non_empty_dates)*100:.2f}%)")
                    else:
                        print(f"  ⚠️  No dates could be parsed")
                except Exception as e:
                    print(f"  ⚠️  Error parsing dates: {e}")
            else:
                print(f"  No non-null, non-empty values found")
    
    # Special character analysis
    print(f"\n🔤 SPECIAL CHARACTER ANALYSIS")
    print(f"-" * 80)
    
    text_columns = ['OBJECTDESC', 'TITLE', 'CASECLOSUREREASONDESCRIPTION']
    
    for col in text_columns:
        if col in df.columns:
            print(f"\n{col}:")
            non_null_text = df[col].dropna()
            non_empty_text = non_null_text[non_null_text != '']
            
            if len(non_empty_text) > 0:
                # Combine all text
                all_text = ' '.join(non_empty_text.astype(str))
                
                # Find special characters (non-ASCII)
                special_chars = set(re.findall(r'[^\x00-\x7F]', all_text))
                
                if special_chars:
                    print(f"  ⚠️  Non-ASCII characters found: {len(special_chars)} unique")
                    print(f"  Examples: {list(special_chars)[:20]}")
                else:
                    print(f"  ✓ No non-ASCII characters found")
                
                # Check for common problematic characters
                problematic = {
                    'Newlines': all_text.count('\n'),
                    'Tabs': all_text.count('\t'),
                    'Carriage Returns': all_text.count('\r'),
                    'Quotes (")': all_text.count('"'),
                    'Single Quotes (\')': all_text.count("'"),
                    'Commas': all_text.count(','),
                }
                
                print(f"  Potentially problematic characters:")
                for char_type, count in problematic.items():
                    if count > 0:
                        print(f"    - {char_type}: {count:,}")
                
                # Show sample values
                print(f"  Sample values (first 3):")
                for val in non_empty_text.head(3):
                    preview = str(val)[:100] + ('...' if len(str(val)) > 100 else '')
                    print(f"    - {preview}")
    
    # Value distribution for categorical columns
    print(f"\n📈 VALUE DISTRIBUTION")
    print(f"-" * 80)
    
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"\n{col}:")
        print(f"  Unique values: {unique_count:,}")
        
        if unique_count <= 20:  # Show distribution for low-cardinality columns
            value_counts = df[col].value_counts(dropna=False).head(10)
            print(f"  Top values:")
            for val, count in value_counts.items():
                val_display = str(val)[:50] + ('...' if len(str(val)) > 50 else '')
                print(f"    - {val_display}: {count:,} ({count/len(df)*100:.2f}%)")
    
    # Data quality summary
    print(f"\n⚠️  DATA QUALITY SUMMARY")
    print(f"-" * 80)
    total_nulls = df.isnull().sum().sum()
    total_empties = (df == '').sum().sum()
    total_cells = len(df) * len(df.columns)
    
    print(f"Total cells: {total_cells:,}")
    print(f"Null cells: {total_nulls:,} ({total_nulls/total_cells*100:.2f}%)")
    print(f"Empty string cells: {total_empties:,} ({total_empties/total_cells*100:.2f}%)")
    print(f"Missing (null or empty): {total_nulls + total_empties:,} ({(total_nulls + total_empties)/total_cells*100:.2f}%)")


def main():
    """Main function to explore both CSV files."""
    print("\n" + "="*80)
    print("CALL CENTER DATA EXPLORATION")
    print("="*80)
    
    # Explore current data
    explore_csv_file('original_data/callcenterdatacurrent.csv', 'Current Data')
    
    # Explore historical data
    explore_csv_file('original_data/callcenterdatahistorical.csv', 'Historical Data')
    
    print("\n" + "="*80)
    print("EXPLORATION COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
