# app1/models/allocation_alert.py

from django.db import models

class AllocationAlert(models.Model):
    # Define the fields you need for AllocationAlert
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    alert_message = models.CharField(max_length=255)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.project} - {self.employee}: {self.alert_message}"
