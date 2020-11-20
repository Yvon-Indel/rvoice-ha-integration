import logging

_LOGGER = logging.getLogger(__name__)

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "mqtt_rvoice"

# List of integration names (string) your integration depends upon.
DEPENDENCIES = ["mqtt"]

CONF_TOPIC = "topic"
DEFAULT_TOPIC_PUB = "/tts/message"
DEFAULT_TOPIC_SUB = "/tts/lienmp3"

def setup(hass, config):
    """Set up the MQTT 2 ResponsiveVoice."""
    mqtt = hass.components.mqtt
    topic_pub = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC_PUB)
    topic_sub = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC_SUB)   
    entity_id = "mqtt_rvoice.last_message"
    entity_id2 = "mqtt_rvoice.mp3_link"
    entity_id3 = "mqtt_rvoice.last_player"
    entity_id4 = "mqtt_rvoice.last_volume"

    # Listener to be called when we receive a message.
    # The msg parameter is a Message object with the following members:
    # - topic, payload, qos, retain
    def message_received(msg):
        """Handle new MQTT messages."""
        hass.states.set(entity_id2, msg.payload)
        media_link = hass.states.get(entity_id2).state
        media_tts = hass.states.get(entity_id).state
        media_id = hass.states.get(entity_id3).state
        media_volume = float(hass.states.get(entity_id4).state)
        _LOGGER.debug('Last tts responsive voice: ')
        _LOGGER.debug('1/4 media_id: ' + str(media_id))
        _LOGGER.debug('2/4 mp3 link: ' + str(media_link))
        _LOGGER.debug('3/4 media_tts: ' + str(media_tts))
        _LOGGER.debug('4/4 media_volume: ' + str(media_volume))
        hass.services.call('media_player', 'volume_set', {"entity_id": media_id,"volume_level": media_volume}, False)
        hass.services.call('media_player', 'play_media', {"entity_id": media_id,"media_content_id":msg.payload,"media_content_type": "music"}, False)
    # Subscribe our listener to a topic.
    mqtt.subscribe(topic_sub, message_received)

    # Set the initial state.
    hass.states.set(entity_id, "No message")
    hass.states.set(entity_id2, "No link")
    hass.states.set(entity_id3, "No player")
    hass.states.set(entity_id4, "No volume")

    # Service to publish a message on MQTT.
    def set_state_service(call):
        """Service to send a message."""
        mqtt.publish(topic_pub, call.data.get("message"))
        hass.states.set(entity_id, call.data.get("message"))
        hass.states.set(entity_id3, call.data.get("entity_id"))
        hass.states.set(entity_id4, call.data.get("volume"))
    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, "play", set_state_service)

    # Return boolean to indicate that initialization was successfully.
    return True