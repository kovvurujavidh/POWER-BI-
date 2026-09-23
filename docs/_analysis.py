"""Business-level analysis of the IBM HR attrition dataset.
Emits every number used in the README, KPI dictionary and dashboard.
"""
import csv, statistics as st
from collections import defaultdict

P = r"C:\Opencode\POWER-BI-\data\HR_Employee_Attrition.csv"
rows = list(csv.DictReader(open(P, encoding="utf-8-sig")))
N = len(rows)
for r in rows:
    for k in ("Age","DistanceFromHome","Education","EnvironmentSatisfaction",
              "JobInvolvement","JobLevel","JobSatisfaction","MonthlyIncome",
              "NumCompaniesWorked","PercentSalaryHike","PerformanceRating",
              "StockOptionLevel","TotalWorkingYears","TrainingTimesLastYear",
              "WorkLifeBalance","YearsAtCompany","YearsInCurrentRole",
              "YearsSinceLastPromotion","YearsWithCurrManager","EmployeeNumber"):
        r[k] = int(r[k])

def left(rs): return sum(1 for r in rs if r["Attrition"] == "Yes")
def rate(rs): return left(rs)/len(rs)*100 if rs else 0.0
def avg(rs, f): return st.mean([f(r) for r in rs]) if rs else 0.0

print("="*78); print("1. HEADLINE KPIs"); print("="*78)
L = left(rows)
print(f"Headcount          : {N}")
print(f"Leavers            : {L}   Retained: {N-L}")
print(f"Attrition rate     : {L/N*100:.2f}%")
print(f"Avg monthly income : ${avg(rows, lambda r:r['MonthlyIncome']):,.0f}")
print(f"Avg annual income  : ${avg(rows, lambda r:r['MonthlyIncome'])*12:,.0f}")
print(f"Avg years at co    : {avg(rows, lambda r:r['YearsAtCompany']):.2f}")
print(f"Avg age            : {avg(rows, lambda r:r['Age']):.1f}")
print(f"Avg total work yrs : {avg(rows, lambda r:r['TotalWorkingYears']):.1f}")
print(f"Avg distance (mi)  : {avg(rows, lambda r:r['DistanceFromHome']):.1f}")
print(f"Stayer income      : ${avg([r for r in rows if r['Attrition']=='No'], lambda r:r['MonthlyIncome']):,.0f}")
print(f"Leaver income      : ${avg([r for r in rows if r['Attrition']=='Yes'], lambda r:r['MonthlyIncome']):,.0f}")
gap = (1 - avg([r for r in rows if r['Attrition']=='Yes'], lambda r:r['MonthlyIncome']) /
           avg([r for r in rows if r['Attrition']=='No'],  lambda r:r['MonthlyIncome']))*100
print(f"Pay gap (leaver vs stayer): {gap:.1f}% lower")

def group(title, key, order=None):
    print("\n"+"-"*78); print(title); print("-"*78)
    g = defaultdict(list)
    for r in rows: g[key(r)].append(r)
    items = sorted(g.items(), key=lambda kv: -rate(kv[1])) if not order else \
            [(k, g[k]) for k in order if k in g]
    print(f"{'Segment':<34}{'HC':>6}{'Left':>6}{'Rate%':>8}{'AvgInc':>9}{'AvgYrs':>8}")
    for k, rs in items:
        print(f"{str(k):<34}{len(rs):>6}{left(rs):>6}{rate(rs):>8.1f}"
              f"${avg(rs, lambda r:r['MonthlyIncome']):>8,.0f}{avg(rs, lambda r:r['YearsAtCompany']):>8.1f}")
    return g

group("2. DEPARTMENT", lambda r: r["Department"])
group("3. JOB ROLE", lambda r: r["JobRole"])
group("4. OVERTIME", lambda r: r["OverTime"])
group("5. BUSINESS TRAVEL", lambda r: r["BusinessTravel"])

print("\n"+"-"*78); print("6. TENURE BANDS (early-tenure risk curve)"); print("-"*78)
def tenure(r):
    y = r["YearsAtCompany"]
    return "<1 yr" if y<1 else "1-2 yrs" if y<3 else "3-5 yrs" if y<6 else \
           "6-10 yrs" if y<11 else "11-20 yrs" if y<21 else "20+ yrs"
order = ["<1 yr","1-2 yrs","3-5 yrs","6-10 yrs","11-20 yrs","20+ yrs"]
tb = group("x", tenure, order)

print("\n"+"-"*78); print("7. INCOME BANDS"); print("-"*78)
def incb(r):
    m = r["MonthlyIncome"]
    return "<$3k" if m<3000 else "$3k-$5k" if m<5000 else "$5k-$8k" if m<8000 else \
           "$8k-$12k" if m<12000 else "$12k+"
group("x", incb, ["<$3k","$3k-$5k","$5k-$8k","$8k-$12k","$12k+"])

print("\n"+"-"*78); print("8. JOB LEVEL"); print("-"*78)
group("x", lambda r: f"Level {r['JobLevel']}")

lab4 = {1:"Low",2:"Medium",3:"High",4:"Very High"}
print("\n"+"-"*78); print("9. SATISFACTION & WORK-LIFE"); print("-"*78)
for f, nm in [("JobSatisfaction","Job Satisfaction"),("EnvironmentSatisfaction","Environment Satisfaction"),
              ("JobInvolvement","Job Involvement"),("WorkLifeBalance","Work-Life Balance")]:
    g = defaultdict(list)
    for r in rows: g[lab4[r[f]]].append(r)
    print(f"\n  {nm}:")
    for k in ["Low","Medium","High","Very High"]:
        if k in g: print(f"    {k:<11} HC={len(g[k]):>5}  rate={rate(g[k]):5.1f}%")

print("\n"+"-"*78); print("10. STOCK OPTION (retention lever)"); print("-"*78)
g = defaultdict(list)
for r in rows: g[r["StockOptionLevel"]].append(r)
for k in sorted(g): print(f"  Level {k}: HC={len(g[k]):>5}  rate={rate(g[k]):5.1f}%")

print("\n"+"-"*78); print("11. PROMOTION / MANAGER TENURE"); print("-"*78)
def promo(r):
    y = r["YearsSinceLastPromotion"]
    return "0-1 yrs" if y<2 else "2-4 yrs" if y<5 else "5+ yrs"
g = defaultdict(list)
for r in rows: g[promo(r)].append(r)
print("  Years since last promotion:")
for k in ["0-1 yrs","2-4 yrs","5+ yrs"]: print(f"    {k:<9} HC={len(g[k]):>5}  rate={rate(g[k]):5.1f}%")
g = defaultdict(list)
for r in rows: g["0-2 yrs" if r["YearsWithCurrManager"]<3 else "3-6 yrs" if r["YearsWithCurrManager"]<7 else "7+ yrs"].append(r)
print("  Years with current manager:")
for k in ["0-2 yrs","3-6 yrs","7+ yrs"]: print(f"    {k:<9} HC={len(g[k]):>5}  rate={rate(g[k]):5.1f}%")

print("\n"+"-"*78); print("12. AGE BANDS"); print("-"*78)
def ageb(r):
    a=r["Age"]; return "Under 25" if a<25 else "25-34" if a<35 else "35-44" if a<45 else "45-54" if a<55 else "55+"
g = defaultdict(list)
for r in rows: g[ageb(r)].append(r)
for k in ["Under 25","25-34","35-44","45-54","55+"]:
    if k in g: print(f"  {k:<9} HC={len(g[k]):>5}  rate={rate(g[k]):5.1f}%")

print("\n"+"-"*78); print("13. RISK SEGMENTS (rate>=25% AND HC>=40)"); print("-"*78)
g = defaultdict(list)
for r in rows: g[(r["Department"], r["JobRole"], r["OverTime"])].append(r)
hits = [(k, rs) for k, rs in g.items() if rate(rs) >= 25 and len(rs) >= 40]
for k, rs in sorted(hits, key=lambda x: -rate(x[1])):
    print(f"  {k[0][:20]:<20} | {k[1][:24]:<24} | OT={k[2]:<3} | HC={len(rs):>4} rate={rate(rs):5.1f}%")

print("\n"+"-"*78); print("14. OVERTIME x TENURE interaction"); print("-"*78)
for ot in ["Yes","No"]:
    for tb2 in ["<3 yrs","3-10 yrs","10+ yrs"]:
        rs = [r for r in rows if r["OverTime"]==ot and
              (tb2=="<3 yrs" and r["YearsAtCompany"]<3 or
               tb2=="3-10 yrs" and 3<=r["YearsAtCompany"]<10 or
               tb2=="10+ yrs" and r["YearsAtCompany"]>=10)]
        if rs: print(f"  OT={ot:<3} {tb2:<9} HC={len(rs):>5} rate={rate(rs):5.1f}%")

print("\n"+"-"*78); print("15. TOP DRIVER RANKING (leaver rate spread vs baseline)"); print("-"*78)
base = L/N*100
drivers = []
for f, nm in [("OverTime","Overtime=Yes"),("JobRole","Job Role (worst)"),
              ("BusinessTravel","Travel Frequently"),("StockOptionLevel","No stock option"),
              ("JobSatisfaction","Low job sat"),("WorkLifeBalance","Bad WLB")]:
    if f=="OverTime": rs=[r for r in rows if r["OverTime"]=="Yes"]
    elif f=="JobRole":
        gg=defaultdict(list)
        for r in rows: gg[r["JobRole"]].append(r)
        rs=max(gg.values(), key=rate)
    elif f=="BusinessTravel": rs=[r for r in rows if r["BusinessTravel"]=="Travel_Frequently"]
    elif f=="StockOptionLevel": rs=[r for r in rows if r["StockOptionLevel"]==0]
    elif f=="JobSatisfaction": rs=[r for r in rows if r["JobSatisfaction"]==1]
    else: rs=[r for r in rows if r["WorkLifeBalance"]==1]
    drivers.append((nm, rate(rs), rate(rs)-base))
for nm, rt, dl in sorted(drivers, key=lambda x:-x[2]):
    print(f"  {nm:<26} rate={rt:5.1f}%   lift={dl:+5.1f} pts vs baseline {base:.1f}%")
print("\nDONE")
