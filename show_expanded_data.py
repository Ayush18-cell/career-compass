import pandas as pd

df = pd.read_csv('data/cleaned_jobs.csv')

print('📊 Dataset Expansion Summary')
print('=' * 80)
print(f'Total Records: {len(df)}')
print(f'Total Unique Roles: {df["title"].nunique()}')

print(f'\n📈 All Roles:')
print(df['title'].value_counts())

print(f'\n💼 MBA/Management Roles with Certifications:')
mba_roles = ['Product Manager', 'Project Manager', 'Finance Manager', 'Business Manager',
             'Scrum Master', 'Agile Coach', 'Operations Manager', 'Strategy Consultant',
             'Management Consultant', 'Business Analyst Manager', 'Program Manager', 'Product Lead']

mba_df = df[df['title'].isin(mba_roles)].drop_duplicates(['title', 'experience', 'certifications'])
print(mba_df[['title', 'experience', 'salary_lpa', 'certifications']].to_string(index=False))

print(f'\n📊 Salary Comparison:')
mba_avg = df[df['title'].isin(mba_roles)]['salary_lpa'].mean()
tech_avg = df[~df['title'].isin(mba_roles)]['salary_lpa'].mean()
print(f'MBA/Management Average: {mba_avg:.2f} LPA')
print(f'Technical Average: {tech_avg:.2f} LPA')
print(f'Difference: +{(mba_avg - tech_avg):.2f} LPA ({((mba_avg/tech_avg - 1)*100):.1f}%)')

print(f'\n🎓 Certification Types Found:')
cert_counts = df[df['certifications'].str.len() > 0].groupby('title')['certifications'].count().sort_values(ascending=False)
print(cert_counts.head(10))
