import pandas as pd
import random
from event import schedule_event

def handle_failed_shot_event(team1, team2, event, event_queue, game_stats):
    print(f"Shot on goal by team {team1.name} at {event.time} minutes")
    if random.random() < 0.5:

        schedule_event(event_queue, event.time + 0.1, 'block_shot', team2)
    else:
        schedule_event(event_queue, event.time + 0.1, 'save_shot', team2)


def handle_faceoff(team1, team2, event, event_queue, game_stats):
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
        game_stats.teams[team1.name]['faceOffsWon'] += 1
        game_stats.teams[team2.name]['faceOffsLost'] += 1
 
    else:
        winning_team = team2
        losing_team = team1
        game_stats.teams[team2.name]['faceOffsWon'] += 1
        game_stats.teams[team1.name]['faceOffsLost'] += 1
 
    

    print(f"Faceoff won by team {winning_team.name} at {event.time} minutes")
    schedule_event(event_queue, event.time + random.gauss(8, 2), 'attempt_goal', winning_team)

def handle_shot_attempt(team1, team2, event, event_queue, game_stats):
    print("Shot attempt by ", team1.name)
    teams = pd.read_csv('data/teams_2024.csv')
    team1_stat = teams[(teams['team'] == team1.name) & (teams['situation'] == 'all')]
    team1_stats = team1_stat.iloc[0]

    team1_shot_attempts_for = team1_stats['shotAttemptsFor']
    team1_blocked_shot_attempts_for = team1_stats['blockedShotAttemptsFor']
    team1_missed_shot_attempts_for = team1_stats['missedShotsFor']
    team1_on_goal_shot_attempts_for = team1_stats['shotsOnGoalFor']

    team1_blocked_shot_attempts_for_percentage = team1_blocked_shot_attempts_for/team1_shot_attempts_for
    team1_missed_shot_attempts_for_percentage = team1_missed_shot_attempts_for/team1_shot_attempts_for
    team1_on_goal_shot_attempts_for_percentage = team1_on_goal_shot_attempts_for/team1_shot_attempts_for
    

    team2_stat = teams[(teams['team'] == team2.name) & (teams['situation'] == 'all')]
    team2_stats = team2_stat.iloc[0]
    team2_shot_attempts_against = team2_stats['shotAttemptsAgainst']
    team2_blocked_shot_attempts_against = team2_stats['blockedShotAttemptsAgainst']
    team2_missed_shot_attempts_against = team2_stats['missedShotsAgainst']
    team2_on_goal_shot_attempts_against = team1_stats['shotsOnGoalAgainst']

    team2_blocked_shot_attempts_against_percentage = team2_blocked_shot_attempts_against/team2_shot_attempts_against
    team2_missed_shot_attempts_against_percentage = team2_missed_shot_attempts_against/team2_shot_attempts_against
    team2_on_goal_shot_attempts_against_percentage = team2_on_goal_shot_attempts_against/team2_shot_attempts_against

    blocked_shot_attempt_relative_percentage = (team1_blocked_shot_attempts_for_percentage + team2_blocked_shot_attempts_against_percentage) / 2
    missed_shot_attempt_relative_percentage = (team1_missed_shot_attempts_for_percentage + team2_missed_shot_attempts_against_percentage) / 2
    on_goal_shot_attempt_relative_percentage = (team1_on_goal_shot_attempts_for_percentage + team2_on_goal_shot_attempts_against_percentage) / 2

    random_number = random.random() 

    if random_number < blocked_shot_attempt_relative_percentage:
        # Blocked shot 
        schedule_event(event_queue, event.time + 1, 'block_shot', team2)
    elif random_number < blocked_shot_attempt_relative_percentage + missed_shot_attempt_relative_percentage:
        # Missed shot 
        schedule_event(event_queue, event.time + 1, 'missed_shot', team1)
    else:
        # On target shot 
        print("On target shot")
        # schedule_event(event_queue, event.time + 0.1, 'save_shot', team2)
        handle_on_goal_shot_attempt(team1, team2, event, event_queue, game_stats)


def handle_on_goal_shot_attempt(team1, team2, event, event_queue, game_stats):
    teams = pd.read_csv('data/teams_2024.csv')
    team1_stat = teams[(teams['team'] == team1.name) & (teams['situation'] == 'all')]
    team1_stats = team1_stat.iloc[0]

    team1_on_goal_shot_attempts_for = team1_stats['shotsOnGoalFor']
    team1_goals_for = team1_stats['goalsFor']
    team1_on_saved_goal_shot_attempts_for = team1_stats['savedShotsOnGoalFor']

    team1_goals_for_percentage = team1_goals_for/team1_on_goal_shot_attempts_for
    team1_on_saved_goal_shot_attempts_for_percentage = team1_on_saved_goal_shot_attempts_for/team1_on_goal_shot_attempts_for


    team2_stat = teams[(teams['team'] == team2.name) & (teams['situation'] == 'all')]
    team2_stats = team2_stat.iloc[0]

    team2_on_goal_shot_attempts_against = team2_stats['shotsOnGoalAgainst']
    team2_goals_against = team2_stats['goalsAgainst']
    team2_on_saved_goal_shot_attempts_against = team2_stats['savedShotsOnGoalAgainst']

    team2_goals_against_percentage = team2_goals_against/team2_on_goal_shot_attempts_against
    team2_on_saved_goal_shot_attempts_against_percentage = team2_on_saved_goal_shot_attempts_against/team2_on_goal_shot_attempts_against

    goals_relative_percentage = (team1_goals_for_percentage + team2_goals_against_percentage)/2
    saved_on_goal_shot_attempt = (team1_on_saved_goal_shot_attempts_for_percentage + team2_on_saved_goal_shot_attempts_against_percentage)/2

    random_number = random.random() 

    if random_number < goals_relative_percentage:
        game_stats.teams[team1.name]['goals'] +=1
        print("GOAL")
        print(f"Team {team1.name} scored at {event.time} minutes")
        schedule_event(event_queue, event.time + 0.001, 'assist', team1)
    else:
        handle_failed_shot_event(team1, team2, event, event_queue, game_stats)

def handle_shot_saved(team1, team2, event, event_queue, game_stats):
    teams = pd.read_csv('data/teams_2024.csv')
    team1_stat = teams[(teams['team'] == team1.name) & (teams['situation'] == 'all')]
    team1_stats = team1_stat.iloc[0]
    team1_saved_on_goal_shot_attempts_for = team1_stats['savedShotsOnGoalFor']
    team1_rebounds_for = team1_stats['reboundsFor']

    team2_stat = teams[(teams['team'] == team2.name) & (teams['situation'] == 'all')]
    team2_stats = team2_stat.iloc[0]
    team2_saved_on_goal_shot_attempts_against = team2_stats['savedShotsOnGoalAgainst']
    team2_rebounds_against = team2_stats['reboundsAgainst']

    team1_rebound_for_percentage = team1_rebounds_for/team1_saved_on_goal_shot_attempts_for
    team2_rebound_against_percentage = team2_rebounds_against/team2_saved_on_goal_shot_attempts_against

    rebound_relative_percentage = (team1_rebound_for_percentage/team2_rebound_against_percentage)

    if random.random() < rebound_relative_percentage:
        print("rebound")
    else:
        print("saved")    


def handle_create_shot_attempt(team1, team2, event, event_queue, game_stats):
    teams = pd.read_csv('data/teams_2024.csv')
    team1_stat = teams[(teams['team'] == team1.name) & (teams['situation'] == 'all')]