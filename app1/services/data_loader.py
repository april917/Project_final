import csv

def load_employee_data(file_path):
    dataset = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            employee_data = {
                'Skills': row['Skills'],
                'Roles': row['Roles'],
                'Experience': row['Experience'],
                'Availability': row['Availability'],
                'ProjectAssignment': row['ProjectAssignment'],
                'BurnRate': row['BurnRate'],
                'PerformanceRating': row['PerformanceRating'],
                'Overtime': row['Overtime'],
                'NumberOfProject': row['NumberOfProject'],
                'AverageMonthlyHours': row['AverageMonthlyHours'],
                'TimeSpendCompany': row['TimeSpendCompany'],
                'Age': row['Age'],
                'Gender': row['Gender'],
                'HistoricalPerformanceData': row['HistoricalPerformanceData'],
                'YearsAtCompany': row['YearsAtCompany'],
                'PromotionLast5Years': row['PromotionLast5Years']
            }
            dataset.append(employee_data)
    return dataset
