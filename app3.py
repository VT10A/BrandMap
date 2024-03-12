import pandas as pd
import plotly.graph_objects as go
import numpy as np
from APIcall import get_chat_completions
import streamlit as st

# Read data from CSV
df1 = pd.read_csv("coordinatesPD.csv")
df2 = pd.read_csv("coordinatesPD2.csv")



@st.cache_data()
def get_summary(prompt):
    summary = get_chat_completions(prompt)
    return summary


@st.cache_data()
def get_summary2(prompt):
    summary = get_chat_completions(prompt)
    return summary


# App #######################################################################


st.image('Image.jpg', use_column_width=False, width=200)

st.title('Correspondence Maps')

# Dropdown menu to select dataframe
selected_df = st.selectbox("Select crosstab", ("df1: Age and Political Party", "df2: Perceptions and Brexit"))

if selected_df == "df1: Age and Political Party":
    title = 'Age and Political Party'
    df = df1

    # Define function to create scatter plot
    def create_scatter_plot(df, title):
        # Extract data
        x = df['Dim 1']
        y = df['Dim 2']
        labels = df.iloc[:, 0]  # Extract labels from the first unnamed column

        # Add jitter to x-coordinates for age categories
        jitter_amount = 0.02
        age_indices = [0, 1, 2, 3, 4, 5]  # Assuming age categories are the first 6 rows
        x[age_indices] = x[age_indices] + np.random.uniform(-jitter_amount, jitter_amount, len(age_indices))

        # Create scatter plot
        fig = go.Figure()

        # Add markers for all categories
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', text=labels,
                                marker=dict(color=['red' if i in age_indices else 'blue' for i in range(len(x))], size=10)))

        # Add annotations for all categories except "Aged_"
        for i, txt in enumerate(labels):
            if i not in age_indices:
                y_coord = y[i] - 0.03 - (i % 5) * 0.01  # Adjust y-coordinate to space out the labels
                fig.add_annotation(x=x[i], y=y_coord, text=txt,
                                showarrow=False, font=dict(color='blue', size=10))

        # Add annotations for "Aged_" values with leader lines
        aged_labels = [labels[i] for i in age_indices]
        for i, txt in enumerate(aged_labels):
            fig.add_annotation(x=x[age_indices[i]], y=y[age_indices[i]]+0.03, text=txt,
                            showarrow=True, arrowhead=1, ax=0, ay=-20, arrowwidth=1, arrowcolor='red', font=dict(color='red', size=10))

        # Add vertical line through the X axis
        fig.add_shape(type="line", x0=0, y0=-0.4, x1=0, y1=0.75,
                    line=dict(color="lightgrey", width=1))

        # Add horizontal line through the Y axis
        fig.add_shape(type="line", x0=-1, y0=0, x1=1, y1=0,
                    line=dict(color="lightgrey", width=1))

        # Calculate dynamic axis range
        x_range = [x.min() - 0.1, x.max() + 0.1]
        y_range = [y.min() - 0.1, y.max() + 0.1]

        # Update layout with dynamic axis range
        fig.update_layout(title=title,
                        xaxis_title='Dimension 1',
                        yaxis_title='Dimension 2',
                        xaxis=dict(showline=True, linecolor='lightgrey', zeroline=False, range=x_range),
                        yaxis=dict(showline=True, linecolor='lightgrey', zeroline=False, range=y_range),
                        plot_bgcolor='white',  # Set background color to white
                        height=700)  # Adjust height here
        return fig



elif selected_df == "df2: Perceptions and Brexit":
    title = 'Perceptions and Brexit'
    df = df2

    # Define function to create scatter plot
    def create_scatter_plot(df, title):
        # Extract data
        x = df['Dim 1']
        y = df['Dim 2']
        labels = df.iloc[:, 0]  # Extract labels from the first unnamed column

        # Add jitter to x-coordinates for age categories
        jitter_amount = 0.02
        age_indices = [0, 1, 2]  # Assuming  categories are the first 3 rows
        x[age_indices] = x[age_indices] + np.random.uniform(-jitter_amount, jitter_amount, len(age_indices))

        # Create scatter plot
        fig = go.Figure()

        # Add markers for all categories
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', text=labels,
                                marker=dict(color=['red' if i in age_indices else 'blue' for i in range(len(x))], size=10)))

        # Add annotations for all categories except "Voted_"
        for i, txt in enumerate(labels):
            if i not in age_indices:
                y_coord = y[i] - 0.03 - (i % 5) * 0.01  # Adjust y-coordinate to space out the labels
                fig.add_annotation(x=x[i], y=y_coord, text=txt,
                                showarrow=False, font=dict(color='blue', size=10))

        # Add annotations for "Aged_" values with leader lines
        aged_labels = [labels[i] for i in age_indices]
        for i, txt in enumerate(aged_labels):
            fig.add_annotation(x=x[age_indices[i]], y=y[age_indices[i]]+0.03, text=txt,
                            showarrow=True, arrowhead=1, ax=0, ay=-20, arrowwidth=1, arrowcolor='red', font=dict(color='red', size=10))

        # Add vertical line through the X axis
        fig.add_shape(type="line", x0=0, y0=-0.4, x1=0, y1=0.75,
                    line=dict(color="lightgrey", width=1))

        # Add horizontal line through the Y axis
        fig.add_shape(type="line", x0=-1, y0=0, x1=1, y1=0,
                    line=dict(color="lightgrey", width=1))

        # Calculate dynamic axis range
        x_range = [x.min() - 0.1, x.max() + 0.1]
        y_range = [y.min() - 0.1, y.max() + 0.1]

        # Update layout with dynamic axis range
        fig.update_layout(title=title,
                        xaxis_title='Dimension 1',
                        yaxis_title='Dimension 2',
                        xaxis=dict(showline=True, linecolor='lightgrey', zeroline=False, range=x_range),
                        yaxis=dict(showline=True, linecolor='lightgrey', zeroline=False, range=y_range),
                        plot_bgcolor='white',  # Set background color to white
                        height=700)  # Adjust height here
        return fig

# Create and display scatter plot
fig = create_scatter_plot(df, title)
st.plotly_chart(fig)

# Get bullet points
#bullets = get_chat_completions(f"From this correspondence analysis data {selected_df}, summarize the key results of political lean by age (say 16 to 24 and not X16to24 etc). Bullet point the results and don't comment on the Dim values, just the main takeouts. Just say 16 to 24 not X16 etc.")


if selected_df == "df1: Age and Political Party":
    bullets = get_summary(f"From this correspondence analysis data {df1}, summarize the key results of political lean by age (say 16 to 24 and not X16to24 etc). Bullet point the results and don't comment on the Dim values, just the main takeouts.")    
elif selected_df == "df2: Perceptions and Brexit":
    bullets = get_summary2(f"From this correspondence analysis data {df2}, summarize the key results of perception of issues by brexit vote Bullet point the results and don't comment on the Dim values, just the main takeouts - i.e. what perceptions the brexit voters are most associated with. ")    



st.write(bullets)

