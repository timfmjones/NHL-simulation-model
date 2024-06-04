import pandas as pd
from data_structures import Skater, Goalie, Team

def load_data(skaters_file, goalies_file, teams_file):
    skaters_df = pd.read_csv(skaters_file)
    goalies_df = pd.read_csv(goalies_file)
    teams_df = pd.read_csv(teams_file)
    
    skaters = {}
    goalies = {}
    teams = {}

    # Populate teams dictionary
    for _, row in teams_df.iterrows():
        team = Team(**row.to_dict())
        teams[row['team']] = team

    # Populate skaters dictionary and add them to their respective teams
    for _, row in skaters_df.iterrows():
        skater = Skater(**row.to_dict())
        skaters[row['playerId']] = skater
        teams[skater.team].add_skater(skater)

    # Populate goalies dictionary and add them to their respective teams
    for _, row in goalies_df.iterrows():
        goalie = Goalie(**row.to_dict())
        goalies[row['playerId']] = goalie
        teams[goalie.team].add_goalie(goalie)

    return skaters, goalies, teams
