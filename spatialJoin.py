import pandas as pd
import argparse
import geopandas as gpd
import csv
import os

"""
Use Case:

python spatial_join.py --crs EPSG:4326 --input_csv <input csv> --input_poly <input FIR>

"""


def get_args():
    parser = argparse.ArgumentParser(description="Spatial Join")
    parser.add_argument("--crs", type=str, help="Input CRS, Default - 4326")
    parser.add_argument("--input_csv", type=str, help="Input CSV File")
    parser.add_argument("--input_poly", type=str, help="Polygon File")

    return parser.parse_args()


def spatial_join(input_csv, neighborhood_polygon, crs="EPSG:4326"):
    output_location = os.path.dirname(input_csv)
    output_file = os.path.join(output_location, "output.csv")
    listings = pd.read_csv(input_csv)
    # covert to geopandas geodataframe
    gdf_listings = gpd.GeoDataFrame(
        listings,
        geometry=gpd.points_from_xy(listings.longitude, listings.latitude),
        crs=crs,
    )

    neighborhoods = gpd.read_file(neighborhood_polygon)
    # value of op would be either "intersects" or "within"
    sjoined_listings = gpd.sjoin(gdf_listings, neighborhoods, op="intersects")
    sjoined_listings.to_csv(
        output_file,
        columns=[
            "uid",
            "vin",
            "ys_time_stamp",
            "sourceSystem",
            "validationFlag",
            "latitude",
            "longitude",
            "angle",
            "custom1",
            "custom2",
            "custom3",
            "custom4",
            "location1",
            "Yard",
            "Grid",
            "location4",
            "image",
        ],
    )


def main(input_csv, neighborhood_polygon, crs):
    spatial_join(input_csv, neighborhood_polygon, crs)


if __name__ == "__main__":
    args = get_args()
    main(args.input_csv, args.input_poly, args.crs)
