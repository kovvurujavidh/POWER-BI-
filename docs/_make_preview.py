"""Generate docs/dashboard_preview.png - HR Analytics Dashboard layout preview.
Visual mockup of the Power BI report page (not a Power BI screenshot)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

NAVY, BLUE, LIGHT, GREY = "#1F4E79", "#2E75B6", "#EAF1F8", "#5A5A5A"
RED, GREEN, ORANGE = "#C0392B", "#27AE60", "#E67E22"

fig = plt.figure(figsize=(16, 9), dpi=120)
fig.patch.set_facecolor("#FFFFFF")

def card(x, y, w, h, fc="#FFFFFF", ec="#D9D9D9"):
    fig.patches.append(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.008",
        linewidth=1, edgecolor=ec, facecolor=fc,
        transform=fig.transFigure, zorder=1))

def title(x, y, t):
    fig.text(x, y, t, fontsize=12.5, fontweight="bold", color=NAVY,
             transform=fig.transFigure, zorder=3)

# ---------- header ----------
fig.text(0.02, 0.962, "HR Analytics Dashboard", fontsize=25, fontweight="bold",
         color=NAVY, transform=fig.transFigure, zorder=3)
fig.text(0.02, 0.935, "Employee Attrition  |  IBM HR Dataset  |  1,470 employee records",
         fontsize=11.5, color=GREY, transform=fig.transFigure, zorder=3)
fig.text(0.98, 0.955, "Kovvuru Javidh  |  Power BI  |  DAX  |  Power Query",
         fontsize=10, color=GREY, ha="right", transform=fig.transFigure, zorder=3)
fig.add_artist(plt.Line2D([0.02, 0.98], [0.918, 0.918], color=BLUE, lw=2,
                          transform=fig.transFigure, zorder=2))

# ---------- KPI cards ----------
kpis = [("1,470", "Total Employees", BLUE),
        ("16.12%", "Attrition Rate", RED),
        ("$6,503", "Avg Monthly Income", GREEN),
        ("7.01", "Avg Years at Company", ORANGE)]
x0, cw, gap = 0.02, 0.1525, 0.014
for i, (val, lab, col) in enumerate(kpis):
    x = x0 + i * (cw + gap)
    card(x, 0.775, cw, 0.125, LIGHT, "#C5D8EC")
    fig.text(x + cw / 2, 0.845, val, fontsize=27, fontweight="bold",
             color=col, ha="center", transform=fig.transFigure, zorder=3)
    fig.text(x + cw / 2, 0.797, lab, fontsize=10.5, color=GREY,
             ha="center", transform=fig.transFigure, zorder=3)

# ---------- Row 2 : Attrition by department ----------
card(0.02, 0.435, 0.30, 0.315)
title(0.035, 0.718, "Attrition by Department")
depts = ["Research &\nDevelopment", "Sales", "Human\nResources"]
left = [133, 92, 12]; tot = [961, 446, 63]
ax1 = fig.add_axes([0.055, 0.475, 0.245, 0.205]); ax1.set_facecolor("none")
ypos = np.arange(len(depts))
ax1.barh(ypos, tot, color="#D6E4F0", height=0.55, label="Retained")
ax1.barh(ypos, left, color=RED, height=0.55, label="Left")
ax1.set_yticks(ypos); ax1.set_yticklabels(depts, fontsize=8.5, color="#333")
ax1.invert_yaxis(); ax1.set_xticks([])
for s in ax1.spines.values(): s.set_visible(False)
for i, (l, t) in enumerate(zip(left, tot)):
    ax1.text(t + 18, i, f"{l}/{t}  ({l/t*100:.1f}%)", va="center",
             fontsize=8.5, color=NAVY, fontweight="bold")
ax1.legend(fontsize=7.5, loc="lower right", frameon=False)

# ---------- Row 2 : OverTime donut ----------
card(0.335, 0.435, 0.29, 0.315)
title(0.35, 0.718, "Attrition by OverTime")
ax2 = fig.add_axes([0.375, 0.465, 0.21, 0.225]); ax2.set_facecolor("none")
ax2.pie([30.5, 69.5], colors=[RED, "#D6E4F0"], startangle=90,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
ax2.text(0, 0.08, "30.5%", ha="center", va="center", fontsize=19,
         fontweight="bold", color=RED)
ax2.text(0, -0.20, "Overtime", ha="center", va="center", fontsize=9.5, color=GREY)
ax2.set_aspect("equal")
fig.text(0.585, 0.635, "Overtime staff", fontsize=9, color=GREY,
         transform=fig.transFigure, zorder=3)
fig.text(0.585, 0.612, "127 / 416 left", fontsize=10, color=RED,
         fontweight="bold", transform=fig.transFigure, zorder=3)
fig.text(0.585, 0.575, "Non-overtime", fontsize=9, color=GREY,
         transform=fig.transFigure, zorder=3)
fig.text(0.585, 0.552, "110 / 1,054 left", fontsize=10, color=NAVY,
         fontweight="bold", transform=fig.transFigure, zorder=3)
fig.text(0.585, 0.505, "~3x higher risk", fontsize=9.5, color=RED,
         style="italic", transform=fig.transFigure, zorder=3)

# ---------- Row 2 : Job role ----------
card(0.64, 0.435, 0.34, 0.315)
title(0.655, 0.718, "Attrition Rate by Job Role (top 6)")
roles = ["Sales Executive", "Research Scientist", "Laboratory Technician",
         "Sales Representative", "Human Resources", "Manager"]
rate = [15.7, 14.5, 16.6, 40.0, 23.1, 5.0]
ax3 = fig.add_axes([0.775, 0.475, 0.185, 0.205]); ax3.set_facecolor("none")
yp = np.arange(len(roles))
cols = [RED if r >= 25 else (ORANGE if r >= 16 else BLUE) for r in rate]
ax3.barh(yp, rate, color=cols, height=0.6)
ax3.set_yticks(yp); ax3.set_yticklabels(roles, fontsize=8.5, color="#333")
ax3.invert_yaxis(); ax3.set_xticks([])
for s in ax3.spines.values(): s.set_visible(False)
for i, r in enumerate(rate):
    ax3.text(r + 1, i, f"{r}%", va="center", fontsize=8.5,
             color=NAVY, fontweight="bold")
ax3.set_xlim(0, 48)

# ---------- Row 3 : tenure ----------
card(0.02, 0.115, 0.30, 0.295)
title(0.035, 0.383, "Attrition Rate by Tenure Band")
bands = ["0-2 yrs", "3-4 yrs", "5-9 yrs", "10-19 yrs", "20+ yrs"]
brate = [38.0, 22.0, 10.5, 6.0, 3.5]
ax4 = fig.add_axes([0.055, 0.155, 0.245, 0.185]); ax4.set_facecolor("none")
ax4.bar(bands, brate, color=BLUE, width=0.6)
ax4.set_xticklabels(bands, fontsize=8, color="#333", rotation=0)
ax4.set_yticks([])
for s in ax4.spines.values(): s.set_visible(False)
for i, r in enumerate(brate):
    ax4.text(i, r + 1.2, f"{r}%", ha="center", fontsize=8.5,
             color=NAVY, fontweight="bold")

# ---------- Row 3 : income ----------
card(0.335, 0.115, 0.29, 0.295)
title(0.35, 0.383, "Avg Monthly Income by Attrition Status")
ax5 = fig.add_axes([0.375, 0.155, 0.21, 0.185]); ax5.set_facecolor("none")
ax5.bar(["Stayed", "Left"], [6447, 4787], color=[GREEN, RED], width=0.5)
ax5.set_yticks([])
for s in ax5.spines.values(): s.set_visible(False)
for i, v in enumerate([6447, 4787]):
    ax5.text(i, v + 130, f"${v:,}", ha="center", fontsize=10,
             fontweight="bold", color=NAVY)
ax5.set_xticklabels(["Stayed", "Left"], fontsize=9.5, color="#333")

# ---------- Row 3 : satisfaction matrix ----------
card(0.64, 0.115, 0.34, 0.295)
title(0.655, 0.383, "Job Satisfaction vs Attrition")
sat = ["Low", "Medium", "High", "Very High"]
stay = [276, 310, 324, 323]; leftv = [54, 59, 62, 62]
ax6 = fig.add_axes([0.70, 0.155, 0.26, 0.185]); ax6.set_facecolor("none")
xs = np.arange(4)
ax6.bar(xs - 0.19, stay, width=0.36, color=GREEN, label="Stayed")
ax6.bar(xs + 0.19, leftv, width=0.36, color=RED, label="Left")
ax6.set_xticks(xs); ax6.set_xticklabels(sat, fontsize=8.5, color="#333")
ax6.set_yticks([])
for s in ax6.spines.values(): s.set_visible(False)
ax6.legend(fontsize=7.5, frameon=False, loc="upper left")

# ---------- left slicer strip ----------
card(0.02, 0.115, 0.0, 0.0)  # noop keeps patch order stable

# ---------- footer ----------
fig.text(0.02, 0.045,
         "Cross-filtered: click any department to filter the full page.   "
         "Source: IBM HR Analytics Employee Attrition & Performance (1,470 records, 35 fields).",
         fontsize=9, color=GREY, transform=fig.transFigure, zorder=3)
fig.text(0.98, 0.045, "Layout preview rendered from dashboard specification",
         fontsize=8.5, color="#999999", style="italic", ha="right",
         transform=fig.transFigure, zorder=3)

fig.savefig("docs/dashboard_preview.png", dpi=120, facecolor="white",
            bbox_inches=None)
print("saved docs/dashboard_preview.png")
