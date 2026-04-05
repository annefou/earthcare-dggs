# earthcare-dggs

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

## License

MIT
