from django.urls import path
from . import views
from .views import allocation, assign_project

urlpatterns = [
    path('allocation/', allocation, name='allocation'),
    #path('assign_project/<int:employee_id>/', assign_project, name='assign_project'),
    path('capacity/', views.capacity, name='capacity'),
    path('dynamic/', views.dynamic, name='dynamic'),
    #path('skill/', views.skill, name='skill'),
    path('predictive/', views.predictive, name='predictive'),
    path('planning/', views.planning, name='planning'),
    #path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search_employee/', views.search_employee, name='search_employee'),
    path('project_search/', views.project_search, name='project_search'),
    path('search/', views.search_employee, name='search_employee')
    # Other paths
]


