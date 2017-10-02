import appdaemon.appapi as appapi

# Apps for triggering evening light scenes
#
# Args:
#   

class LivingroomOn(appapi.AppDaemon):

  def initialize(self):

    self.cloud_offset = self.get_app("cloud_offset").cloud_offset
    self.handle = self.run_at_sunset(self.sunset, offset = self.cloud_offset * 60)

  def sunset(self, kwargs):

    self.log(self.datetime())
    self.log("sunset has happened")
    self.call_service("light/hue_activate_scene", group_name = "Living room", scene_name = "Home")