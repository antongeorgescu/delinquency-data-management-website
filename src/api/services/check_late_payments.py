import csv

late_count = 0
total_count = 0
days_late_distribution = {}

with open('../../../database_exports/loan_payments_20260403_145308.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_count += 1
        days_late_str = row.get('days_late', '0')
        try:
            days_late = float(days_late_str) if days_late_str else 0.0
        except ValueError:
            days_late = 0.0
            
        if days_late > 0:
            late_count += 1
        
        if days_late == 0:
            bucket = '0 days'
        elif days_late <= 2:
            bucket = '1-2 days'
        elif days_late <= 7:
            bucket = '3-7 days'
        elif days_late <= 30:
            bucket = '8-30 days'
        else:
            bucket = '30+ days'
        
        days_late_distribution[bucket] = days_late_distribution.get(bucket, 0) + 1

print('Days late distribution:', days_late_distribution)
print(f'Payments with days_late > 0: {late_count} out of {total_count} ({late_count/total_count*100:.2f}%)')