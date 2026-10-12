"""Figure 2: raw skill-induced deltas vs rerun-null bands for the 16 pilot units.
Three stacked panels (trajectory, tool-use, failed-action efficiency component),
8 gemini-3.5-flash units then 8 MiniMax-M3 units. Reads data from the
first_measurement results.json files so the figure always matches the pipeline.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 7,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

C_GEM = '#0077BB'
C_MM = '#EE7733'
C_BAND = '#333333'

DOM_ORDER = ['cybersecurity', 'finance-economics', 'industrial-physical-systems',
             'mathematics-or-formal-reasoning', 'media-content-production',
             'natural-science', 'office-white-collar', 'software-engineering']
DOM_SHORT = ['cyber', 'finance', 'industr.', 'math', 'media', 'nat-sci', 'office', 'softw.']

def load(path):
    d = json.load(open(path))
    units = {sid.split('__')[1]: v for sid, v in d['skills'].items() if v.get('status') == 'ok'}
    return d['bands'], units

bands_g, units_g = load('first_measurement/results_gemini/results.json')
bands_m, units_m = load('first_measurement/results_minimax/results.json')

def series(units, key):
    out = []
    for dom in DOM_ORDER:
        v = units[dom]['deltas']
        out.append(v['eff']['failed_actions'] if key == 'eff_failed' else v[key])
    return out

panels = [
    ('traj', r'(a) trajectory shift $\Delta_{\mathrm{traj}}$',
     [bands_g['traj']['band'], bands_m['traj']['band']], (0, 0.85)),
    ('tool', r'(b) tool-use shift $\Delta_{\mathrm{tool}}$',
     [bands_g['tool']['band'], bands_m['tool']['band']], (0, 1.05)),
    ('eff_failed', r'(c) failed-action shift $\Delta_{\mathrm{eff}}$',
     [bands_g['eff_failed_actions']['band'], bands_m['eff_failed_actions']['band']], (-1.1, 1.75)),
]

vals_g = {k: series(units_g, k) for k, *_ in panels}
vals_m = {k: series(units_m, k) for k, *_ in panels}

fig, axes = plt.subplots(3, 1, figsize=(3.45, 3.9), sharex=True)
x = np.arange(16)

for ax, (key, title, bands, ylim) in zip(axes, panels):
    vals = vals_g[key] + vals_m[key]
    colors = [C_GEM] * 8 + [C_MM] * 8
    ax.bar(x, vals, 0.72, color=colors, edgecolor='white', linewidth=0.4, zorder=3)
    # per-config null-band segments
    ax.plot([-0.5, 7.5], [bands[0]] * 2, color=C_BAND, lw=1.0, ls=(0, (4, 2)), zorder=4)
    ax.plot([7.5, 15.5], [bands[1]] * 2, color=C_BAND, lw=1.0, ls=(0, (4, 2)), zorder=4)
    ax.axhline(0, color='#999999', lw=0.6, zorder=1)
    ax.set_ylim(*ylim)
    ax.set_title(title, fontsize=7, loc='left', pad=1.5)
    ax.tick_params(axis='y', pad=1)

# annotate the single qualifying bar (gemini industrial, index 2, panel c)
axc = axes[2]
axc.annotate('z = 1.42', xy=(2, 1.424), xytext=(3.1, 1.52), fontsize=6.5,
             color='#CC3311', arrowprops=dict(arrowstyle='-', color='#CC3311', lw=0.7))
axc.patches[2].set_edgecolor('#CC3311')
axc.patches[2].set_linewidth(1.1)

axes[0].text(3.5, 0.79, 'gemini-3.5-flash', fontsize=6.5, ha='center', color=C_GEM)
axes[0].text(11.5, 0.79, 'MiniMax-M3', fontsize=6.5, ha='center', color=C_MM)
axes[0].annotate('null band', xy=(14.9, 0.685), xytext=(14.9, 0.52), fontsize=6,
                 color=C_BAND, ha='right',
                 arrowprops=dict(arrowstyle='-', color=C_BAND, lw=0.6))
axes[2].set_xticks(x)
axes[2].set_xticklabels(DOM_SHORT * 2, rotation=45, ha='right')
for ax in axes:
    ax.axvline(7.5, color='#CCCCCC', lw=0.8, zorder=0)
axes[2].set_xlim(-0.6, 15.6)

plt.tight_layout(pad=0.2, h_pad=0.4)
plt.savefig('figures/figure_pilot_bars.pdf')
plt.savefig('figures/figure_pilot_bars.png', dpi=300)
print('saved figures/figure_pilot_bars.{pdf,png}')
