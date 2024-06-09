import heapq
import random
import pandas as pd
import joblib
from data_loader import load_data

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
    print ("hello from event.py")
