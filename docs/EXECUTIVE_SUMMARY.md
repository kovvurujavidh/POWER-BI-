# Executive Summary — Workforce Attrition Analysis

**Prepared for:** HR Leadership / Business Stakeholders
**Dataset:** IBM HR Analytics Employee Attrition & Performance — 1,470 employees, 35 fields
**Baseline attrition:** 16.12% (237 leavers)

---

## TL;DR

> Attrition is **16.12%** and it is **not evenly distributed**. Three segments
> — employees on **overtime**, staff with **under two years' tenure**, and
> **entry-level role families** — account for the majority of losses. The
> combined effect is an estimated **$13.6M** in annual turnover cost at a
> conservative 1.0× replacement multiplier.
>
> **Two of the three levers are cheap and fast to pull:** overtime scheduling
> and stock-option eligibility.

---

## The five findings that matter

### 1. Overtime is the dominant — and most actionable — driver

| Segment | Headcount | Leavers | Attrition |
|---|---|---|---|
| Works overtime | 416 | 127 | **30.5%** |
| Does not | 1,054 | 110 | **10.4%** |

A **2.9× risk multiple.** This matters more than any other finding because
overtime is a *scheduling decision* — it can change next quarter, unlike pay
bands or job architecture.

**Recommendation:** Treat sustained overtime as a retention risk trigger. Flag
any employee crossing a monthly overtime threshold for a workload review.

---

### 2. This is fundamentally an early-tenure problem

| Tenure band | Attrition |
|---|---|
| <1 yr | **36.4%** |
| 1–2 yrs | **28.9%** |
| 3–5 yrs | ~17% |
| 6–10 yrs | ~10% |
| 11–20 yrs | ~6% |
| 20+ yrs | ~3% |

The curve is a smooth, steep decay: **risk falls monotonically with tenure.**
Roughly **half of all leavers exit within their first three years.**

**Recommendation:** Shift retention spend *forward* — structured 30/60/90
onboarding, early mentorship, and a 6-month and 18-month check-in. Money spent
on year-five engagement is spent after most attrition has already happened.

---

### 3. A specific pocket is critically exposed

Intersecting department × role × overtime surfaces a segment at **50%
attrition**:

| Segment | Headcount | Attrition |
|---|---|---|
| R&D — Laboratory Technicians, on overtime | 62 | **50.0%** |
| Overtime + tenure under 3 yrs | 201 | **51.2%** |

Half of a sixty-person population leaving in one period is not statistical
noise — it is a live operational problem.

**Recommendation:** Immediate workload audit of R&D lab technicians; this
single role family should be the first retention programme targeted.

---

### 4. Compensation structure, not individual pay

| | Avg monthly income |
|---|---|
| Stayers | **$6,833** |
| Leavers | **$4,787** |

Leavers earn **29.9% less.** But the confounder is role level: high-turnover
families (Sales Reps $2,626, Lab Techs $3,237) sit at the bottom of the pay
architecture by construction.

The honest reading: **the organisation is shedding its cheapest employees
first.** They represent 16.1% of headcount but only ~11.8% of payroll.

**Recommendation:** Review market positioning for *role families*, not
individual adjustments. Correlate with external benchmark data before acting —
this dataset alone cannot establish causation.

---

### 5. Stock options are the second-cheapest lever

| Stock option level | Headcount | Attrition |
|---|---|---|
| 0 (none) | 884 | **24.4%** |
| 1 | 540 | 9.4% |
| 2 | 31 | 4.1% |
| 3 | 15 | 0.0% |

A **~15-point spread** between level 0 and level 1.

**Recommendation:** Evaluate extending option eligibility one level down the
ladder. At an estimated 11.8% payroll-loss rate, even a modest reduction in
attrition pays for itself.

---

## Where the losses actually sit — rate vs. volume

The two views answer different questions and must not be conflated:

**By rate (where to intervene):**

| Role | Attrition | Lift vs 16.12% baseline |
|---|---|---|
| Sales Representative | **39.8%** | **+23.7 pp** |
| Laboratory Technician | 23.9% | +7.8 pp |
| Human Resources | 23.1% | +7.0 pp |
| Sales Executive | 17.5% | +1.4 pp |
| Research Scientist | 16.1% | −0.0 pp |
| Manufacturing Director | 6.9% | −9.2 pp |
| Research Director | 2.5% | −13.6 pp |

**By volume (where the damage is):**

| Segment | Leavers | % of all leavers |
|---|---|---|
| Research & Development | 133 | 56.1% |
| Sales | 92 | 38.8% |
| Human Resources | 12 | 5.1% |

**Read together:** Sales Reps have the worst *rate* — fix that role. R&D
carries the most *volume* — that is where absolute headcount is bleeding.
Optimising one view alone misallocates the retention budget.

---

## Financial exposure

| KPI | Value |
|---|---|
| Total annual payroll | **$115.3M** |
| Payroll lost to attrition | **$13.6M (~11.8%)** |
| Cost per leaver (1.0× replacement) | **$57,444** |
| Total turnover cost | **$13.6M** |

| Scenario | Multiplier | Total cost |
|---|---|---|
| Optimistic | 0.5× | $6.8M |
| **Base case** | **1.0×** | **$13.6M** |
| Pessimistic | 2.0× | $27.2M |

> **Stated assumption:** the replacement multiplier (1.0×) is a parameter, not
> a measurement. Industry guidance ranges 50%–200% of annual salary. The model
> exposes it as a single variable so finance can substitute their own figure —
> the value of the measure is the sensitivity range, not point precision.

---

## Prioritised recommendations

| # | Action | Lever cost | Expected impact | Owner |
|---|---|---|---|---|
| 1 | **Audit overtime in R&D lab tech role** | Low | Addresses the 50% segment directly | R&D + HR Ops |
| 2 | **Rebuild 30/60/90 onboarding + 6 & 18-month check-ins** | Low | Attacks the early-tenure curve where ~50% of leavers sit | HR / L&D |
| 3 | **Trigger workload review at overtime threshold** | Low | Targets the 2.9× risk multiple | Line managers |
| 4 | **Extend stock-option eligibility one level down** | Medium | ~15 pp spread observed | Compensation |
| 5 | **Benchmark role-family pay externally** | Low | Tests the 29.9% pay-gap hypothesis properly | Compensation |
| 6 | **Deploy the Attrition Risk Score for early warning** | Low | Shifts from retrospective to predictive | HR Analytics |

---

## Method notes & limitations

Stated openly, because credibility depends on it:

1. **Correlation ≠ causation.** The pay gap and satisfaction findings are
   associations. Overtime and tenure are the strongest, but this is
   observational data with no control group.
2. **Voluntary vs involuntary is not distinguished.** The dataset only records
   `Attrition = Yes/No`, so regretted-loss analysis isn't possible from source.
3. **No dates.** There is no hire/termination date column, so genuine
   time-series and YoY trends cannot be computed. Tenure bands are the
   closest available proxy for the time dimension.
4. **Turnover cost is modelled, not measured.** Multiplier is an explicit,
   tunable parameter.
5. **Synthetic data.** IBM released this as a fictional sample — figures are
   methodologically sound but are not a real company's results.
6. **Risk-score weights are assumptions.** They are transparent and intended
   to be challenged and retuned with an HR partner.

---

## Dashboard navigation

| Question | Visual |
|---|---|
| How healthy is the workforce? | Row 1 — KPI cards |
| What is the single biggest driver? | Row 2 — Overtime donut |
| Which roles are worst? | Row 2 — Job role bar (rate) |
| Is it an onboarding problem? | Row 3 — Tenure band column |
| What does it cost? | Row 3 — Turnover cost card |
| Who is *about* to leave? | Row 3 — Risk band RAG |
