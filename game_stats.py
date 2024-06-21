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
            "date": date,
            "location": location,
            "attendance": attendance,
            "duration": "",
        }
        self.players = {
            "home": [],
            "away": []
        }

    def __str__(self):
        return f"GameStats(teams={self.teams}, game_details={self.game_details}, players={self.players})"

    def print_game_stats(self):
        print("Game Details:")
        print(f"  Date: {self.game_details['date']}")
        print(f"  Location: {self.game_details['location']}")
        print(f"  Attendance: {self.game_details['attendance']}\n")

        for team in self.teams.values():
            print(f"Team: {team['name']}")
            print(f"  Goals: {team['goals']}")
            print(f"  Shots: {team['shots']}")
            print(f"  Saves: {team['saves']}")
            print(f"  Face-offs Won: {team['faceOffsWon']}")
            print(f"  Face-offs Lost: {team['faceOffsLost']}")
            print(f"  Penalty Minutes: {team['penaltyMinutes']}")
            print(f"  Power Plays: {team['powerPlays']}")
            print(f"  Power Play Goals: {team['powerPlayGoals']}")
            print(f"  Hits: {team['hits']}")
            print(f"  Blocked Shots: {team['blockedShots']}\n")
