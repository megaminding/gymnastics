import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv("data_2022_2023.csv")
df['Country'] = df['Country'].str.strip().str.upper()  # Normalize country names

def scatterplot_by_country(country):
    """
    Generates a scatter plot of gymnastics scores for a given country.
    """
    filtered_data = df[df['Country'] == country]

    # 🔹 Print debug info
    print(f"Selected Country: {country}")
    print(f"Filtered Data: {filtered_data.shape[0]} rows")  # Show number of rows

    if filtered_data.empty:
        print("⚠ No data found for the selected country!")

    fig = px.scatter(
        filtered_data,
        x="LastName",
        y="Score",
        color="Apparatus",
        title=f"Gymnastics Scores for {country}",
        labels={"LastName": "Gymnast", "Score": "Final Score"},
    )

    # 🔹 Rotate x-axis labels for better readability
    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title="Gymnast",
        yaxis_title="Final Score",
        margin=dict(l=40, r=40, t=40, b=100)
    )

    # 🔹 Make points larger for visibility
    fig.update_traces(marker=dict(size=8))

    return fig
