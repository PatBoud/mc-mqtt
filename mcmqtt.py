#!/usr/bin/python3
#
# MCMQTT
# Script qui prend les infos du serveur Minecraft via le plugin ServerTap
# et les envoie vers un serveur MQTT.
#
# PatBoud
# 2022-02-17
#
# Prérequis:
#   - Serveur Minecraft JAVA avec Plugin ServerTap
#   - Fichier "secrets.py" qui contient les informations confidentielles
#   - Librairie paho-mqtt -> https://github.com/eclipse/paho.mqtt.python
#

# Importation des librairies
from time import sleep
import paho.mqtt.client as mqtt
import requests
import datetime

# Importation des paramètres secrets
# Le fichier secrets.py doit contenir ceci:
#
# mqttServer = ""
# mqttPort = 1883
# mqttUser = ""
# mqttPass = ""
# apiURL = "http://xxxxxx:4567/v1/"
#
import secrets


# Définition des variables
mqttTopicJoueursNb = "minecraft/joueurs/nb"
mqttTopicJoueursListe = "minecraft/joueurs/liste"
mqttTopicVersion = "minecraft/version"
mqttTopicMotd = "minecraft/motd"
mqttTopicUptime = "minecraft/uptime"
mqttTopicPlugins = "minecraft/plugins"
delais = 10


# Initialisation du client MQTT
def on_connect(client, userdata, flags, rc):
  print("Connecté au serveur. Result code: "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(secrets.mqttUser, password=secrets.mqttPass)
client.connect(secrets.mqttServer, secrets.mqttPort, 60)
  

# Boucle infinie
while (True):
  client.loop()

  # Obtention des informations de l'API REST du serveur Minecraft
  # et stockage dans des objets JSON.
  print ("Contact de l'API REST")

  # Informations serveur
  response = requests.get(secrets.apiURL + "server")
  infoServer = response.json()

  # Informations joueurs
  response = requests.get(secrets.apiURL + "players")
  infoPlayers = response.json()


  # Traitement du uptime pour afficher une valeur lisible
  uptimeSecondes = infoServer["health"]["uptime"]
  uptime = datetime.timedelta(seconds = uptimeSecondes)
  uptime = str(uptime)
  uptime = uptime.replace("day", "jour")

  # Traitement de la liste des joueurs pour nettoyer les caractères spéciaux
  # et pour calculer le nombre de joueurs
  listeJoueurs = ""
  nbJoueurs = 0
  for joueur in infoPlayers:
    listeJoueurs = listeJoueurs + joueur["displayName"] + "  "
    nbJoueurs = nbJoueurs + 1
  
  listeJoueurs = listeJoueurs.replace("§4", "")
  listeJoueurs = listeJoueurs.replace("§r", "")


  # Publication des données sur le serveur MQTT
  client.publish(mqttTopicUptime, uptime, qos=0, retain=False)
  client.publish(mqttTopicVersion, infoServer["version"])
  client.publish(mqttTopicMotd, infoServer["motd"])
  client.publish(mqttTopicJoueursListe, listeJoueurs)
  client.publish(mqttTopicJoueursNb, nbJoueurs)

  # Attente selon le délais défini
  sleep(delais)
