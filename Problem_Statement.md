# Problem Statement

## Descriptive Analysis of Hong Kong IT & Finance Job Market (2025–2026)

---

## Research Background

Hong Kong is an international financial and technology hub; IT and Finance have long been two pillars of the local job market. Job seekers want to understand salary levels, popular roles, and geographic distribution, while employers want to track hiring trends. This project conducts a descriptive analysis of the IT and Finance recruitment market using real job postings from Hong Kong platforms from November 2025 to February 2026.

---

## Research Questions

Based on the available fields in the data, we focus on the following questions:

### 1. Salary (fields: `salary`, `salary_label`, `salary_currencyLabel`)

- What share of postings disclose salary? What characterizes postings that do not?
- How is `salary_label` formatted? (monthly p.m. vs annual p.a., range vs single value)
- How do salary bands (e.g. $20k–$30k, $40k–$60k) differ between IT and Finance?
- What are the typical medians or typical ranges for each industry?

### 2. Geography (field: `location_label`)

- How are job counts distributed across districts (e.g. Kwun Tong, Central, Tsim Sha Tsui, Tsuen Wan)?
- How does geographic distribution differ between IT and Finance on `location_label`?
- Which districts are in the Top 5 or Top 10 by job count?

### 3. Time (field: `listedAt_dateTimeUtc`)

- What is the trend in posting volume by month (2025-11, 2025-12, 2026-01, 2026-02)?
- Are monthly posting trends aligned between IT and Finance?

### 4. Job Types (fields: `title`, `classifications`)

- By `classifications` (e.g. IT: Help Desk, Project Management, Networks; Finance: Treasury, Corporate Finance, Banking – Retail), how many jobs fall in each sub-category?
- Which job titles appear most often? How do IT and Finance differ?
- How is `workTypes_label` distributed (Full time, Part time, Contract/Temp)?

### 5. Advertisers (fields: `advertiser_name`, `advertiser_isVerified`)

- Which advertisers post the most jobs?
- What is the share of postings from verified employers (`advertiser_isVerified = True`) vs non-verified?

---

## Data Source and Key Fields

| Field | Meaning | Example |
|-------|---------|---------|
| `title` | Job title | IT Manager, ISDA Negotiator |
| `location_label` | Work location (district level) | Kwun Tong District, Tsim Sha Tsui |
| `salary` / `salary_label` | Salary | $28,000–$40,000 per month |
| `salary_currencyLabel` | Currency | HKD |
| `workTypes_label` | Work arrangement | Full time, Part time, Contract/Temp |
| `listedAt_dateTimeUtc` | Posting time | 2025-12-02T02:33:18.526Z |
| `classifications` | Job category | Help Desk & IT Support, Treasury |
| `advertiser_name` | Employer | UBoT Incorporated Limited |
| `advertiser_isVerified` | Verified employer | True / False |

- **Dataset:** HK Jobs Data (IT + Finance, 2025.11–2026.02)

---

## Analysis Objective

Across these five dimensions and the listed fields, we use data exploration, preprocessing, and visualization to summarize patterns in Hong Kong’s IT and Finance job market and to inform job seekers and employers.
