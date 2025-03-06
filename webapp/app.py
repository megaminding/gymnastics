import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Import the function from visualizations.py
from visualizations import scatterplot_by_country

# Load dataset to get the list of unique countries
df = pd.read_csv("data_2022_2023.csv")
df['Country'] = df['Country'].str.strip().str.upper()  # Normalize country names

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Gymnastics Score Analysis"),
    
    html.Label("Select a Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value='USA',  # Default selection
        clearable=False
    ),

    html.Label("Select Plot Type:"),
    dcc.RadioItems(
        id="plot-type",
        options=[
            {"label": "Scatter Plot", "value": "scatter"},
            {"label": "Box Plot", "value": "box"}
        ],
        value="scatter",  # Default selection
        inline=True
    ),

    dcc.Graph(id='country-plot'),  # This graph updates based on the dropdown & toggle
    dcc.Graph(id='medals-plot')  # This graph updates based on the dropdown & toggle
])

# Callback to update the plot based on user selection
@app.callback(
    dash.Output('country-plot', 'figure'),
    [dash.Input('country-dropdown', 'value'),
     dash.Input('plot-type', 'value')]
)
def update_plot(selected_country, plot_type):
    filtered_data = df[df['Country'] == selected_country]

    if filtered_data.empty:
        # Return an empty graph if no data is available for the selected country
        return px.scatter(title=f"No Data Available for {selected_country}")

    if plot_type == "scatter":
        return scatterplot_by_country(selected_country)  # Calls scatter function
    else:
        # Restore the original Box Plot
        fig = px.box(
            filtered_data, 
            x="Apparatus",
            y="Score", 
            color="Apparatus",
            title=f"Gymnastics Score Distribution for {selected_country}",
            labels={"Apparatus": "Event", "Score": "Final Score"},
            points="all"  # Show all points (outliers included)
        )

        # Layout adjustments for spacing & readability
        fig.update_layout(
            xaxis={'tickangle': -45},  # Rotate event labels for better spacing
            xaxis_title="Event",
            yaxis_title="Final Score",
            margin=dict(l=40, r=40, t=60, b=120)
        )

        # Restore annotation box for explaining Box Plot
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
@app.callback(
    dash.Output('medals-plot', 'figure'),
    [dash.Input('country-dropdown', 'value'),
     dash.Input('plot-type', 'value')]
)
def update_medals_plot(selected_country, plot_type):
    filtered_data = df[df['Country'] == selected_country]

    if filtered_data.empty:
        # Return an empty graph if no data is available for the selected country
        return px.scatter(title=f"No Data Available for {selected_country}")

    if plot_type == "scatter":
        return scatterplot_by_country(selected_country)  # Calls scatter function
    else:
        # Restore the original Box Plot
        fig = px.box(
            filtered_data, 
            x="Apparatus",
            y="Score", 
            color="Apparatus",
            title=f"Gymnastics Score Distribution for {selected_country}",
            labels={"Apparatus": "Event", "Score": "Final Score"},
            points="all"  # Show all points (outliers included)
        )

        # Layout adjustments for spacing & readability
        fig.update_layout(
            xaxis={'tickangle': -45},  # Rotate event labels for better spacing
            xaxis_title="Event",
            yaxis_title="Final Score",
            margin=dict(l=40, r=40, t=60, b=120)
        )

        # Restore annotation box for explaining Box Plot
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
