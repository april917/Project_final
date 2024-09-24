from django.db import models

# Role model
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Skill model
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Project model
class Project(models.Model):
    name = models.CharField(max_length=100)
    timeline = models.DateField()  # If you need a range, consider using DateField for start and end
    required_hours = models.PositiveIntegerField()  # Ensure positive values only
    required_skills = models.ManyToManyField(Skill, related_name='projects')  # Use consistent lowercase for related_name

    def __str__(self):
        return self.name

# Employee model
class Employee(models.Model):
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
    ]
    
    #name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, related_name='employees')  # Many-to-Many relationship with Skill
    roles = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='employees')  # ForeignKey to Role
    experience = models.PositiveIntegerField()  # PositiveIntegerField for positive experience values
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES)  # Use predefined choices
    project_assignment = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name='employees')  # ForeignKey to Project
    burn_rate = models.FloatField(default=0.0)
    performance_rating = models.FloatField(default=0.0)
    overtime = models.BooleanField(default=False)
    number_of_project = models.PositiveIntegerField(default=0)  # Ensure positive integers
    average_monthly_hours = models.PositiveIntegerField(default=0)
    time_spent_company = models.PositiveIntegerField(default=0)  # Positive field for time spent
    age = models.PositiveIntegerField(default=0)  # Age should be positive
    gender = models.CharField(max_length=10, default='Unknown')
    years_at_company = models.PositiveIntegerField()  # Ensure positive years
    historical_performance_data=models.FloatField(default=0.0)
    promotion_last_5_years = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_employees(cls):
        return cls.objects.all()
