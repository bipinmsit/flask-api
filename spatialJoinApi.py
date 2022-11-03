from flask import Flask, jsonify, request
import pandas as pd
import geopandas as gpd

app = Flask(__name__)


@app.route("/")
def hello_world():
    return {"Name": "Bipin", "Degree": "M.Tech"}


@app.route("/info/")
def spatial_join():
    lng = request.args.get("lng")
    lat = request.args.get("lat")
    crs = request.args.get("crs")

    print(lng, lat, crs)
    coords = {"lng": lng, "lat": lat}
    listings = pd.DataFrame(coords, index=[0])
    # covert to geopandas geodataframe
    gdf_listings = gpd.GeoDataFrame(
        listings,
        geometry=gpd.points_from_xy(listings.lng, listings.lat),
        crs=crs,
    )

    neighborhoods = gpd.read_file(
        r"C:\Users\Bipin.Kumar\Downloads\data\demo\output_4326.geojson"
    )
    # value of op would be either "intersects" or "within"
    sjoined_listings = gpd.sjoin(gdf_listings, neighborhoods, op="intersects")
    print(sjoined_listings.to_json())

    return sjoined_listings.to_json()



if __name__ == "__main__":
    app.run(debug=True)
