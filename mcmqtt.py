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
#     (voir README pour détails)
#   - Librairie paho-mqtt -> https://github.com/eclipse/paho.mqtt.python
#   - Tâche planifiée (via cron, par exemple) qui appelle ce script à intervalle régulier
#

print("--- MC-MQTT ---")
print("Initialisation...")

# Importation des librairies
import paho.mqtt.client as mqtt
import requests
import datetime
import time

# Importation des paramètres secrets
import secrets

# Définition des variables
mqttTopicJoueursNb = "minecraft/joueurs/nb"
mqttTopicJoueursListe = "minecraft/joueurs/liste"
mqttTopicVersion = "minecraft/version"
mqttTopicMotd = "minecraft/motd"
mqttTopicUptime = "minecraft/uptime"
mqttTopicPlugins = "minecraft/plugins"

print("OK!")

# Obtention des informations de l'API REST du serveur Minecraft
# et stockage dans des objets JSON.

try:
  print ("Contact de l'API REST...")
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
  uptime = uptime.replace(" day", "j")
  # Retrait des secondes
  uptime = uptime[:-3]
  uptime = uptime.replace(":", "h ")
  uptime = uptime + "m"

  # Traitement de la liste des joueurs pour nettoyer les caractères spéciaux
  # et pour calculer le nombre de joueurs
  listeJoueurs = ""
  nbJoueurs = 0
  for joueur in infoPlayers:
    listeJoueurs = listeJoueurs + joueur["displayName"] + " - "
    nbJoueurs = nbJoueurs + 1
  # Retrait des codes de couleur
  listeJoueurs = listeJoueurs.replace("§4", "")
  listeJoueurs = listeJoueurs.replace("§r", "")
  listeJoueurs = listeJoueurs.replace("§e", "")

  # Retrait des 3 caractères de trop à la fin
  listeJoueurs = listeJoueurs[:-3]

  print ("OK!")
except:
  print("ERREUR: Impossible d'obtenir les informations via l'API REST")
  exit()


try:
  print("Envoi vers MQTT...")
  # Initialisation du client MQTT
  client = mqtt.Client()
  client.username_pw_set(secrets.mqttUser, password=secrets.mqttPass)
  client.connect(secrets.mqttServer, secrets.mqttPort, 60)

  # Publication des données sur le serveur MQTT
  client.publish(mqttTopicUptime, uptime)
  time.sleep (0.25)
  client.publish(mqttTopicVersion, infoServer["version"])
  time.sleep (0.25)
  client.publish(mqttTopicMotd, infoServer["motd"])
  time.sleep (0.25)
  client.publish(mqttTopicJoueursListe, listeJoueurs)
  time.sleep (0.25)
  client.publish(mqttTopicJoueursNb, nbJoueurs)
  time.sleep (0.25)

  # Déconnexion
  client.disconnect()

  print("OK!")
except:
  print("ERREUR: Impossible de publier sur MQTT")


# Fin du programme
print ("--- Opération complétée ---")
