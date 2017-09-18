import appdaemon.appapi as appapi

#
# Chromecast volume card
#
# Args:
# names: dining room, kitchen, stereo
#

class ChromecastVolume(appapi.AppDaemon):

  def initialize(self):

    # check duration parameter - feedback loop still not work properly
    # mute method cycles through and checks/compares/stores values as required.

    self.names = self.args['names'].split(",")
    self.sliders = {}
    self.sensors = {}
    self.media_players = {}
    self.mute_vols = {}

    for name in self.names:
        self.sliders[name] = "input_slider.chromecast_volume_{}".format(name)
        self.sensors[name] = "sensor.chromecast_volume_{}".format(name)
        self.media_players[name] = "media_player.{}".format(name)
        self.mute_vols[name] = 0

    for sensor in self.sensors:
        self.listen_state(self.update_slider, entity = self.sensors[sensor], chromecast_name = sensor)

    for slider in self.sliders:
        self.listen_state(self.update_volume, entity = self.sliders[slider], chromecast_name = slider)

    self.listen_state(self.mute, entity = "input_boolean.chromecast_mute")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):

    chromecast_name = kwargs['chromecast_name']

    sensor_value = self.get_state(self.sensors[chromecast_name])

    if sensor_value != new_state:
        self.log("update volume from {} to {}".format(sensor_value, new_state))
        self.call_service("media_player/volume_set", entity_id = self.media_players[chromecast_name], volume_level = new_state)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):

    chromecast_name = kwargs['chromecast_name']

    slider_value = self.get_state(self.sliders[chromecast_name])

    if slider_value != new_state:
      self.log("update slider from {} to {}".format(slider_value, new_state))
      self.call_service("input_slider/select_value", entity_id = self.sliders[chromecast_name], value = new_state)

  def mute(self, entity, attribute, old_state, new_state, kwargs):

    if new_state == "on":
        mute_status = "true"
    elif new_state == "off":
        mute_status = "false"

    for media_player in self.media_players:
      self.call_service("media_player/volume_mute", entity_id = self.media_players[media_player], is_volume_muted = mute_status)
