import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

def load_yearly_data(start_year, end_year):
    skaters_list = []
    goalies_list = []
    teams_list = []

    for year in range(start_year, end_year + 1):
        skaters_file = f'data/skaters_{year}.csv'
        goalies_file = f'data/goalies_{year}.csv'
        teams_file = f'data/teams_{year}.csv'

        skaters_df = pd.read_csv(skaters_file)
        goalies_df = pd.read_csv(goalies_file)
        teams_df = pd.read_csv(teams_file)

        skaters_list.append(skaters_df)
        goalies_list.append(goalies_df)
        teams_list.append(teams_df)

    skaters_data = pd.concat(skaters_list, ignore_index=True)
    goalies_data = pd.concat(goalies_list, ignore_index=True)
    teams_data = pd.concat(teams_list, ignore_index=True)

    return skaters_data, goalies_data, teams_data

def merge_data(skaters_data, goalies_data, teams_data):
    # Example merging logic, adjust as necessary based on the data structure
    # Assuming each player and team data has a unique identifier for merging
    # For simplicity, we'll assume all necessary features for training are in skaters_data
    # TODO fix the merge

    merged_data = skaters_data.merge(teams_data, on=['team', 'season'], suffixes=('_player', '_team'))
    # print(merged_data.columns)

    # should return merged data. return just team data for now 
    print(teams_data.columns)
    return teams_data

def train_and_save_model(historical_data, model_file):
    # Define features and target variable
    # features = [
    #     'games_played_player', 'icetime', 'shifts', 'gameScore',
    #     'onIce_xGoalsPercentage', 'offIce_xGoalsPercentage',
    #     'onIce_corsiPercentage', 'offIce_corsiPercentage',
    #     'onIce_fenwickPercentage', 'offIce_fenwickPercentage'
    #     # Add more features as necessary
    # ]

    # Test variables
    features = [ 'xGoalsPercentage', 'fenwickPercentage', 'corsiPercentage', 'xGoalsFor']
    target = 'goalsFor'

    # Split data into training and test sets
    X = historical_data[features]
    y = historical_data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train logistic regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

    # Save the trained model to a file
    joblib.dump(model, model_file)

if __name__ == "__main__":
    start_year = 2024
    end_year = 2024
    model_file = 'goal_prediction_model.pkl'

    skaters_data, goalies_data, teams_data = load_yearly_data(start_year, end_year)
    historical_data = merge_data(skaters_data, goalies_data, teams_data)
    train_and_save_model(historical_data, model_file)
