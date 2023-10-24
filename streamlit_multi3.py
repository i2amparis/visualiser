#problem with legends
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components

uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    #Check for csv 
    if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
    #Check for xlsx or xls
    else:
            df = pd.read_excel(uploaded_file)
    #lower case
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    model_values = st.multiselect("Select Models:", df["Model"].unique())
    scenario_values = st.multiselect("Select Scenarios:", df["Scenario"].unique())
    region_values = st.multiselect("Select Regions:", df["Region"].unique())
    variable_value = st.selectbox("Select a Variable:", df["Variable"].unique())

    if model_values and scenario_values and region_values and variable_value:
        filtered_df = df[(df["Model"].isin(model_values)) & 
                        (df["Scenario"].isin(scenario_values))&
                        (df["Region"].isin(region_values))&
                        (df["Variable"]== variable_value)]

        if not filtered_df.empty:
            fig = plt.figure(figsize=(10, 6))

            for model in model_values:
                for scenario in scenario_values:
                    for region in region_values:
                        subset = filtered_df[(filtered_df["Model"] == model) & 
                                            (filtered_df["Scenario"] == scenario) &
                                            (filtered_df["Region"] == region)]
                        
                        if not subset.empty:
                            row_location = subset.index[0]
                            row_values = subset.loc[row_location]
                            values_to_plot = row_values[[col for col in df.columns if str(col).isdigit()]].astype(float)
                            label = f"{model}, {scenario}, {region}"
                            plt.plot(values_to_plot.index, values_to_plot.values, marker='o', linestyle='-', label=label)
                            

            plt.title(f"Line Plot for {variable_value}")
            plt.xlabel("Years")
            plt.ylabel(df.loc[row_location, "Unit"])  
            plt.grid(True)
            plt.legend()
            #st.pyplot(fig)
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=600)
        else:
            st.warning('No data available for the selected choices.')
        st.write(filtered_df)
    else:
        st.warning('Please select at least one option for each category.')
