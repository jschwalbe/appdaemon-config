import appdaemon.appapi as appapi

# Morning and evening lights scenes
#
# Args:
#   
#   
#
# determine sunrise offset based on cloud cover
# turn on daylight scene at sunrise (minus offset) with transition
# turn off either at 9am or when presence is absent

class MorningOn(appapi.AppDaemon):

  def initialize(self):
    
    self.cloud_offset = self.get_app("lights_global").cloud_offset    
    self.handle = self.run_at_sunrise(self.sunrise, offset = self.cloud_offset * 60)

  def sunrise(self, kwargs):

    self.log("sunrise has happened")
    self.call_service("light/hue_activate_scene", group_name = "Living room", scene_name = "Morning")