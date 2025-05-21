import streamlit as st
import pandas as pd
from utils import (load_dummy_data, 
                   filter_data, 
                   plot_ghi_distribution,
                   get_top_regions)

# App configuration
st.set_page_config(
    page_title="🌞 Solar Insights Dashboard",
    page_icon="🌞",
    layout="wide"
)

# File upload function
def handle_file_upload():
    st.sidebar.header("Data Options")
    use_sample_data = st.sidebar.checkbox("Use sample data", value=True)
    
    if not use_sample_data:
        uploaded_file = st.sidebar.file_uploader(
            "Upload your CSV file",
            type=["csv"],
            help="Upload your solar data CSV file"
        )
        return uploaded_file
    return None

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df.columns = [col.lower() for col in df.columns]  # Normalize

            if 'timestamp' not in df.columns:
                raise ValueError("Missing required 'timestamp' column.")

            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

            # Add missing columns
            if 'country' not in df.columns:
                df['country'] = uploaded_file.name.split('.')[0].replace('_', ' ').title()

            if 'region' not in df.columns:
                df['region'] = "Default Region"

            return df

        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            return load_dummy_data()
    else:
        return load_dummy_data()

def sidebar_controls(df):
    st.sidebar.header("Dashboard Controls")

    # Dynamic country selection
    countries = df['country'].unique() if 'country' in df.columns else ["SampleCountry"]

    show_all_option = len(countries) > 1
    country_options = ["All"] + list(countries) if show_all_option else list(countries)
    selected_country = st.sidebar.selectbox("Select Country", country_options)

    # Year range selection
    if 'timestamp' in df.columns:
        years = pd.to_datetime(df['timestamp']).dt.year
        min_year, max_year = int(years.min()), int(years.max())
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    else:
        year_range = (2015, 2020)

    # Metric multiselect
    metric_labels = {
        'ghi': 'GHI (kWh/m²/day)',
        'dni': 'DNI (kWh/m²/day)',
        'dhi': 'DHI (kWh/m²/day)'
    }

    available_metrics = [k for k in metric_labels if k in df.columns]

    selected_metrics = st.sidebar.multiselect(
        "Performance Metric(s)",
        options=available_metrics,
        default=available_metrics[:1],
        format_func=lambda k: metric_labels[k]
    )

    return {
        "country": selected_country,
        "years": year_range,
        "metrics": selected_metrics
    }

def main_content(df, filters):
    st.title("🌍 Solar Energy Potential Analysis")
    st.markdown("Explore solar irradiation data across different countries or regions")
    
    # Show either number of countries or regions
    col1, col2, col3 = st.columns(3)
    with col1:
        if df['country'].nunique() > 1:
            st.metric("Countries Analyzed", df['country'].nunique())
        else:
            st.metric("Regions Analyzed", df['region'].nunique())
    with col2:
        if 'ghi' in df.columns:
            avg_ghi = f"{df['ghi'].mean():.1f} kWh/m²/day"
        else:
            avg_ghi = "N/A"
        st.metric("Average GHI", avg_ghi)
    with col3:
        st.metric("Data Points", len(df))
    
    tab1, tab2 ,tab3= st.tabs(["Distribution Analysis", "Top Performers", "Statistical Summary"])
    
    with tab1:
        st.header(f"Distribution in {filters['country']}")
        if not filters['metrics']:
            st.warning("Please select at least one metric.")
        else:
            fig = plot_ghi_distribution(df, filters['metrics'])
            st.plotly_chart(fig, use_container_width=True)
 
    with tab2:
        st.header(f"Top Performing {'Countries' if df['country'].nunique() > 1 else 'Regions'}")
        top_n = st.number_input("Number of entries to show", 5, 20, 10)

        if not filters["metrics"]:
            st.warning("Please select at least one metric to display top performers.")
        else:
            top_regions = get_top_regions(df, filters['metrics'], top_n)
            st.dataframe(top_regions, use_container_width=True)

    with tab3:
        st.header("Statistical Summary")

        group_col = "country" if df['country'].nunique() > 1 else "region" if "region" in df.columns else "country"

        # Initialize empty dataframe for summary
        summary = pd.DataFrame()

        for metric in filters["metrics"]:
            agg_df = (
                df.groupby(group_col)[metric]
                .agg(["mean", "median", "std", "min", "max", "count"])
                .rename(columns={
                    "mean": f"{metric} Mean",
                    "median": f"{metric} Median",
                    "std": f"{metric} Std Dev",
                    "min": f"{metric} Min",
                    "max": f"{metric} Max",
                    "count": f"{metric} Count"
                })
                .reset_index()
            )
            if summary.empty:
                summary = agg_df
            else:
                summary = summary.merge(agg_df, on=group_col, how='outer')

        st.dataframe(summary, use_container_width=True)


# App execution 
def main():
    uploaded_file = handle_file_upload()
    df = load_data(uploaded_file)
    
    if uploaded_file is None:
        st.sidebar.info("Using sample solar data")
    
    filters = sidebar_controls(df)
    filtered_df = filter_data(df, filters)
    main_content(filtered_df,filters)

if __name__ == "__main__":
    main()