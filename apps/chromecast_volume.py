import appdaemon.appapi as appapi

#
# Chromecast volume card
#
# Args:
#

class ChromecastVolume(appapi.AppDaemon):

  def initialize(self):

    self._kitchen_slider = "input_slider.chromecast_volume_kitchen"
    self._kitchen_sensor = "sensor.chromecast_volume_kitchen"

    self.listen_state(self.update_volume, self._kitchen_slider)
    self.listen_state(self.update_slider, self._kitchen_sensor)

    # self.listen_state(self.update_volume, "input_slider.chromecast_volume_stereo")
    # self.listen_state(self.update_slider, "sensor.chromecast_volume_stereo")
    # self.listen_state(self.mute, "input_boolean.chromecast_mute")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):

    sensor_vol = self.get_state(self._kitchen_sensor)

    if sensor_vol != new_state:
      self.log("volume {} {}".format(sensor_vol, new_state))
      self.call_service("media_player/volume_set", entity_id = "media_player.kitchen", volume_level = new_state)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):

    slider_vol = self.get_state(self._kitchen_slider)

    if slider_vol != new_state:
      self.log("slider {} {}".format(slider_vol, new_state))
      self.call_service("input_slider/select_value", entity_id = "input_slider.chromecast_volume_kitchen", value = new_state)


  def mute(self, entity, attribute, old_state, new_state, kwargs):
    # if new_state == "on":
    #     self.log("log: {}".format(entity))
    # mute_volume_kitchen = self.get_state()

    self.log("mute: {}".format(new_state))
