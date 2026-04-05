"""HEALPix conversion settings for EarthCARE products."""

# HEALPix depth per instrument
# Chosen to match instrument spatial resolution
MSI_DEPTH = 17  # ~458m cells (MSI ~500m resolution)
ATLID_DEPTH = 14  # ~3.7km cells (ATLID ~1km along-track sampling)
CPR_DEPTH = 14  # ~3.7km cells (CPR ~800m horizontal resolution)
BBR_DEPTH = 10  # ~58km cells (BBR ~10km footprint)

ELLIPSOID = "WGS84"  # EarthCARE uses EPSG:4326

# Variable conversion definitions
# Keys: variable name
# Values: source product, aggregation method, optional fill value
MSI_VARIABLES = {
    # MSI_CM__2A — classification variables (aggregate with mode)
    "cloud_mask": {"source": "MSI_CM__2A", "agg": "mode"},
    "cloud_type": {"source": "MSI_CM__2A", "agg": "mode"},
    "cloud_phase": {"source": "MSI_CM__2A", "agg": "mode"},
    "surface_classification": {"source": "MSI_CM__2A", "agg": "mode"},
    # MSI_CM__2A — quality flags (aggregate with max = worst case)
    "quality_status": {"source": "MSI_CM__2A", "agg": "max"},
    # MSI_COP_2A — continuous variables (aggregate with mean)
    "cloud_top_height": {"source": "MSI_COP_2A", "agg": "mean"},
    "cloud_top_temperature": {"source": "MSI_COP_2A", "agg": "mean"},
    "cloud_top_pressure": {"source": "MSI_COP_2A", "agg": "mean"},
    "cloud_optical_thickness": {"source": "MSI_COP_2A", "agg": "mean"},
    "cloud_effective_radius": {"source": "MSI_COP_2A", "agg": "mean"},
    "cloud_water_path": {"source": "MSI_COP_2A", "agg": "mean"},
    # MSI_COP_2A — uncertainty (aggregate with RMS)
    "cloud_top_temperature_error": {"source": "MSI_COP_2A", "agg": "rms"},
    # MSI_COP_2A — classification
    "isccp_cloud_type": {"source": "MSI_COP_2A", "agg": "mode"},
    # MSI_AOT_2A — continuous variables (aggregate with mean)
    "aerosol_optical_thickness_670nm": {"source": "MSI_AOT_2A", "agg": "mean"},
    "aerosol_optical_thickness_865nm": {"source": "MSI_AOT_2A", "agg": "mean"},
    "angstrom_parameter_670nm_865nm": {"source": "MSI_AOT_2A", "agg": "mean"},
    # MSI_AOT_2A — uncertainty (aggregate with RMS)
    "aerosol_optical_thickness_670nm_error": {"source": "MSI_AOT_2A", "agg": "rms"},
    "aerosol_optical_thickness_865nm_error": {"source": "MSI_AOT_2A", "agg": "rms"},
}
