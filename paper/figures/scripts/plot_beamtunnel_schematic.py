"""
Paper version of the beam-in-channel schematic (Figure 5). The thesis note
under the channel said the domain is "one cell thick, effectively 2D"; that
parenthetical is removed because the text of Section 5 now describes the
one-cell-thick domain and its symmetry planes explicitly. Otherwise identical
to the thesis generator
PhD_thesis_UCD/Figures/Chapter5/gen_beamInTunnel_schematic.py.

    python3.11 figures/scripts/plot_beamtunnel_schematic.py
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath,amssymb,bm}",
    "font.family": "serif",
    "font.size": 11,
})

# ── canvas units (kept dimensionless for layout; physical SI values are
#    shown in the dimension labels below) ──────────────────────────────────
L = 4.0          # channel length aspect (physical: 0.04 m)
H = 1.0          # channel height aspect (physical: 0.01 m)
lam = 0.8        # beam length aspect (physical: 0.008 m)
tlf = 0.04       # beam thickness aspect (physical: 4e-4 m)
xroot = 1.0      # beam root x-position aspect (physical: 0.01 m = L/4)

# ── canvas ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8.6, 4.0))
ax.set_aspect("equal")
ax.axis("off")

# ── channel rectangle ───────────────────────────────────────────────────────
channel = Rectangle((0.0, 0.0), L, H, facecolor="#eaf3fb",
                    edgecolor="#1a1a2e", lw=1.2, zorder=1)
ax.add_patch(channel)

# ── upper boundary (symmetry plane): dot-dash line on top ───────────────────
ax.plot([0.0, L], [H, H], color="#1a1a2e", lw=1.4, ls="-.", zorder=4)
ax.text(L * 0.78, H + 0.06,
        r"upper wall: symmetry ($v_y = 0$)",
        ha="center", va="bottom", fontsize=10)

# ── lower wall (no-slip): hatched band ──────────────────────────────────────
wall_thk = 0.10
lower_wall = Rectangle((0.0, -wall_thk), L, wall_thk, facecolor="white",
                       edgecolor="#1a1a2e", lw=0.8, hatch="////", zorder=3)
ax.add_patch(lower_wall)
ax.text(L * 0.78, -wall_thk - 0.10,
        r"lower wall: no-slip ($\mathbf{v}=\mathbf{0}$)",
        ha="center", va="top", fontsize=10)

# ── beam (drawn with exaggerated thickness for visibility) ──────────────────
t_draw = 0.05
beam = Rectangle((xroot - t_draw / 2.0, 0.0), t_draw, lam,
                 facecolor="#1a1a2e", edgecolor="#1a1a2e", lw=0.8, zorder=6)
ax.add_patch(beam)

# The hatched no-slip wall below is itself the clamped support, so no separate
# clamp block is drawn (a solid one reads as a foot on the beam).

# tip marker
ax.plot(xroot, lam, "o", ms=4.5, color="#B71C1C",
        mfc="white", mec="#B71C1C", mew=1.4, zorder=8)
ax.annotate("free tip", xy=(xroot, lam), xytext=(xroot + 0.45, lam + 0.10),
            ha="left", va="center", fontsize=10, color="#B71C1C",
            arrowprops=dict(arrowstyle="-", color="#B71C1C", lw=0.8))

ax.annotate("clamped root", xy=(xroot - t_draw / 2.0, 0.02),
            xytext=(xroot - 0.55, -0.32),
            ha="right", va="top", fontsize=10, color="#1a1a2e",
            arrowprops=dict(arrowstyle="-", color="#1a1a2e", lw=0.8))

# ── beam length (vertical dimension on right of beam) ───────────────────────
dxR = 0.18
ax.annotate("", xy=(xroot + dxR, lam), xytext=(xroot + dxR, 0.0),
            arrowprops=dict(arrowstyle="<->", color="#1a1a2e", lw=1.0))
ax.text(xroot + dxR + 0.05, lam / 2.0,
        r"$b = 8\times10^{-3}~\mathrm{m}$",
        ha="left", va="center", fontsize=10)

# beam thickness callout (kept on the right of the beam: the inlet arrows fill
# the channel to the left of the root, which sits at x = L/4)
ax.annotate(r"$a = 4\times10^{-4}~\mathrm{m}$",
            xy=(xroot + t_draw / 2.0, lam * 0.80),
            xytext=(xroot + 0.38, lam * 0.80),
            ha="left", va="center", fontsize=10,
            arrowprops=dict(arrowstyle="-", color="#1a1a2e", lw=0.7))

# ── channel length L (below the channel) ────────────────────────────────────
yL = -wall_thk - 0.55
ax.annotate("", xy=(L, yL), xytext=(0.0, yL),
            arrowprops=dict(arrowstyle="<->", color="#1a1a2e", lw=1.0))
ax.text(L / 2.0, yL - 0.06, r"$L = 4\times10^{-2}~\mathrm{m}$",
        ha="center", va="top", fontsize=10)
for xt in [0.0, L]:
    ax.plot([xt, xt], [yL - 0.04, yL + 0.04], color="#1a1a2e", lw=0.8)

# ── transverse symmetry + initial condition note ────────────────────────────
ax.text(L / 2.0, yL - 0.42,
        r"transverse faces $z=\pm a/2$: symmetry; "
        r"fluid and beam initially at rest, beam straight",
        ha="center", va="top", fontsize=9, color="#444444")

# beam root marker on L axis
ax.plot([xroot, xroot], [yL + 0.04, -wall_thk - 0.02],
        color="#666666", lw=0.8, ls=":")
ax.text(xroot, yL + 0.10, r"$x = L/4$",
        ha="center", va="bottom", fontsize=9, color="#444444")

# ── channel height H (right side) ───────────────────────────────────────────
xH = L + 0.55
ax.annotate("", xy=(xH, H), xytext=(xH, 0.0),
            arrowprops=dict(arrowstyle="<->", color="#1a1a2e", lw=1.0))
ax.text(xH + 0.06, H / 2.0, r"$H = 1\times10^{-2}~\mathrm{m}$",
        ha="left", va="center", fontsize=10, rotation=90)
for yt in [0.0, H]:
    ax.plot([L + 0.02, xH + 0.02], [yt, yt],
            color="#888888", lw=0.6, ls=":")

# ── inlet velocity arrows (steady parabolic profile) ────────────────────────
# SI form: v_x(y) = -150 y^2 + 3 y (m/s), peak U_max = 0.015 m/s at y = H = 0.01 m
yi = np.linspace(0.08, H - 0.02, 7)
parab_max = 0.55
for yv in yi:
    u = parab_max * (-(yv) ** 2 + 2 * yv) / 1.0
    if u < 0.04:
        continue
    ax.annotate("", xy=(0.0 + u, yv), xytext=(-0.05, yv),
                arrowprops=dict(arrowstyle="-|>",
                                color="#1565C0", lw=1.2,
                                mutation_scale=9))
ax.text(-0.10, H + 0.10,
        r"inlet: $v_x(y)=-150\,y^2 + 3\,y~(\mathrm{m\,s^{-1}})$",
        ha="left", va="bottom", fontsize=10, color="#1565C0")
ax.text(-0.10, H + 0.42,
        r"peak $U_{\max}=1.5\times10^{-2}~\mathrm{m\,s^{-1}}$ at $y=H$",
        ha="left", va="bottom", fontsize=9, color="#1565C0")

# ── outlet ──────────────────────────────────────────────────────────────────
ax.annotate("", xy=(L + 0.32, H / 2.0), xytext=(L + 0.05, H / 2.0),
            arrowprops=dict(arrowstyle="-|>", color="#888888",
                            lw=1.0, mutation_scale=8))
ax.text(L + 0.18, H / 2.0 + 0.10, r"outlet: $p = 0$",
        ha="center", va="bottom", fontsize=10, color="#444444")

# ── origin marker at the inlet plane / lower wall intersection ──────────────
ax.plot(0.0, 0.0, "o", ms=3.6, color="#1a1a2e", zorder=9)
ax.text(-0.07, -0.03, r"$O$", ha="right", va="top", fontsize=10,
        color="#1a1a2e")

# ── coordinate axes (inside the channel, upper-right) ───────────────────────
ox, oy = L + 0.95, H * 0.10
ax.annotate("", xy=(ox + 0.30, oy), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color="#1a1a2e",
                            lw=1.0, mutation_scale=9))
ax.annotate("", xy=(ox, oy + 0.30), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color="#1a1a2e",
                            lw=1.0, mutation_scale=9))
ax.text(ox + 0.34, oy - 0.04, r"$x$", fontsize=10, va="center")
ax.text(ox - 0.06, oy + 0.34, r"$y$", fontsize=10, ha="right")

# ── axes limits ─────────────────────────────────────────────────────────────
ax.set_xlim(-0.40, L + 1.40)
ax.set_ylim(-1.55, H + 0.85)

fig.tight_layout(pad=0.1)
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(os.path.dirname(here), "beamInTunnel_schematic_paper.pdf")
fig.savefig(out, bbox_inches="tight", dpi=300)
print("Saved", out)
