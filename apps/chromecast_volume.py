import appdaemon.appapi as appapi

#
# Chromecast volume card
#
# Args:
# names: dining room, kitchen, stereo
#

class ChromecastVolume(appapi.AppDaemon):

  def initialize(self):

    self.cc_name = self.args['name']
    self.cc_sensor = "sensor.chromecast_volume_{}".format(self.cc_name)
    self.cc_slider = "input_slider.chromecast_volume_{}".format(self.cc_name)
    self.cc_media_player = "media_player.{}".format(self.cc_name)
    self.mute_vol = 0

    self.listen_state(self.update_volume, self.cc_slider)
    self.listen_state(self.update_slider, self.cc_sensor)
    self.listen_state(self.mute, "input_boolean.chromecast_mute")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):

    sensor_vol = self.get_state(self.cc_sensor)

    if sensor_vol == "unknown":
        self.log("{} is off".format(self.cc_name))

    else:
        vol_diff = abs(float(sensor_vol) - float(new_state))

        if sensor_vol != new_state and vol_diff > 0.04:
          self.log("update volume from {} to {}".format(sensor_vol, new_state))
          self.call_service("media_player/volume_set", entity_id = self.cc_media_player, volume_level = new_state)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):

    slider_vol = self.get_state(self.cc_slider)

    vol_diff = abs(float(slider_vol) - float(new_state))

    if slider_vol != new_state and vol_diff > 0.04:
      self.log("update slider from {} to {}".format(slider_vol, new_state))
      self.call_service("input_slider/select_value", entity_id = self.cc_slider, value = new_state)

  def mute(self, entity, attribute, old_state, new_state, kwargs):

    sensor_vol = self.get_state(self.cc_sensor)

    if new_state == "on":
        self.mute_vol = self.get_state(self.cc_sensor)
        self.call_service("media_player/volume_set", entity_id = self.cc_media_player, volume_level = 0)

    elif new_state == "off":
        self.call_service("media_player/volume_set", entity_id = self.cc_media_player, volume_level = self.mute_vol)
