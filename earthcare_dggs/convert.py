"""Conversion functions for EarthCARE data to HEALPix DGGS format."""

from __future__ import annotations

from typing import Any

import healpix_geo as hpxg
import numpy as np
import numpy_groupies as npg
import xarray as xr


def lonlat_to_healpix_cells(
    lon: np.ndarray,
    lat: np.ndarray,
    depth: int,
    ellipsoid: str = "WGS84",
) -> np.ndarray:
    """Convert lon/lat arrays to HEALPix cell IDs.

    Parameters
    ----------
    lon, lat : array-like
        Longitude and latitude in degrees.
    depth : int
        HEALPix depth (refinement level).
    ellipsoid : str
        Reference ellipsoid ("WGS84" or "sphere").

    Returns
    -------
    cell_ids : np.ndarray of uint64
    """
    return hpxg.nested.lonlat_to_healpix(
        np.atleast_1d(lon).astype("float64"),
        np.atleast_1d(lat).astype("float64"),
        depth=depth,
        ellipsoid=ellipsoid,
    )


def aggregate_to_healpix(
    values: np.ndarray,
    group_idx: np.ndarray,
    n_cells: int,
    method: str = "mean",
) -> np.ndarray:
    """Aggregate values into HEALPix cells.

    Parameters
    ----------
    values : np.ndarray
        Values to aggregate (1D, float64).
    group_idx : np.ndarray
        Compact cell index for each value.
    n_cells : int
        Total number of unique cells.
    method : str
        Aggregation method: "mean", "mode", "rms", "max", "min", "sum".

    Returns
    -------
    result : np.ndarray of float32
    """
    vals = values.astype(np.float64)

    if method == "mean":
        result = npg.aggregate(group_idx, vals, func="mean", size=n_cells, fill_value=np.nan)

    elif method == "mode":
        result = np.full(n_cells, np.nan)
        unique_classes = np.unique(vals[np.isfinite(vals)])
        if len(unique_classes) == 0:
            return result.astype(np.float32)
        class_counts = np.zeros((n_cells, len(unique_classes)))
        for ci, cls in enumerate(unique_classes):
            mask = vals == cls
            if mask.any():
                class_counts[:, ci] = npg.aggregate(
                    group_idx[mask], np.ones(mask.sum()),
                    func="sum", size=n_cells, fill_value=0,
                )
        has_data = class_counts.sum(axis=1) > 0
        result[has_data] = unique_classes[class_counts[has_data].argmax(axis=1)]

    elif method == "rms":
        sq = npg.aggregate(group_idx, vals**2, func="mean", size=n_cells, fill_value=np.nan)
        result = np.sqrt(sq)

    elif method == "max":
        result = npg.aggregate(group_idx, vals, func="max", size=n_cells, fill_value=np.nan)

    elif method == "min":
        result = npg.aggregate(group_idx, vals, func="min", size=n_cells, fill_value=np.nan)

    elif method == "sum":
        result = npg.aggregate(group_idx, vals, func="sum", size=n_cells, fill_value=np.nan)

    else:
        raise ValueError(f"Unknown aggregation method: {method}")

    return result.astype(np.float32)


def detect_fill_value(data: np.ndarray) -> float | None:
    """Detect fill value based on dtype."""
    if data.dtype == np.int8:
        return -128
    elif data.dtype == np.int16:
        return -32768
    elif data.dtype in (np.float32, np.float64):
        return None  # Use np.isfinite check instead
    return None


def convert_msi_to_healpix(
    datasets: dict[str, xr.Dataset],
    variables: dict[str, dict[str, Any]],
    depth: int,
    ellipsoid: str = "WGS84",
) -> xr.Dataset:
    """Convert MSI 2D swath variables to HEALPix.

    Parameters
    ----------
    datasets : dict
        Mapping of product type to xarray Dataset (e.g. {"MSI_CM__2A": ds, ...}).
    variables : dict
        Variable definitions with source product and aggregation method.
        Example: {"cloud_mask": {"source": "MSI_CM__2A", "agg": "mode"}}
    depth : int
        HEALPix depth.
    ellipsoid : str
        Reference ellipsoid.

    Returns
    -------
    xr.Dataset
        HEALPix dataset with all converted variables.
    """
    # Get coordinates from first dataset
    primary_ds = next(iter(datasets.values()))
    lat = primary_ds["latitude_swath"].values
    lon = primary_ds["longitude_swath"].values

    # Build valid mask from coordinates
    valid_coords = np.isfinite(lat) & np.isfinite(lon)

    # Get cell IDs for valid coordinate pixels
    cell_ids_valid = lonlat_to_healpix_cells(
        lon[valid_coords], lat[valid_coords], depth=depth, ellipsoid=ellipsoid,
    )
    unique_cells = np.unique(cell_ids_valid)
    n_cells = len(unique_cells)
    cell_to_idx = {c: i for i, c in enumerate(unique_cells)}

    # Convert each variable
    hpx_data = {}
    for var_name, config in variables.items():
        source_ds = datasets.get(config["source"])
        if source_ds is None or var_name not in source_ds:
            continue

        raw = source_ds[var_name].values.ravel()

        # Build validity mask
        fill = config.get("fill") or detect_fill_value(raw)
        if fill is not None:
            var_valid = valid_coords.ravel() & (raw != fill)
        elif raw.dtype in (np.float32, np.float64):
            var_valid = valid_coords.ravel() & np.isfinite(raw) & (raw > -1e30)
        else:
            var_valid = valid_coords.ravel()

        if var_valid.sum() == 0:
            continue

        # Get cell IDs for this variable's valid pixels
        var_cell_ids = lonlat_to_healpix_cells(
            lon.ravel()[var_valid], lat.ravel()[var_valid], depth=depth, ellipsoid=ellipsoid,
        )
        var_group_idx = np.array([cell_to_idx.get(int(c), -1) for c in var_cell_ids])
        keep = var_group_idx >= 0

        hpx_data[var_name] = aggregate_to_healpix(
            raw[var_valid][keep], var_group_idx[keep], n_cells, method=config["agg"],
        )

    return xr.Dataset(
        {name: ("cell_ids", data) for name, data in hpx_data.items()},
        coords={"cell_ids": unique_cells},
    )
