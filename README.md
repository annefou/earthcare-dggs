# earthcare-dggs

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19709327.svg)](https://doi.org/10.5281/zenodo.19709327)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Converting [EarthCARE](https://www.esa.int/Applications/Observing_the_Earth/FutureEO/EarthCARE) satellite data to HEALPix DGGS format using [healpix-geo](https://github.com/eopf-dggs/healpix-geo) and [xdggs](https://github.com/xarray-contrib/xdggs).

## Notebooks

| Notebook | Description |
|---|---|
| [01_download](notebooks/01_download.ipynb) | Download EarthCARE L2 data via earthcarekit |
| [02_explore](notebooks/02_explore.ipynb) | Explore data structure and dimensions |
| [03_msi_to_healpix](notebooks/03_msi_to_healpix.ipynb) | Convert MSI 2D swath to HEALPix with proper aggregation |
| [04_profiles_to_healpix](notebooks/04_profiles_to_healpix.ipynb) | Convert ATLID/CPR profiles to HEALPix |
| [05_dggs_zarr](notebooks/05_dggs_zarr.ipynb) | Save/load as DGGS-Zarr format |

## Setup

```bash
pixi run -e dev jupyterlab
```

## Build documentation

```bash
pixi run -e docs build-docs       # Build static site
pixi run -e docs jupyter-book start  # Preview locally
```

## How to cite

If you use this software, please cite it via its Zenodo DOI.

```
Fouilloux, A. (2026). EarthCARE to DGGS (v0.1.0). Zenodo.
https://doi.org/10.5281/zenodo.19709327
```

BibTeX:

```bibtex
@software{fouilloux_earthcare_dggs,
  author    = {Fouilloux, Anne},
  title     = {EarthCARE to DGGS},
  year      = {2026},
  version   = {0.1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19709327},
  url       = {https://doi.org/10.5281/zenodo.19709327}
}
```

The DOI above is the **concept DOI** — it always resolves to the latest
release. Specific version DOIs are available on the
[Zenodo record page](https://doi.org/10.5281/zenodo.19709327).

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

## License

MIT
