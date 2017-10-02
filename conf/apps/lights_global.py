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

class LightsGlobal(appapi.AppDaemon):

  def initialize(self):
    
    self.cloud_offset = 40    
    self.listen_state(self.update_cloud_offset, entity = "sensor.weather_cloud_coverage", scale = 30, buffer = 10)

  def update_cloud_offset(self, entity, attribute, old_state, new_state, kwargs):
    # calculates cloud cover offset in minutes
    # buffer: number of minutes to add regardless of cloud cover
    # scale: length of time to multiply cloud percentage by

    cloud_perc = float(new_state) / 100
    calc_offset = int((cloud_perc * kwargs["scale"]) + kwargs["buffer"])

    self.cloud_offset = calc_offset