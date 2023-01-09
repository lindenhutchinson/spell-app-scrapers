import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
MAIN_URL = os.environ.get('MAIN_URL')



def output_to_json(obj, filename):
    with open(filename, 'w+') as fn:
        json.dump(obj, fn)

def get_soup(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.content, "lxml")