import os, sys, requests, shutil, json, pandas as pd
from colorama import Fore; from zipfile import ZipFile; from collections import namedtuple;

hbaRepo = 'https://wiiu.cdn.fortheusers.org/repo.json'
hbaCDN = 'https://wiiu.cdn.fortheusers.org/zips/'
hbaDL = 'https://wiiu.cdn.fortheusers.org/zips/appstore.zip'
aromaUpdater = 'https://github.com/thegamershollow/hbl-apps/releases/download/aromaUPD/AromaUpdater.wuhb'
aromaPackages = 'https://aroma.foryour.cafe/api/download?packages=bloopair,wiiload,ftpiiu,sdcafiine,screenshotplugin,swipswapme,environmentloader,wiiu-nanddumper-payload'
aromaBase = 'https://github.com/wiiu-env/Aroma/releases/download/beta-14/aroma-beta-14.zip'
oscURL = 'https://api.oscwii.org/v2/primary/packages'
oscCDN = 'https://hbb1.oscwii.org/hbb/'
vwiiDl = 'https://github.com/thegamershollow/custom-tiramisu-environment/raw/main/custom-tiramisu-environment.zip'

# download function with status        
def download(url: str, fileName: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    length = response.headers.get('content-length')
    block_size = 1000000  # default value
    if length:
        length = int(length)
        block_size = max(4096, length // 20)
    with open(fileName, 'wb') as f:
        size = 0
        for buffer in response.iter_content(block_size):
            if not buffer:
                break
            f.write(buffer)
            size += len(buffer)
            if length:
                percent = int((size / length) * 100)
                print(Fore.RESET+"Downloading"+f[fileName]+':'+Fore.CYAN+f"{percent}%", end='\r')
    print(Fore.GREEN+"\nDone Downloading:"+Fore.CYAN+f"{fileName}"+Fore.RESET)

# json decoder function
def jsonDecoder(jsonDict):
    return namedtuple('x', jsonDict.keys())(*jsonDict.values())

# base homebrew check function
def nohb():
    noWIIU = os.path.isdir(sd+'/wiiu')
    if noWIIU != True:
        print(Fore.RED+'please download the base homebrew apps before downloading anything else')
        sys.exit(5)
#*main function
sdPath = ''
sdVerify = os.path.isfile('.sdpath')
if sdVerify != True:
    giveSdPath = input('Please specify the path of your '+Fore.CYAN+'Wii U'+Fore.RESET+' SD Card: ')
    f = open('.sdpath','w')
    giveSdPath = giveSdPath.replace("'","")
    f.write(giveSdPath)
    f.close
    sdPath = giveSdPath
f = open('.sdpath','r')
sd = f.read()
f.close
sdPath = os.path.isdir(sd)
if sdPath != True:
    print(Fore.RED+'Please reinsert the SD Card and try again')
    sys.exit(1)

# prompt for the whole program
prompt = input('What would you like to do?\nType the number of the corrasponding option that you want to select\n\n1. Download/Update base SD Card files\n2. Download/Update Wii U Homebrew Apps\n3. Download/Update files needed for vWii mod\n4. Download/Update Wii Homebrew\n5. Remove all files from Wii U SD Card\n6. Use a diffrent SD card\n7. Exit\n\nOption: ')

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
    nohb
    # opens the repo.json file located at: https://wiiu.cdn.fortheusers.org/repo.json
    repo = requests.get(hbaRepo)
    jsonSrc = repo.text
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
    # converts list into a printable pkgTable
    pkgTable = pd.DataFrame(allPkg)
    pkgTable.drop(columns=["binary", "title", "license", "url", "changelog", "screens", "extracted", "details", "md5", "description"],inplace=True,)
    pkgTable = pkgTable.reindex(columns=["name", "author", "category", "version", "filesize"])
    pkgTable.rename(columns={"category": "Category", "version" : "Version", "filesize" : "Download Size(KB)", "app_dls" : "App Downloads", "author" : "Author", "updated" : "Update Date","name" : "App Name"},inplace=True,)
    print(pkgTable.to_string())
    # asks for input of what app/s you want to download
    hbSelect = input('Type the app/s name/ to download it '+Fore.LIGHTCYAN_EX+'**if multiple are selected this process will take a lot longer**'+Fore.RESET+'\n\nSeperate the app names with commas if you want to download multiple apps at once.\n\nSelection: '); hbSelect = hbSelect.split(',')
    apps = pkgTable['App Name'].values.tolist()
    os.chdir(sd)
    pkgPath = os.path.isdir(sd+'/wiiu/apps/appstore/.get/packages')
    if pkgPath() != True:
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
            dlPath = os.path.isdir(sd+'/wiiu/apps/appstore/.get/packages/'+item)
            if dlPath != False:
                os.remove(sd+'/manifest.install')
                os.remove(sd+'/info.json')
            if dlPath != True:
                os.mkdir(sd+'/wiiu/apps/appstore/.get/packages/'+item)
                shutil.move(sd+'/manifest.install',sd+'/wiiu/apps/appstore/.get/packages/'+item)
                shutil.move(sd+'/info.json',sd+'/wiiu/apps/appstore/.get/packages/'+item)
            os.remove(sd+'/'+item+'.zip')
    print('\n'+Fore.GREEN+'Finished downloading app/s')

#*Download/Update vWii mod files
if prompt == '3':
    nohb
    os.system('clear')
    os.chdir(sd)
    vWii = download(vwiiDl,'vwii.zip')
    os.remove(sd+'/vwii.zip')

#*Download/Update VWii Homebrew Apps
if prompt == '4':
    os.system('clear')
    nohb
    oscApi = requests.get(oscURL)
    jsonFRMT = '{\n     "packages":'
    after = '}'
    jsonSrc = f'{jsonFRMT}{oscApi.text}'
    jsonSrc = jsonSrc.replace(']',' ]')
    jsonSrc += after
    osc = json.loads(jsonSrc, object_hook=jsonDecoder)
    count = 0
    oscTotal = osc.packages.__len__()
    allOSC = []
    for items in osc.packages.__iter__():
        allOSC.append(osc.packages[count])
        count = count+1
    allOSC = sorted(allOSC)
    oscTable = pd.DataFrame(allOSC)
    apps = oscTable['internal_name'].values.tolist()
    oscTable.drop(columns=["downloads", "extra_directories", "icon_url", "rating", "release_date", "shop_title_id", "shop_title_version", "long_description", "updated", "zip_size", "display_name", "package_type"],inplace=True,)
    oscTable = oscTable.reindex(columns=["internal_name", "category", "version", "short_description", "coder"])
    oscTable.rename(columns={"internal_name":"App Name","category":"Catergory","version":"Version","short_description":"Decription","coder":"Author"},inplace=True,)
    f = open('text.txt','w')
    f.write(oscTable.to_string())
    print(oscTable.to_string())
    oscSelect = input('Type the app/s name/ to download it '+Fore.LIGHTCYAN_EX+'**if multiple are selected this process will take a lot longer**'+Fore.RESET+'\n\nSeperate the app names with commas if you want to download multiple apps at once.\n\nSelection: '); oscSelect = oscSelect.split(',')
    os.chdir(sd)
    oscPath = os.path.isdir(sd+'/apps')
    if oscPath != True:
        os.mkdir(sd+'/apps')
    for item in oscSelect:
        if item in apps:
            dlURL = oscCDN+item+'/'+item+'.zip'
            dl = download(dlURL,item+'.zip')
            dl = ZipFile(item+'.zip')
            dl.extractall()
            dl.close
            print('Copied '+Fore.CYAN+item+Fore.RESET+' to the SD card\n')
            #dlPath = os.path(sd+'/wiiu/apps/appstore/.get/packages/'+item)
            os.remove(sd+'/'+item+'.zip')
    print('\n'+Fore.GREEN+'Finished downloading app/s')
    

#*Delete all files from SD card
if prompt == '5':
    os.system('clear')
    warn=input(Fore.RED+'*⚠️WARNING⚠️* '+Fore.RESET+'This will delete/remove all files from the SD card\nContinue (Y/N):\n')
    if warn == 'Y' or warn == 'y':
        shutil.rmtree(sd, ignore_errors=True)
        os.system('exit')
        sys.exit()
    sys.exit()

#*Use a different sd card
if prompt == '6':
    os.system('clear')
    os.remove('.sdpath')

#*Exit program
if prompt == '7':
    os.system('exit')
    sys.exit()