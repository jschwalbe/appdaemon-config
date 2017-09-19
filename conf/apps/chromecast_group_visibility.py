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
    self.cc_groups = {}

    for chromecast in self.chromecasts:
        self.cc_groups[chromecast] = "group.cc_{}".format(chromecast)

    self.listen_state(self.hide_chromecasts, entity = "media_player.{}".format(self.group), new = "playing")
    self.listen_state(self.show_chromecasts, entity = "media_player.{}".format(self.group), new = "off")

  def hide_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      
    for chromecast in self.chromecasts:
      self.call_service("group/set_visibility", entity_id = self.cc_groups[chromecast], visible = "false")  
      self.call_service("group/set_visibility", entity_id = "group.cc_{}".format(self.group), visible = "true")

  def show_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      
    for chromecast in self.chromecasts:
      self.call_service("group/set_visibility", entity_id = self.cc_groups[chromecast], visible = "true")
      self.call_service("group/set_visibility", entity_id = "group.cc_{}".format(self.group), visible = "false")