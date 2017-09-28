import appdaemon.appapi as appapi
from datetime import timedelta

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

    self.cc_name = self.args["cc_name"]
    self.slider = "input_slider.chromecast_volume_{}".format(self.cc_name)
    self.sensor = "sensor.chromecast_volume_{}".format(self.cc_name)    
    self.media_player = "media_player.{}".format(self.cc_name)
    
    self.prevent_slider_loop = False
    self.prevent_vol_loop = False
    
    self.last_called = self.datetime()
    self.last_state = 0

    self.listen_state(self.update_slider, entity = self.sensor)
    self.listen_state(self.update_volume, entity = self.slider)
    self.listen_state(self.mute_on, entity = "input_boolean.chromecast_mute", new = "on")
    self.listen_state(self.mute_off, entity = "input_boolean.chromecast_mute", new = "off")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):
    # change slider on Homeassitant
    # volume callback called
    # is vol loop prevent true? - yes: stop/false, no> 
    # set slider loop prevent to true
    # change volume
    # * slider callback called
  
    self.log("update volume")

    if self.prevent_vol_loop == True:
      self.log("prevent vol loop {}".format(self.prevent_vol_loop))
      self.prevent_vol_loop = False
      return

    self.prevent_slider_loop = True

    # sensor_value = round(float(self.get_state(self.sensor)), 2)
    sensor_value = 0.99
    set_cc_vol = round(float(new_state), 2)

    self.log("vol sensor_value {}".format(sensor_value))
    self.log("vol set_cc_vol {}".format(set_cc_vol))
    self.log(sensor_value == set_cc_vol)

    if sensor_value != set_cc_vol:
        self.log("update volume from {} to {}".format(sensor_value, set_cc_vol))
        # self.call_service("media_player/volume_set", entity_id = self.media_player, volume_level = set_cc_vol)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):
    # change volume on chromecast
    # slider callback called
    # is slider loop prevent true - yes: stop/false no>
    # set vol loop prevent to true
    # change slider
    # * volume callback called
  
    self.log("update slider called")
  
    if self.prevent_slider_loop == True:
      self.log("vol slider loop {}".format(self.prevent_slider_loop))
      self.prevent_slider_loop = False
      return

    self.prevent_vol_loop = True

    slider_value = round(float(self.get_state(self.slider)), 2)
    set_slider_vol = round(float(new_state), 2)

    self.log("sli slider_value {}".format(slider_value))
    self.log("sli set_slider_vol {}".format(set_slider_vol))
    self.log(slider_value == set_slider_vol)

    if slider_value != set_slider_vol:
      self.log("update slider from {} to {}".format(slider_value, set_slider_vol))
      self.set_state(self.slider, state = set_slider_vol)


  def mute_on(self, entity, attribute, old_state, new_state, kwargs):

    self.call_service("media_player/volume_mute", entity_id = self.media_player, is_volume_muted = "true")

  def mute_off(self, entity, attribute, old_state, new_state, kwargs):

    self.call_service("media_player/volume_mute", entity_id = self.media_player, is_volume_muted = "false")

