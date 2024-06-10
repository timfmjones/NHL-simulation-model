import heapq
import random
import pandas as pd
import joblib
from data_loader import load_data
from game_stats import GameStats
from event_helpers import handle_failed_shot_event, handle_faceoff, handle_failed_shot_event, handle_on_goal_shot_attempt, handle_shot_attempt, handle_shot_saved

class Event:
    def __init__(self, time, event_type, team, player=None):
        self.time = time
        self.event_type = event_type
        self.team = team
        self.player = player

    def __lt__(self, other):
        return self.time < other.time

def schedule_event(event_queue, time, event_type, team, player=None):
    event = Event(time, event_type, team, player)
    heapq.heappush(event_queue, event)

def simulate_game(team1, team2, model):
    event_queue = []
    current_time = 0
    period_duration = 20  # Each period is 20 minutes
    periods = 3
    game_duration = period_duration * periods
    score1 = 0
    score2 = 0
    
    # Initialize an instance of the GameStats class
    game_stats = GameStats(home_team_name=team1.name, away_team_name=team2.name)

    # Schedule initial events (e.g., initial faceoff)
    schedule_event(event_queue, 0, 'faceoff', team1)

    while event_queue and current_time < game_duration:
        event = heapq.heappop(event_queue)
        current_time = event.time

        if event.event_type == 'faceoff':

            handle_faceoff(team1, team2, event, event_queue, game_stats)


        elif event.event_type == 'attempt_goal':
            # features = [
            #     event.team.games_played, event.team.icetime, event.team.shifts, event.team.gameScore,
            #     event.team.onIce_xGoalsPercentage, event.team.offIce_xGoalsPercentage,
            #     event.team.onIce_corsiPercentage, event.team.offIce_corsiPercentage,
            #     event.team.onIce_fenwickPercentage, event.team.offIce_fenwickPercentage
            #     # Add more features as necessary
            # ]

            # features = [event.team.xGoalsPercentage, event.team.fenwickPercentage, event.team.corsiPercentage, event.team.xGoalsFor]
            # prob_goal = model.predict_proba([features])[0][1]
            # print("shot prob goal: ", prob_goal)

            if event.team == team1:
                handle_shot_attempt(team1, team2, event, event_queue, game_stats)
            else:
                handle_shot_attempt(team2, team1, event, event_queue, game_stats)
            # Schedule the next goal attempt
            # next_goal_time = current_time + random.expovariate(1/10)
            # schedule_event(event_queue, next_goal_time, 'attempt_goal', event.team)

        elif event.event_type == 'assist':
            print(f"Assist for team {event.team.name} at {current_time} minutes")
            # Schedule the next faceoff after a goal
            schedule_event(event_queue, current_time + 1, 'faceoff', team1)
            schedule_event(event_queue, current_time + 1, 'faceoff', team2)
        
        elif event.event_type == "on_goal_shot":
            handle_on_goal_shot()

        elif event.event_type == 'block_shot':
            print(f"Blocked shot by team {event.team.name} at {current_time} minutes")
            # Update stats 
            game_stats.teams[event.team.name]['blockedShots'] += 1
            # Schedule the next events after a block
            schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', event.team )
        
        elif event.event_type == 'save_shot':
            print(f"Saved shot by team {event.team.name} at {current_time} minutes")
            # Schedule the next events after a save
            schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', event.team)

        elif event.event_type == 'missed_shot':
            print(f"Missed shot by {event.team.name} at {current_time} minutes")
            schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', team1 if event.team == team2 else team2)


        elif event.event_type == 'penalty':
            # Schedule the end of the penalty
            penalty_duration = 2  # 2 minutes for a standard minor penalty
            schedule_event(event_queue, current_time + penalty_duration, 'end_penalty', event.team)
            print(f"Penalty for team {event.team.name} at {current_time} minutes")

            # Schedule power play events for the other team
            power_play_end = current_time + penalty_duration
            schedule_event(event_queue, current_time + random.expovariate(1/5), 'power_play', team1 if event.team == team2 else team2, power_play_end)

        elif event.event_type == 'end_penalty':
            print(f"Penalty ended for team {event.team.name} at {current_time} minutes")

        elif event.event_type == 'power_play':
            if current_time < event.player:
                print(f"Power play for team {event.team.name} at {current_time} minutes")
                schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', event.team)

        elif event.event_type == 'breakaway':
            print(f"Breakaway for team {event.team.name} at {current_time} minutes")
            schedule_event(event_queue, current_time + 1, 'attempt_goal', event.team)

        elif event.event_type == 'turnover':
            print(f"Turnover by team {event.team.name} at {current_time} minutes")
            next_team = team1 if event.team == team2 else team2
            schedule_event(event_queue, current_time + 1, 'attempt_goal', next_team)

        elif event.event_type == 'interception':
            print(f"Interception by team {event.team.name} at {current_time} minutes")
            next_team = team1 if event.team == team2 else team2
            schedule_event(event_queue, current_time + 1, 'attempt_goal', next_team)

        elif event.event_type == 'injury':
            print(f"Injury for team {event.team.name} at {current_time} minutes")
            # Schedule next shift change if a player is injured
            schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', event.team)

        elif event.event_type == 'timeout':
            print(f"Timeout called by team {event.team.name} at {current_time} minutes")
            # After timeout, schedule faceoff
            schedule_event(event_queue, current_time + 1, 'faceoff', team1)
            schedule_event(event_queue, current_time + 1, 'faceoff', team2)

        elif event.event_type == 'end_period':
            print(f"End of period at {current_time} minutes")
            if current_time < game_duration:
                # Schedule start of next period
                schedule_event(event_queue, current_time + 1, 'start_period', team1)
                schedule_event(event_queue, current_time + 1, 'start_period', team2)

        elif event.event_type == 'start_period':
            print(f"Start of period at {current_time} minutes")
            schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', team1)
            schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', team2)
            schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', team1)
            schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', team2)

    print(game_stats)
    game_summary(game_stats)
    return round(score1), round(score2)

def main():
    print("running main")
    skaters_file = 'data/skaters_2024.csv'
    goalies_file = 'data/goalies_2024.csv'
    teams_file = 'data/teams_2024.csv'
    model_file = 'goal_prediction_model.pkl'

    skaters, goalies, teams = load_data(skaters_file, goalies_file, teams_file)

    # Load the trained model
    model = joblib.load(model_file)



    # Simulate multiple games
    # for _ in range(100):  # Simulate 100 games
    #     for team1 in teams.values():
    #         for team2 in teams.values():
    #             if team1 != team2:
    #                 score1, score2 = simulate_game(team1, team2, model)
    #                 results.append({
    #                     'team1': team1.name,
    #                     'team2': team2.name,
    #                     'score1': score1,
    #                     'score2': score2
    #                 })

    # Simulate one game (randoms)
    random_team_1 = random.choice(list(teams.values()))
    random_team_2 = random.choice(list(teams.values()))
    if random_team_1 != random_team_2:
        score1, score2 = simulate_game(random_team_1, random_team_2, model)
        results
        results.append({
            'team1': random_team_1.name,
            'team2': random_team_2.name,
            'score1': score1,
            'score2': score2
        })

    # results_df = pd.DataFrame(results)
    # results_df.to_csv('simulation_results.csv', index=False)


def game_summary(game_stats):
    print("game stats")
    # print(game_stats.teams[0]['name'])
    # print('goals: ', game_stats.teams[0]['goals'])




if __name__ == "__main__":
    main()
