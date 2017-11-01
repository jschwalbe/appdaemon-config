import appdaemon.appapi as appapi
import datetime

# Apps for triggering evening light scenes
#
# Args:
#   

class LivingroomOn(appapi.AppDaemon):

  def initialize(self):

    off_time = datetime.time(23, 59, 0)
    self.cloud_offset = self.get_app("cloud_offset").cloud_offset

    self.handle_on = self.run_at_sunset(self.evening_on, offset = self.cloud_offset * -60)
    self.handle_off = self.run_daily(self.evening_off, off_time)

  def evening_on(self, kwargs):

    self.log("Evening on triggered")
    self.call_service("light/hue_activate_scene", group_name = "Living room", scene_name = "Home")

  def evening_off(self, kwargs):

    self.log("Evening off triggered")
    self.call_service("light/turn_off", entity_id = "light.living_room")
