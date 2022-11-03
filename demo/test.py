import pandas as pd
import argparse
import geopandas as gpd
import csv
import os

def spatial_join(lng, lat, crs="EPSG:4326"):
    coords = {"lng":lng, "lat":lat}
    listings = pd.DataFrame(coords, index=[0])
    # covert to geopandas geodataframe
    gdf_listings = gpd.GeoDataFrame(
        listings,
        geometry=gpd.points_from_xy(listings.longitude, listings.latitude),
        crs=crs,
    )

    neighborhoods = gpd.read_file("C:\Users\Bipin.Kumar\Downloads\data\demo\output_4326.geojson")
    # value of op would be either "intersects" or "within"
    sjoined_listings = gpd.sjoin(gdf_listings, neighborhoods, op="intersects")
    return sjoined_listings