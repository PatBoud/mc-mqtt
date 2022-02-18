#
# MCMQTT
# Script qui prend les infos du serveur Minecraft via le plugin ServerTap
# et les envoie sur un serveur MQTT.
#
# Prérequis:
#   - Serveur Minecraft JAVA avec Plugin ServerTap
#   - Fichier "secrets.py" qui contient les informations confidentielles
#   - Librairie paho-mqtt -> https://github.com/eclipse/paho.mqtt.python
#

import secrets

