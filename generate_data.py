from src.generate_synthetic_data import generate_dataset

df = generate_dataset(700)
df.to_csv('data/cleaned_jobs.csv', index=False)

print(f'✓ Generated {len(df)} records with MBA roles and certifications\n')
print('Preview:')
print(df.head(8))
print(f'\nSalary statistics (LPA):')
print(df['salary_lpa'].describe())
print(f'\nDataset saved to: data/cleaned_jobs.csv')
