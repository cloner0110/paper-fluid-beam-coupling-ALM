"""
Paper versions of the beam-in-channel study figures (Section 5).

Reviewer round 2 (comments 24, 27, 28, 29):
  * each sensitivity panel carries its own legend directly beneath its axes,
    so no stacked legend strips are needed below the figure;
  * the kernel-width legend no longer labels the widest kernel an "outlier";
  * the sampling-offset legend drops the unexplained (x N) multipliers;
  * the beam-mesh legend carries no "base" tag, because the thesis legend
    marks N_b = 80 as base while the text gives N_b = 20 (flagged to author);
  * the verification legend lists only the three studies that form the band.

Data and palette are read from the thesis plotting tree, which is left
untouched. Run with python3.11 (matplotlib is not installed for python3):

    python3.11 figures/scripts/plot_beamtunnel_studies.py
"""
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

THESIS_SCRIPTS = '/Volumes/OpenFOAM/tmp/Thesis/beamInTunnel/plots/scripts'
sys.path.insert(0, THESIS_SCRIPTS)
from _style import (apply_style, load_dat, DATA,  # noqa: E402
                    C_PRESENT, C_RED, C_MAGENTA, C_REF, DASH_PRESENT)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Panels are drawn at 1.25x their printed size, so every font below prints
# at 0.8 of the stated size (labels ~7.6 pt, ticks ~6.8 pt, legend ~6.4 pt).
FONTS = {
    'font.family': 'serif',
    'axes.labelsize': 9.5,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
    'legend.fontsize': 8.0,
    'mathtext.fontset': 'dejavuserif',
}
LW = 1.4

MESH = [
    ("mesh_xxcoarse.dat", r'Ultra-coarse ($19\times5$)',  '#6A0909', (2, 2)),
    ("mesh_xcoarse.dat",  r'Extra-coarse ($38\times10$)', '#FF4500', (4, 1.5)),
    ("mesh_coarse.dat",   r'Coarse ($75\times19$)',       C_RED,     (6, 3)),
    ("mesh_base.dat",     r'Base ($150\times38$)',        C_PRESENT, DASH_PRESENT),
    ("mesh_fine.dat",     r'Fine ($300\times76$)',        C_MAGENTA, (1.5, 2.0)),
]
BMS = [
    ("bms_xcoarse_20.dat", r'$N_b = 20$', '#FF4500', (4, 1.5)),
    ("bms_coarse_40.dat",  r'$N_b = 40$',        C_RED,     (6, 3)),
    ("bms_base_80.dat",    r'$N_b = 80$',        C_PRESENT, DASH_PRESENT),
    ("bms_fine_160.dat",   r'$N_b = 160$',       C_MAGENTA, (1.5, 2.0)),
]
DT = [
    ("dt_4e-05.dat", r"$4\times10^{-5}$",        '#4D0099', (8, 2, 2, 2, 2, 2)),
    ("dt_5e-05.dat", r"$5\times10^{-5}$",        '#9900CC', (8, 3)),
    ("dt_1e-04.dat", r"$1\times10^{-4}$ (base)", C_PRESENT, DASH_PRESENT),
    ("dt_2e-04.dat", r"$2\times10^{-4}$",        '#4DAF4A', (5, 2, 5, 2)),
    ("dt_5e-04.dat", r"$5\times10^{-4}$",        '#FF7F00', (4, 2)),
    ("dt_1e-03.dat", r"$1\times10^{-3}$",        C_RED,     (6, 3)),
    ("dt_2e-03.dat", r"$2\times10^{-3}$",        '#A52A2A', (3, 1, 3, 1)),
    ("dt_5e-03.dat", r"$5\times10^{-3}$",        '#8B4513', (2, 1, 2, 1)),
    ("dt_1e-02.dat", r"$1\times10^{-2}$",        '#1A1A1A', (4, 1, 1, 1)),
    ("dt_2e-02.dat", r"$2\times10^{-2}$",        '#696969', (2, 2)),
]
EPS = [
    ("eps_3e-4.dat",   r'$\varepsilon = 1.12\,\Delta x = 0.75\,a$', C_RED, (8, 3)),
    ("eps_4e-4.dat",   r'$\varepsilon = 1.50\,\Delta x = 1.00\,a$', '#FF7F00', (6, 3)),
    ("eps_6e-4.dat",   r'$\varepsilon = 2.25\,\Delta x = 1.50\,a$ (base)', C_PRESENT, DASH_PRESENT),
    ("eps_1e-3.dat",   r'$\varepsilon = 3.75\,\Delta x = 2.50\,a$', C_MAGENTA, (4, 2)),
    ("eps_1p5e-3.dat", r'$\varepsilon = 5.62\,\Delta x = 3.75\,a$ (reaches top boundary)', C_REF, (1.5, 2.0)),
]
SAMPLING = [
    ("sampling_dist1.dat", r"$r_s = 0.53$ mm",          C_RED,     (6, 3)),
    ("sampling_dist2.dat", r"$r_s = 1.59$ mm",          '#FF7F00', (6, 2.5, 1.5, 2.5)),
    ("sampling_dist3.dat", r"$r_s = 3.18$ mm (base)",   C_PRESENT, (4, 2)),
    ("sampling_dist5.dat", r"$r_s = 3.71$ mm",          '#4DAF4A', (5, 2)),
    ("sampling_dist6.dat", r"$r_s = 4.77$ mm",          C_MAGENTA, (3, 1, 3, 1)),
    ("sampling_dist4.dat", r"$r_s = 6.36$ mm (upstream of inlet)", C_REF, (1.5, 2.0)),
]


def study_panel(cases, fname, figsize, axrect, ncol, legend_top, title=None):
    """One panel with its legend beneath the axes, at a fixed layout so that
    panels sharing a figure row line up exactly."""
    plt.rcParams.update(FONTS)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes(axrect)
    apply_style(ax)
    handles = []
    for dat, label, color, dashes in cases:
        path = os.path.join(DATA, dat)
        data = load_dat(path)
        if data.size == 0:
            raise SystemExit(f'missing or empty data file: {path}')
        line, = ax.plot(data[:, 0], data[:, 1] * 1000, color=color, lw=LW,
                        dashes=dashes, label=label)
        handles.append(line)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Tip displacement (mm)')
    ax.set_xlim(0, 2.5)
    fig.legend(handles=handles, loc='upper center', ncol=ncol,
               bbox_to_anchor=(0.5, legend_top), frameon=False,
               handlelength=2.6, handletextpad=0.5, columnspacing=1.0,
               labelspacing=0.35, borderaxespad=0.0, title=title,
               title_fontsize=FONTS['legend.fontsize'])
    out = os.path.join(OUT, fname)
    fig.savefig(out)  # no tight bbox: identical canvases keep panels aligned
    plt.close(fig)
    print(f'Saved {out}')


# Figure 9: three panels at 0.32\textwidth (1.89 in printed).
F9 = dict(figsize=(2.36, 3.35), axrect=[0.215, 0.465, 0.745, 0.505], legend_top=0.315)
study_panel(MESH, 'mesh_study_paper.pdf', ncol=1, **F9)
study_panel(BMS,  'bms_study_paper.pdf',  ncol=1, **F9)
study_panel(DT,   'dt_study_paper.pdf',   ncol=2, title=r'$\Delta t$ (s)', **F9)

# Figure 10: two panels at 0.48\textwidth (2.83 in printed).
F10 = dict(figsize=(3.54, 3.45), axrect=[0.145, 0.42, 0.815, 0.555], legend_top=0.295)
study_panel(EPS,      'eps_study_paper.pdf',      ncol=1, **F10)
study_panel(SAMPLING, 'sampling_study_paper.pdf', ncol=1, **F10)

# Figure 7 legend: same canvas and fonts as the thesis strip, three studies.
plt.rcParams.update({'font.family': 'serif'})
handles = [
    mlines.Line2D([], [], color=C_PRESENT, lw=2.0, dashes=DASH_PRESENT,
                  label='Present work (ALM, 1D beam)'),
    mpatches.Patch(facecolor=C_REF, alpha=0.18, edgecolor=C_REF, linestyle='--',
                   label=('Reference range 4.7--6.0 mm '
                          '[Zhang et al. 2012; Long et al. 2021; Yan et al. 2023]')),
]
fig = plt.figure(figsize=(12, 1.2))
fig.legend(handles=handles, ncol=1, loc='center', frameon=False,
           handlelength=2.8, handletextpad=0.6, columnspacing=2.0, fontsize=14)
out = os.path.join(OUT, 'verificationLegend.pdf')
fig.savefig(out, bbox_inches='tight', pad_inches=0.05)
plt.close(fig)
print(f'Saved {out}')
