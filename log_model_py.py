# -*- coding: utf-8 -*-
"""Log_model.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10PdBIqZT3M-2oY3cXIZz8IktHO0g1uLt
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

train_data = pd.read_csv('Titanic_train.csv')
test_data = pd.read_csv('Titanic_test.csv')
train_data.head()

train_data.columns = train_data.columns.str.strip()
test_data.columns = test_data.columns.str.strip()

test_data.head()

train_data.info()

test_data.info()

# Display value counts for some categorical columns
print(train_data['Sex'].value_counts())
print(train_data['Embarked'].value_counts())
print(train_data['Pclass'].value_counts())

# Display descriptive statistics for numerical columns
print(train_data.describe())

# Visualizations
# Histogram of 'Age' and 'Fare'
train_data.hist(column=['Age', 'Fare'], bins=20, figsize=(10, 5))
plt.show()

# Box plot of 'Age' by 'Pclass'
sns.boxplot(x='Pclass', y='Age', data=train_data)
plt.show()

# Heatmap of correlations between numerical features
numerical_cols = train_data.select_dtypes(include=['int64', 'float64']).columns
sns.heatmap(train_data[numerical_cols].corr(), annot=True, cmap='coolwarm')
plt.show()

# Fill Missing Values
train_data['Age'] = train_data['Age'].fillna(train_data['Age'].median())
train_data['Embarked'] = train_data['Embarked'].fillna(train_data['Embarked'].mode()[0])
test_data['Age'] = test_data['Age'].fillna(test_data['Age'].median())
test_data['Fare'] = test_data['Fare'].fillna(test_data['Fare'].median())

# Convert categorical columns to dummy variables
train_data = pd.get_dummies(train_data, columns=['Sex', 'Embarked', 'Pclass'], drop_first=True)
test_data = pd.get_dummies(test_data, columns=['Sex', 'Embarked', 'Pclass'], drop_first=True)

# Ensure train and test data have the same columns
X_train, _ = train_data.align(test_data, join='left', axis=1, fill_value=0)

# Prepare features and target variable
X_train = X_train.drop(columns=['Survived', 'PassengerId', 'Name', 'Ticket', 'Cabin'])
y_train = train_data['Survived']
X_test = test_data.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])



# Scale numerical features
numerical_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
test_data[numerical_cols] = scaler.transform(test_data[numerical_cols])

# Fit the logistic regression model
log_reg = LogisticRegression(max_iter=200)
log_reg.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix

# Predict on the test data
y_pred = log_reg.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_train, log_reg.predict(X_train))
precision = precision_score(y_train, log_reg.predict(X_train))
recall = recall_score(y_train, log_reg.predict(X_train))
f1 = f1_score(y_train, log_reg.predict(X_train))
roc_auc = roc_auc_score(y_train, log_reg.predict(X_train))

print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1-Score: {f1}')
print(f'ROC-AUC Score: {roc_auc}')

conf_matrix = confusion_matrix(y_train, log_reg.predict(X_train))
print("Confusion Matrix:\n", conf_matrix)

fpr, tpr, thresholds = roc_curve(y_train, log_reg.predict_proba(X_train)[:, 1])
plt.plot(fpr, tpr, color='orange', label='ROC Curve')
plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

coefficients = pd.DataFrame(log_reg.coef_.T, index=X_train.columns, columns=['Coefficient'])
print(coefficients)

print(coefficients.sort_values(by='Coefficient', ascending=False))