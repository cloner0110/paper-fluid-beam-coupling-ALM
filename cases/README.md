# Test cases

OpenFOAM case set-ups for the three coupled benchmarks reported in the paper. Each case holds
the input dictionaries only: `0.orig`, `constant`, `system` and the run scripts. Results,
time directories, decomposed `processor*` directories, logs, `postProcessing` and the
generated fluid meshes are left out, since `Allrun` rebuilds the mesh with `blockMesh` (and
`snappyHexMesh` for the drag calibrations). The beam meshes (`constant/beam_0/polyMesh`) and
`constant/cellDecomposition.beams` are kept, because the run scripts copy rather than
regenerate them.

| Directory | Paper section | Reference |
|---|---|---|
| `beamInChannel/` | Flexible beam in a confined channel flow | Zhang, Liu & Khoo (2012) |
| `oscillatingBeam/` | Leaflet driven by a sinusoidal channel flow | Zhang & Gay (2007) |
| `flexibleVegetation/` | Wave-induced motion of a flexible vegetation stem | Jacobsen et al. (2019) |

Only the main runs are included. The mesh, time-step, kernel-width, sampling-distance and
tolerance studies are variations of these cases and are not stored here.

## Requirements

- OpenFOAM v2306 (openfoam.com)
- [moorFV](https://github.com/solids4foam/moorFV), which provides `libsixDoFRigidBodyBeamMotion`
  and the `beamActuatorLine` momentum source
- [beamFoam](https://github.com/solids4foam/beamFoam), the finite volume beam solver

## Layout

```
beamInChannel/
    Allrun, Allclean        regenerate the beam mesh and copy it into beamTunnel/
    beamInitialisation/     beam mesh generation (createBeamMesh, setInitialPositionBeam)
    beamTunnel/             coupled pimpleFoam case
    dragCalib/              steady simpleFoam rigid-plate calibration of Cdn
oscillatingBeam/
    C1, C2, C3, C4          coupled pimpleFoam cases, one per (Re, St) pair
    dragCalib/
        topView/            unbounded cross-section calibration
        sideView-Re10/      rigid-plate channel calibration at Re = 10, with the probe line
        sideView-Re1/       rigid-plate channel calibration at Re = 1
flexibleVegetation/
    mimic3-H040T20-cd4/     coupled interFoam case over the full wave flume
```

| Case | Re | St | U_amp (m/s) | T (s) |
|---|---|---|---|---|
| C1 | 10 | 1.0 | 0.01 | 1 |
| C2 | 1 | 1.0 | 0.01 | 1 |
| C3 | 1 | 0.5 | 0.01 | 2 |
| C4 | 10 | 0.5 | 0.01 | 2 |

The vegetation case is the Mimic 3 stem (l = 0.30 m) under the H040T20 wave (H = 0.04 m,
T = 2.0 s) with C_dn = 4.0. The paper's other wave conditions and drag coefficients use the
same set-up with `constant/waveProperties` and `Cdn` in `constant/beam_0/beamProperties`
changed.

## Running

Coupled channel cases (decomposed onto 10 ranks, see `system/decomposeParDict`):

```sh
cd oscillatingBeam/C1
./Allrun
```

`beamInChannel/beamTunnel` already contains its beam mesh, so it can be run directly in the
same way. To regenerate the beam mesh first, run `./Allclean` and then `./Allrun` from
`beamInChannel/`, and then `./Allrun` inside `beamTunnel/`.

Drag calibrations (serial `simpleFoam`; `gen_stl.py` writes the plate surface and needs
Python 3):

```sh
cd oscillatingBeam/dragCalib/sideView-Re10
./Allrun
```

Vegetation case (decomposed onto 32 ranks):

```sh
cd flexibleVegetation/mimic3-H040T20-cd4
./Allrun.decompose
```

If the number of subdomains is changed, change it in both `system/decomposeParDict` and
`system/beam_0/decomposeParDict`, and regenerate `constant/cellDecomposition.beams` to match.

`bash_tip.sh` in each coupled case extracts the beam tip displacement from the reconstructed
time directories.
