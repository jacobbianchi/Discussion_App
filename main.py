import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import io
import seaborn as sns

st.write('''# Explore a Dataset!''')
st.sidebar.write('''# Options''')

# Prompt the user to upload a csv file in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload a  CSV file", "csv")
if uploaded_file is not None:

    # Read in the csv file as a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # If the user checks the box, display the DataFrame
    if st.checkbox("Show DataFrame"):
        st.dataframe(df)

    # Determine the numeric/categorical/boolean/date-time columns
    numeric_cols = df.select_dtypes(["float64", "int64"])
    categorical_cols = df.select_dtypes(["object", "category"])
    
    # Display relevant info about the dataset
    st.write(f'''
    It is {df.shape[0]} row{'' if df.shape[0] == 1 else 's'} by {df.shape[1]} column{'' if df.shape[1] == 1 else 's'}:
    + {numeric_cols.shape[1]} numeric variable{'' if numeric_cols.shape[1] == 1 else 's'}
    + {categorical_cols.shape[1]} categorical variable{'' if categorical_cols.shape[1] == 1 else 's'}
    ''')

    # Allow the user to select the type of column
    col_type_selection = st.sidebar.selectbox("Select Data Type", ("Data Type", "Numeric", "Categorical"))

    # Allow the user to select an exact column to analyze
    if col_type_selection == "Numeric":
        col_options = ["Column"]
        col_options.extend(list(numeric_cols.columns))
        col_selection = st.sidebar.selectbox("Select a Column", col_options)
    if col_type_selection == "Categorical":
        col_options = ["Column"]
        col_options.extend(list(categorical_cols.columns))
        col_selection = st.sidebar.selectbox("Select a Column", col_options)

    if col_type_selection != "Data Type" and col_selection != "Column":
        st.write(f'''## Analyzing the *{col_selection}* variable''')

        # What to do if it is a numeric variable
        if col_type_selection == "Numeric":

            # Summary Statistics
            st.write('''### Summary Staticstics:''')
            st.table(df[col_selection].describe())

            # Histogram Display
            st.write('''### Histogram''')
            hist_bins = st.slider("Number of Bins", min_value = 5, max_value = 150, value = 30)
            bin_color_selection = st.color_picker("Bin Color", "#2774AE")

            show_density = st.checkbox("Density Curve")
            if show_density:
                density_color_selection = st.color_picker("Density Curve Color", "#FFD100")

            hist_title = st.text_input("Set Title", "Histogram")
            hist_x_title = st.text_input("Set x-axis Title", col_selection)
            hist_y_title = st.text_input("Set y-axis Title", "Count")

            fig, ax = plt.subplots()
            ax.hist(df[col_selection], bins = hist_bins, edgecolor = "black", color = bin_color_selection)
            ax.set_title(hist_title)
            ax.set_xlabel(hist_x_title)
            ax.set_ylabel(hist_y_title)

            if show_density:
                density = sns.kdeplot(df[col_selection], color = density_color_selection, ax = ax.twinx())
                density.set_yticks([])
                density.set_ylabel('')
                
            st.pyplot(fig)
            
            # Download the histogram
            plot_bytes = io.BytesIO()
            fig.savefig(plot_bytes, format='png', dpi = 300, bbox_inches = "tight")
            plot_bytes.seek(0)
            st.download_button(label='Download Plot', data=plot_bytes, file_name='histogram.png', mime='image/png')
        
        # What to do if it is a categorical variable
        if col_type_selection == "Categorical":

            # Preparing the Data
            props = pd.DataFrame(df[col_selection].value_counts(normalize = True).reset_index())

            # Table of Proprtions
            st.write('''### Table of Proportions:''')
            st.table(props)

            # Bar Plot Display
            st.write('''### Bar Plot''')
            sort_bars = st.radio("Sort:", ("Ascending", "Descending"), index = 0)
            if sort_bars == "Ascending":
                props = props.sort_values(by = "proportion", ascending = True)
            else:
                props = props.sort_values(by = "proportion", ascending = False)
            bar_color_selection = st.color_picker("Color", "#2774AE")
            bar_title = st.text_input("Set Title", "Bar Plot")
            bar_x_title = st.text_input("Set x-axis Title", col_selection)
            bar_y_title = st.text_input("Set y-axis Title", "Proportion")
            fig, ax = plt.subplots()
            ax.bar(props[col_selection], props["proportion"], color = bar_color_selection)
            ax.set_title(bar_title)
            ax.set_xlabel(bar_x_title)
            ax.set_ylabel(bar_y_title)
            ax.set_xticklabels(props[col_selection], rotation = 45)
            st.pyplot(fig)

            # Download the bar plot
            plot_bytes = io.BytesIO()
            fig.savefig(plot_bytes, format='png', dpi = 300, bbox_inches = "tight")
            plot_bytes.seek(0)
            st.download_button(label='Download Plot', data=plot_bytes, file_name='bar_plot.png', mime='image/png')