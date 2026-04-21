import pandas as pd
import numpy as np
import re
import os

# ====================== 文件路径 ======================
FOLDER_PATH = "/Users/liyingdong/Desktop/7810/HK Job 2025_2026"

FILE_LIST = [
    "140-2025-11 IT jobs.csv",
    "hk-2025-12 Finance jobs.csv",
    "hk-2025-12 IT jobs.csv",
    "hk-2026-01 Finance jobs.csv",
    "hk-2026-01 IT jobs.csv",
    "hk-2026-02 Finance jobs.csv",
    "hk-2026-02 IT jobs.csv"
]

all_dfs = []
for file in FILE_LIST:
    file_path = os.path.join(FOLDER_PATH, file)
    df = pd.read_csv(file_path, low_memory=False)
    df["industry"] = "IT" if "IT" in file else "Finance"
    all_dfs.append(df)

df = pd.concat(all_dfs, ignore_index=True)

# ====================== 所有统计（双薪资字段独立统计） ======================
it_count = len(df[df["industry"] == "IT"])
finance_count = len(df[df["industry"] == "Finance"])
total_count = len(df)

# 1. 具体薪资数值（salary 字段）缺失统计
salary_num_missing = df["salary"].isna().sum()
salary_num_missing_rate = round(salary_num_missing / total_count * 100, 2)

# 2. 薪资描述（salary_label 字段）缺失统计
salary_label_missing = df["salary_label"].isna().sum()
salary_label_missing_rate = round(salary_label_missing / total_count * 100, 2)

# 3. 地点（location_label 字段）缺失统计
location_missing = df["location_label"].isna().sum()
location_missing_rate = round(location_missing / total_count * 100, 2)

# 4. 发布时间（listedAt_dateTimeUtc 字段）缺失统计
publish_missing = df["listedAt_dateTimeUtc"].isna().sum()
publish_missing_rate = round(publish_missing / total_count * 100, 2)

# 5. 字段数统计
total_cols = df.shape[1]
it_cols = total_cols
finance_cols = total_cols

# ====================== 输出（英文，直接复制进PPT） ======================
print("======= DATA SUMMARY =======")
print(f"IT Jobs Count:      {it_count}")
print(f"Finance Jobs Count: {finance_count}")
print(f"Total Count:        {total_count}")
print("---------------------------")
print(f"IT Columns Count:      {it_cols}")
print(f"Finance Columns Count: {finance_cols}")
print(f"Total Columns Count:   {total_cols}")
print("---------------------------")
print(f"Salary (Numeric) Missing:     {salary_num_missing}")
print(f"Salary (Numeric) Missing Rate: {salary_num_missing_rate}%")
print("---------------------------")
print(f"Salary Label (Description) Missing:     {salary_label_missing}")
print(f"Salary Label (Description) Missing Rate: {salary_label_missing_rate}%")
print("---------------------------")
print(f"Location Missing:         {location_missing}")
print(f"Location Missing Rate:     {location_missing_rate}%")
print("---------------------------")
print(f"Publish Time Missing:     {publish_missing}")
print(f"Publish Time Missing Rate: {publish_missing_rate}%")
print("===========================\n")

# ====================== 缺失值处理 ======================
df["salary_missing"] = df["salary_label"].isna().astype(int)  # 标记薪资描述缺失

cat_cols = ["title", "location_label", "workTypes_label"]
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# 发布时间缺失填充（兜底）
if "listedAt_dateTimeUtc" in df.columns and publish_missing > 0:
    df["listedAt_dateTimeUtc"] = df["listedAt_dateTimeUtc"].fillna(df["listedAt_dateTimeUtc"].mode()[0])

df = df.dropna(how="all")

# ====================== 薪资清洗（基于 salary_label 计算平均薪资） ======================
def clean_salary_to_avg(salary_str):
    if pd.isna(salary_str) or str(salary_str).strip() in ["-", "Open", "Negotiable", ""]:
        return np.nan

    s = str(salary_str).lower()
    s = re.sub(r'[$,hk\s]', '', s)
    s = re.sub(r'permonth|p\.m\.|mth|month|upto', '', s)

    def convert_val(x):
        return float(x.replace('k', '')) * 1000 if 'k' in x else float(x)

    match = re.search(r'(\d+\.?\d*k?)[-–](\d+\.?\d*k?)', s)
    if match:
        val1 = convert_val(match.group(1))
        val2 = convert_val(match.group(2))
        avg = (val1 + val2) / 2
    else:
        single_match = re.search(r'\d+\.?\d*k?', s)
        avg = convert_val(single_match.group()) if single_match else np.nan

    if not (5000 <= avg <= 500000):
        return np.nan
    return avg

df["avg_salary"] = df["salary_label"].apply(clean_salary_to_avg)

# ====================== 格式统一 ======================
if "listedAt_dateTimeUtc" in df.columns:
    df["publish_date"] = pd.to_datetime(df["listedAt_dateTimeUtc"], errors="coerce").dt.strftime("%Y-%m-%d")

if "location_label" in df.columns:
    df["location"] = df["location_label"].apply(
        lambda x: "Hong Kong" if "hong kong" in str(x).lower() else "Unknown"
    )

if "title" in df.columns:
    df["clean_title"] = df["title"].str.lower().str.replace(r'[^\w\s]', '', regex=True).str.strip()

df["industry"] = df["industry"].str.upper()

# ====================== 保存 ======================
core_cols = ["clean_title", "industry", "location", "publish_date", "avg_salary", "salary_missing", "workTypes_label"]
df_output = df[[col for col in core_cols if col in df.columns]]

output_path = os.path.join(FOLDER_PATH, "final_cleaned_data.csv")
df_output.to_csv(output_path, index=False, encoding="utf-8-sig")

print("✅ All processing completed!")
print(f"Cleaned data saved to: {output_path}")
print(f"Final records: {len(df_output)}")