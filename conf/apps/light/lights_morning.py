import appdaemon.appapi as appapi
import datetime

# Apps for triggering morning light scenes
#
# Args:
#   

class LivingroomOn(appapi.AppDaemon):

  def initialize(self):
    
    on_time = datetime.time(6, 30, 0)
    self.cloud_offset = self.get_app("cloud_offset").cloud_offset * 60

    self.handle_on = self.run_daily(self.morning_on, on_time)
    self.handle_off = self.run_at_sunrise(self.morning_off, offset = self.cloud_offset)
    
  def morning_on(self, kwargs):

    self.log("Living room morning lights on")
    self.call_service("light/hue_activate_scene", group_name = "Living room", scene_name = "Morning")

  def morning_off(self, kwargs):

    self.log("Living room morning lights off")
    self.call_service("light/turn_off", entity_id = "light.living_room")
