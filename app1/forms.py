# app1/forms.py

from django import forms
from .models import Employee, Project, CapacityReport

class EmployeeSearchForm(forms.Form):
    employee_name = forms.CharField(
        label='Employee Name',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter employee name'
        })
    )

class AllocationForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label='Select Employee',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label='Select Project',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class SkillBasedForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label='Employee',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label='Project',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PredictionForm(forms.Form):
    workload = forms.FloatField(
        label='Workload',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.1',
            'placeholder': 'Enter workload value'
        })
    )
    performance_trend = forms.FloatField(
        label='Performance Trend',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '-10',
            'max': '10',
            'step': '0.1',
            'placeholder': 'Enter performance trend (-10 to 10)'
        })
    )
    burn_rate = forms.FloatField(
        label='Burn Rate',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '1',
            'step': '0.01',
            'placeholder': 'Enter burn rate (0.0 to 1.0)'
        })
    )
    
    overtime = forms.ChoiceField(
        label='Overtime',
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    promotion_last_5_years = forms.ChoiceField(
        label='Promotion in Last 5 Years',
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    availability = forms.ChoiceField(
        label='Availability',
        choices=[(1, 'Available'), (0, 'Occupied')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    years_at_company = forms.FloatField(
        label='Years at Company',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.1',
            'placeholder': 'Enter years at company'
        })
    )

class CapacityReportForm(forms.ModelForm):
    capacity_status = forms.ChoiceField(
        label='Capacity Status',
        choices=[
            ('Normal', 'Normal'),
            ('Overloaded', 'Overloaded'),
            ('Underutilized', 'Underutilized')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    resource_needs = forms.CharField(
        label='Resource Needs',
        max_length=200,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe the resource needs'
        })
    )

    class Meta:
        model = CapacityReport
        fields = ['capacity_status', 'resource_needs']
