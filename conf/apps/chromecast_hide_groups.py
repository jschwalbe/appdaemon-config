import appdaemon.appapi as appapi

#
# Make chromecast group visible when playing
#
# Args:
#
#

class ChromecastHide(appapi.AppDaemon):

  def initialize(self):
      self.listen_state(self.hide_chromecasts, entity = "media_player.downstairs", new = "playing")

  def hide_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      