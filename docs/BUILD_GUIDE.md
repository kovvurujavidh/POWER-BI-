# Build Guide — HR Analytics Power BI Dashboard

A visual-by-visual walkthrough to reproduce the dashboard in Power BI Desktop.
Estimated build time: **45–60 minutes**.

---

## Before You Start

| Requirement | Detail |
|-------------|--------|
| Power BI Desktop | Free — download from [powerbi.microsoft.com/desktop](https://powerbi.microsoft.com/desktop/) |
| Source data | `../data/HR_Employee_Attrition.csv` (1,470 rows) |
| Power Query code | `../powerquery/HR_Data_Transformation.m` |
| DAX measures | `../dax/HR_Dashboard_Measures.dax` |

---

## Step 1 — Load the Data

1. **Home → Get data → Text/CSV**
2. Select `data/HR_Employee_Attrition.csv`
3. In the preview dialog choose **Transform Data** (not Load) — you need the editor to apply cleaning.

---

## Step 2 — Apply Transformations

1. In Power Query Editor: **Home → Advanced Editor**
2. Delete existing contents, paste in the query you want
3. Edit the `File.Contents(...)` path to your local clone
4. **Home → Close & Apply**

### Which query?

| Query | Choose it when |
|---|---|
| `powerquery/HR_Data_Transformation.m` | Single flat table — fastest to stand up |
| `powerquery/Star_Schema.m` | Full dimensional model — **recommended**, see below |

### What the flat query does

| Step | Action |
|------|--------|
| Typed | Enforces Int64 / text types so DAX aggregation works |
| RemovedConstants | Drops `EmployeeCount`, `StandardHours`, `Over18`, `HourlyRate`, `MonthlyRate`, `DailyRate` |
| *Labeled | Converts 1–5 survey codes into `Low / Medium / High / Very High` |
| AddAnnualIncome | `MonthlyIncome × 12` |
| AddAgeBand / AddTenureBand | Bins for charting |
| CheckedRows | **Errors if row count ≠ 1,470** |

> ⚠️ **Important:** rename the final query to **`Employees`** — the DAX
> measures reference `'Employees'[...]`.

### If you used the star schema

Rename the fact table to `FactEmployee`, then globally replace `'Employees'`
with `FactEmployee` in `HR_Dashboard_Measures.dax`.

Set relationships in **Model view** — Power BI cannot infer them automatically
because the dimensions are derived, not looked up:

| From | To | Cardinality | Cross-filter |
|---|---|---|---|
| `DimDepartment[Department]` | `FactEmployee[Department]` | 1 → * | Single |
| `DimJobRole[JobRole]` | `FactEmployee[JobRole]` | 1 → * | Single |
| `DimTenureBand[TenureBand]` | `FactEmployee[TenureBand]` | 1 → * | Single |
| `DimIncomeBand[IncomeBand]` | `FactEmployee[IncomeBand]` | 1 → * | Single |
| `DimAgeBand[AgeBand]` | `FactEmployee[AgeBand]` | 1 → * | Single |
| `DimOvertime[OverTime]` | `FactEmployee[OverTime]` | 1 → * | Single |

For each dimension, set its `SortOrder` column as **Sort by column** for the
band field so slicers and axes sort correctly.

**Why star schema?** Slicer performance (descriptive text stored once per
member, not repeated across 1,470 rows), correct `ALL()` baseline behaviour in
the lift measures, and no ambiguous filter paths.

---

## Step 3 — Create the Measures

**Home → New measure** (repeat for each). Paste from `HR_Dashboard_Measures.dax`.

Set formatting per measure:

| Measure | Format | Suggested display |
|---------|--------|-------------------|
| `Attrition Rate` | Percentage | `0.00%` |
| `Total Employees` | Whole number | `#,##0` |
| `Average Monthly Income` | Currency USD | `$#,##0` |
| `Average Years at Company` | Decimal | `0.00` |

---

## Step 4 — Build the Visuals

### Row 1 — KPI cards

Add four **Card** visuals:

| Card | Field |
|------|-------|
| Total Employees | `[Total Employees]` |
| Attrition Rate | `[Attrition Rate]` |
| Avg Monthly Income | `[Average Monthly Income]` |
| Avg Years at Company | `[Average Years at Company]` |

*Format → Callout value → 24pt bold; Background → light grey `#F5F5F5`, rounded corners.*

### Row 2 — Where the leak is

| Visual | X axis | Y axis | Notes |
|--------|--------|--------|-------|
| **Clustered bar** — Attrition by Department | `Department` | `[Attrition Count]` | Sort descending |
| **Clustered bar** — Attrition % by Job Role | `JobRole` | `[Attrition Rate]` | Data labels on, % format |
| **Donut** — Attrition by OverTime | `OverTime` | `[Attrition Count]` | This is your headline visual |

### Row 3 — Why they leave

| Visual | Field well | Notes |
|--------|-----------|-------|
| **Clustered column** — Attrition by Tenure Band | X: `TenureBand`, Y: `[Attrition Rate]` | Set column sort by `TenureBand` |
| **Clustered bar** — Avg Income by Attrition | Y: `Attrition Status`, X: `[Average Monthly Income]` | Highlights pay gap |
| **Matrix** — Satisfaction breakdown | Rows: `JobSatisfaction`, Columns: `Attrition Status`, Values: `[Total Employees]` | Conditional formatting: background color by value |

### Filter pane — slicers

Add **Slicer** visuals for: `Department`, `JobRole`, `Gender`, `Education`, `OverTime`.
Arrange in a left-hand vertical strip, **Slicer → Selection → Single select: off**.

---

## Step 5 — Cross-Filtering

1. Select any visual
2. **Format (paint roller) → Edit interactions**
3. Ensure visuals are set to **Filter** (not None) where appropriate

**Test:** click *Sales* in the department bar — every other visual should update.

---

## Step 6 — Formatting & Theme

| Setting | Value |
|---------|-------|
| Theme | **View → Customize theme** → primary `#1F4E79`, accent `#2E75B6` |
| Canvas background | White, transparency 0% |
| Visual titles | 14pt, semibold, `#1F4E79` |
| Page | 16:9, fixed size 1280 × 720 |

---

## Step 7 — Publish

1. **Home → Publish** → select your workspace
2. Verify in the Power BI Service (`app.powerbi.com`)
3. Screenshot the finished page → save as `docs/dashboard_preview.png`

---

## Validation Checklist

Confirm these before publishing — every value is computed from the source data,
so a mismatch means something is wired up wrong:

**Data integrity**
- [ ] Row count = **1,470** (query assertion passes — errors if not)
- [ ] `FactEmployee` (or `Employees`) has **237** rows where `Attrition = Yes`
- [ ] Model view shows **no** "invalid identifier" or ambiguous relationship warnings
- [ ] All 6 dimension relationships are **single-direction**

**Headline KPIs**
- [ ] Total Headcount = **1,470**
- [ ] Attrition Rate = **16.12%**
- [ ] Retention Rate = **83.88%**
- [ ] Avg Monthly Income ≈ **$6,503**
- [ ] Avg Years at Company ≈ **7.01**

**Driver measures**
- [ ] Overtime Attrition Rate = **30.5%** (127 of 416)
- [ ] Non-Overtime Attrition Rate = **10.4%** (110 of 1,054)
- [ ] Overtime Risk Multiple ≈ **2.9×**
- [ ] Average Income (Stayers) ≈ **$6,833** / (Leavers) ≈ **$4,787**
- [ ] Pay Gap % ≈ **29.9%**
- [ ] Sales Representative rate = **39.8%** (+23.7 pp lift)
- [ ] `<1 yr` tenure band rate = **36.4%**

**Financial measures**
- [ ] Total Turnover Cost ≈ **$13.6M** at 1.0× multiplier
- [ ] Cost per Leaver ≈ **$57,444**
- [ ] % Payroll Lost ≈ **11.8%**

**Behaviour**
- [ ] Slicers cross-filter all visuals
- [ ] Clicking *Sales* in the department bar updates every other visual
- [ ] With a slicer selecting an empty combination, no `#DIV/0!` appears
- [ ] Attrition Lift shows `+`/`−` in **pp**, not `%`
- [ ] Tenure bands sort `<1 yr → 20+` (not alphabetically)

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Employee[Attrition]` invalid identifier | Query not named `Employees` | Rename query |
| `FactEmployee[...]` invalid identifier | Used star schema but didn't replace refs | Global replace `'Employees'` → `FactEmployee` |
| Slicers do nothing / no filter effect | Relationship missing or wrong direction | Model view → set 1→* , Single |
| Division by zero errors | Used `/` instead of `DIVIDE` | Use `DIVIDE` measures |
| Percentages display as `0.16` | Measure format not set | Format → Percentage → 2 decimals |
| Lift shows `23.7%` not `+23.7 pp` | Custom format missing | Apply `Attrition Lift (pp)` format string |
| Band chart out of order | Text sort | Column tools → Sort by column |
| Row-count assertion fails | Edited or swapped CSV | Restore the original 1,470-row file |
| Row count assertion fails | Wrong/edited CSV | Restore original 1,470-row file |
