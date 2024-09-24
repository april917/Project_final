import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
import joblib

# Load the dataset
df = pd.read_csv('employee_profile.csv')

# Feature Engineering
df['Workload'] = df['NumberOfProject'] * df['AverageMonthlyHours']
df['PerformanceTrend'] = df['HistoricalPerformanceData'].apply(lambda x: [int(i) for i in x.split(', ')])
df['PerformanceTrend'] = df['PerformanceTrend'].apply(lambda x: pd.Series(x).diff().mean() if len(x) > 1 else 0)
df['Overtime'] = df['Overtime'].astype(int)
df['PromotionLast5Years'] = df['PromotionLast5Years'].astype(int)
df['Availability'] = df['Availability'].map({'Available': 1, 'Occupied': 0})

# Handle Missing Values in 'Availability'
df['Availability'].fillna(1, inplace=True)  # Assuming '1' means 'Available'

# Define target variable
workload_mean = df['Workload'].mean()
workload_std = df['Workload'].std()

def categorize_work_balance(workload):
    if workload < workload_mean - workload_std:
        return 0  # Underutilized
    elif workload > workload_mean + workload_std:
        return -1  # Overworked
    else:
        return 1  # Balanced

df['WorkBalance'] = df['Workload'].apply(categorize_work_balance)

# Features and target
features = ['Workload', 'PerformanceTrend', 'BurnRate', 'Overtime', 'PromotionLast5Years', 'Availability', 'YearsAtCompany']
numerical_features = ['Workload', 'PerformanceTrend', 'BurnRate','PromotionLast5Years', 'YearsAtCompany']  # Define numerical features
X = df[features]
y = df['WorkBalance'].map({0: 0, 1: 1, -1: 2})

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Imputation and scaling
imputer_numerical = SimpleImputer(strategy='mean')
X_train[numerical_features] = imputer_numerical.fit_transform(X_train[numerical_features])
X_test[numerical_features] = imputer_numerical.transform(X_test[numerical_features])

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model training
final_model_full = LogisticRegression(C=1, solver='liblinear', max_iter=5000, random_state=42)
final_model_full.fit(X_train, y_train)

# Model evaluation
y_pred_full = final_model_full.predict(X_test)
final_accuracy_full = accuracy_score(y_test, y_pred_full)
final_report_full = classification_report(y_test, y_pred_full)
print(f"Accuracy: {final_accuracy_full}")
print(f"Report:\n{final_report_full}")

# Save model and scaler
joblib.dump(final_model_full, 'workforce_optimization_model3.pkl')
joblib.dump(scaler, 'scaler3.pkl')
joblib.dump(features, 'features3.pkl')  # Save the feature names
