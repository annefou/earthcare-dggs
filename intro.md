# EarthCARE to DGGS

Converting [EarthCARE](https://www.esa.int/Applications/Observing_the_Earth/FutureEO/EarthCARE) satellite data to HEALPix Discrete Global Grid System (DGGS) format.

## About EarthCARE

EarthCARE (Earth Cloud Aerosol and Radiation Explorer) is a joint ESA-JAXA satellite mission studying clouds, aerosols, and radiation in the Earth's atmosphere. It carries four instruments:

- **ATLID** (Atmospheric Lidar) — vertical profiles of aerosols and thin clouds
- **CPR** (Cloud Profiling Radar) — vertical profiles of clouds and precipitation
- **MSI** (Multi-Spectral Imager) — 2D swath imagery of cloud and aerosol properties
- **BBR** (Broadband Radiometer) — top-of-atmosphere radiative fluxes

## Why HEALPix for EarthCARE?

HEALPix (Hierarchical Equal Area isoLatitude Pixelisation) provides several advantages for EarthCARE data:

- **Equal-area cells** at all latitudes — essential for global atmospheric statistics and climatologies
- **Hierarchical resolution** — multi-scale analysis from coarse overviews to full-resolution data
- **Consistent grid across instruments** — MSI, ATLID, CPR, and BBR data can share the same cell IDs
- **No projection discontinuities** — no UTM zones, no date line issues, no polar singularities
- **WGS84 ellipsoid support** — geodetically correct cell placement via [healpix-geo](https://github.com/eopf-dggs/healpix-geo)

## Data patterns

EarthCARE data presents two distinct conversion patterns:

1. **MSI (2D swath)** — similar to Sentinel-3 OLCI/SLSTR, with `(along_track, across_track)` dimensions and 2D lat/lon arrays. Converted by assigning each pixel to its nearest HEALPix cell with aggregation.

2. **ATLID/CPR (1D profiles)** — vertical atmospheric profiles along the satellite ground track. Each profile is mapped to a HEALPix cell ID while preserving the vertical dimension.

## Aggregation by variable type

Different variables require different aggregation strategies when multiple pixels fall into the same HEALPix cell:

| Variable type | Strategy | Examples |
|---|---|---|
| Classification | **Mode** (most frequent) | cloud_mask, cloud_type, cloud_phase |
| Continuous | **Mean** | cloud_top_height, AOT, temperature |
| Uncertainty | **RMS** (root mean square) | error estimates |
| Quality flags | **Max** (worst case) | quality_status |

## Visualization

HEALPix data can be visualized at multiple scales:

- **Interactive maps** (`xdggs.explore()` via [lonboard](https://github.com/developmentseed/lonboard)) — renders HEALPix cell polygons on a web map with a dropdown to switch between variables. For performance, data is coarsened from depth 17 to depth 10 (~58km cells) using the same aggregation strategies.
- **Full-swath static plots** (matplotlib/cartopy) — scatter plots of all cells along the full satellite swath, showing the data at native resolution.
- **Zoomed static views** — zoom into a small region (e.g. 2° × 2°) to see individual cell positions at depth 17 (~50m).

## Tools used

This project builds on the DGGS ecosystem developed in the [GRID4EARTH](https://github.com/eopf-dggs) ESA project:

- [healpix-geo](https://github.com/eopf-dggs/healpix-geo) — Rust+Python HEALPix operations with WGS84 ellipsoid support
- [xdggs](https://github.com/xarray-contrib/xdggs) — Xarray extension for DGGS with interactive visualization
- [earthcarekit](https://github.com/TROPOS-RSD/earthcarekit) — Python tools for downloading and reading EarthCARE data

## Contents

```{tableofcontents}
```
