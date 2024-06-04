class Skater:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Goalie:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Team:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.skaters = []
        self.goalies = []

    def add_skater(self, skater):
        self.skaters.append(skater)

    def add_goalie(self, goalie):
        self.goalies.append(goalie)
