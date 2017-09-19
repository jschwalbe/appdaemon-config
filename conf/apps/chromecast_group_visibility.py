import appdaemon.appapi as appapi

# Make chromecast group visible when playing
#
# Args:
#   group: name of chromecast group to hide when not playing
#   chromecasts: list of chromecasts to hide when group is shown
#

class ChromecastGroupVisibility(appapi.AppDaemon):

  def initialize(self):
    
    self.group = self.args['group']
    self.chromecasts = self.args['chromecasts'].split(",")

    self.listen_state(self.hide_chromecasts, entity = self.group, new = "playing")
    self.listen_state(self.show_chromecasts, entity = self.group, new = "off")

  def hide_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      
    self.log("hiding chromecasts")
      
    for chromecast in self.chromecasts:
      self.call_service("group/set_visibility", entity_id = self.chromecasts[chromecast], visible = "false")

  def show_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      
    self.log("showing chromecasts")
      
    for chromecast in self.chromecasts:
      self.call_service("group/set_visibility", entity_id = self.chromecasts[chromecast], visible = "true")