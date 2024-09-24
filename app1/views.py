import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect, get_object_or_404
from plotly.offline import plot
import joblib
import numpy as np
from .forms import PredictionForm, AllocationForm, EmployeeSearchForm, CapacityReportForm, SkillBasedForm
#from .preprocessing import preprocess_features  # Assuming you have a preprocessing function
from .models.model_loader import model, scaler, features
from .models import Project, Employee, CapacityReport, AllocationAlert
from .allocation_logic import allocate_resources
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib import messages  # For flash messages
from django.urls import reverse   

# # Load your pre-trained model and scaler (ensure these paths are correct)
# model = joblib.load('workforce_optimization_model3.pkl')
# scaler = joblib.load('scaler3.pkl')

# # Define the features (ensure these match the model training features)
# features = ['Workload', 'PerformanceTrend', 'BurnRate', 'Overtime', 'PromotionLast5Years', 'Availability', 'YearsAtCompany']

#def preprocess_features(data):
#     preprocessing_pipeline = joblib.load('features3.pkl')
#     data_df = pd.DataFrame([data])
#     processed_data = preprocessing_pipeline.transform(data_df)
#     return processed_data

def home_view(request):
    return render(request, 'home.html')

# def dashboard_view(request):
#     data = pd.read_csv('employee_profile.csv')
    
#     data['Workload'] = data['NumberOfProject'] * data['AverageMonthlyHours']
#     data['PerformanceTrend'] = data['HistoricalPerformanceData'].apply(lambda x: [int(i) for i in x.split(', ')])
#     data['PerformanceTrend'] = data['PerformanceTrend'].apply(lambda x: pd.Series(x).diff().mean() if len(x) > 1 else 0)
#     data['Overtime'] = data['Overtime'].astype(int)
#     data['PromotionLast5Years'] = data['PromotionLast5Years'].astype(int)
#     data['Availability'] = data['Availability'].map({'Available': 1, 'Occupied': 0})
    
#     total_employees = len(data)
#     projects_completed = data['projects_completed'].sum() if 'projects_completed' in data.columns else 0
#     ongoing_projects = data['ongoing_projects'].sum() if 'ongoing_projects' in data.columns else 0
#     overworked_employees = len(data[data['Workload'] > data['Workload'].mean() + data['Workload'].std()])
    
#     fig_workload = px.histogram(data, x='Workload', nbins=20, title='Workload Distribution')
#     workload_plot = plot(fig_workload, output_type='div', include_plotlyjs=False)

#     fig_performance_trend = px.line(data, x='YearsAtCompany', y='PerformanceTrend', title='Employee Performance Trend Over Time')
#     performance_trend_plot = plot(fig_performance_trend, output_type='div', include_plotlyjs=False)
    
#     fig_employee_segmentation = px.scatter(data, x='Workload', y='PerformanceTrend',
#                                            color='WorkBalance', title='Employee Segmentation: Workload vs. Performance',
#                                            labels={'WorkBalance': 'Workload Balance'},
#                                            hover_data=['Roles', 'Skills'])
#     employee_segmentation_plot = plot(fig_employee_segmentation, output_type='div', include_plotlyjs=False)
    
#     features = ['Workload', 'PerformanceTrend', 'BurnRate', 'Overtime', 'PromotionLast5Years', 'Availability', 'YearsAtCompany']
#     X = data[features]
    
#     model = joblib.load('workforce_optimization_model4.pkl')
    
#     X_scaled = scaler.transform(X)
#     predictions = model.predict(X_scaled)
    
#     unique, counts = np.unique(predictions, return_counts=True)
#     workload_balance_distribution = dict(zip(unique, counts))
    
#     fig_predictive = px.pie(values=list(workload_balance_distribution.values()),
#                             names=['Underutilized', 'Balanced', 'Overworked'],
#                             title='Predicted Workload Balance Distribution')
#     predictive_plot = plot(fig_predictive, output_type='div', include_plotlyjs=False)

#     context = {
#         'total_employees': total_employees,
#         'projects_completed': projects_completed,
#         'ongoing_projects': ongoing_projects,
#         'overworked_employees': overworked_employees,
#         'workload_plot': workload_plot,
#         'performance_trend_plot': performance_trend_plot,
#         'employee_segmentation_plot': employee_segmentation_plot,
#         'predictive_plot': predictive_plot,
#     }

#     return render(request, 'dashboard.html', context)

def allocation(request):
    # Use the existing method to get all employees, but filter by availability
    employees = Employee.get_all_employees().filter(availability='Available').distinct()
    projects = Project.objects.all().distinct()
    search_results = None
    error_message = None

    if request.method == 'POST':
        search_by = request.POST.get('search_by')
        search_value = request.POST.get('search_value')

        if search_by == 'employee' and search_value:
            search_results = employees.filter(name__icontains=search_value).distinct()
        elif search_by == 'role' and search_value:
            search_results = employees.filter(roles__icontains=search_value).distinct()
        else:
            error_message = 'Please enter a valid search term.'

        if search_results and search_results.exists():
            return render(request, 'allocation.html', {
                'employees': employees,
                'search_results': search_results,
                'search_by': search_by,
                'total_employees': search_results.count(),  # Calculate the total number of results
            })
        else:
            error_message = 'No matching records found.'

    return render(request, 'allocation.html', {
        'employees': employees,  # Maintain the full list of available employees
        'search_results': search_results,
        'error_message': error_message,
        'total_employees': search_results.count() if search_results else 0,
    })


def assign_project(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = Project.objects.get(id=project_id)
        # Assign the project to the employee
        employee.ProjectAssignment = project
        employee.save()
        # Redirect to the allocation page or wherever you want
        return redirect(reverse('allocation'))

    projects = Project.objects.all().distinct()
    return render(request, 'assign_project.html', {
        'employee': employee,
        'projects': projects
    })

def search_employee(request):
    form = EmployeeSearchForm()
    employees = None

    if request.method == 'POST':
        form = EmployeeSearchForm(request.POST)
        if form.is_valid():
            employee_name = form.cleaned_data['employee_name']
            employees = Employee.objects.filter(name__icontains=employee_name.strip())
            if employees.exists():
                return render(request, 'search_employee.html', {'form': form, 'employees': employees})
            else:
                messages.info(request, f'No employees found matching "{employee_name}".')
                return render(request, 'search_employee.html', {'form': form})

    return render(request, 'search_employee.html', {'form': form})

def project_search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if the request is AJAX
        query = request.GET.get('term', '')
        projects = Project.objects.filter(name__icontains=query)
        results = [{'id': project.id, 'label': project.name, 'value': project.name} for project in projects]
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# User Story 2: Capacity Reporting and Analysis
def capacity(request):
    form = CapacityReportForm(request.GET)
    if form.is_valid():
        date_range = form.cleaned_data.get('date_range')
        reports = CapacityReport.objects.filter(date_range=date_range)
        return render(request, 'capacity.html', {'reports': reports})
    return render(request, 'capacity.html', {'form': form})

# User Story 3: Dynamic Capacity Management
def dynamic(request):
    if request.method == 'POST':
        # Implement logic to adjust capacity dynamically based on real-time data
        pass
    return render(request, 'dynamic.html')


# User Story 4: Skill-Based Resource Allocation

def skill(request):
    form = SkillBasedForm()
    context = {'form': form}

    if request.method == 'POST':
        form = SkillBasedForm(request.POST)
        if form.is_valid():
            # Retrieve the employee and project instances
            employee = form.cleaned_data['employee']
            project = form.cleaned_data['project']

            # Prepare the data dictionary for preprocessing
            data = {
                'Workload': employee.workload,
                'PerformanceTrend': employee.performance_trend,
                'BurnRate': employee.burnrate,
                'Overtime': employee.overtime,
                'PromotionLast5Years': employee.promotion_last_5_years,
                'Availability': employee.availability,
                'YearsAtCompany': employee.years_at_company
            }

            # # Process the data
            # processed_data = preprocess_features(data)

            # # Add the processed data to the context to pass to the template
            # context['processed_data'] = processed_data

        # Render the template with the form and processed data
        return render(request, 'skill.html', context)

    # If not a POST request, render the form with an empty context
    return render(request, 'skill.html', context)


# User Story 5: Predictive Over-Allocation Alerts

def predictive(request):
    prediction_label = None
    alerts = AllocationAlert.objects.filter(is_resolved=False)

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            try:
                # Collecting form data
                data_dict = {
                    'Workload': form.cleaned_data['workload'],
                    'PerformanceTrend': form.cleaned_data['performance_trend'],
                    'BurnRate': form.cleaned_data['burn_rate'],
                    'Overtime': form.cleaned_data['overtime'],
                    'PromotionLast5Years': form.cleaned_data['promotion_last_5_years'],
                    'Availability': form.cleaned_data['availability'],
                    'YearsAtCompany': form.cleaned_data['years_at_company']
                }

                # Create a DataFrame with the correct order of columns
                data_ordered = pd.DataFrame([data_dict], columns=features)

                # Scale the input data using the previously trained scaler
                data_scaled = scaler.transform(data_ordered)

                # Get the prediction from the model
                prediction = model.predict(data_scaled)[0]

                # Print the prediction to debug
                print(f"Prediction result: {prediction}")

                # Interpret the prediction result
                if prediction == 0:
                    prediction_label = "Underutilized"
                elif prediction == 1:
                    prediction_label = "Balanced Workload"
                elif prediction == 2:
                    prediction_label = "Overworked"

            except Exception as e:
                print(f"Error during prediction: {e}")
        else:
            print(form.errors)  # Print form validation errors if any
    else:
        form = PredictionForm()

    return render(request, 'predictive.html', {
        'form': form,
        'prediction_label': prediction_label,
        'alerts': alerts
    })



# User Story 6: Role-Based Capacity Planning
def planning(request):
    if request.method == 'POST':
        # Implement logic for role-based capacity planning
        pass
    return render(request, 'planning.html')