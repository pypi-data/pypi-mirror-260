import geopandas as gpd
import numpy as np
import math

from ..processing import read_raster
from ..processing import normalised_difference
from ..processing import mask_raster

def water_quality(image_name,aoi_mask,storage):
    # read_raster image
    ds, raster = read_raster(image_name, storage, bands=[3,4,5,8])
    date_and_tif = image_name.split("_")[1]
    date = date_and_tif.split(".")[0]
    # calculate ndwi
    ndwi = normalised_difference(raster, [1,4])

    # save_raster ndwi
    
    raster_name_ndwi = f"ndwi_{date}.tif"
    storage.create(ndwi, raster_name_ndwi, ds=ds)

    # read_geojson aoi_mask
    aoi_mask_gdf = gpd.GeoDataFrame.from_features(aoi_mask["features"], crs=4326)

    # mask_raster ndwi with aoi_mask
    ndwi_masked, out_transform = mask_raster(raster_name_ndwi, aoi_mask_gdf, storage)

    # save_raster ndwi_masked
    raster_name_ndwi_masked = f"ndwi_masked_{date}.tif"
    storage.create(ndwi_masked, raster_name_ndwi_masked, ds=ds)

    # apply thershold to calculate water-mask
    threshold = -0.1
    water_mask = ndwi >= threshold

    # save_raster water_mask
    raster_name_water_mask = f"water_mask_{date}.tif"
    storage.create(water_mask, raster_name_water_mask, ds=ds)

    # mask_raster water_mask with aoi_mask
    water_mask_masked, out_transform = mask_raster(raster_name_water_mask, aoi_mask_gdf, storage)

    # save_raster water_mask_masked
    raster_name_water_mask_masked = f"water_mask_masked_{date}.tif"
    storage.create(water_mask_masked, raster_name_water_mask_masked, ds=ds)


    # calculate ndti
    ndti = normalised_difference(raster, [2,1])

    # save_raster ndti
    raster_name_ndti = f"ndti_{date}.tif"
    storage.create(ndti, raster_name_ndti, ds=ds)

    # mask_raster ndti with aoi_mask
    ndti_masked, out_transform = mask_raster(raster_name_ndti, aoi_mask_gdf, storage)

    # save_raster ndti_masked
    raster_name_ndti_masked = f"ndti_masked_{date}.tif"
    storage.create(ndti_masked, raster_name_ndti_masked, ds=ds)

    # calculate ndci
    ndci = normalised_difference(raster, [3,2])

    # save_raster ndci
    raster_name_ndci = f"ndci_{date}.tif"
    storage.create(ndci, raster_name_ndci, ds=ds)

    # mask_raster ndci with aoi_mask
    ndci_masked, out_transform = mask_raster(raster_name_ndci, aoi_mask_gdf, storage)

    # save_raster ndci_masked
    raster_name_ndci_masked = f"ndci_masked_{date}.tif"
    storage.create(ndci_masked, raster_name_ndci_masked, ds=ds)

    # calculate doc
    bands = [1,2]
    bands = np.array(bands) - 1
    # Separate the bands
    band1 = raster[bands[0], :, :]
    band2 = raster[bands[1], :, :]
    # convert the bands to floats
    band1 = band1.astype(float)
    band2 = band2.astype(float)
    doc = 432 * pow(math.e, -2.24 * band1/band2)

    # save_raster doc
    raster_name_doc = f"doc_{date}.tif"
    storage.create(doc, raster_name_doc, ds=ds)

    # mask_raster doc with aoi_mask
    doc_masked, out_transform = mask_raster(raster_name_doc, aoi_mask_gdf, storage)

    # save_raster doc_masked
    raster_name_doc_masked = f"doc_masked_{date}.tif"
    storage.create(doc_masked, raster_name_doc_masked, ds=ds)