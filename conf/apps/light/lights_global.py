import appdaemon.appapi as appapi

# Calculate time to offset light automations by depending on cloud cover
#
# Updates a global variable with the current time to offset instruction by in minutes
# Parameters for calcualation are set by scale and buffer.
# buffer adds x number of minutes to the calculation
# scale is the time period by which the cloud cover percentage is multiplied by
#
# Args: None
#  

class CloudOffset(appapi.AppDaemon):

  def initialize(self):
    
    self.cloud_offset = 40    
    self.listen_state(self.update_cloud_offset, entity = "sensor.weather_cloud_coverage", scale = 30, buffer = 10)

  def update_cloud_offset(self, entity, attribute, old_state, new_state, kwargs):

    cloud_perc = float(new_state) / 100
    calc_offset = int((cloud_perc * kwargs["scale"]) + kwargs["buffer"])

    self.cloud_offset = calc_offset