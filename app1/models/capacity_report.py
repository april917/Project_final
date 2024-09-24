# app1/models/capacity_report.py
from django.db import models

class CapacityReport(models.Model):
    capacity_status = models.CharField(max_length=50, choices=[('Normal', 'Normal'), ('Overloaded', 'Overloaded'), ('Underutilized', 'Underutilized')])
    resource_needs = models.TextField(max_length=200)

    def __str__(self):
        return self.capacity_status


