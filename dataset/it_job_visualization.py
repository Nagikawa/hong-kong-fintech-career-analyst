import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re

# Set style and font
plt.rcParams['figure.figsize'] = (12, 8)
sns.set_style("whitegrid")
plt.rcParams['axes.unicode_minus'] = False

# Load the data
df = pd.read_csv('final_cleaned_data.csv')

# Data preprocessing
df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
df['publish_month'] = df['publish_date'].dt.to_period('M').astype(str)
df['avg_salary'] = pd.to_numeric(df['avg_salary'], errors='coerce')

print("Data loaded successfully. Generating 15 visualizations...\n")

# ==================== 1. Work Types Distribution (Pie Chart) ====================
plt.figure(figsize=(11, 9))

work_types = df['workTypes_label'].value_counts()

wedges, texts = plt.pie(work_types, 
                        startangle=90, 
                        colors=sns.color_palette('Set3', len(work_types)),
                        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})


percentages = work_types / work_types.sum() * 100
legend_labels = [f'{label} ({pct:.1f}%)' for label, pct in zip(work_types.index, percentages)]

plt.legend(wedges, legend_labels,
           title="Work Types",
           loc="upper right", 
           bbox_to_anchor=(1.25, 1.0),  
           fontsize=11)

plt.title('1. Work Types Distribution', fontsize=16, pad=20)
plt.axis('equal')

plt.savefig('viz1_work_types_pie.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 2. Job Postings Trend Over Time ====================
plt.figure(figsize=(12, 6))
monthly_posts = df.groupby('publish_month').size()
monthly_posts.plot(kind='line', marker='o', linewidth=2.5, color='#1f77b4')
plt.title('2. Job Postings Trend Over Time', fontsize=16)
plt.xlabel('Publish Month')
plt.ylabel('Number of Jobs')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.savefig('viz2_postings_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 3. Salary Distribution Histogram ====================
plt.figure(figsize=(12, 7))
salary_data = df['avg_salary'].dropna()
plt.hist(salary_data, bins=50, color='#66b3ff', edgecolor='black', alpha=0.85)
plt.title('3. Salary Distribution Histogram', fontsize=16)
plt.xlabel('Average Salary (HKD)')
plt.ylabel('Frequency')
plt.savefig('viz3_salary_histogram.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 4. Location Distribution ====================
plt.figure(figsize=(10, 6))
location_counts = df['location'].value_counts()
sns.barplot(x=location_counts.values, y=location_counts.index, palette='viridis')
plt.title('4. Location Distribution', fontsize=16)
plt.xlabel('Number of Jobs')
plt.ylabel('Location')
plt.savefig('viz4_location_bar.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 5. Top 10 Job Titles ====================
plt.figure(figsize=(12, 8))
top_titles = df['clean_title'].value_counts().head(10)
sns.barplot(x=top_titles.values, y=top_titles.index, palette='mako')
plt.title('5. Top 10 Job Titles', fontsize=16)
plt.xlabel('Count')
plt.ylabel('Job Title')
plt.savefig('viz5_top_titles.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 6. Salary Data Availability ====================
plt.figure(figsize=(10, 8))
salary_status = df['salary_missing'].value_counts()
labels = ['Has Salary', 'Missing Salary']
plt.pie(salary_status, labels=labels, autopct='%1.1f%%', startangle=90, 
        colors=['#66b3ff', '#ff9999'])
plt.title('6. Salary Data Availability', fontsize=16)
plt.axis('equal')
plt.savefig('viz6_salary_availability.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 7. Average Salary by Work Type ====================
plt.figure(figsize=(10, 6))
avg_salary_by_type = df.groupby('workTypes_label')['avg_salary'].mean().dropna()
sns.barplot(x=avg_salary_by_type.index, y=avg_salary_by_type.values, palette='plasma')
plt.title('7. Average Salary by Work Type', fontsize=16)
plt.xlabel('Work Type')
plt.ylabel('Average Salary (HKD)')
plt.xticks(rotation=45)
plt.savefig('viz7_avg_salary_by_type.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 8. Monthly Average Salary Trend ====================
plt.figure(figsize=(12, 6))
monthly_avg = df.groupby('publish_month')['avg_salary'].mean()
monthly_avg.plot(kind='line', marker='o', color='green', linewidth=2.5)
plt.title('8. Monthly Average Salary Trend', fontsize=16)
plt.xlabel('Publish Month')
plt.ylabel('Average Salary (HKD)')
plt.xticks(rotation=45)
plt.savefig('viz8_monthly_avg_salary.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 9. Top Keywords in Job Titles ====================
all_text = ' '.join(df['clean_title'].dropna().astype(str).str.lower())
words = re.findall(r'\b\w+\b', all_text)
word_freq = Counter(words)
top_keywords = pd.Series(dict(word_freq.most_common(12)))

plt.figure(figsize=(12, 8))
sns.barplot(x=top_keywords.values, y=top_keywords.index, palette='cubehelix')
plt.title('9. Top Keywords in Job Titles', fontsize=16)
plt.xlabel('Frequency')
plt.ylabel('Keyword')
plt.savefig('viz9_top_keywords.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 10. Salary Missing Rate by Work Type ====================
missing_rate = df.groupby('workTypes_label')['salary_missing'].mean() * 100
plt.figure(figsize=(12, 6))
sns.barplot(x=missing_rate.index, y=missing_rate.values, palette='magma')
plt.title('10. Salary Missing Rate by Work Type (%)', fontsize=16)
plt.xlabel('Work Type')
plt.ylabel('Missing Rate (%)')
plt.xticks(rotation=45)
plt.savefig('viz10_missing_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 11. Salary Boxplot by Work Type ====================
plt.figure(figsize=(12, 8))
sns.boxplot(x='workTypes_label', y='avg_salary', data=df, palette='Set2')
plt.title('11. Salary Boxplot by Work Type', fontsize=16)
plt.xlabel('Work Type')
plt.ylabel('Average Salary (HKD)')
plt.xticks(rotation=45)
plt.savefig('viz11_salary_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 12. Full-time vs Other Types Trend ====================
plt.figure(figsize=(14, 7))
full_time = df[df['workTypes_label'].str.contains('Full time', na=False)].groupby('publish_month').size()
others = df[~df['workTypes_label'].str.contains('Full time', na=False)].groupby('publish_month').size()

plt.plot(full_time.index, full_time.values, marker='o', label='Full Time', linewidth=3)
plt.plot(others.index, others.values, marker='s', label='Other Types', linewidth=3)
plt.title('12. Full-time vs Other Types Job Postings Trend', fontsize=16)
plt.xlabel('Publish Month')
plt.ylabel('Number of Jobs')
plt.legend()
plt.xticks(rotation=45)
plt.savefig('viz12_fulltime_vs_others.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 13. High Salary Jobs Proportion ====================
high_salary_count = (df['avg_salary'] > 50000).sum()
total_salary = df['avg_salary'].notna().sum()
labels = ['High Salary (>50k HKD)', 'Other Salaries']
plt.figure(figsize=(10, 8))
plt.pie([high_salary_count, total_salary - high_salary_count], labels=labels, autopct='%1.1f%%',
        colors=['#ff6666', '#66b3ff'], startangle=90)
plt.title('13. High Salary Jobs Proportion', fontsize=16)
plt.axis('equal')
plt.savefig('viz13_high_salary_pie.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 14. Top 10 Highest Average Salary Titles ====================
top_high_salary = df.groupby('clean_title')['avg_salary'].mean().nlargest(10)
plt.figure(figsize=(14, 10))
sns.barplot(x=top_high_salary.values, y=top_high_salary.index, palette='rocket')
plt.title('14. Top 10 Highest Average Salary Job Titles', fontsize=16)
plt.xlabel('Average Salary (HKD)')
plt.ylabel('Job Title')
plt.savefig('viz14_top_high_salary_titles.png', dpi=300, bbox_inches='tight')
plt.close()

# ==================== 15. Salary Range Distribution ====================
bins = [0, 20000, 30000, 40000, 50000, 70000, 100000, np.inf]
labels_bin = ['<20k', '20-30k', '30-40k', '40-50k', '50-70k', '70-100k', '>100k']
df['salary_range'] = pd.cut(df['avg_salary'], bins=bins, labels=labels_bin)

plt.figure(figsize=(12, 7))
range_count = df['salary_range'].value_counts().sort_index()
sns.barplot(x=range_count.index, y=range_count.values, palette='coolwarm')
plt.title('15. Salary Range Distribution', fontsize=16)
plt.xlabel('Salary Range (HKD)')
plt.ylabel('Number of Jobs')
plt.savefig('viz15_salary_range.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ All 15 visualizations have been successfully generated!")
print("Files saved as: viz1_work_types_pie.png to viz15_salary_range.png")