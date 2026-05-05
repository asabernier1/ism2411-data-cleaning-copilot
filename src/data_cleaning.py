"""
Data Cleaning Pipeline

This script cleans a messy sales dataset by:
- Standardizing column names
- Removing extra whitespace
- Handling missing values
- Removing invalid negative values
"""

import pandas as pd


# Copilot-assisted function:
# Load the raw CSV file into a pandas DataFrame.
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


# Copilot-assisted function:
# Standardize column names so they are easier to work with.
def clean_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


# Remove extra whitespace from text columns.
# This prevents inconsistent product/category names.
def clean_text_fields(df):
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].str.strip()
    return df



# Handle missing prices and quantities.
# Missing numeric values can break analysis later.
def handle_missing_values(df):

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")

    df = df.dropna(subset=["price", "qty"])

    return df


# Remove invalid negative values.
# Negative prices or quantities are considered data entry errors.
def remove_invalid_rows(df):

    df = df[(df["price"] >= 0) & (df["qty"] >= 0)]

    return df


if __name__ == "__main__":

    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    # Load raw dataset
    df_raw = load_data(raw_path)

    # Clean column names
    df_clean = clean_column_names(df_raw)

    # Clean whitespace
    df_clean = clean_text_fields(df_clean)

    # Handle missing values
    df_clean = handle_missing_values(df_clean)

    # Remove invalid rows
    df_clean = remove_invalid_rows(df_clean)

    # Save cleaned data
    df_clean.to_csv(cleaned_path, index=False)

    print("Cleaning complete.")
    print(df_clean.head())
    