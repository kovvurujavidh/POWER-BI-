# Interview Guide — Explaining This Project

A scripted way to talk about this project in interviews, plus the questions
you will be asked and how to answer them.

---

## The 60-second version

> *"I built an HR attrition analytics dashboard on the IBM dataset — 1,470
> employees, 35 fields. The headline is a 16.12% attrition rate, but the real
> finding is that it's concentrated: employees on overtime leave at 30.5%
> versus 10.4% for everyone else — a 2.9× multiple — and over half of all
> leavers exit within their first three years.*
>
> *"I modelled it as a star schema rather than a flat table so slicers and the
> `ALL()` baseline comparisons behave predictably, used Power Query to clean
> and band the data with a row-count assertion so it fails loudly if the source
> changes, and built a measure library covering volume, attrition, drivers,
> benchmarks, turnover cost, and a weighted early-warning risk score.*
>
> *"The output is a one-page cross-filtered dashboard plus an executive summary
> that ranks interventions by cost and impact."*

**Target: 45–60 seconds.** Stop there and let them ask. Do not front-run the
technical detail — wait for which direction they push.

---

## Structure: the STAR of the analysis

When asked to "walk me through the project," use this four-beat structure. It
reads as business judgement, not tutorial-following.

| Beat | Content | ~Time |
|---|---|---|
| **1. Business question** | *"Not 'make a dashboard' — the question was why 237 people left and what to do first."* | 10s |
| **2. Data & modelling** | 1,470 records, cleaned 6 constant/redundant columns, star schema, row-count guard. | 15s |
| **3. Analysis** | Overtime 2.9×; early-tenure decay; rate-vs-volume distinction; 29.9% pay gap (with confounder caveat). | 20s |
| **4. Recommendation** | Ranked actions: overtime audit, onboarding rebuild, stock-option extension — each with cost/impact. | 10s |

The **rate vs. volume** distinction in beat 3 and the **confounder caveat** on
the pay gap are the two moments that separate a analyst from a
dashboard-builder. Use them.

---

## Questions they will ask

### "What's the attrition rate and how did you calculate it?"

**Answer:**
> *"16.12% — 237 leavers over 1,470 total employees. It's a `DIVIDE` of
> `[Leaver Count]` by `[Total Headcount]`, both of which anchor to a single
> `[Workforce]` measure so the denominator can't drift when a slicer is
> applied."*

Then the follow-up you should volunteer:
> *"One thing the dataset doesn't support is a true 12-month annualised rate —
> there's no hire or termination date column. So this is a cumulative
> point-in-time rate, not a time-series one. If I had dates I'd compute
> average headcount as the denominator."*

**That admission is a strength.** Knowing what your data *cannot* do is a
senior trait.

---

### "What was the most interesting insight?"

**Answer — pick the overtime one:**
> *"Overtime. 30.5% attrition for staff on overtime versus 10.4% for those not —
> a 2.9× multiple. It matters most because it's the one lever that's cheap and
> fast: pay bands and job architecture take quarters, scheduling takes a week.*
>
> *"Drilling in, R&D lab technicians on overtime show 50% attrition — 31 of 62.
> That's a specific, actionable population, not a statistical abstraction."*

**Backup insight if they want a second:** the rate-vs-volume split.
> *"Sales Reps have the worst rate at 39.8%, but R&D loses the most people in
> absolute terms — 133 of 237 leavers. Rate tells you where to intervene,
> volume tells you where the damage already is. Confusing them would send the
> retention budget to the wrong place."*

---

### "Is the pay gap proof that low pay causes attrition?"

**This is a trap question. Answer it precisely:**

> *"No — and I'd flag that explicitly. Leavers earn 29.9% less on average,
> $4,787 versus $6,833. But job level and role are confounders: Sales
> Representatives and Lab Techs are both low-paid and high-turnover by
> construction.*
>
> *"So the defensible claim is that the organisation is shedding its
> lower-paid role families — they're 16.1% of headcount but only about 11.8%
> of payroll. To claim causation I'd need external market-benchmark data and,
> ideally, a controlled comparison. This is observational data with no control
> group."*

**Do not** let yourself be led into asserting causation from correlational
data. This is the single most likely methodology probe.

---

### "Why a star schema instead of one flat table?"

> *"Three reasons. Slicer performance — the descriptive text is stored once per
> member rather than repeated across 1,470 rows. Correct filter propagation —
> single-direction relationships from dim to fact mean `ALL()` on the fact gives
> a reliable company baseline for the lift measures. And authoring safety — a
> report builder can't accidentally create ambiguous paths.*
>
> *"I did keep the flat `HR_Data_Transformation.m` version alongside it, because
> for a single-table model the flat version is faster to stand up. It was a
> deliberate trade-off, not an oversight."*

---

### "Explain the DAX `DIVIDE` vs `/`."

> *"`/` throws `#DIV/0!` when a slicer empties the table — you get an error
> card in the middle of a stakeholder demo. `DIVIDE` takes an alternate value
> and returns that instead, so the card shows 0 and the layout holds.*
>
> *"`DIVIDE` also has different precedence semantics — with `/`, whether
> division happens before or after an `AND` in a larger expression can produce
> subtle bugs. `DIVIDE` makes the intent explicit."*

**Concrete example from the project:**
```dax
Attrition Rate = DIVIDE ( [Leaver Count], [Total Headcount], 0 )
```

---

### "What does `ALL` do in the Attrition Lift measure?"

> *"It removes filters, so `CALCULATE ( [Attrition Rate], ALL ( 'Employees' ) )`
> re-evaluates the rate across the entire table regardless of what the visual
> or slicers are filtering — that's the company baseline.*
>
> *`Attrition Lift` is then the segment's rate minus that baseline, expressed
> in percentage points. So Sales Reps show +23.7 pp against the 16.12% company
> rate.*
>
> *"Two things make it robust: `DIVIDE` handles the empty-selection case, and
> single-direction relationships mean `ALL` on the fact table doesn't produce
> unexpected cross-filter behaviour from the dimensions."*

---

### "How did you clean the data?"

> *"Six columns dropped: `EmployeeCount`, `StandardHours` and `Over18` are
> constants with zero variance; `HourlyRate`, `DailyRate` and `MonthlyRate` are
> redundant with `MonthlyIncome`. Dropping constants also prevents
> multicollinearity if the data later feeds a model.*
>
> *"I kept `PercentSalaryHike` though — that measures raise magnitude, a
> different concept from pay level, so it isn't redundant.*
>
> *"Then I converted the 1–5 coded survey fields into labels, added a
> `LeftFlag` 1/0 column for easy `SUM` aggregation, derived tenure/income/age
> bands, and wrapped it in a row-count assertion: if the source ever isn't
> 1,470 rows, the query errors instead of silently producing wrong KPIs."*

---

### "The risk score weights look arbitrary."

**Expected challenge. Have a real answer:**

> *"They're assumptions and I present them that way — deliberately transparent
> so they can be argued with. Max is 100: overtime 35, tenure under a year 25,
> job level 1 at 15, no stock option 10, low satisfaction 8, low involvement 7.*
>
> *"The weights follow the observed effect sizes in this dataset — overtime has
> the largest spread, so it carries the largest weight — and they're all in one
> measure so an HR partner can retune them without touching the model.*
>
> *"The real justification for having a score at all is direction: the attrition
> *rate* is backward-looking, it tells you who already left. The score is
> forward-looking, so HR can intervene before the resignation."*

---

### "What would you do differently with more time?"

Pick two:

1. **Dates.** *"There's no hire/termination date, so no genuine time series or
   YoY. I'd add a `DimDate` and compute a proper 12-month annualised rate with
   average headcount as the denominator."*
2. **Validation.** *"The risk score is a heuristic, not a model. I'd split the
   data, fit a logistic regression, and compare its AUC against the weighted
   heuristic to see whether the expert weights actually earn their keep."*
3. **Voluntary vs involuntary.** *"The dataset lumps them together. Regretted
   loss is the metric that matters, so I'd segment it and exclude involuntary
   exits from the headline rate."*
4. **External benchmarking.** *"The 12% target is a placeholder. I'd wire in
   industry and region benchmark data so 'vs target' means something."*

---

### "What's the turnover cost and how did you get it?"

> *"$13.6M — the sum of leaver annual salaries at a 1.0× replacement
> multiplier, giving about $57,444 per leaver.*
>
> *That 1.0× is an explicit assumption, not a measurement. Industry guidance
> runs 50% to 200% of annual salary depending on seniority, so I exposed it as
> a single variable: at 0.5× the total is $6.8M, at 2.0× it's $27.2M. The value
> of the measure is the sensitivity range, not point precision — I'd want the
> HR director to substitute their own figure."*

---

## Terms to use, and what they signal

| Phrase | Signals |
|---|---|
| *"percentage points"* (not percent) | Statistical literacy |
| *"correlation, not causation"* | Methodological rigour |
| *"confounded by job level"* | Multivariate thinking |
| *"rate vs volume"* | Business judgement |
| *"explicit, tunable assumption"* | Honesty about modelling |
| *"fails loudly if the source changes"* | Production mindset |
| *"single-direction relationships"* | Real Power BI modelling |
| *"backward-looking vs forward-looking"* | Analytics maturity |

---

## Phrases to avoid

| Instead of… | Say |
|---|---|
| *"the data proves"* | *"the data suggests / is consistent with"* |
| *"I did X because ChatGPT said"* | *"I chose X because…"* |
| *"it's just a dataset"* | name the business question |
| *"I don't know"* (flat) | *"Not from this data — here's what I'd need to answer it"* |
| Claiming a real `.pbix` you didn't build | Describe what the repo contains |

---

## Questions YOU should ask them

Asking one good question at the end moves you from candidate to colleague:

1. *"How does the team currently define and report attrition — is there a
   standard denominator, and does it separate voluntary from involuntary?"*
2. *"What's your rough replacement-cost assumption? I modelled 1.0× but ours
   may differ."*
3. *"Is the analysis one-off or operationalised? I'm interested in whether it
   lands in a scheduled report or stays a project."*

---

## Quick-reference numbers

Memorise these — they come up constantly:

| KPI | Value |
|---|---|
| Headcount | 1,470 |
| Leavers | 237 |
| **Attrition rate** | **16.12%** |
| Overtime attrition | 30.5% vs 10.4% (**2.9×**) |
| Overtime headcount | 416 |
| Worst role | Sales Rep **39.8%** |
| Best role | Research Director **2.5%** |
| <1 yr tenure attrition | **36.4%** |
| Leavers inside 3 years | **~56%** |
| Pay gap | **29.9%** ($4,787 vs $6,833) |
| Stock option 0 vs 1 | **24.4%** vs 9.4% |
| Worst segment | R&D Lab Tech + OT **50%** (62 HC) |
| Avg income | **$6,503**/mo |
| Avg tenure | **7.01** yrs |
| Avg age | **36.9** |
| Total payroll | **$115.3M**/yr |
| Turnover cost (1.0×) | **$13.6M** |
| Cost per leaver | **$57,444** |
| DAX measures | 30+ |
