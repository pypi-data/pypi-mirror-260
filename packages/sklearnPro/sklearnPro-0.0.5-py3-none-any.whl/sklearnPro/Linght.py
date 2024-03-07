import os  

def main():
    sklearn_txt='''
import pandas as pd
import numpy as np

data = pd.read_csv("wine.csv")
data.sample(5)
data.info()
data.hist(grid=False,figsize=(16,9),bins=20)

from sklearn import preprocessing
data_scale = preprocessing.scale(data["Ash"])
data["Ash"] =  data_scale
data.sample(5)

#针对数值型数据如何判断是否异常  1.5*iqn，在这个方位之外的就是异常
# data.describe()
# iqr = 1.5*(5.5845 - 3.38565)
# count = len(data.loc[data["Width"]>iqr+5.5845])+len(data.loc[data["Width"]<iqr-3.38565])
# print(count)
data = data.drop(columns="Ash_scale")

from sklearn.model_selection import train_test_split

#下抽样数据
data_undersample = data.sample(n=80,replace=False)
# data_undersample.info()
x_undersample = data_undersample.iloc[:,:-1]
y_undersample = data_undersample.iloc[:,-1:]
# x_undersample.info()
# y_undersample.info()
x_under_train,x_under_test,y_under_train,y_under_test = train_test_split(x_undersample,y_undersample,test_size=0.2,random_state=47)

#过抽样数据
from imblearn.over_sampling import SMOTE
x = data.iloc[:,:-1]
y = data.iloc[:,-1:]
x_oversample,y_oversample = SMOTE().fit_resample(x,y)
x_over_train,x_over_test,y_over_train,y_over_test = train_test_split(x_oversample,y_oversample,test_size=0.2,random_state=47)

#正常采样
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=47)

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

#逻辑回归下抽样建模
logist_under = LogisticRegression()
logist_under.fit(x_under_train,y_under_train)
y_pred_under = logist_under.predict(x_under_test)
confusion_matrix(y_under_test,y_pred_under)

#逻辑回归过抽样建模
logist_over = LogisticRegression()
logist_over.fit(x_over_train,y_over_train)
y_pred_over = logist_over.predict(x_over_test)
confusion_matrix(y_over_test,y_pred_over)

#逻辑回归正常抽样建模
logist = LogisticRegression()
logist.fit(x_train,y_train)
y_pred = logist.predict(x_test)
confusion_matrix(y_test,y_pred)

from sklearn.metrics import recall_score

#计算召回率
recall_over=recall_score(y_over_test,y_pred_over,average="weighted")
print("过抽样召回率：",recall_over)
recall=recall_score(y_test,y_pred,average="weighted")
print("正常抽样召回率：",recall)
recall_under=recall_score(y_under_test,y_pred_under,average="weighted")
print("下抽样召回率：",recall_under)
'''
    print(sklearn_txt)
