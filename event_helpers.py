def failed_shot_event(team1, team2, event, event_queue):
    print(f"Shot on goal by team {team1.name} at {event.time} minutes")
    if random.random() < 0.5:
        schedule_event(event_queue, event.time + 1, 'block_shot', team2)
    else:
        schedule_event(event_queue, event.time + 1, 'save_shot', team2)


def handle_faceoff(team1, team2, event, event_queue):
    