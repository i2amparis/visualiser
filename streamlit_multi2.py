import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    # Check for csv or Excel file format
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    # Convert strings to lowercase
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    model_values = st.multiselect("Select Models:", df["Model"].unique())
    scenario_values = st.multiselect("Select Scenarios:", df["Scenario"].unique())
    region_values = st.multiselect("Select Regions:", df["Region"].unique())
    variable_value = st.selectbox("Select a Variable:", df["Variable"].unique())

    if model_values and scenario_values and region_values and variable_value:
        filtered_df = df[(df["Model"].isin(model_values)) & 
                        (df["Scenario"].isin(scenario_values)) &
                        (df["Region"].isin(region_values)) &
                        (df["Variable"] == variable_value)]

        if not filtered_df.empty:
            values_to_plot = filtered_df[[col for col in df.columns if str(col).isdigit()]].astype(float)
            values_to_plot = values_to_plot.T
            
            st.line_chart(values_to_plot)
        

        else:
            st.warning('No data available for the selected choices.')
        st.write(filtered_df)
        
    else:
        st.warning('Please select at least one option for each category.')
