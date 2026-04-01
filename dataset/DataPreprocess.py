import pandas as pd
import numpy as np
import re
import os

# ====================== 1. 批量读取所有文件并合并 ======================
# 文件路径与列表（对应你所有的IT/金融CSV）
FOLDER_PATH = "./"
FILE_LIST = [
    "140-2025-11 IT jobs.csv",
    "hk-2025-12 Finance jobs.csv",
    "hk-2025-12 IT jobs.csv",
    "hk-2026-01 Finance jobs.csv",
    "hk-2026-01 IT jobs.csv",
    "hk-2026-02 Finance jobs.csv",
    "hk-2026-02 IT jobs.csv"
]

# 批量读取合并
all_dfs = []
for file in FILE_LIST:
    file_path = os.path.join(FOLDER_PATH, file)
    df = pd.read_csv(file_path, low_memory=False)
    # 从文件名提取行业(IT/Finance)
    df["industry"] = "IT" if "IT" in file else "Finance"
    all_dfs.append(df)

# 合并所有数据
df = pd.concat(all_dfs, ignore_index=True)
print(f"合并完成，总数据量：{len(df):,} 条")

# ====================== 2. 缺失值处理 ======================
# 薪资缺失标记
df["salary_missing"] = df["salary_label"].isna().astype(int)

# 分类字段缺失填充
cat_cols = ["title", "location_label", "workTypes_label"]
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# 日期字段用众数填充
if "listedAt_dateTimeUtc" in df.columns:
    df["listedAt_dateTimeUtc"] = df["listedAt_dateTimeUtc"].fillna(df["listedAt_dateTimeUtc"].mode()[0])

# 删除全空行
df = df.dropna(how="all")
print("缺失值处理完成")


# ====================== 3. 薪资字段清洗（范围直接取均值） ======================
def clean_salary_to_avg(salary_str):
    """薪资清洗：直接返回均值，45k-50k → 47500"""
    if pd.isna(salary_str) or str(salary_str).strip() in ["-", "Open", "Negotiable"]:
        return np.nan

    # 清理字符：去掉$、,、hk、空格、单位
    s = str(salary_str).lower()
    s = re.sub(r'[$,hk\s]', '', s)
    s = re.sub(r'permonth|p\.m\.|mth|month|upto', '', s)

    # 处理k单位
    def convert_val(x):
        return float(x.replace('k', '')) * 1000 if 'k' in x else float(x)

    # 匹配薪资范围
    match = re.search(r'(\d+\.?\d*k?)[-–](\d+\.?\d*k?)', s)
    if match:
        # 范围值：取平均
        val1 = convert_val(match.group(1))
        val2 = convert_val(match.group(2))
        avg = (val1 + val2) / 2
    else:
        # 单值：直接用
        single_match = re.search(r'\d+\.?\d*k?', s)
        avg = convert_val(single_match.group()) if single_match else np.nan

    # 过滤不合理薪资（5000-500000港币/月）
    if not (5000 <= avg <= 500000):
        return np.nan
    return avg


# 执行薪资清洗
df["avg_salary"] = df["salary_label"].apply(clean_salary_to_avg)
print(f"薪资清洗完成，有效薪资：{df['avg_salary'].notna().sum():,} 条")

# ====================== 4. 字段格式统一 ======================
# 1. 日期统一为 YYYY-MM-DD
if "listedAt_dateTimeUtc" in df.columns:
    df["publish_date"] = pd.to_datetime(df["listedAt_dateTimeUtc"], errors="coerce").dt.strftime("%Y-%m-%d")

# 2. 地区统一：香港地区统一为 Hong Kong
if "location_label" in df.columns:
    df["location"] = df["location_label"].apply(
        lambda x: "Hong Kong" if "hong kong" in str(x).lower() else "Unknown"
    )

# 3. 岗位标题统一：小写+去特殊符号
if "title" in df.columns:
    df["clean_title"] = df["title"].str.lower().str.replace(r'[^\w\s]', '', regex=True).str.strip()

# 4. 行业标签统一大写
df["industry"] = df["industry"].str.upper()

print("字段格式统一完成")

# ====================== 保存最终结果 ======================
# 保留核心字段输出
core_cols = ["clean_title", "industry", "location", "publish_date", "avg_salary", "salary_missing", "workTypes_label"]
df_output = df[[col for col in core_cols if col in df.columns]]

# 保存文件
output_path = os.path.join(FOLDER_PATH, "final_cleaned_data.csv")
df_output.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n✅ 全部处理完成！")
print(f"清洗后数据已保存至：{output_path}")
print(f"最终数据量：{len(df_output):,} 条")