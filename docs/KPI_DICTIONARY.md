# KPI Dictionary — HR Analytics Dashboard

Every KPI on the dashboard, its business definition, DAX, the actual value from
this dataset, and — critically — **how to explain it in an interview.**

Baseline for all comparisons: **16.12%** company-wide attrition.

---

## 1. Volume & Workforce KPIs

| # | KPI | Value | Definition |
|---|-----|-------|-----------|
| 1 | **Total Headcount** | **1,470** | Count of employee records in scope. |
| 2 | **Active Headcount** | **1,233** | Employees whose `Attrition Status = No`. |
| 3 | **Leaver Count** | **237** | Employees whose `Attrition Status = Yes`. |

```dax
Total Headcount = COUNTROWS ( 'Employees' )
Active Headcount = CALCULATE ( [Total Headcount], 'Employees'[Attrition Status] = "No" )
Leaver Count     = CALCULATE ( [Total Headcount], 'Employees'[Attrition Status] = "Yes" )
```

**Why it matters:** Headcount is the denominator for *every* other rate on the
page. Establishing it first stops the classic mistake of mixing a rate's
numerator and denominator from different filter contexts.

**Say this:** *"I anchor every rate to a single `[Workforce]` measure so a
slicer can't silently break the denominator."*

---

## 2. Attrition KPIs

| # | KPI | Value | Definition |
|---|-----|-------|-----------|
| 4 | **Attrition Rate** | **16.12%** | `Leavers ÷ Headcount` for the selected context. |
| 5 | **Retention Rate** | **83.88%** | `1 − Attrition Rate`. |
| 6 | **First-Year Attrition Rate** | **36.4%*** | Leavers with `<1 yr` tenure ÷ headcount. |
| 7 | **Leaver Concentration (0–2 yrs)** | **~56%** | Share of *all* leavers who left inside 3 years. |

```dax
Attrition Rate =
DIVIDE ( [Leaver Count], [Total Headcount], 0 )

Retention Rate =
DIVIDE ( [Active Headcount], [Total Headcount], 0 )

Leaver Concentration (0-2 yrs) =
DIVIDE (
    CALCULATE ( [Leaver Count], 'Employees'[YearsAtCompany] < 3 ),
    [Leaver Count], 0
)
```

*Denominator here is the `<1 yr` tenure band (206 employees), giving 75 ÷ 206 = 36.4%.

**Design note:** `DIVIDE` not `/`. When a slicer empties the table, `/` throws
`#DIV/0!`; `DIVIDE` returns the alternate (0) and the card stays clean.

**Say this:** *"Attrition is 16.12% overall, but over half of all leavers quit
inside their first three years — so this is a retention/onboarding problem far
more than a late-career engagement problem."*

---

## 3. Diagnostic Driver KPIs

### 3a. Overtime — the headline insight

| KPI | Value |
|-----|-------|
| Overtime Headcount | 416 |
| **Overtime Attrition Rate** | **30.5%** (127 leavers) |
| Non-Overtime Attrition Rate | **10.4%** (110 leavers) |
| **Overtime Risk Multiple** | **2.9×** |

```dax
Overtime Risk Multiple =
DIVIDE ( [Overtime Attrition Rate], [Non-Overtime Attrition Rate] )
```

**Why it matters:** Overtime is a *controllable* variable. Pay and job level
are slow to change; scheduling is not. This measure quantifies exactly how much
leverage changing it buys.

**Say this:** *"Staff on overtime leave at 30.5% versus 10.4% for everyone
else — a 2.9× multiple. It's the single strongest and most actionable driver in
the model, so it gets the headline donut visual."*

### 3b. Pay Gap

| KPI | Value |
|-----|-------|
| Average Income (Stayers) | **$6,833 /mo** |
| Average Income (Leavers) | **$4,787 /mo** |
| **Pay Gap %** | **29.9%** |

```dax
Pay Gap % =
DIVIDE (
    [Average Income (Stayers)] - [Average Income (Leavers)],
    [Average Income (Stayers)], 0
)
```

**Interpretation — say it carefully:** Leavers earn ~30% less than stayers.
This is **correlation, not proof of causation** — the effect is heavily
confounded by job level and role (Sales Reps and Lab Techs are both low-paid
*and* high-turnover). A rigorous read: *underpaid role families are being
shed*, which is a compensation-mix problem, not necessarily an individual-pay
problem.

### 3c. Stock Options

| Stock Option Level | Headcount | Attrition |
|--------------------|-----------|-----------|
| 0 (none) | 884 | **24.4%** |
| 1 | 540 | 9.4% |
| 2 | 31 | 4.1% |
| 3 | 15 | 0.0% |

**Say this:** *"Zero stock options correlates with 24.4% attrition versus 9.4%
at level one. That's a ~15-point spread and the second-cheapest lever after
scheduling."*

---

## 4. Comparative & Benchmark KPIs

These are what turn a chart into an insight.

| # | KPI | Value | Definition |
|---|-----|-------|-----------|
| 8 | **Attrition Lift** | varies | `Segment Rate − Company Rate`, in **percentage points**. |
| 9 | **Attrition Flag** | RAG status | Critical / Above Baseline / On Baseline / Healthy. |
| 10 | **% of Total Leavers** | varies | Segment leavers ÷ 237 — shows *volume*, not rate. |
| 11 | **Attrition Rank** | 1 = worst | `RANKX` over the current selection. |
| 12 | **vs Target (12%)** | +4.12 pp | Gap to an external HR benchmark. |

```dax
Attrition Lift =
VAR SegmentRate = [Attrition Rate]
VAR CompanyRate = CALCULATE ( [Attrition Rate], ALL ( 'Employees' ) )
RETURN SegmentRate - CompanyRate

Attrition Flag =
VAR R  = [Attrition Rate]
VAR Co = CALCULATE ( [Attrition Rate], ALL ( 'Employees' ) )
RETURN
    SWITCH ( TRUE (),
        R >= Co * 1.5,  "Critical",
        R >= Co * 1.15, "Above Baseline",
        R >= Co * 0.85, "On Baseline",
        "Healthy" )
```

**Why both Lift *and* % of Total Leavers:** they answer different questions and
teams routinely confuse them.

| Segment | Rate | Lift | % of Leavers | Reading |
|---|---|---|---|---|
| Sales Representative | 39.8% | +23.7 pp | 13.9% | **High rate, low volume** — fix the role |
| R&D / Research Scientist | 16.1% | 0.0 pp | 19.8% | **On baseline, high volume** — biggest *count* of leavers |

**Say this:** *"Rate tells you where to intervene; volume tells you where the
damage already is. Sales Reps have the worst rate but R&D loses the most
people — you need both views or you'll optimise the wrong thing."*

**Design note on `pp`:** Lift is a difference of two percentages, so it's
**percentage points**, not percent. Displaying `+23.7 pp` instead of `+23.7%`
is a small detail that signals statistical literacy.

---

## 5. Financial / Cost of Turnover KPIs

| # | KPI | Value | Definition |
|---|-----|-------|-----------|
| 13 | **Total Payroll** | **$115.3M /yr** | Σ `MonthlyIncome × 12` across all 1,470. |
| 14 | **Departing Payroll** | **$13.6M /yr** | Annualised pay of the 237 leavers. |
| 15 | **% Payroll Lost** | **~11.8%** | Departing ÷ Total payroll. |
| 16 | **Turnover Cost per Leaver** | **$57,444** | Leaver annual salary × replacement multiplier. |
| 17 | **Total Turnover Cost** | **$13.6M** | Σ across leavers at 1.0× multiplier. |

```dax
Total Turnover Cost =
SUMX (
    FILTER ( 'Employees', 'Employees'[Attrition Status] = "Yes" ),
    'Employees'[AnnualIncome] * 1.0      // replacement multiplier
)
```

**The multiplier — be explicit about it:** industry research (SHRM, Center for
American Progress) puts replacement cost at **50%–200%** of annual salary for
most roles, higher for specialists. This model defaults to **1.0×** and exposes
it as a single variable so a reviewer can run low/high scenarios.

| Scenario | Multiplier | Total Turnover Cost |
|---|---|---|
| Optimistic | 0.5× | $6.8M |
| **Base case** | **1.0×** | **$13.6M** |
| Pessimistic | 2.0× | $27.2M |

**Caveat — say it, don't hide it:** *"That 1.0× is an assumption, not a
measurement. It's parameterised so the HR director can substitute their own
figure — the point of the measure is the sensitivity, not false precision."*

**Payroll lost vs headcount lost — the sharpest line on the dashboard:**
237 of 1,470 leavers = **16.1% of headcount**, but they represent **~11.8% of
payroll**. The company is losing *proportionally cheaper* employees — the
low-tenure, low-level, low-pay population. That is a structural signal, not
noise.

---

## 6. Risk Scoring KPIs

| # | KPI | Value | Definition |
|---|-----|-------|-----------|
| 18 | **Attrition Risk Score** | 0–100 | Weighted composite of leading indicators. |
| 19 | **Risk Band** | Critical/High/Medium/Low | Banded score for RAG visuals. |
| 20 | **Headcount at High Risk** | scored | Count with score ≥ 50. |
| 21 | **% Workforce at Risk** | scored | Headcount at risk ÷ workforce. |

```dax
Attrition Risk Score =
VAR WOvertime    = IF ( 'Employees'[OverTime] = "Yes",                35, 0 )
VAR WTenure      = SWITCH ( TRUE (),
                    'Employees'[YearsAtCompany] < 1, 25,
                    'Employees'[YearsAtCompany] < 3, 18,
                    'Employees'[YearsAtCompany] < 6,  8, 0 )
VAR WLevel       = IF ( 'Employees'[JobLevel] = 1,                    15, 0 )
VAR WStock       = IF ( 'Employees'[StockOptionLevel] = 0,            10, 0 )
VAR WSat         = SWITCH ( TRUE (),
                    'Employees'[JobSatisfaction] = "Low",    8,
                    'Employees'[JobSatisfaction] = "Medium", 4, 0 )
VAR WInvolvement = IF ( 'Employees'[JobInvolvement] = "Low",           7, 0 )
RETURN WOvertime + WTenure + WLevel + WStock + WSat + WInvolvement

Risk Band =
SWITCH ( TRUE (),
    [Attrition Risk Score] >= 70, "Critical",
    [Attrition Risk Score] >= 50, "High",
    [Attrition Risk Score] >= 30, "Medium",
    "Low" )
```

**Weights are explicit and auditable on purpose.** Max attainable = 35+25+15+
10+8+7 = 100. Each weight is a *stated assumption* an HR partner can challenge
and retune — that is a feature. A black-box score invites disbelief; a
transparent one invites a productive argument about the weights.

**Why a score at all:** rates are *backward-looking* (who already left); a
score is *forward-looking* (who is likely to). HR needs the second one to act
in time.

**Say this:** *"The rate measures tell you what happened. The risk score
weights the leading indicators — overtime, tenure under a year, level 1, no
stock option, low satisfaction — into one 0–100 number so HR can prioritise
interventions before the resignation, not after."*

---

## KPI → Visual mapping

| KPI | Visual | Why |
|-----|--------|-----|
| Headcount, Attrition Rate, Avg Income, Avg Tenure | **4 KPI cards** | Headline health at a glance |
| Overtime Attrition Rate + Multiple | **Donut** | Single strongest driver, gets prime position |
| Dept / Job Role rate | **Bar, sorted desc** | Ranking by rate |
| % of Total Leavers | **Bar, % labels** | Complements rate view |
| Tenure Band rate | **Column** | Reveals early-tenure decay curve |
| Attrition Lift | **Diverging bar, ± centred at 0** | Above/below baseline reads instantly |
| Pay Gap % | **Clustered bar** | Stayers vs leavers side by side |
| Risk Band | **RAG card + gauge** | Actionable prioritisation |
| Turnover Cost | **Card, $ format** | Puts money on the number |

---

## Formatting reference

| Measure | Format | Display |
|---------|--------|---------|
| `Attrition Rate` | Percentage, 2 dp | `16.12%` |
| `Attrition Lift` | Custom | `+23.7 pp` |
| `Overtime Risk Multiple` | Decimal, 1 dp + `×` | `2.9×` |
| `Average Monthly Income` | Currency, whole | `$6,503` |
| `Total Turnover Cost` | Currency, compact | `$13.6M` |
| `Total Headcount` | Whole, thousands sep | `1,470` |
| `Attrition Risk Score` | Whole, 0–100 | `63` |
