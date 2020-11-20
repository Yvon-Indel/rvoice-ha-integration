
# rvoice-ha-integration
This is the Home Assistant integration for using with the [rvoice-mqtt-gateway](http://handlebarsjs.com/)

## Features
* Send a TTS message to the rvoice-mqtt-gateway using MQTT
* Play back the mp3 link of a TTS message on a media player

### Prerequisites
* The [rvoice-mqtt-gateway](http://handlebarsjs.com/) is up and running.
* You know how to access to the [config file of HA](https://www.home-assistant.io/getting-started/configuration/)

### Install the integration on Home Assistant
#### Copy files in config directory
 - Go to your HA custom components directory: \config\custom_components
 If it's your first custom componenet, you have to create this
   directory. 
   
 - Create a subdirectory mqtt_rvoice 
 
 - Copy all the file in
   \config\custom_components\mqtt_rvoice

#### Add integration in configuration.yaml
Add this to the file configuration.yaml:

    #tts responsivevoice
    mqtt_rvoice:  

## Configuration
There is **no configuration if you use the default MQTT topics** in the rvoice-mqtt-gateway setup.
If not, you have to change these lines in the file ***\_\_init\_\_.py*** , according to your own MQTT topics :

    DEFAULT_TOPIC_PUB = "/tts/message"
    DEFAULT_TOPIC_SUB = "/tts/lienmp3"
In both case, it's time to **restart Home Assistant**
 
## How it work
The integration create a service called ***mqtt_rvoice.play***

 - This service send a mqtt message on the TOPIC_PUB with the message
    you want to tts as payload.
 - The service get back a mqtt message on
    the TOPIC_SUB with the url of the tts mp3 file as payload. 
 - The service send the mp3 link to the player.

The integration create also **4 sensors** :
 - ***mqtt_rvoice.last_message*** : state is the last message sent
 - ***mqtt_rvoice.last_player*** : state is the last media player used
 - ***mqtt_rvoice.last_volume*** : state is the last volume used
 - ***mqtt_rvoice.mp3_link*** :state is the mp3 link of the last message sent

 ![rvoice_sensors]( https://github.com/Yvon-Indel/rvoice-ha-integration/blob/main/sensors.jpg)


## How to use
### Testing

You can test the integration in the Developer Tools :
 - select ***mqtt_rvoice.play*** as service
 
 - select ***a media player*** of your choice as entity
 
 - add a message to speak :
    message: 'C''est super, ça fonctionne'
    
 - set the volume:
    volume: 0.5

![developer tools](https://github.com/Yvon-Indel/rvoice-ha-integration/blob/main/Devtool.jpg)

### Using in automation
Here is an exemple of an automation playing aa message when my 3d print is over. 
   

       #Fin d'impression 3D 
            - alias: fin impression 3d
              trigger:
                platform: numeric_state
                entity_id: sensor.imprimante_3d_mss310_power_sensor_w_0
                below: 30
                for:
                  minutes: 1    
              action:
              - service: mqtt_rvoice.play
                data:
                  entity_id: media_player.veranda
                  message: "Attention, l'impression 3 dé est terminée, je répète: l'impression 3 dé est terminée."
                  volume: 0.6
          
## To do list
 - Using HACS for install process, 
 - Set some parametrers to change MQTT
   topics, 
 - ...

## Authors
It's my first integration, so please, be tolerant.

## License

[GPL3-0](https://github.com/Yvon-Indel/rvoice-mqtt-gateway/blob/master/LICENSE)


