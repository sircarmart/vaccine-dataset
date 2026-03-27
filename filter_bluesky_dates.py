#!/usr/bin/env python
"""
Filter bluesky CSV files to specific date ranges to match reddit data availability.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime

def filter_by_date_range(input_file, start_date, end_date, output_file=None):
    """
    Filter CSV file to include only rows within the specified date range.

    Args:
        input_file: Path to input CSV file
        start_date: Start date string in YYYY-MM-DD format
        end_date: End date string in YYYY-MM-DD format
        output_file: Path to output CSV file (if None, overwrites input file)
    """
    print(f"Reading {input_file}...")

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Parse the created_iso column to extract date
    df['date'] = pd.to_datetime(df['created_iso']).dt.date

    # Convert start and end dates to date objects
    start = pd.to_datetime(start_date).date()
    end = pd.to_datetime(end_date).date()

    # Filter rows within the date range
    mask = (df['date'] >= start) & (df['date'] <= end)
    filtered_df = df[mask]

    # Remove the temporary date column
    filtered_df = filtered_df.drop('date', axis=1)

    # Save the filtered data
    output_path = output_file if output_file else input_file
    filtered_df.to_csv(output_path, index=False)

    print(f"Filtered {len(df)} rows to {len(filtered_df)} rows")
    print(f"Saved to {output_path}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Actual date range in filtered data: {filtered_df['created_iso'].min()} to {filtered_df['created_iso'].max()}")

    return len(filtered_df)

def main():
    base_path = Path("code/EmotionDynamics/code/my_data")

    # Filter texasff bluesky data: 2025-07-01 to 2025-07-17
    texasff_file = base_path / "texasff_bluesky.csv"
    if texasff_file.exists():
        print("\n" + "="*60)
        print("FILTERING TEXASFF BLUESKY DATA")
        print("="*60)
        filter_by_date_range(
            input_file=texasff_file,
            start_date="2025-07-01",
            end_date="2025-07-17"
        )

    # Filter hurricane_milton bluesky data: 2024-10-01 to 2024-10-17
    hurricane_file = base_path / "hurricane_milton_bluesky.csv"
    if hurricane_file.exists():
        print("\n" + "="*60)
        print("FILTERING HURRICANE MILTON BLUESKY DATA")
        print("="*60)
        filter_by_date_range(
            input_file=hurricane_file,
            start_date="2024-10-01",
            end_date="2024-10-17"
        )

if __name__ == "__main__":
    main()