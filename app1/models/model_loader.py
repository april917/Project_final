import joblib
import os

# Define the path to the model and scaler
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../workforce_optimization_model3.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '../scaler3.pkl')
FEATURES_PATH = os.path.join(os.path.dirname(__file__), '../features3.pkl')

# Load the model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
features = joblib.load(FEATURES_PATH)


