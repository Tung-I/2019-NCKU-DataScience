import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd 
import random
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import fetch_mldata
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report, confusion_matrix

def preProcess(features):
	for i, d in enumerate(features):
		mini = min(d)
		maxi = max(d)-mini
		for ii, dd in enumerate(d):
			tmp = (dd-mini)/maxi
			if tmp==1:
				features[i][ii] = 0.99
			elif tmp==0:
				features[i][ii] = 0.01
			else:
				features[i][ii] = tmp

df = pd.read_csv('train.csv')
CreditScore = df['CreditScore'].tolist()
Geography = df['Geography'].tolist()
Gender = df['Gender'].tolist()
Age = df['Age'].tolist()
Tenure = df['Tenure'].tolist()
Balance = df['Balance'].tolist()
NumOfProducts = df['NumOfProducts'].tolist()
HasCrCard = df['HasCrCard'].tolist()
IsActiveMember = df['IsActiveMember'].tolist()
EstimatedSalary = df['EstimatedSalary'].tolist()
Exited = df['Exited'].tolist()

features = (CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
preProcess(features)        

for i, d in enumerate(Geography):
	if d=='S0':
		Geography[i] = 0.01
	elif d=='S1':
		Geography[i] = 0.5
	else:
			Geography[i] = 0.99
        
for i, d in enumerate(Gender):
	if d=='Male':
		Gender[i] = 0.99
	else:
		Gender[i] = 0.01

X = []
for _ind in range(len(Exited)):
	# X.append((CreditScore[_ind], Geography[_ind], Gender[_ind], Age[_ind], Tenure[_ind], Balance[_ind],\
	# 		NumOfProducts[_ind], HasCrCard[_ind], IsActiveMember[_ind], EstimatedSalary[_ind]))
	X.append((CreditScore[_ind], Tenure[_ind], Balance[_ind],\
	 		NumOfProducts[_ind], HasCrCard[_ind], IsActiveMember[_ind], EstimatedSalary[_ind]))
y = Exited.copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20) 

_solver = 'adam'
_activation = 'relu'
_alpha = 1e-4
_hidden_layer = (64, 64)
_lr_rate = 0.0001
_batch = 64


mlp = MLPClassifier(solver=_solver, activation=_activation, alpha=_alpha, hidden_layer_sizes=_hidden_layer,\
				batch_size=_batch, learning_rate_init=_lr_rate)
mlp.fit(X_train, y_train)
y_pred = mlp.predict(X_test)

print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred)) 



df_test = pd.read_csv('test.csv')
df_test.head()

CreditScore = df_test['CreditScore'].tolist()
Geography = df_test['Geography'].tolist()
Gender = df_test['Gender'].tolist()
Age = df_test['Age'].tolist()
Tenure = df_test['Tenure'].tolist()
Balance = df_test['Balance'].tolist()
NumOfProducts = df_test['NumOfProducts'].tolist()
HasCrCard = df_test['HasCrCard'].tolist()
IsActiveMember = df_test['IsActiveMember'].tolist()
EstimatedSalary = df_test['EstimatedSalary'].tolist()

features = (CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
preProcess(features)        
for i, d in enumerate(Geography):
    if d=='S0':
        Geography[i] = 0.01
    elif d=='S1':
        Geography[i] = 0.5
    else:
        Geography[i] = 0.99
        
for i, d in enumerate(Gender):
    if d=='Male':
        Gender[i] = 0.99
    else:
        Gender[i] = 0.01

X_test = []
for _ind in range(len(Age)):
    # X_test.append((CreditScore[_ind], Geography[_ind], Gender[_ind], Age[_ind], Tenure[_ind], Balance[_ind],\
    #                NumOfProducts[_ind], HasCrCard[_ind], IsActiveMember[_ind], EstimatedSalary[_ind]))
    X_test.append((CreditScore[_ind], Tenure[_ind], Balance[_ind],\
	 		NumOfProducts[_ind], HasCrCard[_ind], IsActiveMember[_ind], EstimatedSalary[_ind]))
y_pred = mlp.predict(X_test)

df_sample = pd.read_csv('sample_upload.csv')
df_sample['Exited'] = y_pred
df_sample.to_csv('to_upload.csv', index=False, sep=',')