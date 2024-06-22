import pandas as pd
# import datetime
from random import randint
from time import sleep
import os
# from urllib.request import urllib
# import urllib2


url = "https://www.hockey-reference.com/leagues/NHL_2023_games.html"
dfs = pd.read_html(url)
df = dfs[0]

dates = pd.to_datetime(df["Date"], format = "%Y-%m-%d").dt.date
dates = pd.Series(dates).drop_duplicates().to_list()

# today = pd.Timestamp("today").floor("D")
end_date = dates[-1]
output_path = "nhl_data.csv"


for date in (dates):
    nhl_url = f"https://www.naturalstattrick.com/teamtable.php?fromseason=20222023&thruseason=20222023&stype=2&sit=ev&score=all&rate=y&team=all&loc=B&gpf=410&fd={date}&td={date}"

    if(date <= end_date):
        nhl_dfs = pd.read_html(nhl_url, index_col = 0)
        nhl_df = nhl_dfs[0]

        nhl_df["Date"] = date
        nhl_df.to_csv(output_path, mode = "a", header = not os.path.exists(output_path), index = False)
        # print("loop back")
        sleep(randint(15, 30))

print("Complete")