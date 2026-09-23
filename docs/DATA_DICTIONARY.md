# Data Dictionary — IBM HR Analytics Employee Attrition & Performance

**Source:** IBM (fictional sample data, released for educational use)
**Shape:** 1,470 rows × 35 columns
**Grain:** one row per employee
**Target:** `Attrition` (Yes = 16.12%, 237 employees)

---

## Column reference

| # | Column | Type | Domain | Business meaning | Role in model |
|---|--------|------|--------|------------------|---------------|
| 1 | `Age` | int | 18–60 | Employee age in years. | Attribute |
| 2 | `Attrition` | text | Yes / No | **Target.** Whether the employee left during the period. | **Fact → LeftFlag** |
| 3 | `BusinessTravel` | text | Non-Travel, Travel_Rarely, Travel_Frequently | Expected travel frequency. | Attribute |
| 4 | `DailyRate` | int | 102–1499 | Daily pay rate. *Redundant* with `MonthlyIncome`. | Dropped in clean |
| 5 | `Department` | text | 3 values | Organisational unit. | **Dimension** |
| 6 | `DistanceFromHome` | int | 1–29 | Commute distance in miles. | Attribute |
| 7 | `Education` | int | 1–5 | Ordinal education level. | Ordinal (labelled) |
| 8 | `EducationField` | text | 6 values | Undergraduate field of study. | Attribute |
| 9 | `EmployeeCount` | int | always 1 | Constant. Zero analytical signal. | **Dropped** |
| 10 | `EmployeeNumber` | int | unique | **Primary key.** | **Fact PK** |
| 11 | `EnvironmentSatisfaction` | int | 1–4 | Ordinal: satisfaction with physical/work environment. | Ordinal (labelled) |
| 12 | `Gender` | text | Female / Male | Recorded gender. | Attribute |
| 13 | `HourlyRate` | int | 24–100 | Hourly pay rate. *Redundant*. | Dropped in clean |
| 14 | `JobInvolvement` | int | 1–4 | Ordinal: psychological identification with the job. | Ordinal (labelled) |
| 15 | `JobLevel` | int | 1–5 | Seniority tier. 1 = entry, 5 = executive. | Attribute |
| 16 | `JobRole` | text | 9 values | Specific role title. | **Dimension** |
| 17 | `JobSatisfaction` | int | 1–4 | Ordinal: satisfaction with the role. | Ordinal (labelled) |
| 18 | `MaritalStatus` | text | Single, Married, Divorced | Marital status. | Attribute |
| 19 | `MonthlyIncome` | int | 1,005–19,999 | Gross monthly pay. **Primary financial measure.** | **Measure** |
| 20 | `MonthlyRate` | int | 2,094–26,999 | Monthly rate. *Redundant*. | Dropped in clean |
| 21 | `NumCompaniesWorked` | int | 0–9 | Prior employers — career-mobility proxy. | Attribute |
| 22 | `Over18` | text | always Y | Constant. | **Dropped** |
| 23 | `OverTime` | text | Yes / No | **Strongest driver in the dataset.** | **Dimension** |
| 24 | `PercentSalaryHike` | int | 11–25 | Last raise, as a percentage. | Attribute |
| 25 | `PerformanceRating` | int | 3–4 | Manager rating: 3 = Excellent, 4 = Outstanding. *No 1 or 2 exist.* | Ordinal (labelled) |
| 26 | `RelationshipSatisfaction` | int | 1–4 | Ordinal: satisfaction with supervisor/peers. | Ordinal (labelled) |
| 27 | `StandardHours` | int | always 80 | Constant. | **Dropped** |
| 28 | `StockOptionLevel` | int | 0–3 | Equity eligibility. **Second-strongest lever.** | Attribute |
| 29 | `TotalWorkingYears` | int | 0–40 | Total career tenure. | Attribute |
| 30 | `TrainingTimesLastYear` | int | 0–6 | Count of training events. | Attribute |
| 31 | `WorkLifeBalance` | int | 1–4 | Ordinal: self-rated work-life balance. | Ordinal (labelled) |
| 32 | `YearsAtCompany` | int | 0–40 | **Tenure.** Drives the early-tenure decay curve. | **Derived → TenureBand** |
| 33 | `YearsInCurrentRole` | int | 0–18 | Time in present role. | Attribute |
| 34 | `YearsSinceLastPromotion` | int | 0–15 | Promotion staleness — a known flight-risk signal. | Attribute |
| 35 | `YearsWithCurrManager` | int | 0–17 | Manager relationship tenure. | Attribute |

---

## Ordinal label mapping

Applied in Power Query so charts show readable text rather than bare integers:

| Field | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| `Education` | Below College | College | Bachelor | Master | Doctor |
| `EnvironmentSatisfaction` | Low | Medium | High | Very High | — |
| `JobSatisfaction` | Low | Medium | High | Very High | — |
| `JobInvolvement` | Low | Medium | High | Very High | — |
| `WorkLifeBalance` | Bad | Good | Better | Best | — |
| `PerformanceRating` | — | — | Excellent | Outstanding | — |

> ⚠️ **`PerformanceRating` has no 1 or 2.** Every employee is rated Excellent or
> Outstanding. It is therefore a near-constant with almost no variance and
> **should not be used as a driver** — it will produce a misleading chart with
> only two near-empty bars. Worth mentioning in review; it is a data-quality
> observation, not an analysis finding.

---

## Columns dropped during cleaning

| Column | Constant / issue | Reason |
|---|---|---|
| `EmployeeCount` | always `1` | Zero variance — carries no signal |
| `StandardHours` | always `80` | Zero variance |
| `Over18` | always `Y` | Zero variance |
| `HourlyRate` | 24–100 | Redundant with `MonthlyIncome` |
| `DailyRate` | 102–1499 | Redundant with `MonthlyIncome` |
| `MonthlyRate` | 2,094–26,999 | Redundant with `MonthlyIncome` |

Dropping redundant rate columns prevents **multicollinearity** if the data is
later fed into a model, and keeps the field list clean for report authors.

> Kept: `PercentSalaryHike` — it is *not* redundant. It measures raise
> magnitude, a different concept from pay *level*.

---

## Derived columns (created in Power Query)

| Column | Logic | Why |
|---|---|---|
| `LeftFlag` | `1 if Attrition = Yes else 0` | Enables `SUM()` aggregation without a measure |
| `AnnualIncome` | `MonthlyIncome × 12` | Payroll and turnover-cost maths |
| `TenureBand` | `<1 / 1-2 / 3-5 / 6-10 / 11-20 / 20+` | Exposes the early-tenure decay curve |
| `IncomeBand` | `<3k / 3k-5k / 5k-8k / 8k-12k / 12k+` | Segmented pay analysis |
| `AgeBand` | `Under 25 / 25-34 / 35-44 / 45-54 / 55+` | Generational slicing |

Band labels are **zero-prefixed** (`"1. <1 yr"`) so text sorting in slicers and
axes matches the intended ordinal sequence. The numeric `SortOrder` column in
each dimension gives an alternative via *Sort by column*.

---

## Star schema

```
DimDepartment ─┐
DimJobRole    ─┤
DimTenureBand ─┼── FactEmployee ── DimDate (when dates are available)
DimIncomeBand ─┤
DimAgeBand    ─┤
DimOvertime   ─┘
```

| Table | Grain | Rows |
|---|---|---|
| `FactEmployee` | one row per employee | 1,470 |
| `DimDepartment` | one row per department | 3 |
| `DimJobRole` | one row per role | 9 |
| `DimTenureBand` | one row per tenure band | 6 |
| `DimIncomeBand` | one row per income band | 5 |
| `DimAgeBand` | one row per age band | 5 |
| `DimOvertime` | one row per overtime state | 2 |

All relationships are **single-direction** (dimension → fact), which is both
best practice and a prerequisite for the `ALL ( 'Employees' )` baseline
comparisons in the DAX to behave predictably.

---

## Data quality checks

| Check | Expected | Where enforced |
|---|---|---|
| Row count | 1,470 | Power Query assertion — **errors if violated** |
| `EmployeeNumber` | unique, non-null | PK constraint |
| `Attrition` domain | exactly `Yes`/`No` | Type + validation |
| Leaver count | 237 | Analysis regression check |
| Attrition rate | 16.12% | KPI validation |
| Nulls | none | CSV source is complete |

The row-count assertion is deliberate: if anyone swaps in an edited CSV, the
query fails loudly instead of silently producing a dashboard with wrong KPIs.
