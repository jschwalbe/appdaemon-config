import appdaemon.appapi as appapi

# Chromecast volume card
# 
# Updates the volume of a chromecast following a change of value from an input_slider. 
# Conversely, it will update the slider value should the volume of the chromecast be 
# updated from another input source (Google Home app, for example)
# 
# Args:
#   name: name of Chromecast as it appears in Homeassitant
#

class ChromecastVolume(appapi.AppDaemon):

  def initialize(self):


    self.name = self.args['name']
    self.slider = "input_slider.chromecast_volume_{}".format(self.name)
    self.sensor = "sensor.chromecast_volume_{}".format(self.name)
    self.media_player = "media_player.{}".format(self.name)

    # !!!!
    # check duration parameter - slide volume change still fires multiple service calls
    # !!!!
    self.listen_state(self.update_slider, entity = self.sensor, duration = 1)
    self.listen_state(self.update_volume, entity = self.slider)

    self.listen_state(self.mute_on, entity = "input_boolean.chromecast_mute", new = "on")
    self.listen_state(self.mute_off, entity = "input_boolean.chromecast_mute", new = "off")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):

    sensor_value = self.get_state(self.sensor)
    set_cc_vol = float(new_state) / 10

    if sensor_value != set_cc_vol:
        self.log("update volume from {} to {}".format(sensor_value, new_state))
        self.call_service("media_player/volume_set", entity_id = self.media_player, volume_level = set_cc_vol)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):

    slider_value = self.get_state(self.slider)
    set_slider_vol = float(new_state) * 10

    if slider_value != set_slider_vol:
      self.log("update slider from {} to {}".format(slider_value, new_state))
      self.call_service("input_slider/select_value", entity_id = self.slider, value = set_slider_vol)

  def mute_on(self, entity, attribute, old_state, new_state, kwargs):

    self.call_service("media_player/volume_mute", entity_id = self.media_player, is_volume_muted = "true")

  def mute_off(self, entity, attribute, old_state, new_state, kwargs):

    self.call_service("media_player/volume_mute", entity_id = self.media_player, is_volume_muted = "false")

