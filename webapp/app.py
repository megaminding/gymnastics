import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv("data_2022_2023.csv")  # Ensure this file is in the same directory

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Gymnastics Medal Predictions"),
    
    html.Label("Select a Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in df['Country'].unique()],
        value='USA',  # Default selection
        clearable=False
    ),

    html.Label("Select Plot Type:"),
    dcc.RadioItems(
        id="plot-type",
        options=[
            {"label": "Box Plot", "value": "box"},
            {"label": "Scatter Plot", "value": "scatter"}
        ],
        value="box",  # Default selection
        inline=True
    ),

    dcc.Graph(id='scatter-plot')
])

# Callback for updating the scatterplot
@app.callback(
    dash.Output('scatter-plot', 'figure'),
    [dash.Input('country-dropdown', 'value'),
     dash.Input('plot-type', 'value')]
)
def update_scatterplot(selected_country, plot_type):
    filtered_data = df[df['Country'] == selected_country]

    # Define event order for proper sorting
    apparatus_order = ["VT1", "VT2", "VT", "UB", "BB", "FX", "PH", "SR", "PB", "HB"]
    filtered_data["Apparatus"] = pd.Categorical(filtered_data["Apparatus"], categories=apparatus_order, ordered=True)

    # Generate Box Plot or Scatter Plot based on selection
    if plot_type == "box":
        fig = px.box(
            filtered_data, 
            x="Apparatus",
            y="Score", 
            color="Apparatus",
            title=f"Gymnastics Score Distribution for {selected_country}",
            labels={"Apparatus": "Event", "Score": "Final Score"},
            points="outliers",  # Show only outliers separately
            hover_data=["LastName", "D_Score", "E_Score"]  # Show gymnast name & scores on hover
        )
    else:
        fig = px.scatter(
            filtered_data, 
            x="Apparatus",
            y="Score", 
            color="LastName",
            title=f"Gymnastics Scores for {selected_country}",
            labels={"Apparatus": "Event", "Score": "Final Score"},
            hover_data=["LastName", "D_Score", "E_Score"]
        )

    # Customize layout for clarity
    fig.update_layout(
        xaxis={'tickangle': -45},
        xaxis_title="Gymnastics Event",
        yaxis_title="Final Score",
        margin=dict(l=40, r=40, t=60, b=120),
        showlegend=True,
        legend_title_text="Event"
    )

    # Add a description about the box plot statistics (for Box Plot mode)
    if plot_type == "box":
        fig.add_annotation(
            x=0.5, y=-0.2,
            text="🔹 Box represents the middle 50% of scores (Q1 to Q3).<br>"
                 "🔹 Line inside the box = Median (middle score).<br>"
                 "🔹 Whiskers extend to non-outlier min/max scores.<br>"
                 "🔹 Dots outside whiskers = Outliers (exceptionally high/low scores).",
            showarrow=False,
            xref="paper", yref="paper",
            font=dict(size=14, color="black"),
            align="center",
            bordercolor="black",
            borderwidth=2,
            bgcolor="white",
            opacity=0.95
        )

    return fig

# Ensure the app runs
if __name__ == '__main__':
    app.run_server(debug=True)
