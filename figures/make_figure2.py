"""Figure 1: Illustrative divergence in behavioral delta at equal task completion.

Single-panel grouped bar. Two skills (A=checklist, B=restructure) yield
identical completion rates (equal grey bars) but diverge on induced behavioral
shift |Delta| := max_j z_j (the largest per-dimension standardized delta;
Section 4): Skill A qualifies on no dimension (z_j <= 1 throughout),
Skill B's |Delta| exceeds the qualification threshold.

Design notes (v1.7 — z-scale, closes reviewer W4):
- The delta axis is now z (standardized per-dimension deltas), NOT raw delta
  magnitude. The bar values are max_j z_j, which are reproducible from the
  Appendix A worked example: z_A = (0.20, 0.10, 0.03, 0.07) -> |Delta_A| = 0.20;
  z_B = (2.20, 2.00, 0.50, 0.13) -> |Delta_B| = 2.20. The previous raw-scale
  values (0.17/0.72) matched no stated reduction and drew a reviewer flag.
- The shaded region is the qualification threshold z = 1 (i.e., a delta at
  the 95th-percentile null band of its own dimension), drawn ONLY under the
  delta bars: it is a delta-only concept and must not contaminate the
  completion bars.
- No y-axis label: the legend names both metrics ('Completion rate' /
  'Behavioral shift |Delta| (max z)'), so a generic 'value' label adds nothing.
- No arc arrow: the height difference + value labels are self-evident.
  Annotate the non-obvious fact (same completion, via the bracket).
The body text (Section 1) forward-references Section 4 for the formal
definition. Values remain schematic, not empirical; the figure is
regenerated from measured data by the First Measurement protocol.
ARS visualization_agent APA 7.0 + colorblind-safe palette.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 9,
    'axes.titlesize': 11,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 7.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

C_GREY = '#BBBBBB'   # completion (neutral: equal)
C_A    = '#0077BB'   # Skill A delta (blue)
C_B    = '#EE7733'   # Skill B delta (orange)
C_BAND = '#EEEEEE'   # null-control band
C_MUTE = '#555555'

fig, ax = plt.subplots(figsize=(3.4, 2.7))

groups = ['Skill A\n(checklist)', 'Skill B\n(restructure)']
completion = [0.62, 0.62]
# z-scale: |Delta| := max_j z_j, reproducible from Appendix A's worked example
delta = [0.20, 2.20]
x = np.arange(len(groups))
w = 0.34

# Qualification threshold z=1 drawn ONLY under the delta bars (delta-only
# concept: must not contaminate the completion bars). Drawn first so bars
# sit on top.
ax.bar(x + w/2, [1.0, 1.0], w, color=C_BAND, alpha=0.85,
       edgecolor='none', zorder=0)
ax.text(1 + w/2, 0.5, 'qualification\nthreshold ($z{=}1$)', fontsize=6.5,
        color=C_MUTE, va='center', ha='center')

# Completion bars (grey, equal height = same completion)
ax.bar(x - w/2, completion, w, color=C_GREY, edgecolor='white', linewidth=0.8, zorder=3)
# Delta bars (colored: A blue, B orange) drawn on top of the band rectangles
ax.bar(x + w/2, delta, w, color=[C_A, C_B], edgecolor='white', linewidth=0.8, zorder=3)

# Bracket: "same completion rate" above the two equal grey bars (annotate the
# non-obvious fact; the obvious delta difference shows itself via 4x heights)
yb = 0.70
ax.plot([x[0]-w/2, x[1]-w/2], [yb, yb], color=C_MUTE, lw=1.0, zorder=4)
ax.plot([x[0]-w/2, x[0]-w/2], [yb-0.02, yb], color=C_MUTE, lw=1.0, zorder=4)
ax.plot([x[1]-w/2, x[1]-w/2], [yb-0.02, yb], color=C_MUTE, lw=1.0, zorder=4)
ax.text((x[0]+x[1])/2 - w/2, yb+0.03, 'same completion rate',
        ha='center', fontsize=7.5, color=C_MUTE)

# Value labels on delta bars
ax.text(x[0]+w/2, 0.20+0.04, '0.20', ha='center', fontsize=7.5, color=C_A, fontweight='bold')
ax.text(x[1]+w/2, 2.20+0.04, '2.20', ha='center', fontsize=7.5, color=C_B, fontweight='bold')
# Value labels on completion bars
ax.text(x[0]-w/2, 0.62+0.04, '0.62', ha='center', fontsize=7.5, color=C_MUTE)
ax.text(x[1]-w/2, 0.62+0.04, '0.62', ha='center', fontsize=7.5, color=C_MUTE)

ax.set_xticks(x)
ax.set_xticklabels(groups)
ax.set_ylim(0, 2.65)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(['0', '1', '2'])
# No y-axis label: the legend names both metrics
ax.legend([plt.Rectangle((0,0),1,1,fc=C_GREY), plt.Rectangle((0,0),1,1,fc=C_A)],
          ['Completion rate', r'Behavioral shift $|\Delta|$ ($\max_j z_j$)'],
          loc='upper left', frameon=False, fontsize=7,
          handlelength=1.2, handletextpad=0.5, borderaxespad=0.3)

plt.tight_layout(pad=0.3)
plt.savefig('figures/figure_delta_divergence.pdf')
plt.savefig('figures/figure_delta_divergence.png', dpi=300)
print("saved figures/figure_delta_divergence.{pdf,png}")
