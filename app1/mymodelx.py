import pandas as pd 
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from xgboost import XGBClassifier
import joblib
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('employee_profile.csv')  # Adjust the path if needed

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

# Additional Feature Engineering
df['Workload_PerExperience'] = df['Workload'] / (df['YearsAtCompany'] + 1)  # Avoid division by zero
df['Performance_Workload_Ratio'] = df['PerformanceTrend'] / (df['Workload'] + 1)

# Top Features based on importance analysis
top_features = ['Workload', 'Workload_PerExperience', 'Performance_Workload_Ratio']

# Features and target
X_top = df[top_features]
y = df['WorkBalance'].map({0: 0, 1: 1, -1: 2})

# Train/test split
X_train_top, X_test_top, y_train, y_test = train_test_split(X_top, y, test_size=0.3, random_state=42)

# Imputation and scaling
imputer_numerical = SimpleImputer(strategy='mean')
scaler = StandardScaler()

# Preprocessing for numerical features
X_train_top = imputer_numerical.fit_transform(X_train_top)
X_test_top = imputer_numerical.transform(X_test_top)
X_train_top = scaler.fit_transform(X_train_top)
X_test_top = scaler.transform(X_test_top)

# Applying SMOTE to oversample minority classes
smote = SMOTE(random_state=42)
X_train_top_resampled, y_train_resampled = smote.fit_resample(X_train_top, y_train)

# Define individual models
rf_model = RandomForestClassifier(random_state=42, class_weight='balanced')
xgb_model = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss')
gb_model = GradientBoostingClassifier(random_state=42)

# Combine models into a Voting Classifier
voting_clf = VotingClassifier(estimators=[
    ('rf', rf_model),
    ('xgb', xgb_model),
    ('gb', gb_model)
], voting='soft')  # Use soft voting to consider class probabilities

# Train Voting Classifier
voting_clf.fit(X_train_top_resampled, y_train_resampled)

# Evaluate Voting Classifier
y_pred_voting = voting_clf.predict(X_test_top)
voting_accuracy = accuracy_score(y_test, y_pred_voting)
voting_report = classification_report(y_test, y_pred_voting)

# Display evaluation results for Voting Classifier
print(f"Voting Classifier Model Accuracy: {voting_accuracy}")
print(f"Voting Classifier Model Classification Report:\n{voting_report}")

# Confusion Matrix for Voting Classifier Model
voting_conf_matrix = confusion_matrix(y_test, y_pred_voting)
plt.figure(figsize=(8, 6))
sns.heatmap(voting_conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Underutilized', 'Balanced', 'Overworked'], yticklabels=['Underutilized', 'Balanced', 'Overworked'])
plt.title('Confusion Matrix for Voting Classifier Model')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Cross-Validation for Voting Classifier Model
cv_scores_voting = cross_val_score(voting_clf, X_train_top_resampled, y_train_resampled, cv=5, scoring='accuracy')
print(f'Cross-Validation Accuracy Scores for Voting Classifier Model: {cv_scores_voting}')
print(f'Mean Cross-Validation Accuracy for Voting Classifier Model: {cv_scores_voting.mean()}')

# Save the Voting Classifier model for future use
joblib.dump(voting_clf, 'workforce_optimization_voting_clf_model.pkl')
joblib.dump(scaler, 'scaler_voting.pkl')
joblib.dump(top_features, 'features_voting.pkl')  # Save the updated feature names
