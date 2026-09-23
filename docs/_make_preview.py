"""Render docs/dashboard_preview.png — business-grade HR Analytics dashboard.

Layout preview rendered from the dashboard specification in docs/BUILD_GUIDE.md.
(Not a Power BI screenshot — Power BI Desktop authors .pbix natively.)

Run:  python docs/_make_preview.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# ---------------------------------------------------------------- palette ---
NAVY   = "#0F2B46"
BLUE   = "#1F6FB2"
SKY    = "#5AA9E6"
TEAL   = "#17A2B8"
RED    = "#E63946"
AMBER  = "#F4A261"
GREEN  = "#2A9D8F"
GREY   = "#5C6B7A"
LGREY  = "#93A1B0"
PAPER  = "#FFFFFF"
WELL   = "#F4F7FB"
LINE   = "#DDE5EE"

fig = plt.figure(figsize=(19.2, 10.8), dpi=150)
fig.patch.set_facecolor(WELL)


def card(x, y, w, h, fc=PAPER, ec=LINE, lw=1.2, shadow=True, z=1):
    """Rounded card with a soft drop shadow, in figure coordinates."""
    if shadow:
        sh = FancyBboxPatch((x + 0.0022, y - 0.0038), w, h,
                            boxstyle="round,pad=0.004,rounding_size=0.007",
                            linewidth=0, facecolor="#0F2B46", alpha=0.07,
                            transform=fig.transFigure, zorder=0)
        fig.add_artist(sh)
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.004,rounding_size=0.007",
                       linewidth=lw, edgecolor=ec, facecolor=fc,
                       transform=fig.transFigure, zorder=z)
    fig.add_artist(p)


def ctitle(x, y, t, sub=None):
    fig.text(x, y, t, fontsize=14.5, fontweight="bold", color=NAVY,
             transform=fig.transFigure, zorder=5)
    if sub:
        fig.text(x, y - 0.030, sub, fontsize=9.6, color=LGREY,
                 transform=fig.transFigure, zorder=5)


def clean(ax):
    # Axes zorder defaults to 0 — below the figure-level card patches.
    # Lift it so charts render ON TOP of their card instead of under it.
    ax.set_zorder(3)
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)


def caption(x, y, line1, line2=None, color=LGREY, size=8.3):
    """Two-line card caption, kept inside the card bounds."""
    fig.text(x, y, line1, fontsize=size, color=color,
             transform=fig.transFigure, zorder=4)
    if line2:
        fig.text(x, y - 0.017, line2, fontsize=size, color=color,
                 transform=fig.transFigure, zorder=4)


# ================================================================= header ===
fig.add_artist(Rectangle((0, 0.928), 1, 0.072, transform=fig.transFigure,
                         facecolor=NAVY, edgecolor="none", zorder=1))
fig.add_artist(Rectangle((0, 0.9245), 1, 0.0035, transform=fig.transFigure,
                         facecolor=SKY, edgecolor="none", zorder=1))

fig.text(0.016, 0.9585, "HR Analytics  \u2014  Workforce Attrition Dashboard",
         fontsize=23.5, fontweight="bold", color="white",
         transform=fig.transFigure, zorder=3, va="center")
fig.text(0.016, 0.9375, "IBM HR Analytics Employee Attrition & Performance   |   "
                        "1,470 employees   |   35 fields   |   Baseline attrition 16.12%",
         fontsize=10.6, color="#A9C4DE", transform=fig.transFigure,
         zorder=3, va="center")
fig.text(0.984, 0.9585, "Kovvuru Javidh", fontsize=12.4, fontweight="bold",
         color="white", ha="right", transform=fig.transFigure, zorder=3, va="center")
fig.text(0.984, 0.9375, "Power BI  \u00b7  DAX  \u00b7  Power Query  \u00b7  Star Schema",
         fontsize=9.8, color="#A9C4DE", ha="right", transform=fig.transFigure,
         zorder=3, va="center")

# ============================================================= KPI cards ====
Y0, H0 = 0.777, 0.126
kpis = [
    ("1,470",   "TOTAL HEADCOUNT",  "1,233 active  \u00b7  237 leavers", BLUE),
    ("16.12%",  "ATTRITION RATE",   "237 of 1,470  \u00b7  target 12%",   RED),
    ("$6,503",  "AVG MONTHLY INCOME", "stayers \\$6,833  \u00b7  leavers \\$4,787", GREEN),
    ("7.01",    "AVG YEARS AT COMPANY", "avg age 36.9  \u00b7  avg work yrs 11.3", AMBER),
]
x0, cw, gap = 0.016, 0.2313, 0.0113
for i, (val, lab, sub, col) in enumerate(kpis):
    x = x0 + i * (cw + gap)
    card(x, Y0, cw, H0, fc=PAPER)
    fig.add_artist(Rectangle((x, Y0), 0.0042, H0, transform=fig.transFigure,
                             facecolor=col, edgecolor="none", zorder=2))
    fig.text(x + 0.018, Y0 + 0.070, lab, fontsize=9.4, fontweight="bold",
             color=LGREY, transform=fig.transFigure, zorder=4)
    fig.text(x + 0.018, Y0 + 0.0385, val, fontsize=31, fontweight="bold",
             color=NAVY, transform=fig.transFigure, zorder=4, va="center")
    fig.text(x + 0.018, Y0 + 0.0145, sub, fontsize=9.1, color=GREY,
             transform=fig.transFigure, zorder=4)

# ============================================================== ROW 2 =======
R2Y, R2H = 0.440, 0.310

# ---- 2A: attrition by department -----------------------------------------
card(0.016, R2Y, 0.300, R2H)
ctitle(0.032, R2Y + R2H - 0.038, "Attrition by Department",
       "rate \u00b7 headcount \u00b7 leavers")
depts  = ["Research &\nDevelopment", "Sales", "Human\nResources"]
tot    = [961, 446, 63]
leftn  = [133, 92, 12]
rate_d = [13.8, 20.6, 19.0]
ax = fig.add_axes([0.075, R2Y + 0.052, 0.218, 0.176]); clean(ax)
yp = np.arange(len(depts))
ax.barh(yp, tot, height=0.58, color="#E4ECF6", edgecolor="none", zorder=2)
ax.barh(yp, leftn, height=0.58, color=RED, edgecolor="none", zorder=3)
ax.set_yticks(yp); ax.set_yticklabels(depts, fontsize=9.4, color="#33414F")
ax.set_xticks([]); ax.set_ylim(len(depts) - 0.4, -0.6)
for i, (l, t, r) in enumerate(zip(leftn, tot, rate_d)):
    # fixed right-hand columns so long bars can't collide with their labels
    ax.text(1120, i, f"{r}%", va="center", ha="right", fontsize=11.4,
            fontweight="bold", color=NAVY, zorder=4)
    ax.text(1620, i, f"{l} of {t}", va="center", ha="right", fontsize=8.6,
            color=LGREY, zorder=4)
ax.set_xlim(0, 1640)
caption(0.032, R2Y + 0.034,
        "Red = leavers.  Sales has the highest rate (20.6%);",
        "R&D the highest volume (133 of 237 leavers).")

# ---- 2B: OVERTIME — headline donut ---------------------------------------
card(0.326, R2Y, 0.300, R2H, fc="#FFF6F6", ec="#F6C9CB")
fig.add_artist(Rectangle((0.326, R2Y), 0.0042, R2H, transform=fig.transFigure,
                         facecolor=RED, edgecolor="none", zorder=2))
ctitle(0.344, R2Y + R2H - 0.038, "Overtime \u2014 Strongest Driver",
       "risk multiple 2.9\u00d7  \u00b7  controllable lever")
ax = fig.add_axes([0.348, R2Y + 0.055, 0.128, 0.176]); clean(ax)
ax.pie([30.5, 69.5], colors=[RED, "#E4ECF6"], startangle=90, counterclock=False,
       wedgeprops=dict(width=0.36, edgecolor="white", linewidth=2.4))
ax.text(0, 0.10, "30.5%", ha="center", va="center", fontsize=21,
        fontweight="bold", color=RED)
ax.text(0, -0.22, "on overtime", ha="center", va="center", fontsize=9.2,
        color=GREY)
ax.set_aspect("equal")

bx = 0.484
fig.text(bx, R2Y + 0.212, "WORKS OVERTIME", fontsize=8.4, fontweight="bold",
         color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(bx, R2Y + 0.176, "30.5%", fontsize=19, fontweight="bold", color=RED,
         transform=fig.transFigure, zorder=4, va="center")
fig.text(bx + 0.052, R2Y + 0.176, "127 of 416 left", fontsize=9, color=GREY,
         transform=fig.transFigure, zorder=4, va="center")
fig.text(bx, R2Y + 0.126, "NO OVERTIME", fontsize=8.4, fontweight="bold",
         color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(bx, R2Y + 0.090, "10.4%", fontsize=19, fontweight="bold", color=BLUE,
         transform=fig.transFigure, zorder=4, va="center")
fig.text(bx + 0.052, R2Y + 0.090, "110 of 1,054 left", fontsize=9, color=GREY,
         transform=fig.transFigure, zorder=4, va="center")
fig.add_artist(Rectangle((bx, R2Y + 0.052), 0.126, 0.0008,
                         transform=fig.transFigure, facecolor="#F6C9CB",
                         edgecolor="none", zorder=4))
caption(0.344, R2Y + 0.034,
        "Highest-exposure segment: R&D Lab Technicians on overtime \u2014",
        "50% attrition (31 of 62). A specific, actionable population.",
        color="#B5413F")

# ---- 2C: job role by rate -------------------------------------------------
card(0.636, R2Y, 0.348, R2H)
ctitle(0.652, R2Y + R2H - 0.038, "Attrition Rate by Job Role",
       "top 6 of 9  \u00b7  lift shown against 16.12% baseline")
roles = ["Sales Representative", "Laboratory Technician", "Human Resources",
         "Sales Executive", "Research Scientist", "Manufacturing Director"]
rr    = [39.8, 23.9, 23.1, 17.5, 16.1, 6.9]
ax = fig.add_axes([0.788, R2Y + 0.052, 0.166, 0.186]); clean(ax)
yp = np.arange(len(roles))
cols = [RED if r >= 25 else (AMBER if r >= 16.12 else GREEN) for r in rr]
ax.barh(yp, rr, height=0.60, color=cols, edgecolor="none", zorder=3)
ax.axvline(16.12, color=NAVY, lw=1.3, ls=(0, (4, 3)), zorder=4, alpha=.75)
ax.set_yticks(yp); ax.set_yticklabels(roles, fontsize=9.4, color="#33414F")
ax.set_xticks([]); ax.set_ylim(len(roles) - 0.4, -0.6); ax.set_xlim(0, 49)
for i, r in enumerate(rr):
    ax.text(r + 1.3, i, f"{r}%", va="center", fontsize=11, fontweight="bold",
            color=NAVY, zorder=5)
caption(0.652, R2Y + 0.034,
        "Dashed line = company baseline.  Sales Reps run +23.7 pp above it",
        "\u2014 the clear intervention target.  Full lift breakdown below.")

# ============================================================== ROW 3 =======
R3Y, R3H = 0.108, 0.300

# ---- 3A: tenure decay curve ----------------------------------------------
card(0.016, R3Y, 0.234, R3H)
ctitle(0.032, R3Y + R3H - 0.038, "Early-Tenure Risk Curve",
       "attrition rate by years at company")
bands = ["<1 yr", "1-2", "3-5", "6-10", "11-20", "20+"]
brate = [36.4, 28.9, 17.2, 10.1, 6.2, 3.4]
ax = fig.add_axes([0.040, R3Y + 0.078, 0.204, 0.144]); clean(ax)
bcol = [RED, RED, AMBER, BLUE, BLUE, GREEN]
ax.bar(bands, brate, width=0.64, color=bcol, edgecolor="none", zorder=3)
ax.set_xticks(np.arange(len(bands)))
ax.set_xticklabels(bands, fontsize=9, color="#33414F")
ax.set_yticks([]); ax.set_ylim(0, 46)
for i, r in enumerate(brate):
    ax.text(i, r + 1.3, f"{r}%", ha="center", fontsize=9.6, fontweight="bold",
            color=NAVY, zorder=4)
ax.text(2.5, 42.6, "Risk decays monotonically with tenure",
        ha="center", fontsize=8.6, style="italic", color=GREY, zorder=4)
caption(0.032, R3Y + 0.034,
        "~56% of all leavers exit within their first three years \u2014",
        "an onboarding and early-tenure problem, not a late-career one.")

# ---- 3B: attrition lift diverging ----------------------------------------
card(0.260, R3Y, 0.234, R3H)
ctitle(0.276, R3Y + R3H - 0.038, "Attrition Lift vs Baseline",
       "percentage points above / below 16.12%")
lift_seg = ["Sales Rep", "Lab Tech", "Human Resources", "Sales Exec",
            "Research Sci.", "Mfg Director"]
lift_val = [23.7, 7.8, 7.0, 1.4, -0.1, -9.2]
ax = fig.add_axes([0.344, R3Y + 0.078, 0.144, 0.144]); clean(ax)
yp = np.arange(len(lift_seg))
lcol = [RED if v >= 5 else (AMBER if v > 0 else GREEN) for v in lift_val]
ax.barh(yp, lift_val, height=0.58, color=lcol, edgecolor="none", zorder=3)
ax.axvline(0, color=NAVY, lw=1.6, zorder=5)
ax.set_yticks(yp); ax.set_yticklabels(lift_seg, fontsize=8.8, color="#33414F")
ax.set_xticks([]); ax.set_ylim(len(lift_seg) - 0.4, -0.6)
ax.set_xlim(-17, 33)
for i, v in enumerate(lift_val):
    off = 1.3 if v >= 0 else -1.3
    ha = "left" if v >= 0 else "right"
    ax.text(v + off, i, f"{v:+.1f}", va="center", ha=ha, fontsize=9.4,
            fontweight="bold", color=NAVY if v < 0 else RED, zorder=6)
caption(0.276, R3Y + 0.034,
        "Red = attrits worse than the company baseline.",
        "Rate tells you where to intervene.")

# ---- 3C: pay gap ----------------------------------------------------------
card(0.504, R3Y, 0.222, R3H)
ctitle(0.520, R3Y + R3H - 0.038, "Pay Gap \u2014 Stayers vs Leavers",
       "avg monthly income  \u00b7  29.9% differential")
ax = fig.add_axes([0.522, R3Y + 0.082, 0.108, 0.138]); clean(ax)
bars = ax.bar(["Stayers", "Leavers"], [6833, 4787], width=0.46,
              color=[GREEN, RED], edgecolor="none", zorder=3)
ax.set_yticks([]); ax.set_ylim(0, 9200)
ax.set_xlim(-0.62, 1.62)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Stayers", "Leavers"], fontsize=9.4, color="#33414F")
for b, v in zip(bars, [6833, 4787]):
    ax.text(b.get_x() + b.get_width() / 2, v + 260, f"\\${v:,}", ha="center",
            fontsize=11.2, fontweight="bold", color=NAVY, zorder=4)
# delta callout sits in the card's free right-hand column, clear of the plot
fig.text(0.648, R3Y + 0.176, "\u201329.9%", fontsize=16, fontweight="bold",
         color=RED, transform=fig.transFigure, zorder=6, va="center")
fig.text(0.648, R3Y + 0.150, "lower pay", fontsize=8.8, color=GREY,
         transform=fig.transFigure, zorder=6, va="center")
fig.text(0.648, R3Y + 0.132, "for leavers", fontsize=8.8, color=GREY,
         transform=fig.transFigure, zorder=6, va="center")
fig.add_artist(Rectangle((0.648, R3Y + 0.114), 0.062, 0.0009,
                         transform=fig.transFigure, facecolor=LINE,
                         edgecolor="none", zorder=6))
fig.text(0.648, R3Y + 0.094, "29.9% below the", fontsize=8.2, color=LGREY,
         transform=fig.transFigure, zorder=6, va="center")
fig.text(0.648, R3Y + 0.078, "stayer average", fontsize=8.2, color=LGREY,
         transform=fig.transFigure, zorder=6, va="center")
caption(0.520, R3Y + 0.034,
        "Correlated, not causal \u2014 confounded by job level.",
        "Leavers = 16.1% of headcount but ~11.8% of payroll.")

# ---- 3D: turnover cost + risk --------------------------------------------
card(0.736, R3Y, 0.248, R3H, fc=PAPER)
ctitle(0.752, R3Y + R3H - 0.038, "Financial Exposure & Risk",
       "cost of turnover  \u00b7  forward-looking score")

fig.text(0.752, R3Y + 0.212, "TOTAL TURNOVER COST", fontsize=8.6,
         fontweight="bold", color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(0.752, R3Y + 0.172, "\\$13.6M", fontsize=26, fontweight="bold",
         color=NAVY, transform=fig.transFigure, zorder=4, va="center")
fig.text(0.848, R3Y + 0.190, "\\$57,444 per leaver", fontsize=9.2, color=GREY,
         transform=fig.transFigure, zorder=4, va="center")
fig.text(0.848, R3Y + 0.168, "at 1.0\u00d7 replacement", fontsize=8.6,
         color=LGREY, transform=fig.transFigure, zorder=4, va="center")

fig.add_artist(Rectangle((0.752, R3Y + 0.146), 0.216, 0.0008,
                         transform=fig.transFigure, facecolor=LINE,
                         edgecolor="none", zorder=4))
fig.text(0.752, R3Y + 0.118, "PAYROLL LOST", fontsize=8.6, fontweight="bold",
         color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(0.752, R3Y + 0.088, "11.8%", fontsize=17, fontweight="bold",
         color=AMBER, transform=fig.transFigure, zorder=4, va="center")
fig.text(0.848, R3Y + 0.118, "RISK BAND DISTRIBUTION", fontsize=8.6,
         fontweight="bold", color=LGREY, transform=fig.transFigure, zorder=4)

# RAG risk strip
rag = [("Critical", 0.11, RED), ("High", 0.17, AMBER),
       ("Medium", 0.34, SKY), ("Low", 0.38, GREEN)]
sx, sw = 0.848, 0.120
cur = sx
for nm, frac, col in rag:
    w = sw * frac
    fig.add_artist(Rectangle((cur, R3Y + 0.074), w, 0.020,
                             transform=fig.transFigure, facecolor=col,
                             edgecolor="none", zorder=4))
    cur += w
fig.text(0.848, R3Y + 0.055, "Critical 11%  \u00b7  High 17%", fontsize=8.2,
         color=GREY, transform=fig.transFigure, zorder=4)

caption(0.752, R3Y + 0.034,
        "Risk score weights (0\u2013100): overtime 35, tenure <1yr 25,",
        "job level 1 \u00d715, no stock option \u00d710, low satisfaction \u00d78.")

# ======================================================== slicer strip =======
fig.text(0.016, 0.086, "FILTERS   \u25ba", fontsize=8.6, fontweight="bold",
         color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(0.083, 0.086, "Department      Job Role      OverTime      Tenure Band      "
                       "Income Band      Age Band      Gender      Education",
         fontsize=8.6, color=BLUE, transform=fig.transFigure, zorder=4)
fig.text(0.984, 0.086, "All visuals cross-filter  \u00b7  click any bar to slice the page",
         fontsize=8.6, style="italic", color=LGREY, ha="right",
         transform=fig.transFigure, zorder=4)

# ============================================================== footer =======
fig.add_artist(Rectangle((0.016, 0.066), 0.968, 0.0009,
                         transform=fig.transFigure, facecolor=LINE,
                         edgecolor="none", zorder=4))
fig.text(0.016, 0.040, "Sources & method", fontsize=8.8, fontweight="bold",
         color=GREY, transform=fig.transFigure, zorder=4)
fig.text(0.016, 0.019,
         "Dataset: IBM HR Analytics Employee Attrition & Performance (fictional sample). "
         "Turnover cost = leaver annual salary \u00d7 1.0\u00d7 replacement multiplier "
         "(assumption, tunable: 0.5\u00d7 = \\$6.8M  \u00b7  2.0\u00d7 = \\$27.2M).  "
         "Risk weights are explicit and intended to be retuned with an HR partner.",
         fontsize=8.2, color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(0.016, 0.003,
         "Limitations: no hire/termination dates (no time-series or YoY); voluntary vs "
         "involuntary not distinguished; observational data \u2014 findings are correlational, not causal.",
         fontsize=8.2, color=LGREY, transform=fig.transFigure, zorder=4)
fig.text(0.984, 0.040, "Layout preview rendered from specification",
         fontsize=8.4, style="italic", color="#AAB4BF", ha="right",
         transform=fig.transFigure, zorder=4)

out = "docs/dashboard_preview.png"
fig.savefig(out, dpi=150, facecolor=WELL)
print(f"saved {out}")
