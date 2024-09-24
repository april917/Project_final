from faker import Faker
import pandas as pd
import random

# Initialize Faker
Faker.seed(0)
fake = Faker()

# Define relevant skills and roles
roles_skills = {
    "Software Engineer": ["Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "React", "Django"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Data Analysis", "Statistics", "TensorFlow", "Pandas", "Matplotlib"],
    "System Analyst": ["System Design", "SQL", "UML", "Business Analysis", "Data Modeling", "Project Management", "Requirements Gathering"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes", "AWS", "Azure", "Linux", "Shell Scripting", "Jenkins", "Monitoring"],
    "IT Manager": ["Project Management", "Leadership", "Budgeting", "Vendor Management", "ITIL", "Strategic Planning", "Risk Management"],
    "Cloud Engineer": ["AWS", "Azure", "Google Cloud", "Cloud Security", "Kubernetes", "Docker", "Terraform", "Networking", "Python"]
}

# Function to generate random IT employee data
def generate_it_hr_data(num_rows=50000):
    data = []
    for _ in range(num_rows):
        role = random.choice(list(roles_skills.keys()))
        skills = ', '.join(random.sample(roles_skills[role], k=random.randint(3, 5)))
        employee = {
            "Skills": skills,
            "Roles": role,
            "Experience": random.randint(1, 30),  # years of experience
            "Availability": random.choice(["Available", "Occupied"]),
            "ProjectAssignment": fake.catch_phrase(),
            "BurnRate": round(random.uniform(0, 1), 2),
            "PerformanceRating": random.randint(1, 5),
            "Overtime": random.choice([True, False]),
            "NumberOfProject": random.randint(1, 10),
            "AverageMonthlyHours": random.randint(150, 250),
            "TimeSpendCompany": random.randint(1, 10),  # years
            "Age": random.randint(22, 60),
            "Gender": random.choice(["Male", "Female"]),
            "HistoricalPerformanceData": ', '.join(str(random.randint(1, 5)) for _ in range(5)),
            "YearsAtCompany": random.randint(0, 10),
            "PromotionLast5Years": random.choice([True, False]),
        }
        data.append(employee)
    
    return pd.DataFrame(data)

# Generate the dataset with 20000 rows
df = generate_it_hr_data(50000)

# Display the first few rows of the DataFrame
df.head()

# Save DataFrame to a CSV file
df.to_csv('employee_profile.csv', index=False)

# Save DataFrame to an Excel file
df.to_excel('employee_profile.xlsx', index=False)

print("Data saved to 'employee_profile.csv' and 'employee_profile.xlsx'")