
from flask import Blueprint, request
import os
from dotenv import load_dotenv
import requests

load_dotenv()

bp = Blueprint("proxy_bp", __name__)

location_key = os.environ.get("LOCATION_KEY")
weather_key = os.environ.get("WEATHER_KEY")
timezone_key = os.environ.get("TIMEZONEDB_KEY")

@bp.get("/location")
def get_lat_lon():
    loc_query = request.args.get("q")
    if not loc_query:
        return {"message": "must provide q parameter (location)"}, 400

    response = requests.get(
        "https://us1.locationiq.com/v1/search.php",
        params={"q": loc_query, "key": location_key, "format": "json"}
    )

    return response.json(), 200

@bp.get("/weather")
def get_weather():
    lat_query = request.args.get("lat")
    lon_query = request.args.get("lon")

    if not lat_query or not lon_query:
        return {"message": "must provide lat and lon parameters"}, 400

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"lat": lat_query, "lon": lon_query, "appid": weather_key, "units": "imperial"}
    )
    return response.json(), 200

@bp.get("/timezone")
def get_timezone():
    lat_query = request.args.get("lat")
    lon_query = request.args.get("lng")

    if not lat_query or not lon_query:
        return {"message": "must provide lat and lng parameters"}, 400

    response = requests.get(
            "http://api.timezonedb.com/v2.1/get-time-zone",
            params={"key": timezone_key, "by": "position", "lat": lat_query, "lng": lon_query, "format": "json",}
        )

    return response.json(), 200