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
2. Delete existing contents, paste in `HR_Data_Transformation.m`
3. Edit the `File.Contents(...)` path to your local clone
4. **Home → Close & Apply**

### What the query does

| Step | Action |
|------|--------|
| Typed | Enforces Int64 / text types so DAX aggregation works |
| RemovedConstants | Drops `EmployeeCount`, `StandardHours`, `Over18`, `HourlyRate`, `MonthlyRate`, `DailyRate` |
| *Labeled | Converts 1–5 survey codes into `Low / Medium / High / Very High` |
| AddAnnualIncome | `MonthlyIncome × 12` |
| AddAgeBand / AddTenureBand | Bins for charting |
| CheckedRows | Errors if row count ≠ 1,470 |

> **Important:** rename the final query to **`Employees`** — the DAX measures reference `'Employees'[...]`.

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

Confirm these before publishing:

- [ ] Row count = **1,470** (query assertion passes)
- [ ] Attrition Rate KPI shows **16.12%**
- [ ] Overtime donut shows 127 leavers / 416 overtime staff
- [ ] Avg Monthly Income ≈ **$6,503**
- [ ] Avg Years at Company ≈ **7.01**
- [ ] Slicers cross-filter all visuals
- [ ] No "invalid identifier" errors in the model view

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Employee[Attrition]` invalid identifier | Query not named `Employees` | Rename query |
| Division by zero errors | Used `/` instead of `DIVIDE` | Use `DIVIDE` measures |
| Percentages display as `0.16` | Measure format not set | Format → Percentage → 2 decimals |
| Band chart out of order | Text sort | Column tools → Sort by column |
| Row count assertion fails | Wrong/edited CSV | Restore original 1,470-row file |
