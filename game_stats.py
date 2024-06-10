class GameStats:
    def __init__(self, home_team_name="", away_team_name="", date="", location="", attendance=""):
        self.teams = {
            home_team_name: {
                "name": home_team_name,
                "goals": 0,
                "shots": 0,
                "saves": 0,
                "faceOffsWon": 0,
                "faceOffsLost": 0,
                "penaltyMinutes": 0,
                "powerPlays": 0,
                "powerPlayGoals": 0,
                "hits": 0,
                "blockedShots": 0,
            },
            away_team_name: {
                "name": away_team_name,
                "goals": 0,
                "shots": 0,
                "saves": 0,
                "faceOffsWon": 0,
                "faceOffsLost": 0,
                "penaltyMinutes": 0,
                "powerPlays": 0,
                "powerPlayGoals": 0,
                "hits": 0,
                "blockedShots": 0,
            }
        }
        self.game_details = {
            "date": "",
            "location": "",
            "attendance": 0,
            "duration": "",
        }
        self.players = {
            "home": [],
            "away": []
        }

    def __str__(self):
        return f"GameStats(teams={self.teams}, game_details={self.game_details}, players={self.players})"
