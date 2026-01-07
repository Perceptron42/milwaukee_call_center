"""
This module cleans the call center datasets by processing text and date columns.
It normalizes text by removing non-ASCII characters and standardization,
and converts date strings into proper datetime objects.
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path


def clean_text(text):
    """
    Clean text by removing/replacing problematic characters.
    
    Args:
        text: Input text string
        
    Returns:
        Cleaned text string
    """
    if pd.isna(text) or text == '':
        return text
    
    # Convert to string
    text = str(text)
    
    # Replace non-ASCII quotes with standard quotes
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('"', '"')
    text = text.replace('"', '"')
    
    # Replace em-dash and en-dash with regular dash
    text = text.replace('—', '-')
    text = text.replace('–', '-')
    
    # Replace special bullet points
    text = text.replace('•', '-')
    text = text.replace('·', '-')
    
    # Remove emojis and other problematic Unicode characters
    # Keep only printable ASCII and common punctuation
    text = re.sub(r'[^\x20-\x7E\n\r\t]', '', text)
    
    # Normalize whitespace - replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace newlines and carriage returns with spaces to prevent CSV issues
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    
    # Replace tabs with spaces
    text = text.replace('\t', ' ')
    
    # Clean up multiple spaces again after newline replacement
    text = re.sub(r' +', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def convert_to_datetime(date_str):
    """
    Convert date string to datetime object.
    
    Args:
        date_str: Date string to convert
        
    Returns:
        Datetime object or NaT if conversion fails
    """
    if pd.isna(date_str) or date_str == '':
        return pd.NaT
    
    try:
        return pd.to_datetime(date_str)
    except Exception as e:
        print(f"Warning: Could not parse date '{date_str}': {e}")
        return pd.NaT


def clean_csv_file(input_filepath, output_filepath):
    """
    Clean a CSV file by removing problematic characters and converting dates.
    
    Args:
        input_filepath: Path to input CSV file
        output_filepath: Path to save cleaned CSV file
    """
    print(f"\n{'='*80}")
    print(f"CLEANING: {input_filepath}")
    print(f"{'='*80}\n")
    
    # Load the data
    print("Loading data...")
    df = pd.read_csv(input_filepath, dtype=str)
    
    print(f"Loaded {len(df):,} rows")
    
    # Text columns to clean
    text_columns = ['OBJECTDESC', 'TITLE', 'CASECLOSUREREASONDESCRIPTION']
    
    # Clean text columns
    print("\nCleaning text columns...")
    for col in text_columns:
        if col in df.columns:
            print(f"  - Cleaning {col}...")
            df[col] = df[col].apply(clean_text)
    
    # Date columns to convert
    date_columns = ['CREATIONDATE', 'CLOSEDDATETIME']
    
    # Convert date columns
    print("\nConverting date columns to datetime...")
    for col in date_columns:
        if col in df.columns:
            print(f"  - Converting {col}...")
            df[col] = df[col].apply(convert_to_datetime)
    
    # Save cleaned data
    print(f"\nSaving cleaned data to {output_filepath}...")
    df.to_csv(output_filepath, index=False)
    
    print(f"✓ Successfully saved {len(df):,} rows to {output_filepath}")
    
    # Show summary statistics
    print("\n" + "="*80)
    print("CLEANING SUMMARY")
    print("="*80)
    
    # Count non-null values in date columns
    for col in date_columns:
        if col in df.columns:
            non_null = df[col].notna().sum()
            print(f"{col}: {non_null:,} valid dates ({non_null/len(df)*100:.2f}%)")
    
    # Count non-null values in text columns
    for col in text_columns:
        if col in df.columns:
            non_null = df[col].notna().sum()
            non_empty = (df[col].notna() & (df[col] != '')).sum()
            print(f"{col}: {non_empty:,} non-empty values ({non_empty/len(df)*100:.2f}%)")
    
    print()


def main():
    """Main function to clean both CSV files."""
    print("\n" + "="*80)
    print("CALL CENTER DATA CLEANING")
    print("="*80)
    
    # Create output directory if it doesn't exist
    output_dir = Path('cleaned_data')
    output_dir.mkdir(exist_ok=True)
    
    # Clean current data
    clean_csv_file(
        'original_data/callcenterdatacurrent.csv',
        output_dir / 'callcenterdatacurrent_cleaned.csv'
    )
    
    # Clean historical data
    clean_csv_file(
        'original_data/callcenterdatahistorical.csv',
        output_dir / 'callcenterdatahistorical_cleaned.csv'
    )
    
    print("\n" + "="*80)
    print("CLEANING COMPLETE")
    print(f"Cleaned files saved to: {output_dir.absolute()}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
