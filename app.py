import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback
# Import the function from visualizations.py
from visualizations import scatterplot_by_country
from sqlPlots import query_pivoted_database
from simulations import add_user_entry
from simulations import delete_recent_entry
from simulations import monte_carlo
from simulations import medal_count_by_country


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

    dcc.Graph(id='country-plot'),  
    html.H1("Enter a Hypothetical Athlete to Run Simulations on Country Medal Count"),
    
    html.P("Your gymnast's first name:"), 
    dcc.Textarea(
        id='FirstName',
        style={'width': 500, 'height': 20}, 
    ),
    html.P("Your gymnast's last name:"), 
    dcc.Textarea(
        id='LastName',
        style={'width': 500, 'height': 20}, 
    ),
    html.P("Your gymnast's country:"),
    dcc.Dropdown(
        id='Country',
        options=[{'label': country, 'value': country} for country in df['Country'].unique()],
        value='USA', 
        clearable=False
    ),
    html.P("Your gymnast's expected balance beam score: "),
      dcc.Textarea(
        id='BB_PredictedScore',
        style={'width': 500, 'height': 20},
    ),
    html.P("Your gymnast's expected vault score: "),
      dcc.Textarea(
        id='VT_PredictedScore',
        style={'width': 500, 'height': 20},
    ),
    html.P("Your gymnast's expected floor exercise score: "),
      dcc.Textarea(
        id='FX_PredictedScore',
        style={'width': 500, 'height': 20},
    ),
    html.P("Your gymnast's expected unbalanced bars score: "),
      dcc.Textarea(
        id='UB_PredictedScore',
        style={'width': 500, 'height': 20},
    ),
      html.Button('Submit', id='submit-button', n_clicks=0,  #keeping track of when the user clicked on the button
                    style={ 
        'backgroundColor': '#643843', #changing background color to dark pink
        'color': 'white', #text is white
        'padding': '10px 20px', #padding for better design
        'borderRadius': '5px', #more rounded edges
    }),
    html.Div(id='textarea-output', style={'whiteSpace': 'pre-line', 'margin': 40, 'border': 50}), #margin for more white space
    dcc.Graph(id='medals-plot')  # This graph updates based on the dropdown & toggle
], style={'whiteSpace': 'pre-line', 'margin': 40, 'border': 50})

# Callback to update the plot based on user selection
@app.callback(
    dash.Output('country-plot', 'figure'),
    [dash.Input('country-dropdown', 'value'),
     dash.Input('plot-type', 'value')]
)
def update_plot(selected_country, plot_type):
    filtered_data = df[df['Country'] == selected_country]

    if filtered_data.empty:
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
    # dash.Output('textarea-output', 'children'),
    Output('medals-plot', 'figure'),
    
    # dash.Input('country-dropdown', 'value'),
    Input('submit-button', 'n_clicks'), 
    State('FirstName', 'value'), 
    State('LastName', 'value'), 
    State('Country', 'value'), 
    State('BB_PredictedScore', 'value'), 
    State('VT_PredictedScore', 'value') ,
    State('FX_PredictedScore', 'value') ,
    State('UB_PredictedScore', 'value') ,
)

def update_medals_plot(n_clicks, FirstName, LastName, Country, BB_PredictedScore, VT_PredictedScore, FX_PredictedScore, UB_PredictedScore):
    if n_clicks == 0:
        return px.scatter(title="No Data Available Yet- Please fill in Athlete's Details")
    
    if None in [FirstName, LastName, Country, BB_PredictedScore, VT_PredictedScore, FX_PredictedScore, UB_PredictedScore]:
        return px.scatter(title="Please fill in all fields.")


    if n_clicks > 0:
        BB_PredictedScore = float(BB_PredictedScore) if BB_PredictedScore else 0.0
        VT_PredictedScore = float(VT_PredictedScore) if VT_PredictedScore else 0.0
        FX_PredictedScore = float(FX_PredictedScore) if FX_PredictedScore else 0.0
        UB_PredictedScore = float(UB_PredictedScore) if UB_PredictedScore else 0.0

        # return(f' FirstName"{FirstName}" LastName"{LastName}"  Country"{Country}"  BB_PredictedScore"{BB_PredictedScore}"  VT_PredictedScore"{VT_PredictedScore}"  FX_PredictedScore"{FX_PredictedScore}" UB_PredictedScore"{UB_PredictedScore}" ') 
        pivoted_database = query_pivoted_database()
        new_pivoted_database = add_user_entry(pivoted_database,FirstName, LastName, Country, BB_PredictedScore, VT_PredictedScore, FX_PredictedScore, UB_PredictedScore)
        medal_pivoted_database = monte_carlo(pivoted_database)
        return medal_count_by_country(medal_pivoted_database, Country)  # Calls medal count by country
    


if __name__ == '__main__':
    app.run_server(debug=True)
