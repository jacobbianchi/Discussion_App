import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

st.write('''# Explore a Dataset!''')
st.sidebar.write('''# Options''')

# Prompt the user to upload a csv file in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload a  CSV file", "csv")
if uploaded_file is not None:

    # Read in the csv file as a pandas DataFrame
    df = pd.read_csv(uploaded_file)

    # If the user checks the box, display the DataFrame
    show_df = st.checkbox("Show DataFrame")
    if show_df:
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

            st.write('''### Five Number Summary:''')

            st.write('''### Histogram''')
            color_selection = st.color_picker("Color", "#2774AE")
            hist_bins = st.slider("Number of Bins", min_value = 5, max_value = 150, value = 30)
            hist_title = st.text_input("Set Title", "Histogram")
            hist_x_title = st.text_input("Set x-axis Title", col_selection)
            hist_y_title = st.text_input("Set y-axis Title", "Count")
            fig, ax = plt.subplots()
            ax.hist(df[col_selection], bins = hist_bins, edgecolor = "black", color = color_selection)
            ax.set_title(hist_title)
            ax.set_xlabel(hist_x_title)
            ax.set_ylabel(hist_y_title)
            st.pyplot(fig)
            
            # Download the histogram
            