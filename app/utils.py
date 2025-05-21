import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

def load_dummy_data():
    """Generate dummy data for testing purposes"""

    num_records = 120  # 10 years of monthly data
    data = {
        "timestamp": pd.date_range("2010-01-01", periods=num_records, freq="ME"),
        "GHI": np.random.uniform(4, 7, num_records),
        "DNI": np.random.uniform(5, 8, num_records),
        "DHI": np.random.uniform(2, 4, num_records),
        "ModA": np.random.uniform(10, 40, num_records),
        "ModB": np.random.uniform(10, 40, num_records),
        "Tamb": np.random.uniform(20, 35, num_records),
        "RH": np.random.uniform(30, 90, num_records),
        "WS": np.random.uniform(0, 10, num_records),
        "WSgust": np.random.uniform(0, 15, num_records),
        "WSstdev": np.random.uniform(0, 2, num_records),
        "WD": np.random.uniform(0, 360, num_records),
        "WDstdev": np.random.uniform(0, 60, num_records),
        "BP": np.random.uniform(950, 1050, num_records),
        "Cleaning": np.random.uniform(0, 1, num_records),
        "Precipitation": np.random.uniform(0, 100, num_records),
        "TModA": np.random.uniform(20, 60, num_records),
        "TModB": np.random.uniform(20, 60, num_records),
        'country': 'SampleCountry',
        'region': 'SampleRegion'
    }
    df = pd.DataFrame(data)
    df.columns = [col.lower() for col in df.columns]  # lowercase all columns
    return df

def validate_uploaded_data(df):
    """Ensure uploaded data has required columns and valid timestamps"""
    required_columns = {'timestamp', 'country', 'region'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Convert and validate dates
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    # Keep within pandas datetime bounds
    min_date = pd.Timestamp.min + pd.Timedelta(days=1)
    max_date = pd.Timestamp.max - pd.Timedelta(days=1)
    df = df[(df['timestamp'] >= min_date) & (df['timestamp'] <= max_date)]

    return df


def filter_data(df, filters):
    min_year, max_year = filters["years"]
    filtered_df = df[
        (df["timestamp"].dt.year >= min_year) &
        (df["timestamp"].dt.year <= max_year)
    ].copy()

    # Filter by country if not "All"
    if "country" in filters and filters["country"].lower() != "all":
        filtered_df = filtered_df[filtered_df["country"] == filters["country"]]

    return filtered_df

def plot_ghi_distribution(df, metrics):
    """
    Create a single box plot combining multiple metrics, grouped by country or region.
    """
    if not metrics:
        return None

    group_col = "country" if df['country'].nunique() > 1 else "region"

    # Melt the dataframe so metrics appear in one column for box plot
    df_melted = df[[group_col] + metrics].melt(id_vars=group_col, 
                                                value_vars=metrics,
                                                var_name="Metric", 
                                                value_name="Value")

    fig = px.box(
        df_melted,
        x=group_col,
        y="Value",
        color="Metric",
        title=f"Distribution of Selected Metrics by {group_col.capitalize()}",
        labels={"Value": "Irradiance / Energy (kWh/m²/day)"},
        height=550
    )

    fig.update_layout(boxmode="group")
    return fig


def get_top_regions(df, metrics, n=10):
    """
    Return top performing regions/countries by selected metrics.
    """
    group_col = "country" if df['country'].nunique() > 1 else "region"
    
    summary = (
        df.groupby(group_col)[metrics]
        .mean()
        .sort_values(by=metrics[0], ascending=False)  # sort by the first metric
        .head(n)
        .reset_index()
    )

    # Rename columns for clarity
    summary.columns = [group_col] + [f"Avg. {metric}" for metric in metrics]
    return summary
