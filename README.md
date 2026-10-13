# Two-way actuator-line coupling of a geometrically exact finite-volume beam

Manuscript source for the actuator-line (ALM) beam–fluid coupling paper.

## Repository layout

- `paper/`: manuscript source (`article.tex`, `sections/`, `figures/`, `bibliography.bib`,
  class and bibliography style). Build from inside `paper/` with
  `pdflatex article; bibtex article; pdflatex article; pdflatex article`.
- `cases/`: OpenFOAM set-ups of the coupled test cases reported in the paper (beam in a
  confined channel, oscillating leaflet, flexible vegetation stem). See `cases/README.md`.
