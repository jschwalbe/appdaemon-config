import appdaemon.appapi as appapi
import datetime

# Apps for triggering morning light scenes
#
# Args:
#   

class LivingroomOn(appapi.AppDaemon):

  def initialize(self):
    
    on_time = datetime.time(6, 30, 0)
    self.log(on_time)
    self.cloud_offset = self.get_app("cloud_offset").cloud_offset
    self.log(self.cloud_offset)

    self.run_once(self.morning_on, on_time)
    self.handle = self.run_at_sunrise(self.morning_off, offset = self.cloud_offset * 60)
    

  def morning_on(self, kwargs):

    self.log(self.datetime())
    self.log("morning lights on")
    self.call_service("light/hue_activate_scene", group_name = "Living room", scene_name = "Morning")

  def morning_off(self, kwargs):

    self.log(self.datetime())
    self.log("morning lights off")
    self.call_service("light/turn_off", entity_id = "light.living_room")
