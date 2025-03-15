import pandas as pd
import sqlite3
maindf = pd.read_csv("data_2022_2023.csv")
import plotly.express as px
import plotly
from plotly import express as px
import plotly.io as pio


def data_cleaning(maindf):
    maindf.dropna(inplace=True, subset=[ 'Apparatus', 'Score', 'Country', 'D_Score', "E_Score"])
    maindf.loc[maindf['Apparatus'] == 'VT1', 'Apparatus'] = 'VT'
    maindf.loc[maindf['Apparatus'] == 'VT2', 'Apparatus'] = 'VT'
    maindf = maindf[maindf['Gender'] == 'w']
    return maindf


def difficultyVsExecutionPlot(maindf):
    fig = px.scatter(maindf, 
                  x="D_Score", 
                  y="E_Score", 
                  color="Apparatus", 
                  hover_data=['LastName', 'FirstName'],
                  title="Difficulty vs Execution Tradeoff Across Apparatuses",
                  trendline="ols")

    fig.update_layout(
        xaxis_title="Average Difficulty Score (D_Score)", 
        yaxis_title="Average Execution Score (E_Score)",
        legend_title="Apparatus",
    )

    fig.show()
    
def query_gym_country_database(country):
    with sqlite3.connect('gym') as conn:
        cmd = \
        f'''
        SELECT LastName, FirstName, Apparatus, AVG(Score) AS PredictedScore, MAX(Score) as Maxscore, 
        SQRT(AVG(score * score) - AVG(score) * AVG(score)) AS StdDevScore,
        COUNT(DISTINCT Date) AS CompetitionsCount
        FROM gym 
        WHERE Country = '{country}'
        GROUP BY LastName, FirstName, Apparatus 
        ORDER BY Apparatus, Maxscore DESC
        '''
    df = pd.read_sql_query(cmd, conn)
    return (df)

def scatterplot_by_country(country):
    fig = px.scatter(query_gym_country_database(country),
                x = "Apparatus", 
                y = "PredictedScore", 
                color="LastName",
                size='CompetitionsCount', hover_data=['PredictedScore'])


    fig.update_layout(
        title=f"Scatterplot of Gymnasts' MaxScore in Country '{country}'", #The colorbar and overall plot have professional titles.
        yaxis_title="Max Score of Gymnasts",
        )


    fig.show()

def query_pivoted_database():
    with sqlite3.connect('gym') as conn:
        cmd = f'''
        WITH AthleteScores AS (
            SELECT 
                LastName, 
                FirstName,
                Apparatus,
                AVG(Score) AS PredictedScore,
                COUNT(DISTINCT Date) AS CompetitionsCount,
                Country
            FROM gym 
            GROUP BY LastName, FirstName, Apparatus
        )
        SELECT 
            LastName, 
            FirstName,
            Country,
            MAX(CASE WHEN Apparatus = 'BB' THEN PredictedScore END) AS BB_PredictedScore,
            MAX(CASE WHEN Apparatus = 'VT' THEN PredictedScore END) AS VT_PredictedScore,
            MAX(CASE WHEN Apparatus = 'FX' THEN PredictedScore END) AS FX_PredictedScore,
            MAX(CASE WHEN Apparatus = 'UB' THEN PredictedScore END) AS UB_PredictedScore
          
        FROM AthleteScores
        GROUP BY LastName, FirstName, Country
        ORDER BY LastName, FirstName, Country
        '''

        df = pd.read_sql_query(cmd, conn)
    
    return df

