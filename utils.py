import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
MAIN_URL = os.environ.get("MAIN_URL")
APP_NAME = 'feedapp'


def clean_str(str):
    return str.strip(" :.").lower().replace(" ", "_")


def output_to_json(obj, filename):
    with open(filename, "w+") as fn:
        json.dump(obj, fn)


def get_soup(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return BeautifulSoup(resp.content, "lxml")
    raise ValueError(f"{resp.status_code} received - not 200")
