import numpy as np
import math
import geopandas as gpd
from datetime import datetime, timedelta
import pandas as pd

from scipy.ndimage import median_filter
from skimage.exposure import equalize_hist

from ..data.satellite import download_satellite_image
from ..data.satellite import explore_satellite_images
from ..processing import mask_raster
from ..processing import read_raster
from ..processing import colorize_raster
from ..processing import px_count
from ..processing import save_table
from ..processing import normalised_difference
from ..processing import convert_array_to_vector


def water_quality(image_name, aoi_mask, storage, desired_images=2, date=None):
    """
    This function calculates the water quality of a given image.

    It calculates the following layers:
        - Normalized Difference Water Index (NDWI) - ndwi_{date}.tif, ndwi_masked_{date}.tif, ndwi_categorized_{date}.tif
        - Normalized Difference Turbidity Index (NDTI) - ndti_{date}.tif, ndti_masked_{date}.tif, ndti_categorized_{date}.tif
        - Normalized Difference Chlorophyll Index (NDCI) - ndci_{date}.tif, ndci_masked_{date}.tif, ndci_categorized_{date}.tif
        - Median Water Mask - median_water_mask_{date}.tif
        - Dissolved Organic Carbon (DOC) - DOC_{date}.tif, DOC_masked_{date}.tif, DOC_categorized_{date}.tif

    It also calculates the following analytics:
        - Water Extent (in hectares and percentage) - table_water_extent.json
        - Water Turbidity (in hectares and percentage) - table_turbidity_Ha.json, table_turbidity_percent.json
        - Water Chlorophyll (in hectares and percentage) - table_chlorophyll_Ha.json, table_chlorophyll_percent.json
        - Water DOC (in hectares and percentage) - table_DOC_Ha.json, table_DOC_percent.json

    Parameters
    ----------
    image_name : str
        The name of the image to be processed.
    aoi_mask : dict
        The GeoJSON of the area of interest.
    storage : Storage
        The Storage object.
    desired_images : int, optional
        The number of images to be downloaded to determine the water body status, by default 2.
    date : str, optional
        The date of the image from which start downloading earlier images to determine the water body status,
        by default None, which uses the date given in the image name.

    Returns
    -------
    None

    """
    # read_raster image
    ds, raster = read_raster(image_name, storage, bands=[3, 4, 5, 8])
    date = image_name.split(".")[0].split("_")[-1]

    """ LAYERS """
    # NDWI

    # calculate ndwi
    ndwi = normalised_difference(raster, [1, 4])

    # save_raster ndwi
    raster_name_ndwi = f"ndwi_{date}.tif"
    storage.create(ndwi, raster_name_ndwi, ds=ds)

    # NDTI
    # calculate ndti
    ndti = normalised_difference(raster, [2, 1])

    # save_raster ndti
    raster_name_ndti = f"ndti_{date}.tif"
    storage.create(ndti, raster_name_ndti, ds=ds)

    # NDCI
    # calculate ndci
    ndci = normalised_difference(raster, [3, 2])
    ndci = equalize_hist(ndci)

    # save_raster ndci
    raster_name_ndci = f"ndci_{date}.tif"
    storage.create(ndci, raster_name_ndci, ds=ds)

    # MEDIAN WATER MASK
    # calculate median_water_mask
    median_water_mask, stored_images, _ = compute_median_water_mask(
        aoi_mask, desired_images, date, storage
    )  # aoi_mask is needed for downloading

    # save raster median_water_mask
    raster_name_median_water_mask = f"median_water_mask_{date}.tif"
    median_water_mask_path = storage.create(
        median_water_mask, raster_name_median_water_mask, ds=ds
    )

    # DOC
    # calculate doc
    doc_layers_array, doc_values_array, ds = compute_doc(stored_images, storage)

    # save_raster doc
    raster_name_doc = f"DOC_{date}.tif"
    storage.create(doc_layers_array[0], raster_name_doc, ds=ds)

    """ MASK LAYERS """
    shp = convert_array_to_vector(median_water_mask, median_water_mask_path)

    # mask_raster ndwi with aoi_mask
    ndwi_masked, _ = mask_raster(raster_name_ndwi, shp, storage)

    # save_raster ndwi_masked
    raster_name_ndwi_masked = f"ndwi_masked_{date}.tif"
    storage.create(ndwi_masked, raster_name_ndwi_masked, ds=ds)

    # mask_raster ndti with aoi_mask
    ndti_masked, _ = mask_raster(raster_name_ndti, shp, storage)
    ndti_masked[ndti_masked == False] = -9999  # convert false to nan

    # save_raster ndti_masked
    raster_name_ndti_masked = f"ndti_masked_{date}.tif"
    storage.create(ndti_masked, raster_name_ndti_masked, ds=ds)

    # mask_raster ndci with aoi_mask
    ndci_masked, _ = mask_raster(raster_name_ndci, shp, storage)
    ndci_masked[ndci_masked == False] = -9999  # convert false to nan

    # save_raster ndci_masked
    raster_name_ndci_masked = f"ndci_masked_{date}.tif"
    storage.create(ndci_masked, raster_name_ndci_masked, ds=ds)

    # mask_raster doc with aoi_mask
    doc_masked, _ = mask_raster(raster_name_doc, shp, storage)
    doc_masked[doc_masked == False] = -9999  # convert false to nan

    # save_raster doc_masked
    raster_name_doc_masked = f"DOC_masked_{date}.tif"
    storage.create(doc_masked, raster_name_doc_masked, ds=ds)

    """ ANALYTICS """
    # Water Extent
    extent_has = np.divide(median_water_mask.sum(axis=(1, 2)).max(), 100)
    update_extent_table(extent_has, date, storage)

    # Water Turbidity
    ndti_categories = np.digitize(ndti_masked, [-np.inf, -0.2, 0.4, np.inf])
    raster_name_ndti_categorized = f"ndti_categorized_{date}.tif"
    storage.create(ndti_categories, raster_name_ndti_categorized, ds=ds)

    ndti_colorized = colorize_raster(ndti_categories, colors=["green", "yellow", "red"])
    raster_name_ndti_colorized = f"ndti_categorized_rgb_{date}.tif"
    storage.create(ndti_colorized, raster_name_ndti_colorized, ds=ds)

    ndti_px_counted = px_count(ndti_categories, [1, 2, 3])
    ndti_has = np.divide(
        ndti_px_counted,
        100,
        out=np.zeros_like(ndti_px_counted, dtype=np.float64),
        where=100 != 0,
    )
    # save_table turbidity hectareas
    turbidity_table_name = "table_turbidity_Ha.json"
    turbidity_columns = ["Good [Has]", "Careful [Has]", "Bad [Has]", "Total [Has]"]
    save_table(
        data=ndti_has,
        columns=turbidity_columns,
        table_name=turbidity_table_name,
        date=date,
        storage=storage,
    )
    ndti_percent = [
        np.divide(ndti_has[i], ndti_has[-1]) * 100 for i in range(len(ndti_has) - 1)
    ]
    # save_table turbidity percent
    turbidity_percent_table_name = "table_turbidity_percent.json"
    turbidity_percent_columns = ["Good [%]", "Careful [%]", "Bad [%]"]
    save_table(
        data=ndti_percent,
        columns=turbidity_percent_columns,
        table_name=turbidity_percent_table_name,
        date=date,
        storage=storage,
    )

    # Water Chlorophyll
    ndci_categories = np.digitize(ndci_masked, [-np.inf, -0.3, 0.5, np.inf])
    raster_name_ndci_categorized = f"ndci_categorized_{date}.tif"
    storage.create(ndci_categories, raster_name_ndci_categorized, ds=ds)

    ndci_colorized = colorize_raster(ndci_categories, colors=["green", "yellow", "red"])
    raster_name_ndci_colorized = f"ndci_categorized_rgb_{date}.tif"
    storage.create(ndci_colorized, raster_name_ndci_colorized, ds=ds)

    ndci_px_counted = px_count(ndci_categories, [1, 2, 3])
    ndci_has = np.divide(
        ndci_px_counted,
        100,
        out=np.zeros_like(ndci_px_counted, dtype=np.float64),
        where=100 != 0,
    )
    # save_table chlorophyll hectareas
    chlorophyll_table_name = "table_chlorophyll_Ha.json"
    chlorophyll_columns = ["Good [Has]", "Careful [Has]", "Bad [Has]", "Total [Has]"]
    save_table(
        data=ndci_has,
        columns=chlorophyll_columns,
        table_name=chlorophyll_table_name,
        date=date,
        storage=storage,
    )
    ndci_percent = [
        np.divide(ndci_has[i], ndci_has[-1]) * 100 for i in range(len(ndci_has) - 1)
    ]
    # save_table chlorophyll percent
    chlorophyll_percent_table_name = "table_chlorophyll_percent.json"
    chlorophyll_percent_columns = ["Good [%]", "Careful [%]", "Bad [%]"]
    save_table(
        data=ndci_percent,
        columns=chlorophyll_percent_columns,
        table_name=chlorophyll_percent_table_name,
        date=date,
        storage=storage,
    )

    # DOC
    # Compute the mean of the doc values
    mean_mean_doc = np.mean([dict["mean_doc"] for dict in doc_values_array])
    mean_max_doc = np.mean([dict["max_doc"] for dict in doc_values_array])
    mean_min_doc = np.mean([dict["min_doc"] for dict in doc_values_array])
    mean_std_doc = np.mean([dict["std_doc"] for dict in doc_values_array])

    # Categorize the doc values
    a = 1
    min_to_N0 = -np.inf
    N0_to_N1 = mean_mean_doc + 2 * mean_std_doc / a
    N1_to_N2 = mean_mean_doc + 3 * mean_std_doc / a
    N2_to_N3 = mean_mean_doc + 4 * mean_std_doc / a
    N3_to_max = np.inf

    doc_categories = np.digitize(
        doc_masked, [min_to_N0, N0_to_N1, N1_to_N2, N2_to_N3, N3_to_max]
    )
    raster_name_doc_categorized = f"DOC_categorized_{date}.tif"
    storage.create(doc_categories, raster_name_doc_categorized, ds=ds)

    doc_colorized = colorize_raster(
        doc_categories, colors=["green", "yellow", "orange", "red"]
    )
    raster_name_doc_colorized = f"DOC_categorized_rgb_{date}.tif"
    storage.create(doc_colorized, raster_name_doc_colorized, ds=ds)

    doc_px_counted = px_count(doc_categories, [1, 2, 3, 4])
    doc_has = np.divide(
        doc_px_counted,
        100,
        out=np.zeros_like(doc_px_counted, dtype=np.float64),
        where=100 != 0,
    )
    # save_table DOC hectareas
    doc_table_name = "table_DOC_Ha.json"
    doc_columns = ["N0 [Has]", "N1 [Has]", "N2 [Has]", "N3 [Has]", "Total [Has]"]
    save_table(
        data=doc_has,
        columns=doc_columns,
        table_name=doc_table_name,
        date=date,
        storage=storage,
    )
    doc_percent = [
        np.divide(doc_has[i], doc_has[-1]) * 100 for i in range(len(doc_has) - 1)
    ]
    # save_table DOC percent
    doc_percent_table_name = "table_DOC_percent.json"
    doc_percent_columns = ["N0 [%]", "N1 [%]", "N2 [%]", "N3 [%]"]
    save_table(
        data=doc_percent,
        columns=doc_percent_columns,
        table_name=doc_percent_table_name,
        date=date,
        storage=storage,
    )


"""
Methods for Layers: Median Water Mask
"""


def compute_median_water_mask(aoi_mask, desired_images, from_date_to_earlier, storage):
    # Get the bbox from the aoi_mask
    bbox = gpd.GeoDataFrame.from_features(aoi_mask["features"]).geometry[0]

    stored_images = download_missing_images(
        desired_images=desired_images,
        from_date_to_earlier=from_date_to_earlier,
        bbox=bbox,
        storage=storage,
    )
    water_masks_array, ds = compute_water_masks(stored_images, storage)
    median_water_mask = median_filter(water_masks_array, size=(7, 3, 3))
    binary_median_water_mask = median_water_mask.astype(np.uint8)

    # save_raster
    median_raster_name = "median_water_mask.tif"
    storage.create(median_water_mask, median_raster_name, ds=ds)
    return binary_median_water_mask, stored_images, water_masks_array


def download_missing_images(desired_images, from_date_to_earlier, bbox, storage):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(from_date_to_earlier, "%Y-%m-%d")
    # Check how many images that begin with "S2L2A" are in storage
    files = storage.list()
    stored_images = []
    for file in files:
        # If the file is a Sentinel-2 image of a date equal or earlier than 'from_date_to_earlier' , add it to the list:
        if file.startswith("S2L2A"):
            image_date = datetime.strptime(file.split("_")[1].split(".")[0], "%Y-%m-%d")
            if image_date <= date_obj and len(stored_images) < desired_images:
                stored_images.append(file)
    # If images are less than desired, download the missing ones
    images_found = []
    while len(stored_images) < desired_images:
        time_interval = (
            (date_obj - timedelta(days=10)).strftime("%Y-%m-%d"),
            date_obj.strftime("%Y-%m-%d"),
        )
        images_found = explore_satellite_images(
            bbox, time_interval=time_interval, cloud_cover=5
        )
        for image in images_found:
            if f"S2L2A_{image['date'].split('T')[0]}.tif" not in stored_images:
                path = download_satellite_image(
                    storage, bbox, image["date"].split("T")[0]
                )
                stored_images.append(path)
        date_obj -= timedelta(days=10)
    return stored_images


def compute_water_masks(stored_images, storage):
    water_masks_array = []
    for path in stored_images:
        image_name = path.split("/")[-1]
        date = image_name.split("_")[1].split(".")[0]
        # read raster
        ds, raster = read_raster(image_name, storage, bands=[3, 4, 5, 8])

        # calculate ndwi
        ndwi = normalised_difference(raster, [1, 4])

        # apply thershold to calculate water-mask
        threshold = 0
        water_mask = ndwi >= threshold

        # save_raster water_mask
        raster_name_water_mask = f"water_mask_{date}.tif"
        storage.create(water_mask, raster_name_water_mask, ds=ds)
        water_masks_array.append(water_mask)

    return water_masks_array, ds


""" 
Methods for Layers: DOC
"""


def compute_doc(stored_images, storage):
    doc_layers_array = []
    doc_values_array = []
    for path in stored_images:
        image_name = path.split("/")[-1]
        # read raster
        ds, raster = read_raster(image_name, storage, bands=[3, 4, 5, 8])

        # calculate doc for each image
        # calculate doc
        bands = [1, 2]
        bands = np.array(bands) - 1
        # Separate the bands
        band1 = raster[bands[0], :, :]
        band2 = raster[bands[1], :, :]
        # convert the bands to floats
        band1 = band1.astype(float)
        band2 = band2.astype(float)
        doc = 432 * pow(math.e, -2.24 * band1 / band2)
        mean_doc = np.nanmean(doc)
        max_doc = np.nanmax(doc)
        min_doc = np.nanmin(doc)
        std_doc = np.nanstd(doc)
        doc_values_dict = {
            "mean_doc": mean_doc,
            "max_doc": max_doc,
            "min_doc": min_doc,
            "std_doc": std_doc,
        }
        doc_values_array.append(doc_values_dict)
        doc_layers_array.append(doc)
    return doc_layers_array, doc_values_array, ds


"""
Methods for Analytics: Water Extent
"""


def update_df(df):
    df["Total [Has]"] = df["Water [Has]"].max()
    df["Not Water [Has]"] = df["Total [Has]"] - df["Water [Has]"]
    df["Percentage [%]"] = df["Water [Has]"] / df["Total [Has]"] * 100
    return df


def update_extent_table(extent_has, date, storage):
    if f"table_water_extent.json" not in storage.list():
        df = pd.DataFrame(
            {
                "Water [Has]": extent_has,
                "Not Water [Has]": 0,
                "Total [Has]": extent_has,
                "Percentage [%]": 100,
            },
            index=[date],
        )
        df = update_df(df)
    else:
        df = storage.read(f"table_water_extent.json")
        if date in df.index:
            df.loc[date, "Water [Has]"] = extent_has
            update_df(df)
            return df
        if isinstance(df.index, pd.DatetimeIndex):
            # Handle pd.DateTimeIndex, converting index to string
            df.index = df.index.strftime("%Y-%m-%d")
        new_row = pd.DataFrame(
            {
                "Water [Has]": extent_has,
                "Not Water [Has]": 0,
                "Total [Has]": 0,
                "Percentage [%]": 0,
            },
            index=[date],
        )
        df = pd.concat([new_row, df.loc[:]])
        df = update_df(df)
    storage.create(df, f"table_water_extent.json")
    return df
