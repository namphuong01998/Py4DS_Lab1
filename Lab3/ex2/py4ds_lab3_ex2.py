# -*- coding: utf-8 -*-
"""Py4DS_Lab3_ex2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kz7FolpTjk14wxlUEGV8wNMNhulqz60N
"""


import numpy as np
import pandas as pd

df = pd.read_csv('AB_NYC_2019.csv')
df

from sklearn.preprocessing import LabelEncoder
df = df.drop(['id','host_name','name','last_review'], axis = 1)

for name_col in df.columns:
  if (isinstance(df[name_col][0],str)):
    df[name_col] = LabelEncoder().fit_transform(df[name_col])
df['host_id'] = LabelEncoder().fit_transform(df['host_id'])
df['reviews_per_month']=df['reviews_per_month'].fillna(0)
df.drop_duplicates()
df.reset_index()
X = df.drop(['price'],axis=1)
Y = df['price']
X

for i in range(0,df.shape[1]):
  print(df.iloc[:,i].describe())
  print("*"*30)

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3)

"""Scaling X with StandardScaler"""

scaler = preprocessing.StandardScaler()
X_train_ss = scaler.fit_transform(X_train)
X_test_ss = scaler.transform(X_test)

"""Scaling X with MinMaxScaler"""

scaler = preprocessing.MinMaxScaler()
X_train_mms = scaler.fit_transform(X_train)
X_test_mms = scaler.transform(X_test)

"""Scaling X with MaxAbsScaler"""

scaler = preprocessing.MaxAbsScaler()
X_train_mas = scaler.fit_transform(X_train)
X_test_mas = scaler.transform(X_test)

"""Scaling X with RobustScaler"""

scaler = preprocessing.RobustScaler()
X_train_rs = scaler.fit_transform(X_train)
X_test_rs = scaler.transform(X_test)

"""Scaling X with PCA"""

from sklearn.decomposition import PCA
scaler = PCA(n_components = "mle", svd_solver = "full")
X_train_pca = scaler.fit_transform(X_train)
X_test_pca = scaler.transform(X_test)

"""Mapping X with Uniform distribution"""

transformer = preprocessing.QuantileTransformer()
X_train_u = transformer.fit_transform(X_train)
X_test_u = transformer.transform(X_test)

"""Mapping X with Normalize distribution"""

transformer = preprocessing.Normalizer(norm = 'l2')
X_train_n = transformer.transform(X_train)
X_test_n = transformer.transform(X_test)

"""Encoder X with KBin Discretization"""

encoder = preprocessing.KBinsDiscretizer(n_bins = 10, strategy = 'uniform')
X_train_kbin = encoder.fit_transform(X_train)
X_test_kbin = encoder.transform(X_test)

"""Function to Regression"""

def SVRmse(X_train,X_test,Y_train,Y_test):
  import time
  from sklearn import svm
  from sklearn.metrics import mean_squared_error
  start = time.time()
  clf = svm.SVR()
  clf.fit(X_train,Y_train)
  Y_predict = clf.predict(X_test)
  mse = mean_squared_error(Y_test,Y_predict)
  end = time.time()
  print("MSE for Support Vector Regression: {:.4f}".format(mse))
  print("Time estimated: ",end-start)
  return mse

def DTRmse(X_train, X_test,Y_train,Y_test):
  import time
  from sklearn import tree
  from sklearn.metrics import mean_squared_error
  start = time.time()
  clf = tree.DecisionTreeRegressor()
  clf.fit(X_train,Y_train)
  Y_predict = clf.predict(X_test)
  mse = mean_squared_error(Y_test,Y_predict)
  end = time.time()
  print("MSE for Decision Tree Regression: {:.4f}".format(mse))
  print("Time estimatimated: ",end-start)
  return mse

def RFRmse(X_train,X_test,Y_train,Y_test):
  import time
  from sklearn.ensemble import RandomForestRegressor
  from sklearn.metrics import mean_squared_error
  start = time.time()
  clf = RandomForestRegressor()
  clf.fit(X_train,Y_train)
  Y_predict = clf.predict(X_test)
  #res = pd.DataFrame({"pred":np.round(Y_predict.ravel()), "test":Y_test})
  #res.to_csv("/content/drive/My Drive/Datasets/Py4DS_Lab3/RFR.csv",index = 'false',header = 'true')
  mse = mean_squared_error(Y_test,Y_predict)
  end = time.time()
  print("MSE for Random Forest Regression: {:.4f}".format(mse))
  print("Time estimated: ",end-start)
  return mse

def GBRmse(X_train,X_test,Y_train,Y_test):
  import time
  from sklearn.ensemble import GradientBoostingRegressor
  from sklearn.metrics import mean_squared_error
  start = time.time()
  clf = GradientBoostingRegressor(random_state=0)
  clf.fit(X_train,Y_train)
  Y_predict = clf.predict(X_test)
  #res = pd.DataFrame({"pred":np.round(Y_predict.ravel()), "test":Y_test})
  #res.to_csv("/content/drive/My Drive/Datasets/Py4DS_Lab3/GBR.csv",index = 'false',header = 'true')
  mse = mean_squared_error(Y_test,Y_predict)
  end = time.time()
  print("MSE for Gradient Boosting Regressor: {:.4f}".format(mse))
  print("Time estimated: ",end-start)
  return mse

def Regression(X_train,X_test,Y_train,Y_test):
  svr = SVRmse(X_train,X_test,Y_train,Y_test)
  dtr = DTRmse(X_train,X_test,Y_train,Y_test)
  rfr = RFRmse(X_train,X_test,Y_train,Y_test)
  gbr = GBRmse(X_train,X_test,Y_train,Y_test)
  print("*"*50)
  return np.array([svr,dtr,rfr,gbr])

def Compare(NoneProcessing, Processing):
  for i in range(len(NoneProcessing)):
    state = ""
    if (NoneProcessing[i]>Processing[i]):
      state = "Good"
    else:
      state = "Bad"
    switcher = {
        0: "Support Vector Regression",
        1: "Decision Tree Regression",
        2: "Random Forest Regression",
        3: "Gradient Boosting Regression"
    }
    print(state + " " + switcher.get(i))
  print("*"*50)
  print("*"*50)

"""Compare before and after preprocessing"""

print("Regression without preprocessing: ")
scores_before = Regression(X_train,X_test,Y_train,Y_test)

print("Regression with StandardScaler: ")
scores_after = Regression(X_train_ss,X_test_ss,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with MinMaxScaler: ")
scores_after = Regression(X_train_mms,X_test_mms,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with MaxAbsScaler: ")
scores_after = Regression(X_train_mas,X_test_mas,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with RobustScaler: ")
scores_after = Regression(X_train_rs,X_test_rs,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with PCA")
scores_after = Regression(X_train_pca,X_test_pca,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with Uniform distribution")
scores_after = Regression(X_train_u,X_test_u,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with Nomalize distribution")
scores_after = Regression(X_train_n,X_test_n,Y_train,Y_test)
Compare(scores_before,scores_after)

print("Regression with KBinDiscrete")
scores_after = Regression(X_train_kbin,X_test_kbin,Y_train,Y_test)
Compare(scores_before,scores_after)

#scaler = preprocessing.StandardScaler()
#X_ss = scaler.fit_transform(X)
#rfr = RFRmse(X_train_ss,X_ss,Y_train,Y)

#scaler = preprocessing.MinMaxScaler()
#X_mms = scaler.fit_transform(X)
#gbr = GBRmse(X_train_mms,X_mms,Y_train,Y)
