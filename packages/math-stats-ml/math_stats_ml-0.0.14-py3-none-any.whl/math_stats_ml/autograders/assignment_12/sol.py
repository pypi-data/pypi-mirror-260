import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB

def print_type_error(solution):
    if isinstance(solution[0], np.float32) | isinstance(solution[0], np.float64):
        return f"\033[91mYour `{solution[1]}` should be a floating point number (i.e., decimal).\n"
    if isinstance(solution[0], np.ndarray):
        return f"\033[91mYour `{solution[1]} should be a NumPy array of shape {solution[0].shape}.\n"







### PROBLEM 1 ###

url = 'https://raw.githubusercontent.com/jmyers7/stats-book-materials/main/data/data-12-1.csv'
df = pd.read_csv(url)
X = df['x'].to_numpy().reshape(-1, 1)
y = df['y'].to_numpy()
pf = PolynomialFeatures(degree=19, include_bias=False)
lr = LinearRegression()
model19 = Pipeline([('preprocessor', pf), ('linear regressor', lr)])
model19.fit(X, y)
beta0_19, beta_19 = model19['linear regressor'].intercept_, model19['linear regressor'].coef_
y_hat = model19.predict(X)

### PROBLEM 3 ###

mse = mean_squared_error(y, y_hat)

### PROBLEM 4 ###

model1 = LinearRegression()
model1.fit(X, y)
cv_mse19 = -cross_val_score(model19, X, y, scoring='neg_mean_squared_error', cv=4)
cv_mse1 = -cross_val_score(model1, X, y, scoring='neg_mean_squared_error', cv=4)

### PROBLEM 6 ###

url = 'https://raw.githubusercontent.com/jmyers7/stats-book-materials/main/data/data-12-3.csv'
df = pd.read_csv(url)
X = df[['x1', 'x2', 'x3', 'x4', 'x5', 'x6']].to_numpy()
y = df['y'].to_numpy()
model = BernoulliNB()
cv_accuracy = cross_val_score(model, X, y, scoring='accuracy', cv=6)




class Solutions():
    def __init__(self):
        pass
    def get_solutions(self, prob_num):
        match prob_num:
            case 1:
                return [(beta0_19, 'beta0_19'), (beta_19, 'beta_19'), (y_hat, 'y_hat')]
            case 3:
                return [(mse, 'mse')]
            case 4:
                return [(cv_mse19, 'cv_mse19'), (cv_mse1, 'cv_mse1')]
            case 6:
                return [(cv_accuracy, 'cv_accuracy'), (cv_accuracy.mean(), 'accuracy_mean')]