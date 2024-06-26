import pandas as pd
import glob
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# Load and combine data from skaters_2008.csv to skaters_2023.csv
file_paths = glob.glob('data/skaters_20*.csv')
data_combined = pd.concat([pd.read_csv(file) for file in file_paths])

# Define the feature columns and target column
features = [
    'I_F_savedShotsOnGoal', 'I_F_savedUnblockedShotAttempts', 'I_F_shotsOnGoal',
    'I_F_shotAttempts', 'penalties',
    'I_F_hits', 'I_F_lowDangerShots', 'I_F_xGoals',
    'I_F_mediumDangerShots', 'I_F_highDangerShots', 'I_F_lowDangerxGoals',
    'I_F_mediumDangerxGoals', 'I_F_highDangerxGoals'
]
target = 'I_F_goals'

# Split the combined data into training and testing sets
X_combined = data_combined[features]
y_combined = data_combined[target]
X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)

# Train the Gradient Boosting Regressor model
gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gbm.fit(X_train, y_train)

# Make predictions on the test set to evaluate the model
y_pred_test = gbm.predict(X_test)
mse_test = mean_squared_error(y_test, y_pred_test)
print(f"Mean Squared Error on combined test set: {mse_test}")

# Load the 2024 data
data_2024 = pd.read_csv('data/skaters_2024.csv')

# Ensure the 2024 data has the same features
X_2024 = data_2024[features]
y_2024 = data_2024[target]

# Make predictions on the 2024 data
y_pred_2024 = gbm.predict(X_2024)

# Evaluate the model on the 2024 data
mse_2024 = mean_squared_error(y_2024, y_pred_2024)
print(f"Mean Squared Error on 2024 data: {mse_2024}")

# Add the predictions to the 2024 data
data_2024['Predicted_Goals'] = y_pred_2024

# Sort the players by predicted goals
top_scorers = data_2024[['name', 'Predicted_Goals']].sort_values(by='Predicted_Goals', ascending=False).head(10)

# Print the top ten predicted goal scorers
print("Top Ten Predicted Goal Scorers for 2024:")
print(top_scorers)

# Optionally, display feature importances
importances = gbm.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': features, 'Importance': importances})
print(feature_importance_df.sort_values(by='Importance', ascending=False))