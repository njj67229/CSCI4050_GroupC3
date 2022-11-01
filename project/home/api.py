import os
from urllib import response
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = " https://api.themoviedb.org/3/person/"
BASE_URL_IMG = "http://image.tmdb.org/t/p/"


def get_actor_info(actor_id):
    """Returns actor name and image as a tuple"""
    params = {"api_key": os.getenv("TMDB_KEY")}
    #    146750
    query = BASE_URL + actor_id
    response = requests.get(query, params=params)
    info = response.json()

    cast_img = BASE_URL_IMG + "w600_and_h900_bestv2/" + info["profile_path"]

    res = (info["name"], cast_img)
    return res


print(get_actor_info(str(146750)))
