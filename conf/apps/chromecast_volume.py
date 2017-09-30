import appdaemon.appapi as appapi
from datetime import timedelta

# Chromecast volume card
# 
# Updates the volume of a chromecast following a change of value from an input_slider. 
# Conversely, it will update the slider value should the volume of the chromecast be 
# updated from another input source (Google Home app, for example)
# Requires the following components to be available in Homeassistant:
# - input_slider.chromecast_volume_<name> : values 0-1, 0.01 increments
# - sensor.chromecast_volume_<name> : see template sensor for chromecast volume
# - media_player.<name> : chromecast device
# 
# Args:
#   name : name of Chromecast as it appears in Homeassitant
#

class ChromecastVolume(appapi.AppDaemon):

  def initialize(self):

    self.cc_name = self.args["cc_name"]
    self.slider = "input_slider.chromecast_volume_{}".format(self.cc_name)
    self.sensor = "sensor.chromecast_volume_{}".format(self.cc_name)    
    self.media_player = "media_player.{}".format(self.cc_name)

    self.last_called = self.datetime()
    self.laststate = 0

    self.prevent_slider_loop = False
    self.prevent_vol_loop = False
    
    self.listen_state(self.update_slider, entity = self.sensor)
    self.listen_state(self.update_volume, entity = self.slider)
    self.listen_state(self.mute_on, entity = "input_boolean.chromecast_mute", new = "on")
    self.listen_state(self.mute_off, entity = "input_boolean.chromecast_mute", new = "off")

  def update_volume(self, entity, attribute, old_state, new_state, kwargs):
  
    if self.prevent_vol_loop == True:
      self.prevent_vol_loop = False
      return

    self.prevent_slider_loop = True

    set_cc_vol = round(float(new_state), 2)
    self.call_service("media_player/volume_set", entity_id = self.media_player, volume_level = set_cc_vol)

  def update_slider(self, entity, attribute, old_state, new_state, kwargs):
  
    if (self.datetime() - self.last_called) < timedelta(seconds=0.5):
      self.cancel_timer(self.handle)
    self.handle = self.run_in(self.update_slider_now,1,new_state = new_state)
    self.last_called = self.datetime()
    self.laststate = new_state

  def update_slider_now(self,kwargs):
    
    if self.prevent_slider_loop == True:
      self.prevent_slider_loop = False
      return

    self.prevent_vol_loop = True
    
    set_slider_vol = round(float(kwargs["new_state"]), 2)
    self.call_service("input_slider/select_value", entity_id = self.slider, value = set_slider_vol)

  def mute_on(self, entity, attribute, old_state, new_state, kwargs):

    self.call_service("media_player/volume_mute", entity_id = self.media_player, is_volume_muted = "true")

  def mute_off(self, entity, attribute, old_state, new_state, kwargs):

    self.call_service("media_player/volume_mute", entity_id = self.media_player, is_volume_muted = "false")
