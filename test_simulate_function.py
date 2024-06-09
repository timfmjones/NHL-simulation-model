import heapq
import random
import pandas as pd
import joblib
from data_loader import load_data
import events
import faceoffs


# This file was made to try rewriting the simulate_game function in game_simulatior.py using a dictionary.
# Depending on the outcome, using a dictionary may reduce the amount of code required for the simulate_game function. 

def simulate_game(team1, team2, model):
    event_queue = []
    current_time = 0
    period_duration = 20  # Each period is 20 minutes
    periods = 3
    game_duration = period_duration * periods
    score1 = 0
    score2 = 0

    # Schedule initial events (e.g., initial faceoff)
    events.schedule_event(event_queue, 0, faceoffs.handle_faceoff, team1)

    while event_queue and current_time < game_duration:
        event = heapq.heappop(event_queue)
        current_time = event.time

        def faceoff():
            faceoffs.handle_faceoff(team1, team2, event, event_queue)

        def attempt_goal():
            features = [event.team.xGoalsPercentage, event.team.fenwickPercentage, event.team.corsiPercentage, event.team.xGoalsFor]
            prob_goal = model.predict_proba([features])[0][1]
            print("shot prob goal: ", prob_goal)

            if event.team == team1:
                handle_on_goal_shot_attempt(team1, team2, event, event_queue)
            else:
                handle_on_goal_shot_attempt(team2, team1, event, event_queue)

        def assist():
            print(f"Assist for team {event.team.name} at {current_time} minutes")
            # Schedule the next faceoff after a goal
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team1)
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team2)
        
        def on_goal_shot():
            handle_on_goal_shot_attempt()

        def blocked_shot():
            print(f"Shot blocked by team {event.team.name} at {current_time} minutes")
            # Schedules the next events after a blocked shot
            events.schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', team1 if event.team == team2 else team2)

        def saved_shot():
            print(f"Shot saved by team {event.team.name} at {current_time} minutes")
            # Schedules the next events after a saved shot
            events.schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', team1 if event.team == team2 else team2)
        
        def penalty():
            # Schedules the end of a penalty
            penalty_duration = 2  # 2 minutes for a standard minor penalty
            events.schedule_event(event_queue, current_time + penalty_duration, 'end_penalty', event.team)
            print(f"Penalty for team {event.team.name} at {current_time} minutes")

            # Schedules power play events for the other team
            power_play_end = current_time + penalty_duration
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'power_play', team1 if event.team == team2 else team2, power_play_end)
        
        def end_penalty():
            print(f"Penalty ended for team {event.team.name} at {current_time} minutes")
        
        def power_play():
            if current_time < event.player:
                print(f"Power play for team {event.team.name} at {current_time} minutes")
                events.schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', event.team)
        
        def breakaway():
            print(f"Breakaway for team {event.team.name} at {current_time} minutes!")
            events.schedule_event(event_queue, current_time + 1, 'attempt_goal', event.team)

        def turnover():
            print(f"Turnover by team {event.team.name} at {current_time} minutes")
            next_team = team1 if event.team == team2 else team2
            events.schedule_event(event_queue, current_time + 1, 'attempt_goal', next_team)
        
        def interception():
            print(f"Interception by team {event.team.name} at {current_time} minutes")
            next_team = team1 if event.team == team2 else team2
            events.schedule_event(event_queue, current_time + 1, 'attempt_goal', next_team)
        
        def injury():
            print(f"Injury for team {event.team.name} at {current_time} minutes")
            # Schedules next shift change if a player is injured
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', event.team)
        
        def timeout():
            print(f"Timeout called by team {event.team.name} at {current_time} minutes")
            # After timeout, schedule faceoff
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team1)
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team2)
        
        def end_period():
            print(f"End of period at {current_time} minutes")
            if current_time < game_duration:
                # Schedule start of next period
                events.schedule_event(event_queue, current_time + 1, 'start_period', team1)
                events.schedule_event(event_queue, current_time + 1, 'start_period', team2)
        
        def start_period():
            print(f"Start of period at {current_time} minutes")
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', team1)
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', team2)
            events.schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', team1)
            events.schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', team2)

        conditions = {
            'condition_faceoff' : faceoff,
            'condition_attempt_goal' : attempt_goal,
            'condition_assist' : assist,
            'condition_on_goal_shot' : on_goal_shot,
            'condition_blocked_shot' : blocked_shot,
            'condition_saved_shot' : saved_shot,
            'condition_penalty' : penalty,
            'consition_end_penalty' : end_penalty,
            'condition_power_play' : power_play,
            'condition_breakaway' : breakaway,
            'condition_turnover' : turnover,
            'condition_interception' : interception,
            'condition_injury' : injury,
            'condition_timeout' : timeout,
            'condition_end_period' : end_period,
            'condition_start_period' : start_period
        }

    return round(score1), round(score2)


"""
def simulate_game(team1, team2, model):
    event_queue = []
    current_time = 0
    period_duration = 20  # Each period is 20 minutes
    periods = 3
    game_duration = period_duration * periods
    score1 = 0
    score2 = 0

    # Schedule initial events (e.g., initial faceoff)
    events.schedule_event(event_queue, 0, faceoffs.handle_faceoff, team1)

    while event_queue and current_time < game_duration:
        event = heapq.heappop(event_queue)
        current_time = event.time

        if event.event_type == 'faceoff':
            faceoffs.handle_faceoff(team1, team2, event, event_queue)

        elif event.event_type == 'attempt_goal':
            # features = [
            #     event.team.games_played, event.team.icetime, event.team.shifts, event.team.gameScore,
            #     event.team.onIce_xGoalsPercentage, event.team.offIce_xGoalsPercentage,
            #     event.team.onIce_corsiPercentage, event.team.offIce_corsiPercentage,
            #     event.team.onIce_fenwickPercentage, event.team.offIce_fenwickPercentage
            #     # Add more features as necessary
            # ]

            features = [event.team.xGoalsPercentage, event.team.fenwickPercentage, event.team.corsiPercentage, event.team.xGoalsFor]
            prob_goal = model.predict_proba([features])[0][1]
            print("shot prob goal: ", prob_goal)

            if event.team == team1:
                # if random.random() < prob_goal:
                #     #Goal team 1
                #     score1 += 1
                #     print(f"Team {team1.name} scored at {current_time} minutes")
                #     schedule_event(event_queue, current_time + 1, 'assist', team1)
                # else:
                #     #Failed shot attempt team1
                #     # print(f"Shot on goal by team {team1.name} at {current_time} minutes")
                #     # if random.random() < 0.5:
                #     #     schedule_event(event_queue, current_time + 1, 'block_shot', team2)
                #     # else:
                #     #     schedule_event(event_queue, current_time + 1, 'save_shot', team2) 
                #     failed_shot_event(team1, team2, event, event_queue)

                #     #TODO logic to decide how shot attempt failed
                handle_on_goal_shot_attempt(team1, team2, event, event_queue)
            else:
                # if random.random() < prob_goal:
                #     # Goal team 2
                #     score2 += 1
                #     print(f"Team {team2.name} scored at {current_time} minutes")
                #     schedule_event(event_queue, current_time + 1, 'assist', team2)
                # else:
                #     # Failed shot attempt team 2
                #     # print(f"Shot on goal by team {team2.name} at {current_time} minutes")
                #     # schedule_event(event_queue, current_time + 1, 'block_shot', team1)
                #     failed_shot_event(team2, team1, event, event_queue)
                handle_on_goal_shot_attempt(team2, team1, event, event_queue)
            # Schedule the next goal attempt
            # next_goal_time = current_time + random.expovariate(1/10)
            # schedule_event(event_queue, next_goal_time, 'attempt_goal', event.team)

        elif event.event_type == 'assist':
            print(f"Assist for team {event.team.name} at {current_time} minutes")
            # Schedule the next faceoff after a goal
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team1)
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team2)
        
        elif event.event_type == 'on_goal_shot':
            handle_on_goal_shot_attempt()

        elif event.event_type == 'block_shot':
            print(f"Shot blocked by team {event.team.name} at {current_time} minutes")
            # Schedule the next events after a block
            events.schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', team1 if event.team == team2 else team2)
        
        elif event.event_type == 'save_shot':
            print(f"Shot saved by team {event.team.name} at {current_time} minutes")
            # Schedule the next events after a save
            events.schedule_event(event_queue, current_time + random.gauss(5, 2), 'attempt_goal', team1 if event.team == team2 else team2)

        elif event.event_type == 'penalty':
            # Schedule the end of the penalty
            penalty_duration = 2  # 2 minutes for a standard minor penalty
            events.schedule_event(event_queue, current_time + penalty_duration, 'end_penalty', event.team)
            print(f"Penalty for team {event.team.name} at {current_time} minutes")

            # Schedule power play events for the other team
            power_play_end = current_time + penalty_duration
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'power_play', team1 if event.team == team2 else team2, power_play_end)

        elif event.event_type == 'end_penalty':
            print(f"Penalty ended for team {event.team.name} at {current_time} minutes")

        elif event.event_type == 'power_play':
            if current_time < event.player:
                print(f"Power play for team {event.team.name} at {current_time} minutes")
                events.schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', event.team)

        elif event.event_type == 'breakaway':
            print(f"Breakaway for team {event.team.name} at {current_time} minutes")
            events.schedule_event(event_queue, current_time + 1, 'attempt_goal', event.team)

        elif event.event_type == 'turnover':
            print(f"Turnover by team {event.team.name} at {current_time} minutes")
            next_team = team1 if event.team == team2 else team2
            events.schedule_event(event_queue, current_time + 1, 'attempt_goal', next_team)

        elif event.event_type == 'interception':
            print(f"Interception by team {event.team.name} at {current_time} minutes")
            next_team = team1 if event.team == team2 else team2
            events.schedule_event(event_queue, current_time + 1, 'attempt_goal', next_team)

        elif event.event_type == 'injury':
            print(f"Injury for team {event.team.name} at {current_time} minutes")
            # Schedule next shift change if a player is injured
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', event.team)

        elif event.event_type == 'timeout':
            print(f"Timeout called by team {event.team.name} at {current_time} minutes")
            # After timeout, schedule faceoff
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team1)
            events.schedule_event(event_queue, current_time + 1, 'faceoff', team2)

        elif event.event_type == 'end_period':
            print(f"End of period at {current_time} minutes")
            if current_time < game_duration:
                # Schedule start of next period
                events.schedule_event(event_queue, current_time + 1, 'start_period', team1)
                events.schedule_event(event_queue, current_time + 1, 'start_period', team2)

        elif event.event_type == 'start_period':
            print(f"Start of period at {current_time} minutes")
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', team1)
            events.schedule_event(event_queue, current_time + random.expovariate(1/5), 'shift_change', team2)
            events.schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', team1)
            events.schedule_event(event_queue, current_time + random.expovariate(1/10), 'attempt_goal', team2)

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

# Tracks failed shot attempts and whether the shot was blocked or saved.
def failed_shot_event(team1, team2, event, event_queue):

    # Converts shot time from seconds to minutes:seconds.
    shot_time_seconds = event.time
    shot_time_minutes = int(shot_time_seconds // 60)
    shot_time_remaining_seconds = int(shot_time_seconds % 60)

    print(f"Shot on goal by team {team1.name} at {shot_time_minutes} minutes and {shot_time_remaining_seconds} seconds")
    if random.random() < 0.5:
        events.schedule_event(event_queue, event.time + 1, 'block_shot', team2)
    else:
        events.schedule_event(event_queue, event.time + 1, 'save_shot', team2)

# Tracks faceoffs and prints which team won it and when.
#call (handle_faceoff)
"""