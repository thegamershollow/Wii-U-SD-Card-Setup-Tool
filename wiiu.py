import bs4, colorama, os, pathlib, sys, urllib.request, io, requests, shutil, json, numpy as np, pandas as pd
from bs4 import BeautifulSoup; from colorama import Fore; from zipfile import ZipFile; from collections import namedtuple

hbaRepo = 'https://wiiu.cdn.fortheusers.org/repo.json'
hbaCDN = 'https://wiiu.cdn.fortheusers.org/zips/'
hbaDL = 'https://wiiu.cdn.fortheusers.org/zips/appstore.zip'
aromaUpdater = 'https://github.com/thegamershollow/hbl-apps/releases/download/aromaUPD/AromaUpdater.wuhb' #'https://github.com/wiiu-env/AromaUpdater/releases/'
aromaPackages = 'https://aroma.foryour.cafe/api/download?packages=bloopair,wiiload,ftpiiu,sdcafiine,screenshotplugin,swipswapme,environmentloader,wiiu-nanddumper-payload'
aromaBase = 'https://github.com/wiiu-env/Aroma/releases/download/beta-14/aroma-beta-14.zip'
oscURL = 'https://oscwii.org/library/'
#def openZip(fileName: str):
#        zip = ZipFile(fileName)
#        zip.extractall()
#        zip.close()
        
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
                print(Fore.RESET+'Downloading '+fileName+': '+Fore.CYAN+f"{Percent}%")
                r = requests.get(url, fileName)
        print(Fore.GREEN+'\nDone Downloading: '+ fileName+'\n'+Fore.RESET)
        f = open(fileName,'wb')
        f.write(r.content)

appList = ['nanddumper', 'UFDiine', 'UFDiine-wuhb', 'loadiine_gx2', '100_Boxes_Wiiu', 'IOSreboot', 'savemii_inject_mod', 'diibugger', 'tictactoe', 'tik2sd', 'WiiUIdent', 'TicketCleaner', 'Utag', 'lameIRCU', 'AM64DSPatcher', 'SDGeckiine', 'sigpatcher2sysmenu', 'ftpiiu', 'Bloopair', 'ftpiiu-cbhc', 'wudump', 'Button-Break', 'HBL_Dpad', 'WiiAlarmU', 'wudd-wuhb', 'WiiUReboot', 'PacmanGX2', 'wiiu-vnc', 'ftpiiu_everywhere', 'sign_c2w_patcher', 'cfwbooter', 'fireplace-nx-wiiu', 'mocha_fshax', 'TCPgecko', 'flappy_bird', 'spacegame', 'otp2sd', 'menu_sort', 'ddd', 'asturoids', 'wuphax', 'FesTool', 'survey', 'SwipSwapMe_WUPS', 'Bloopair-Tiramisu', 'Screenshot_WUPS', 'wup_installer_gx2_wuhb', 'mocha', 'saviine', 'haxchi', 'SDCafiine_WUPS', 'disc2appWUTPort', 'AocPatcher', 'Opensupaplex', 'swipswapme', 'vwii-compat-installer', 'swapdrc', 'SDcafiine', 'hid_keyboard_monitor', 'Minesweeper_WiiU', 'cbhc', 'loadiine_gx2_y', 'SaveMiiModWUTPort', 'pong', 'hidtovpad', 'wudd', 'homebrew_launcher', 'wupymod', 'PokeMiniU', 'timingu', 'CHIP8', 'gbiine', 'VidChanger', 'drc-test', 'more_ra_arcade', 'wupinstaller', 'wup_installer_gx2_mod', 'nnupatcher', 'NUSspli-Lite', 'TetrisU', 'jezzballu', 'wup_installer_gx2', 'ourloader', 'retroarch', 'spiik', 'MultiDRCSpaceDemo', 'u-paint', 'ft2sd', 'Uclick', 'CafeLoader', 'iosuotp', 'Trogdor-Reburninated', 'Padcon', 'appstore', 'LiveSynthesisU', 'vWii_decaffeinator', 'sm4sh2sd', 'snake', 'SuDokuL', 'wups', 'moonlight-wiiu', 'CloseHBL', 'mocha_fat32', 'shutdown-hbl', 'yapesdl', 'disc2app', 'clock', 'dumpling', 'flappy_bird_3d', 'savemii', 'USBHide', 'geckiine', 'hbl2hbc', 'seeprom2sd', 'vWii-NAND-Restorer', 'GamepadTester', 'Simple_SDL_Snake', 'fuckyoustick', 'ScreenStreaming_WUPS', 'more_ra_cores', 'UselessHomebrew', 'DiiBugger_WUPS', 'PluginPlayground_WUPS', 'ThemeMii', 'keyboard_example', 'hbl_dark', 'WiiU-Shell', 'wim', 'controller-test', 'hidtest', 'UsendMii_Client', 'HIDtoVPAD_WUPS', 'GiveMiiYouTube', 'fsdumper', 'sigpatcher2HBL', 'vgedit', 'ntrview-wiiu', 'RemotePad', 'swapdrc_lite', 'cave', 'Pokemini', 'gacubeboy', 'mocha_sd_access', 'Fireplace-NXU', 'Crispy-Doom']
sdPath = ''
path = pathlib.Path('.sdpath')
if path.is_file() != True:
    giveSdPath = input('Please specify the path of your Wii U SD Card: ')
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
    print('Please reinsert the SD Card and try again')
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

cache = pathlib.Path('cache')
if cache.exists() != True:
    os.mkdir('cache')

#*Download/Update Base Homebrew Files
if prompt == '1':
    os.system('clear')
    os.chdir('cache')
    hbl = download(hbaDL,'appstore.zip')
    hbl = ZipFile('appstore.zip','r')
    hbl.extractall()
    hbl.close
    aPKG = download(aromaPackages, 'aromapkgs.zip')
    aPKG = ZipFile('aromapkgs.zip','r')
    aPKG.extractall()
    aPKG.close
    aroma = download(aromaBase, 'aroma.zip')
    aroma = ZipFile('aroma.zip','r')
    aroma.extractall()
    aroma.close
    print('Finished downloading the base SD Card Files.\n')
    shutil.copytree('wiiu',sd+'/wiiu/',dirs_exist_ok=True)
    print('Copied files to SD Card!\n')
    print('Exiting Program')
    sys.exit(3)

#*Download/Update Wii U Homebrew Apps
if prompt == '2':
    os.system('clear')
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
    table.drop(columns=["binary", "title", "license", "url", "changelog", "screens", "extracted", "details", "md5", "description"],inplace=True,)
    table = table.reindex(columns=["name", "author", "category", "version", "filesize"])
    table.rename(columns={"category": "Category", "version" : "Version", "filesize" : "Download Size(KB)", "app_dls" : "App Downloads", "author" : "Author", "updated" : "Update Date","name" : "App Name"},inplace=True,)
    print(table.to_string())
    # asks for input of what app/s you want to download
    hbSelect = input('Type the app/s name/ to download it '+Fore.LIGHTCYAN_EX+'**if multiple are selected this process will take a lot longer**'+Fore.RESET+'\n\nSeperate the app names with commas if you want to download multiple apps at once.\n\nSelection: '); hbSelect = hbSelect.split(',')
    apps = table['App Name'].values.tolist()
    for item in hbSelect:
        if item in apps:
            os.chdir(cache)
            dlURL = hbaCDN+item+'.zip'
            dl = download(dlURL,item+'.zip')
            dl = ZipFile(item+'.zip')
            dl.extractall()
            dl.close
            shutil.copytree('wiiu',sd+'/wiiu/',dirs_exist_ok=True)

#*Download/Update VWii Homebrew Apps
if prompt == '3':
    os.system('clear')
#* Delete all files from SD card
if prompt == '4':
    warn=input(Fore.RED+'*⚠️WARNING⚠️* '+Fore.RESET+'This will delete/remove all files from the SD card\nContinue (Y/N):\n')
    if warn == 'Y' or warn == 'y':
        shutil.rmtree(sd, ignore_errors=True)
        sys.exit(1)
    sys.exit(1)
#*Exit program
if prompt == '5':
    sys.exit(4)


