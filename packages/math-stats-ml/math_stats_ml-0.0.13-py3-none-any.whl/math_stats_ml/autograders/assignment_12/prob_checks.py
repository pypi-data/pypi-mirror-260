import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB

### PROBLEM 1 ###

url = 'https://raw.githubusercontent.com/jmyers7/stats-book-materials/main/data/data-12-1.csv'
df = pd.read_csv(url)

X = df['x'].to_numpy().reshape(-1, 1)
y = df['y'].to_numpy()
m = len(X)

pf = PolynomialFeatures(degree=19, include_bias=False)
lr = LinearRegression()
model19 = Pipeline([('preprocessor', pf), ('linear regressor', lr)])

model19.fit(X, y)
beta0_19, beta_19 = model19['linear regressor'].intercept_, model19['linear regressor'].coef_
y_hat = model19.predict(X)

def prob_1_check(beta0_19_ans, beta_19_ans, y_hat_ans):
    if isinstance(beta0_19_ans, float):
        if beta0_19_ans == beta0_19:
            print("\033[92mYour `beta0_19` is correct!")
        else:
            print("\033[91mYour `beta0_19` is incorrect!")
    else:
        print("\033[91mYour `beta0_19` should be a floating point number (i.e., a decimal).")
    
    if isinstance(beta_19_ans, np.ndarray):
        if np.array_equal(beta_19_ans, beta_19):
            print("\033[92mYour `beta_19` is correct!")
        else:
            print("\033[91mYour `beta_19` is incorrect!")
    else:
        print(f"\033[91mYour `beta_19` should be a NumPy array of shape {beta_19.shape}.")

    if isinstance(y_hat_ans, np.ndarray):
        if np.array_equal(y_hat_ans, y_hat):
            print("\033[92mYour `y_hat` is correct!")
        else:
            print("\033[91mYour `y_hat` is incorrect!")
    else:
        print(f"\033[91mYour `y_hat` should be a NumPy array of shape {y_hat.shape}.")








### PROBLEM 3 ###

mse = mean_squared_error(y, y_hat)

def prob_3_check(mse_ans):
    if isinstance(mse_ans, float):
        if mse_ans == mse:
            print("\033[92mYour `mse` is correct!")
        else:
            print("\033[91mYour `mse` is incorrect!")
    else:
        print("\033[91mYour `mse` should be a floating point number (i.e., a decimal).")





### PROBLEM 4 ###
        
cv_mse19 = -cross_val_score(model19, X, y, scoring='neg_mean_squared_error', cv=4)

model1 = LinearRegression()
model1.fit(X, y)
cv_mse1 = -cross_val_score(model1, X, y, scoring='neg_mean_squared_error', cv=4)

def prob_4_check(cv_mse19_ans, cv_mse1_ans):
    if isinstance(cv_mse19_ans, np.ndarray):
        if np.array_equal(cv_mse19_ans, cv_mse19):
            print("\033[92mYour `cv_mse19` is correct!")
        else:
            print("\033[91mYour `cv_mse19` is incorrect!")
    else:
        print(f"\033[91mYour `cv_mse19` should be a NumPy array of shape {cv_mse19.shape}.")
    
    if isinstance(cv_mse1_ans, np.ndarray):
        if np.array_equal(cv_mse1_ans, cv_mse1):
            print("\033[92mYour `cv_mse1` is correct!")
        else:
            print("\033[91mYour `cv_mse1` is incorrect!")
    else:
        print(f"\033[91mYour `cv_mse1` should be a NumPy array of shape {cv_mse1.shape}.")






### PROBLEM 6 ###

url = 'https://raw.githubusercontent.com/jmyers7/stats-book-materials/main/data/data-12-3.csv'
df = pd.read_csv(url)
X = df[['x1', 'x2', 'x3', 'x4', 'x5', 'x6']].to_numpy()
y = df['y'].to_numpy()

model = BernoulliNB()
cv_accuracy = cross_val_score(model, X, y, scoring='accuracy', cv=6)

def prob_6_check(cv_accuracy_ans, accuracy_mean_ans):
    if isinstance(cv_accuracy_ans, np.ndarray):
        if np.array_equal(cv_accuracy_ans, cv_accuracy):
            print("\033[92mYour `cv_accuracy` is correct!")
        else:
            print("\033[91mYour `cv_accuracy` is incorrect!")
    else:
        print(f"\033[91mYour `cv_accuracy` should be a NumPy array of shape {cv_accuracy.shape}.")
    
    if isinstance(accuracy_mean_ans, float):
        if accuracy_mean_ans == cv_accuracy.mean():
            print("\033[92mYour `accuracy_mean` is correct!")
        else:
            print("\033[91mYour `accuracy_mean` is incorrect!")
    else:
        print("\033[91mYour `accuracy_mean` should be a floating point number (i.e., a decimal).")