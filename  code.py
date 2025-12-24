import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,date, timedelta
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import  RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.stattools import pacf
from statsmodels.graphics.tsaplots import plot_pacf
from sklearn.pipeline import Pipeline

#Load Data
data = pd.read_csv("Nat_Gas.csv")
data["Dates"] = pd.to_datetime(data["Dates"])
#Preprocess
X_train, X_test, y_train, y_test = train_test_split(data["Dates"],data["Prices"], train_size= 0.8)
X_train, X_test = pd.DataFrame(X_train.map(lambda x: x.timestamp())), pd.DataFrame(X_test.map(lambda x: x.timestamp()))
#Detrend the data
lr = LinearRegression()
lr.fit(pd.DataFrame(X_train), pd.DataFrame(y_train))
lr_line_train, lr_line_test = lr.predict(pd.DataFrame(X_train)).flatten(), lr.predict(pd.DataFrame(X_test)).flatten()
detrend_y_train, detrend_y_test = y_train - lr_line_train,y_test - lr_line_test
#Deseasons the data
rf = RandomForestRegressor()
rf.fit(pd.DataFrame(X_train), detrend_y_train)
rf_predict_train,rf_predict_test = rf.predict(pd.DataFrame(X_train)), rf.predict(pd.DataFrame(X_test))
deseasoned_y_train, deseasoned_y_test = detrend_y_train - rf_predict_train, detrend_y_test - rf_predict_test
#Train and Test predictions
y_total_train_pred = lr_line_train +rf_predict_train
y_total_test_pred = lr_line_test +rf_predict_test

#Testing time:
future_dates = pd.DataFrame({
    "Dates": pd.date_range(start="2025-05-01", end="2025-05-15", freq="D")
}).map(lambda x: x.timestamp())
future_dates_predictions = lr.predict(future_dates).flatten() + + rf.predict(future_dates).flatten()
print(future_dates_predictions)