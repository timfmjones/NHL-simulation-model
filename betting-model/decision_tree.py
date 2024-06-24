"""
Create a decision tree model to predict stanley cup winners based on performance in regular season?
Would require csv file with regular season team stats and which team won the Stanley Cup each year.
"""
import pandas as pd
# df = pd.read_csv("all_teams.csv", encoding = "latin-1")
data = pd.read_csv("all_teams.csv")
data.head()
print(f"Dimensions of dataframe before filtering: {data.shape}")

# Filters dataframe to use only relevant rows and columns
used_columns = ["team", "season", "goalsFor", "goalsAgainst", "playoffGame", "situation"]
df = data[used_columns]
filtered_df = df[(df["season"] == 2018) & (df["situation"] == "all")]
print(f"Dimensions of dataframe after filtering: {filtered_df.shape}")

# Calculates goals for and goals against for each team during regular season
season_stats = filtered_df.groupby(["season", "team"]).agg({"goalsFor" : "sum", "goalsAgainst" : "sum"}).reset_index()
#print(season_stats.head())
print(f"Dimensions of dataframe after grouping by season and team: {season_stats.shape}")
#for(season_stats = filtered_df[filtered_df["season"] == 2008] & season_stats = filtered_df[filtered_df["playoffGame"] == 0]):


#print()

#-----------------------------------------------------------------------------------------------

# Defines features (inputs) and the target value (output).
#X = filtered_df.iloc[:, 0:4]
#y = filtered_df.iloc[:, 4]
#y = filtered_df["playoffGame"]
#X = filtered_df["encoded_team", "season", "goalsFor", "goalsAgainst"]


X = season_stats[["goalsFor", "goalsAgainst"]]
#y = season_stats[["playoffGame"]]
print(f"X sample size: , {X.shape}")#, /n, y sample size: , {y.shape}")

"""
# Converts team names from strings to number format so that they can be used as features
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
X.iloc[:, 0] = encoder.fit_transform(X.iloc[:, 0])
"""

"""
# Split data into 80/20 training and testing sets.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 17, test_size = 0.2)

#-----------------------------------------------------------------------------------------------
# Creates a decision tree classifier object and trains it using the training data.
# This decision tree classifier does not use any splitting criterion.  
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state = 17)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(y_pred)
# Evaluates accuracy
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
#print(f"Accuracy: {accuracy:.2f}")
"""

"""
# Uses Gini Index as the splitting criteria.
def train_using_gini(X_train, X_test, y_train):

    # Creating the classifier object
    clf_gini = DecisionTreeClassifier(criterion="gini", random_state = 17, max_depth = 3, min_samples_leaf = 5)

    # Performing training
    clf_gini.fit(X_train, y_train)
    return clf_gini

#-----------------------------------------------------------------------------------------------------------------------
"""

"""
# Uses Entropy as the splitting criteria.
def train_using_entropy(X_train, X_test, y_train):

    # Creating the classifier object
    clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 17, max_depth = 3, min_samples_leaf = 5)
    
    # Performing training
    clf_entropy.fit(X_train, y_train)
    return clf_entropy

# Creates a confusion matrix to analyze decision tree's ability to predict the data.
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

# Prints how much each feature influenced the decision tree's prediction.
features = pd.DataFrame(clf.feature_importances_, index = X.columns)
print(features.head())

"""