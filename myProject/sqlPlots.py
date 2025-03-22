import pandas as pd
import sqlite3
maindf = pd.read_csv("data_2022_2023.csv")
import plotly.express as px
import plotly
from plotly import express as px
import plotly.io as pio


def data_cleaning(maindf):
    """
    This function  cleans the data by removing NA values. It also replaces apparatus values of 'VT1' and 'VT2' to be 'VT'. It only filters for women gymnasts.

    Args:
        maindf: dataframe

    Returns:
        dataframe
    """
    maindf.dropna(inplace=True, subset=[ 'Apparatus', 'Score', 'Country', 'D_Score', "E_Score"]) #removing NA values
    maindf.loc[maindf['Apparatus'] == 'VT1', 'Apparatus'] = 'VT' #replaces apparatus values of 'VT1' and 'VT2' to be 'VT'
    maindf.loc[maindf['Apparatus'] == 'VT2', 'Apparatus'] = 'VT' #replaces apparatus values of 'VT1' and 'VT2' to be 'VT'
    maindf = maindf[maindf['Gender'] == 'w']#women's only
    return maindf


def difficultyVsExecutionPlot(maindf):
    """
    This function  is a scatterplot that shows the relationship between difficulty and execution

    Args:
        maindf: dataframe

    Returns:
        shows figure
    """
    fig = px.scatter(maindf,  #scatterplot that shows the relationship between difficulty and execution
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
    """
    This function  connects to the SQL database to filter by a particular country and add values called the 'PredictedScore' and 'StdDevScore' and 'CompetitionsCount'

    Args:
        country

    Returns:
        returns df
    """
    with sqlite3.connect('gym') as conn: #  connects to the SQL database to filter by a particular country and add values called the 'PredictedScore' and 'StdDevScore' and 'CompetitionsCount'
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

def scatterplot_of_country(country):
    """
    This function shows a scatterplot of the gymnast's predicted score. 

    Args:
        country

    Returns:
        shows figure
    """
    fig = px.scatter(query_gym_country_database(country), # shows a scatterplot of the gymnast's predicted score. 
                x = "Apparatus", 
                y = "PredictedScore", 
                color="LastName",
                size='CompetitionsCount', hover_data=['PredictedScore'])


    fig.update_layout(
        title=f"Scatterplot of Gymnasts' Predicted Score in Country '{country}'", #The colorbar and overall plot have professional titles.
        yaxis_title="Predicted Score of Gymnasts",
        )


    fig.show()

def query_pivoted_database():
    """
    This function  connects to the SQL database to pivot it, meaning to transform the data from along form table to a wide form table. Achieving this will allow us to consolidate multiple rows of athlete’s scores across different events into just one row with the best scores of each event in each column. 

    Args:
        None

    Returns:
        df
    """
    with sqlite3.connect('gym') as conn: # connects to the SQL database to pivot it, meaning to transform the data from along form table to a wide form table. Achieving this will allow us to consolidate multiple rows of athlete’s scores across different events into just one row with the best scores of each event in each column. 

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

