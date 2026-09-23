# HR Analytics Dashboard — Power BI

An interactive Power BI dashboard analysing employee attrition across **1,470 employee records** and **35 fields**, built to surface the workforce KPIs and turnover drivers that matter to HR decision-making.

![Dashboard](docs/dashboard_preview.png)

---

## Table of Contents

- [Overview](#overview)
- [Key Findings](#key-findings)
- [KPIs](#kpis)
- [Repository Structure](#repository-structure)
- [Dataset](#dataset)
- [How to Build the Dashboard](#how-to-build-the-dashboard)
- [DAX Measures](#dax-measures)
- [Dashboard Layout](#dashboard-layout)
- [Technologies Used](#technologies-used)
- [Author](#author)

---

## Overview

Employee turnover is one of the most expensive operational problems a company faces. This project takes the raw IBM HR attrition dataset and turns it into a single-page interactive dashboard that lets an HR business partner answer, in seconds:

- How many people are we losing, and at what rate?
- Which departments and job roles are bleeding talent?
- Does overtime actually drive attrition?
- Where do leavers sit by tenure, income and satisfaction?

All charts are cross-filtered — clicking a department card filters every other visual on the page.

---

## Key Findings

Findings computed directly from the dataset in this repository:

| # | Finding | Numbers |
|---|---------|---------|
| 1 | **Overall attrition is 16.12%** | 237 of 1,470 employees left |
| 2 | **Overtime is the single strongest driver** | Overtime staff attrit at **30.5%** (127/416) vs **10.4%** (110/1,054) without — roughly **3x higher** |
| 3 | **Research & Development carries the most volume** | 961 employees, 133 left (13.8%) |
| 4 | **Sales has the highest departmental rate** | 446 employees, 92 left (**20.6%**) |
| 5 | **Human Resources is small but risky** | 63 employees, 12 left (19.0%) |
| 6 | Average tenure of leavers is low | Average years at company: **7.01**; average age **36.9** |

> **Headline insight:** overtime is where the leverage is. Nearly 1 in 3 employees working overtime leave, versus 1 in 10 who don't. Scheduling and workload balancing should be the first retention lever HR pulls.

---

## KPIs

The four KPI cards on the dashboard front page:

| KPI | Value | DAX |
|-----|-------|-----|
| Total Employees | **1,470** | `COUNTROWS('Employees')` |
| Attrition Rate | **16.12%** | `[Attrition Count] / [Total Employees]` |
| Avg Monthly Income | **$6,503** | `AVERAGEX('Employees', 'Employees'[MonthlyIncome])` |
| Avg Years at Company | **7.01** | `AVERAGEX('Employees', 'Employees'[YearsAtCompany])` |

---

## Repository Structure

```
POWER-BI-/
│
├── README.md                          ← you are here
│
├── data/
│   └── HR_Employee_Attrition.csv      Raw dataset — 1,470 rows × 35 columns
│
├── powerquery/
│   └── HR_Data_Transformation.m       Power Query (M): load, clean, label, derive
│
├── dax/
│   └── HR_Dashboard_Measures.dax      All KPI, context and banding measures
│
└── docs/
    ├── BUILD_GUIDE.md                 Step-by-step build instructions
    └── dashboard_preview.png          Dashboard screenshot
```

---

## Dataset

| Attribute | Value |
|-----------|-------|
| Source | IBM HR Analytics Employee Attrition & Performance (via Kaggle) |
| Records | 1,470 employees |
| Columns | 35 |
| Target variable | `Attrition` (Yes / No) |
| Leavers | 237 (16.12%) |
| Retained | 1,233 (83.88%) |

**Columns removed during cleaning** — all constant, zero analytical signal:

| Column | Constant value | Why dropped |
|--------|----------------|-------------|
| `EmployeeCount` | `1` | Never varies |
| `StandardHours` | `80` | Never varies |
| `Over18` | `Y` | Never varies |
| `HourlyRate` / `DailyRate` / `MonthlyRate` | Redundant | Income already captured by `MonthlyIncome` |

**Coded fields converted to readable labels:**

| Field | Coding |
|-------|--------|
| Education | 1 Below College → 5 Doctor |
| EnvironmentSatisfaction / JobSatisfaction / JobInvolvement | 1 Low → 4 Very High |
| WorkLifeBalance | 1 Bad → 4 Best |
| PerformanceRating | 3 Excellent, 4 Outstanding |

---

## How to Build the Dashboard

Requires [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free, Windows).

**1. Load the data**

Power BI Desktop → **Home → Get data → Text/CSV** → select `data/HR_Employee_Attrition.csv` → **Transform Data**.

**2. Apply the transformations**

In Power Query Editor: **Home → Advanced Editor** → replace contents with `powerquery/HR_Data_Transformation.m`.

Update the file path in the `Source` step to match your local clone. **Close & Apply**.

> The query ends with a row-count assertion (1,470). If it ever errors, the source data changed.

**3. Create the measures**

**Home → New measure**, then paste each block from `dax/HR_Dashboard_Measures.dax`. Rename the query to `Employees` so the measure references resolve.

**4. Build the visuals**

Follow [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md) for the exact visual-by-visual layout, field wells and formatting.

**5. Add cross-filtering**

Select each visual → **Format → Edit interactions** → ensure cards and charts filter one another. Clicking *Sales* should filter every visual on the page.

---

## DAX Measures

Highlights from [`dax/HR_Dashboard_Measures.dax`](dax/HR_Dashboard_Measures.dax):

```dax
Attrition Rate =
DIVIDE ( [Attrition Count], [Total Employees], 0 )
```

```dax
Overtime Attrition Rate =
DIVIDE (
    CALCULATE ( [Attrition Count], 'Employees'[OverTime] = "Yes" ),
    [Overtime Employees],
    0
)
```

```dax
High Attrition Flag =
IF ( [Attrition Rate] >= 0.20, "High",
    IF ( [Attrition Rate] >= 0.12, "Medium", "Low" ) )
```

`DIVIDE` is used throughout rather than `/` — it safely returns 0 on division-by-zero instead of raising an error, which matters when a slicer filters a card down to an empty table.

---

## Dashboard Layout

Single page, three rows:

| Row | Visuals | Purpose |
|-----|---------|---------|
| **1** | 4 KPI cards — Employees, Attrition Rate, Avg Income, Avg Years | Headline health |
| **2** | Attrition by Department (bar) · Attrition % by Job Role (bar) · Attrition by OverTime (donut) | Where the leak is |
| **3** | Attrition by Tenure Band (column) · Avg Income by Attrition (clustered) · Satisfaction breakdown (matrix) | Why they leave |
| **Filters** | Department, Job Role, Gender, Education, OverTime slicers | Interactive drill-down |

---

## Technologies Used

- **Power BI Desktop** — data modelling and report authoring
- **Power Query (M)** — data cleaning, type casting, derived columns
- **DAX** — KPI measures, context transition, ranking and banding
- **SQL concepts** — `GROUP BY`, aggregate and conditional logic (mirrored in the companion [HR-Analytics-SQL](https://github.com/kovvurujavidh/HR-Analytics-SQL) repo)
- **Microsoft Excel** — source analysis in the companion [HR-Analytics-Excel-Dashboard](https://github.com/kovvurujavidh/HR-Analytics-Excel-Dashboard) repo

---

## Related Projects

| Project | Tool |
|---------|------|
| [HR-Analytics-Excel-Dashboard](https://github.com/kovvurujavidh/HR-Analytics-Excel-Dashboard) | Excel, Pivot Tables, Slicers |
| [HR-Analytics-SQL](https://github.com/kovvurujavidh/HR-Analytics-SQL) | MySQL |
| **This repo** | Power BI, DAX, Power Query |

---

## Author

**Kovvuru Javidh**
Data / MIS Analyst — Excel · SQL · Power BI · Data Visualization

- GitHub: [@kovvurujavidh](https://github.com/kovvurujavidh)
- LinkedIn: [kovvurujavidh](https://www.linkedin.com/in/kovvurujavidh/)
- Portfolio: [localbizz.dpdns.org](https://localbizz.dpdns.org/)

---

## License

Dataset © IBM (fictional sample data, released for educational use). Dashboard code in this repository is open for learning and reuse.
