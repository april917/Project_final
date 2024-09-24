import joblib
from app1.models import Employee  # Import the Employee model

def load_model():
    model = joblib.load('workforce_optimization_model4.pkl')
    model = joblib.load('scaler4.pkl')
    model = joblib.load('features3.pkl')
    return model

def allocate_resources(project):
    model = load_model()

    input_data = {
        'project_timeline': project.timeline,
        'required_hours': project.required_hours,
        # Add more features as required
    }

    # Convert input_data to the format your model expects
    prediction = model.predict([list(input_data.values())])

    employees = Employee.objects.filter(availability__gte=prediction).order_by('number_of_projects')

    return employees
