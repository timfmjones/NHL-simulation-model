import heapq
import random
import pandas as pd
import joblib
from data_loader import load_data
import events

def handle_faceoff(team1, team2, event, event_queue):
    
    teams = pd.read_csv('data/teams_2024.csv')
    team1_stat = teams[(teams['team'] == team1.name) & (teams['situation'] == 'all')]
    team1_stats = team1_stat.iloc[0]
    team1_faceoffs_won = team1_stats['faceOffsWonFor']
    team1_faceoffs_against = team1_stats['faceOffsWonAgainst']
    team1_percent = team1_faceoffs_won / (team1_faceoffs_against + team1_faceoffs_won)

    team2_stat = teams[(teams['team'] == team2.name) & (teams['situation'] == 'all')]
    team2_stats = team2_stat.iloc[0]
    team2_faceoffs_won = team2_stats['faceOffsWonFor']
    team2_faceoffs_against = team2_stats['faceOffsWonAgainst']
    team2_percent = team2_faceoffs_won / (team2_faceoffs_against + team2_faceoffs_won)

    total_percent = team1_percent + team2_percent
    team1_relative_percentage = team1_percent / (team1_percent + team2_percent)

    print(team1_relative_percentage)
    if random.random() < team1_relative_percentage:
        winning_team = team1
        losing_team = team2
    else:
        winning_team = team2
        losing_team = team1

    # Converts faceoff time from seconds to minutes:seconds
    faceoff_time_seconds = event.time
    faceoff_time_minutes = int(faceoff_time_seconds // 60)
    faceoff_time_remaining_seconds = int(faceoff_time_seconds % 60)

    print(f"Faceoff won by team {winning_team.name} at {faceoff_time_minutes} minutes and {faceoff_time_remaining_seconds} seconds")
    
    events.schedule_event(event_queue, event.time + random.gauss(8, 2), 'attempt_goal', winning_team)

print ("hello from faceoffs.py")