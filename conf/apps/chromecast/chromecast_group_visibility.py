import appdaemon.appapi as appapi

# Hide Chromecast groups when not playing
#
# Takes a Chromecast group name and the names of constituent players
# Hides group intially, but will flip visibility of group and players if casting to the group
# This prevents duplicate Chromecast players from appearing on the HA interface
#
# Args:
#   group : name of chromecast group to hide when not playing
#   chromecasts : list of chromecasts to hide when group is shown
#

class SwitchGroupVisibility(appapi.AppDaemon):

  def initialize(self):

    self.group = self.args['group']
    self.chromecasts = self.args['chromecasts'].split(",")
    self.cc_groups = {}

    self.call_service("group/set_visibility", entity_id = "group.cc_{}".format(self.group), visible = "false")

    for chromecast in self.chromecasts:
        self.cc_groups[chromecast] = "group.cc_{}".format(chromecast)

    self.handle_hide = self.listen_state(self.hide_chromecasts, entity = "media_player.{}".format(self.group), new = "playing")
    self.handle_show = self.listen_state(self.show_chromecasts, entity = "media_player.{}".format(self.group), new = "off")

  def hide_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      
    self.call_service("group/set_visibility", entity_id = "group.cc_{}".format(self.group), visible = "true")
    
    for chromecast in self.chromecasts:
      self.call_service("group/set_visibility", entity_id = self.cc_groups[chromecast], visible = "false")  

  def show_chromecasts(self, entity, attribute, old_state, new_state, kwargs):
      
    self.call_service("group/set_visibility", entity_id = "group.cc_{}".format(self.group), visible = "false")

    for chromecast in self.chromecasts:
      self.call_service("group/set_visibility", entity_id = self.cc_groups[chromecast], visible = "true")