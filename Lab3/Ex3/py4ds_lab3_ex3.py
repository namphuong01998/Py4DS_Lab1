# -*- coding: utf-8 -*-
"""Py4DS_Lab3_Ex3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZL42c3TzB0AwJW_iCg3a_0HWvHVE5p7C

Exercise 3 sẽ chia làm 2 bài:
- Ex3 (chưa qua bước pre-processing data) và 
- Ex3 (đã qua bước pre-processing data).

So sánh accuracy.

---
##EXERCISE 3: Not pre-processing data (ignore STEP 1 in Part B)

#**A. Read and view dataset**
"""

import numpy as np
import pandas as pd

df = pd.read_csv(r'./FIFA2018Statistics.csv')
df.head()

"""#**B. Processing data**"""

df.info()

"""#**STEP 1: Pre-processing data** ==> Ignore

#**STEP 2: EDA** (Explotary Data Analysis)

##**0.Summary-statistic**
"""

df.describe()

"""##**1. Biểu đồ cột - histogram.**  (Feature: 'Fouls Committed')"""

df['Fouls Committed'].hist(bins = 10)

"""**Comomments:**

Trục tung y_axis đếm số dữ liệu rơi vào cột nào đó (chính là 1 khoảng của trục hoành x_axis).


Trong 128 đội có:
- 24 đội: phạm lỗi khoảng [13,15] lần ==> Đây là vùng số lỗi có nhiều quốc gia phạm phải nhất.  Chiếm khoảng 19%
- 3 đội: phạm lỗi khoảng [21,13] lần

##**2. Box-plot.  Biểu đồ hình hộp**  (Feature: 'Yellow Card')
"""

df['Yellow Card'].plot(kind = 'box', figsize = (4, 8));
print(df['Yellow Card'].describe())

"""**Comments:**

Feature 'Yellow Card' has outliers

##**3. Heat-map. Biểu đồ nhiệt.**
"""

import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12, 12))
corr = df.corr()
sns.heatmap(corr, cmap='coolwarm_r', annot_kws={'size':20}, ax=ax)
ax.set_title("Correlation Matrix", fontsize=14);

"""#**C. Train-Test**

**Xử lý các dữ liệu category**
"""

cleaned_data  = pd.get_dummies(df)
cleaned_data.shape

"""**Chuyển hóa Encoder**"""

from sklearn.preprocessing import LabelEncoder
df = df.apply(LabelEncoder().fit_transform)
df.head()

"""##**1. Tách dữ liệu**"""

X = df.drop(['Man of the Match'], axis = 1)
y = df['Man of the Match']

"""##**2. Train - Test**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

"""#**D. Choose model**

##**1. Model: Support Vector Machine (SVM)**
"""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf_svm = SVC(kernel = 'poly', C = 10)   
clf_svm.fit(X_train, y_train)

print("Support Vector Machine")
print("\ntrain accuracy: ", accuracy_score(y_train, clf_svm.predict(X_train)))
print("test accuracy: ", accuracy_score(y_test, clf_svm.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf_svm.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf_svm.predict(X_test), digits = 5))

"""##**2. Model: Decision Tree Classifier**"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)

print("Decision Tree Classifier")
print("\ntrain accuracy: ", accuracy_score(y_train, clf.predict(X_train)))
print("test acccuracy: ", accuracy_score(y_test, clf.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf.predict(X_test), digits = 5))

"""##**3. Model: Random Forest Classifier**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf = RandomForestClassifier()
clf.fit(X_train,y_train)

print("Random Forest Classifier")
print("\ntrain acc: ", accuracy_score(y_train, clf.predict(X_train)))
print("test acc: ", accuracy_score(y_test, clf.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf.predict(X_test), digits = 5))

"""##**4. Model: Logistic Regression**"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf = LogisticRegression(max_iter = len(y_train))
clf.fit(X_train,y_train)

print("Logistic Regression")
print("\ntrain acc: ", accuracy_score(y_train, clf.predict(X_train)))
print("test acc: ", accuracy_score(y_test, clf.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf.predict(X_test), digits = 5))

"""---
#EXERCISE 3: Having pre-processing data

#**A. Read and view dataset**
"""

import numpy as np
import pandas as pd

df = pd.read_csv(r'./FIFA2018Statistics.csv')
df.head()

"""#**B. Processing data**

##**STEP 1: Pre-processing data**

##**1. Kiểm tra data cơ bản  &  Remove missing values** (Loại bỏ các giá trị khuyết)
"""

df.info()

"""##**2. Drop Duplicates**  (Loại bỏ các giá trị trùng)"""

N = len(df)  # Count the number of rows in data
print(N)     

df.drop_duplicates(inplace = True) # df after dropping duplicates
print("The new dimension after checking duplicate & removing is:\t (%s, %s)"%(df.shape)) #size of data (rows,columns)
print('There are %s observations is duplicated, take %s percentage on total dataset'%(N - len(df), 
                                                                                      round(100*(N - len(df))/N, 2)))

"""**Comments:**

Có thể thấy, ban đầu có 128 dữ liệu, sau bước Dropping Duplicates còn  128 dữ liệu. Tức không có dữ liệu trùng

##**3. Remove outliers** (Loại bỏ các giá trị ngoại lai))
"""

### Tìm IQR của dữ liệu
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
## Loại bỏ outlier
outlier_condition = (df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))
df = df[~outlier_condition]
df.shape

"""**Comments:**
  - After dropping duplicates, the size of data: (128,27).
  
  i.e 128 rows, 27 columns
  - After removing outliers, the size of data is (128,27). 

  i.e data không thay đổi  ==>  Data không có outliers

##**4. Drop column according to NAN percentage for dataframe**
"""

df=df = df.loc[:, df.isnull().mean() < .8] # remove all columns has values which be NAN accounting for >= 80%

df.shape

"""#**STEP 2: EDA** (Explotary Data Analysis)

##**0.Summary-statistic**
"""

df.describe()

"""##**1. Biểu đồ cột - histogram.**  (Feature: 'Fouls Committed')"""

df['Fouls Committed'].hist(bins = 10)

"""##**2. Box-plot.  Biểu đồ hình hộp**  (Feature: 'Yellow Card')"""


"""**Comment**
After removing outliers (Section 3 in STEP 1), data has NO outliers.

##**3. Heat-map. Biểu đồ nhiệt.**
"""

import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (12, 12))
corr = df.corr()
sns.heatmap(corr, cmap='coolwarm_r', annot_kws={'size':20}, ax=ax)
ax.set_title("Correlation Matrix", fontsize=14);

"""#**C. Train-Test**"""

cleaned_data  = pd.get_dummies(df)
cleaned_data.shape

from sklearn.preprocessing import LabelEncoder
df = df.apply(LabelEncoder().fit_transform)
df.head()

"""##**1. Tách dữ liệu**"""

X = df.drop(['Man of the Match'], axis = 1)
y = df['Man of the Match']

"""##**2. Train - Test**"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

"""#**D. Choose model**

##**1. Model: Support Vector Machine (SVM)**
"""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf_svm = SVC(kernel = 'poly', C = 10)   
clf_svm.fit(X_train, y_train)

print("Support Vector Machine")
print("\ntrain accuracy: ", accuracy_score(y_train, clf_svm.predict(X_train)))
print("test accuracy: ", accuracy_score(y_test, clf_svm.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf_svm.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf_svm.predict(X_test), digits = 5))

"""##**2. Model: Decision Tree Classifier**"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)

print("Decision Tree Classifier")
print("\ntrain accuracy: ", accuracy_score(y_train, clf.predict(X_train)))
print("test acccuracy: ", accuracy_score(y_test, clf.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf.predict(X_test), digits = 5))

"""##**3. Model: Random Forest Classifier**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf = RandomForestClassifier()
clf.fit(X_train,y_train)

print("Random Forest Classifier")
print("\ntrain acc: ", accuracy_score(y_train, clf.predict(X_train)))
print("test acc: ", accuracy_score(y_test, clf.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf.predict(X_test), digits = 5))

"""##**4. Model: Logistic Regression**"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report

clf = LogisticRegression(max_iter = len(y_train))
clf.fit(X_train,y_train)

print("Logistic Regression")
print("\ntrain acc: ", accuracy_score(y_train, clf.predict(X_train)))
print("test acc: ", accuracy_score(y_test, clf.predict(X_test)))
print('\nConfusion matrix : \n', confusion_matrix(y_test, clf.predict(X_test)))
print('Classification report : \n', classification_report(y_test, clf.predict(X_test), digits = 5))