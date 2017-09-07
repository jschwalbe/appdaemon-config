import appdaemon.appapi as appapi

#
# some kind of test
#
# Args:
#

class SliderLog(appapi.AppDaemon):

  def initialize(self):
      self.listen_state(self.slider_log, "input_slider.chromecast_volume_kitchen")
      self.listen_state(self.slider_log, "input_slider.chromecast_volume_stereo")

  def slider_log(self, entity, attribute, old_state, new_state, kwargs):
    #   new_volume = self.get_state("sensor.chromecast_volume_stereo", "new_state")
      self.log("name: {} new_state: {} old_state: {}".format(self.friendly_name(entity), new_state, old_state))
