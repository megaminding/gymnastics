from plotly import express as px
import numpy as np
def add_user_entry(df, FirstName, LastName, Country, BB_PredictedScore, VT_PredictedScore, FX_PredictedScore, UB_PredictedScore):
    """
    This function allows users to add a new entry into the database

    Args:
        df: dataframe
        FirstName
        LastName
        Country
        BB_PredictedScore
        VT_PredictedScore
        FX_PredictedScore
        UB_PredictedScore

    Returns:
        dataframe
    """
    index = len(df)
    df.loc[index] = [FirstName, LastName, Country, BB_PredictedScore, VT_PredictedScore, FX_PredictedScore, UB_PredictedScore]
    print(df)
    return df


def delete_recent_entry(df):
    """
    This function allows users to delete the most recent entry of a database

    Args:
        df: dataframe
      

    Returns:
        dataframe
    """
    index = len(df)
    df = df.drop(index - 1)
    print(df)
    
def monte_carlo(df):
    """
    This function allows users to run Monte Carlo simulations to see the expected medal count of each gymnast

    Args:
        df: dataframe
      

    Returns:
        dataframe
    """
    list_of_events = ['BB', 'VT', 'FX', 'UB']

    num_simulations = 1000

    df['gold'] = 0
    df['silver'] = 0
    df['bronze'] = 0

    for i in range(num_simulations): 
        for event in list_of_events:
            event_data = df[df[f'{event}_PredictedScore'].notna()].copy() #only select data that is the specific event type
            event_data['simulated_score'] = event_data[f'{event}_PredictedScore'] + np.random.normal(0, 0.1, size=len(event_data)) #add noise to create simulated score
            event_data = event_data.sort_values(by='simulated_score', ascending=False).reset_index(drop=True) #sort simulated scores from highest to lowest

            #award medals to top three scorers in simulated score
            df.loc[df['LastName'] == event_data.loc[0, 'LastName'], 'gold'] += 1
            df.loc[df['LastName'] == event_data.loc[1, 'LastName'], 'silver'] += 1
            df.loc[df['LastName'] == event_data.loc[2, 'LastName'], 'bronze'] += 1

    final_results = df.sort_values(by=['gold', 'silver', 'bronze'], ascending=False) #sort by medal count
    print(final_results)
    return (final_results)


def medal_count_by_country(df, country):
    """
    This function visualizes the athlete's who were able to win medals for their country in the simulation

    Args:
        df: dataframe
        country
      

    Returns:
        dataframe
    """
    results_by_country = (df[df['Country']==country]).head()
    print(results_by_country)

    fig = px.histogram(results_by_country, 
                    x="LastName", 
                    y=["gold", 'silver', 'bronze'], 
                    title=f"Medal County per Athele for Country '{country}'",
                    color_discrete_sequence=['gold', 'silver', '#CD7F32']
                    )

    fig.update_layout(
        xaxis_title="Gymnast Last Name", 
        yaxis_title="Predicted Olympic Medal Count out of 1000 Simulations",
        legend_title="Medal Type",
    )

    return fig