# Two-way actuator-line coupling of a geometrically exact finite-volume beam

Manuscript source for the actuator-line (ALM) beam–fluid coupling paper, ported from
Chapters 3, 4 and 5 of the PhD thesis (`~/gate/PhD_thesis_UCD`) into the LaTeX template of
<https://github.com/philipcardiff/paper-monolithic-fsi>.

## Build

```bash
pdflatex article
bibtex   article
pdflatex article
pdflatex article
```

Currently builds clean: 65 pages, no undefined references or citations, no overfull floats, no LaTeX warnings.

The page count is inflated by the template's draft layout (`\parskip` set to a full baseline plus
`onehalfspacing`). Removing both brings the same content to roughly 35 pages.

## Layout

| Path | Contents |
|---|---|
| `article.tex` | Preamble, title, authors, abstract, back matter |
| `sections/sectionIntro.tex` | Motivation, literature, gap, contributions |
| `sections/sectionMathModel.tex` | Fluid (NS + VOF + waves), Simo–Reissner beam, drag closure |
| `sections/sectionNumericalModel.tex` | FV beam discretisation, ALM operators, algorithms, parallel search |
| `sections/sectionCantilever.tex` | Structural-solver verification (Belendez 2003) |
| `sections/sectionBeamTunnel.tex` | Verification 1: beam in a confined channel (Zhang 2012) + 6 sensitivity studies |
| `sections/sectionLeaflet.tex` | Verification 2: leaflet in sinusoidal channel flow (Zhang & Gay 2007) |
| `sections/sectionFlexVeg.tex` | Validation: wave-driven vegetation stem (Jacobsen 2019) |
| `sections/sectionConclusions.tex` | Conclusions, limitations, future work |
| `figures/` | All figures, copied from the thesis `Figures/Chapter{3,4,5}` |
| `bibliography.bib` | Thesis bibliography plus eight entries added for the future-work section |

## Open items

Every open item is marked in the source with `\AUTHORNOTE{...}` and renders as a red
**[AUTHOR ACTION]** box in the PDF:

```bash
grep -n 'AUTHORNOTE{' article.tex sections/*.tex | grep -v newcommand
```

To produce a clean PDF without them, uncomment the `\renewcommand{\AUTHORNOTE}[1]{}` line in
the preamble of `article.tex`.

Two of the thirteen block submission:

1. **Wave-flume run provenance** (`sections/sectionFlexVeg.tex`, §Numerical set-up). The
   text describes the full-flume 1.35e7-cell case on 256 cores; the plotting scripts read the
   truncated-plateau 2.26e5-cell case on 48 cores. Which one produced the figures decides
   the mesh description, the vertical resolution claim, the kernel width, and the cost figures.
2. **Figure-reuse permission** (`sections/sectionFlexVeg.tex`, §Distributed hydrodynamic
   force). Panels (b) and (d) of the space–time force figure are reproduced from *Journal of
   Fluid Mechanics* and need written permission from Cambridge University Press.
