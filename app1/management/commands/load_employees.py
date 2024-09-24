import csv
import os
from django.core.management.base import BaseCommand
from app1.models import Employee, Skill

class Command(BaseCommand):
    help = 'Load employees from CSV file'

    def handle(self, *args, **kwargs):
        # Determine the path to the CSV file
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'employee_profile.csv')

        # Check if the file exists
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_path}'))
            return

        # Open and read the CSV file
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0  # Counter to track progress
            for row in reader:
                row_count += 1
                print(f"Processing row {row_count}: {row['Name']}")

                try:
                    # Extract and convert data from CSV
                    employee_data = {
                        'name': row.get('Name'),
                        'gender': row.get('Gender', 'Unknown'),
                        'roles': row.get('Roles', ''),
                        'experience': int(row.get('Experience', 0)),
                        'availability': row.get('Availability', 'Unavailable'),
                        'project_assignment': row.get('ProjectAssignment', ''),
                        'burn_rate': float(row.get('BurnRate', 0.0)),
                        'performance_rating': float(row.get('PerformanceRating', 0.0)),
                        'overtime': row.get('Overtime', '').strip().lower() == 'true',
                        'number_of_project': int(row.get('NumberOfProjects', 0)),
                        'average_monthly_hours': int(row.get('AverageMonthlyHours', 0)),
                        'time_spend_company': int(row.get('TimeSpendCompany', 0)),
                        'age': int(row.get('Age', 0)),
                        'years_at_company': int(row.get('YearsAtCompany', 0)),
                        'promotion_last_5_years': row.get('PromotionInLast5Years', '').strip().lower() == 'true',
                    }

                    # Create or update the employee record
                    employee, created = Employee.objects.update_or_create(
                        name=employee_data['name'],
                        defaults=employee_data
                    )

                    # Handle the many-to-many relationship for skills
                    skill_names = row.get('Skills', '').split(',')
                    skill_instances = []
                    for skill_name in skill_names:
                        skill, _ = Skill.objects.get_or_create(name=skill_name.strip())
                        skill_instances.append(skill)

                    # Assign skills to the employee
                    employee.skills.set(skill_instances)

                    employee.save()

                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f'Error processing row {row_count}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Unexpected error processing row {row_count}: {e}'))
                    raise

        self.stdout.write(self.style.SUCCESS('Successfully loaded employee data'))
