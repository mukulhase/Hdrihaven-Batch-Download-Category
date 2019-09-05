from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import argparse

BASE_URL = "https://hdrihaven.com"
CATEGORY_URL = BASE_URL + "/hdris/category/"


def getCategories():
    content = requests.get(CATEGORY_URL).text
    soup = BeautifulSoup(content, 'html.parser')
    category_div = soup.find("div", {"class": "category-list-wrapper"})
    links = category_div.findAll("a")
    for link in links:
        url = link["href"]
        name = link.find("li").text
        yield url, name


def getImagesForCategory(url):
    url = BASE_URL + url
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    thumbnail_divs = soup.find("div", {"id": "hdri-grid"}).findAll("a")
    for i in thumbnail_divs:
        image_name = i['href'].split("h=")[1]
        yield image_name


def downloadImage(name):
    url = BASE_URL + "/files/hdris/%s_%s.hdr" % (name, "1k")
    response = requests.get(url, stream=True)
    with open(name + ".hdr", "wb") as handle:
        for data in response.iter_content():
            handle.write(data)


parser = argparse.ArgumentParser(description="A script to download all HDRIs of a certain category")
parser.add_argument("-mode", choices=['list', 'download'], default="list")
parser.add_argument("-category_url", default="/hdris/category/?c=all&o=popular")
cmd = parser.parse_args()

if cmd.mode == "categories":
    print("\n".join("%s: %s" % (name, url) for url, name in getCategories()))
else:
    for name in tqdm(getImagesForCategory(cmd.category_url)):
        downloadImage(name)
