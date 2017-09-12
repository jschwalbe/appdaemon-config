import appdaemon.appapi as appapi

#
# Chromecast volume card
#
# Args:
# names: dining room, kitchen, stereo
#

class ChromecastVolume(appapi.AppDaemon):

  def initialize(self):

    # create dict of components based on chromecast input names
    # mute method cycles through and checks/compares/stores values as required.

    self.cc_name = self.args['name']
    self.cc_sensor = "sensor.chromecast_volume_{}".format(self.cc_name)
    self.cc_slider = "input_slider.chromecast_volume_{}".format(self.cc_name)
    self.cc_media_player = "media_player.{}".format(self.cc_name)
    self.mute_vol = 0

    self.listen_state(self.update_volume, self.cc_slider) # check to see if duration is required
    self.listen_state(self.update_slider, self.cc_sensor, duration = 0.1)
    self.listen_state(self.mute, "input_boolean.chromecast_mute")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):

    sensor_vol = self.get_state(self.cc_sensor)

    if sensor_vol == "unknown":
        self.log("{} is off".format(self.cc_name))

    elif sensor_vol != new_state:
        self.log("update volume from {} to {}".format(sensor_vol, new_state))
        self.call_service("media_player/volume_set", entity_id = self.cc_media_player, volume_level = new_state)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):

    slider_vol = self.get_state(self.cc_slider)

    if slider_vol != new_state:
      self.log("update slider from {} to {}".format(slider_vol, new_state))
      self.call_service("input_slider/select_value", entity_id = self.cc_slider, value = new_state)

  def mute(self, entity, attribute, old_state, new_state, kwargs):

    sensor_vol = self.get_state(self.cc_sensor)

    if new_state == "on":
        self.mute_vol = self.get_state(self.cc_sensor)
        self.call_service("media_player/volume_set", entity_id = self.cc_media_player, volume_level = 0)

    elif new_state == "off":
        self.call_service("media_player/volume_set", entity_id = self.cc_media_player, volume_level = self.mute_vol)
