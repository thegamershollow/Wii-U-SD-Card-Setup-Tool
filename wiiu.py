import os, pathlib, sys, urllib.request, io, requests, shutil, json, pandas as pd
from colorama import Fore; from zipfile import ZipFile; from collections import namedtuple;

hbaRepo = 'https://wiiu.cdn.fortheusers.org/repo.json'
hbaCDN = 'https://wiiu.cdn.fortheusers.org/zips/'
hbaDL = 'https://wiiu.cdn.fortheusers.org/zips/appstore.zip'
aromaUpdater = 'https://github.com/thegamershollow/hbl-apps/releases/download/aromaUPD/AromaUpdater.wuhb' #'https://github.com/wiiu-env/AromaUpdater/releases/'
aromaPackages = 'https://aroma.foryour.cafe/api/download?packages=bloopair,wiiload,ftpiiu,sdcafiine,screenshotplugin,swipswapme,environmentloader,wiiu-nanddumper-payload'
aromaBase = 'https://github.com/wiiu-env/Aroma/releases/download/beta-14/aroma-beta-14.zip'
oscURL = 'https://oscwii.org/library/'

# download function with status        
def download(url: str, fileName: str):
    with urllib.request.urlopen(url) as Response:
        Length = Response.getheader('content-length')
        BlockSize = 1000000  # default value
        if Length:
            Length = int(Length)
            BlockSize = max(4096, Length // 20)
        BufferAll = io.BytesIO()
        Size = 0
        while True:
            BufferNow = Response.read(BlockSize)
            if not BufferNow:
                break
            BufferAll.write(BufferNow)
            Size += len(BufferNow)
            if Length:
                Percent = int((Size / Length)*100)
                print(Fore.RESET+'Downloading '+Fore.BLUE+fileName+Fore.RESET+': '+Fore.CYAN+f"{Percent}%")
                r = requests.get(url, fileName)
        print(Fore.GREEN+'\nFinished Downloading: '+Fore.CYAN+ fileName+'\n'+Fore.RESET)
        f = open(fileName,'wb')
        f.write(r.content)

sdPath = ''
path = pathlib.Path('.sdpath')
if path.is_file() != True:
    giveSdPath = input('Please specify the path of your '+Fore.CYAN+'Wii U'+Fore.RESET+' SD Card: ')
    f = open('.sdpath','w')
    giveSdPath = giveSdPath.replace("'","")
    f.write(giveSdPath)
    f.close
    sdPath = giveSdPath
f = open('.sdpath','r')
sd = f.read()
f.close
sdPath = pathlib.Path(sd)
if sdPath.exists() != True:
    print(Fore.RED+'Please reinsert the SD Card and try again')
    sys.exit(1)
with os.scandir(sdPath) as entries:
    for entry in entries:
        f = open('.cache','a')
        f.write(entry.name)
        f.write('\n')
        f.close
cache = pathlib.Path('cache')
if cache.exists() != False:
    shutil.rmtree('cache', ignore_errors=False, onerror=None)
cl = pathlib.Path('.cache')
if cl.exists() != False:
    os.remove('.cache')

prompt = input('What would you like to do?\nType the number of the corrasponding option that you want to select\n\n1. Download/Update base SD Card files\n2. Download/Update Wii U Homebrew Apps\n3. Download/Update Wii Homebrew\n4. Remove all files from Wii U SD Card\n5. Exit\n\nOption: ')

#*Download/Update Base Homebrew Files
if prompt == '1':
    os.system('clear')

    # changes directory to cache
    os.chdir(sd)
    # downloads the Homebrew appstore and extracts the zip file
    hbl = download(hbaDL,'appstore.zip')
    hbl = ZipFile('appstore.zip','r')
    hbl.extractall()
    hbl.close
    os.mkdir(sd+'/wiiu/apps/appstore/.get/packages')
    os.mkdir(sd+'/wiiu/apps/appstore/.get/packages/appstore')
    shutil.move(sd+'/manifest.install',sd+'/wiiu/apps/appstore/.get/packages/appstore')
    shutil.move(sd+'/info.json',sd+'/wiiu/apps/appstore/.get/packages/appstore')
    os.remove(sd+'/appstore.zip')

    # downloads the aroma packages and extracts the zip file
    aPKG = download(aromaPackages, 'aromapkgs.zip')
    aPKG = ZipFile('aromapkgs.zip','r')
    aPKG.extractall()
    aPKG.close
    os.remove(sd+'/aromapkgs.zip')

    # downloads the base files for aroma and extracts the zip file
    aroma = download(aromaBase, 'aroma.zip')
    aroma = ZipFile('aroma.zip','r')
    aroma.extractall()
    aroma.close
    os.remove(sd+'/aroma.zip')

    # copies the downloaded files from the cache directory to the sd card
    print(Fore.GREEN+'Finished downloading the '+Fore.CYAN+'base SD Card Files.'+Fore.RESET+'\n')

#*Download/Update Wii U Homebrew Apps
if prompt == '2':
    os.system('clear')
    noWIIU = pathlib.Path(sd+'/wiiu')
    if noWIIU.exists() != True:
        print(Fore.RED+'please download the base homebrew apps before installing homebrew apps')
        os.system('exit')
        sys.exit(5)
    # opens the repo.json file located at: https://wiiu.cdn.fortheusers.org/repo.json
    repo = requests.get(hbaRepo)
    jsonSrc = repo.text
    # defines a json decoder
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
    allPkg = sorted(allPkg)
    # converts list into a printable table
    table = pd.DataFrame(allPkg)
    table.drop(columns=["binary", "title", "license", "url", "changelog", "screens", "extracted", "details", "md5", "description"],inplace=True,)
    table = table.reindex(columns=["name", "author", "category", "version", "filesize"])
    table.rename(columns={"category": "Category", "version" : "Version", "filesize" : "Download Size(KB)", "app_dls" : "App Downloads", "author" : "Author", "updated" : "Update Date","name" : "App Name"},inplace=True,)
    print(table.to_string())

    # asks for input of what app/s you want to download
    hbSelect = input('Type the app/s name/ to download it '+Fore.LIGHTCYAN_EX+'**if multiple are selected this process will take a lot longer**'+Fore.RESET+'\n\nSeperate the app names with commas if you want to download multiple apps at once.\n\nSelection: '); hbSelect = hbSelect.split(',')
    apps = table['App Name'].values.tolist()
    os.chdir(sd)
    pkgPath = pathlib.Path(sd+'/wiiu/apps/appstore/.get/packages')
    if pkgPath.exists() != True:
        os.mkdir(sd+'/wiiu/apps/appstore/.get/packages')
    # downloads the homebrew apps specified in hbSelect
    for item in hbSelect:
        if item in apps:
            dlURL = hbaCDN+item+'.zip'
            dl = download(dlURL,item+'.zip')
            dl = ZipFile(item+'.zip')
            dl.extractall()
            dl.close
            print('Copied '+Fore.CYAN+item+Fore.RESET+' to the SD card\n')
            dlPath = pathlib.Path(sd+'/wiiu/apps/appstore/.get/packages/'+item)
            if dlPath.exists() != False:
                os.remove(sd+'/manifest.install')
                os.remove(sd+'/info.json')
            if dlPath.exists() != True:
                os.mkdir(sd+'/wiiu/apps/appstore/.get/packages/'+item)
                shutil.move(sd+'/manifest.install',sd+'/wiiu/apps/appstore/.get/packages/'+item)
                shutil.move(sd+'/info.json',sd+'/wiiu/apps/appstore/.get/packages/'+item)
            os.remove(sd+'/'+item+'.zip')
    print('\n'+Fore.GREEN+'Finished downloading app/s')

#*Download/Update VWii Homebrew Apps
if prompt == '3':
    os.system('clear')

#* Delete all files from SD card
if prompt == '4':
    os.system('clear')
    warn=input(Fore.RED+'*⚠️WARNING⚠️* '+Fore.RESET+'This will delete/remove all files from the SD card\nContinue (Y/N):\n')
    if warn == 'Y' or warn == 'y':
        shutil.rmtree(sd, ignore_errors=True)
        os.system('exit')
        sys.exit()
    sys.exit()
#*Exit program
if prompt == '5':
    os.system('exit')
    sys.exit()