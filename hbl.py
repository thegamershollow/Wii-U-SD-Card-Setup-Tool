import bs4, colorama, os, pathlib, sys, urllib.request, urllib.error, io, requests, shutil, json, numpy as np, pandas as pd, re
from bs4 import BeautifulSoup; from colorama import Fore; from zipfile import ZipFile; from collections import namedtuple

# urls for the base download servers of the files
hbaRepo = 'https://wiiu.cdn.fortheusers.org/repo.json'
hbaCDN = 'https://wiiu.cdn.fortheusers.org/zips/'

repo = requests.get(hbaRepo)
jsonSrc = repo.text
def jsonDecoder(jsonDict):
    return namedtuple('package', jsonDict.keys())(*jsonDict.values())
pkg = json.loads(jsonSrc, object_hook=jsonDecoder)
count = 0
pkgTotal = pkg.packages.__len__()
# create an empty list
allPkg = []
# iterate through items in json file
for items in pkg.packages.__iter__():
    allPkg.append(pkg.packages[count])
    count = count+1
# sorts the list alphabetically
allPkg = sorted(allPkg)
# converts list into a printable table
table = pd.DataFrame(allPkg)
table.drop(columns=["binary", "license", "url", "changelog", "screens", "extracted", "details", "md5", "description"],inplace=True,)
table = table.reindex(columns=["title", "author", "category", "version", "filesize", "app_dls"])
table.rename(columns={"category": "Category", "title": "App Name", "version" : "Version", "filesize" : "Download Size(KB)", "app_dls" : "App Downloads", "author" : "Author", "updated" : "Update Date"},inplace=True,)
print(table.to_string())