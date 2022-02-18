# mc-mqtt

### Script qui récupère des infos sur un serveur Minecraft via une API REST offerte par le plugin ServerTap et les publie sur un serveur MQTT.


#### Prérequis

- Serveur Minecraft JAVA avec Plugin [ServerTap](https://github.com/phybros/servertap)
- Fichier "secrets.py" que vous devez créer, et qui contient les informations confidentielles
- Librairie [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)



#### Exemple de fichier secrets.py

```
mqttServer = "192.168.1.104"
mqttPort = 1883
mqttUser = "utilisateur"
mqttPass = "motdepasse"
apiURL = "http://192.168.1.104:4567/v1/"
```
