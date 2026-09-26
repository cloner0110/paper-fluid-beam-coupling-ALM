"""
Paper version of the rigid-plate channel drag calibration at Re = 10
(Figure 13b). Reviewer round 2, comment 36: the wall-configuration marker
(Cd ~ 59, leaflet root on a no-slip wall) is removed together with the
paragraph that discussed it, so only the calibration used by the closure
is shown. Otherwise identical to the thesis generator
PhD_thesis_UCD/Figures/Chapter5/gen_leaflet_dragCalib_sideview.py.

    python3.11 figures/scripts/plot_leaflet_dragcalib_sideview.py
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath,amssymb,bm}",
    "font.family": "serif",
    "font.size": 11,
})

path = ("/Volumes/OpenFOAM/tmp/Thesis/leaflet/cfd_Analysis_cases/"
        "dragCalib/sideViews/sideView-Re10/postProcessing/"
        "forceCoeffs/0/coefficient.dat")
data = np.loadtxt(path, comments="#")
it, Cd = data[:, 0], data[:, 1]
n_tail = max(10, len(it) // 200)
Cd_mid = np.mean(Cd[-n_tail:])

fig, ax = plt.subplots(figsize=(5.6, 3.6))
ax.plot(it, Cd, color="#1565C0", lw=1.2,
        label=rf"in-channel calibration $\to C_d \approx {Cd_mid:.1f}$")
ax.set_xlabel(r"iteration")
ax.set_ylabel(r"$C_{d}$")
ax.set_yscale("log")
ax.set_ylim(40, 600)
# newer matplotlib labels the minor log ticks; the thesis figure did not
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_xlim(0, it[-1] * 1.02)
ax.grid(True, which="both", ls=":", lw=0.4, color="0.65")
ax.legend(loc="upper right", frameon=False, fontsize=10)

plt.tight_layout()
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(os.path.dirname(here), "leaflet_dragCalib_sideview_paper.pdf")
plt.savefig(out, bbox_inches="tight", pad_inches=0.05)
print(f"saved: {out}")
print(f"converged Cd = {Cd_mid:.3f}")
