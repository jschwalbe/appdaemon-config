import appdaemon.appapi as appapi
import datetime

# Trigger morning sunrise in bedroom based on phone alarm times.
# Listens to MQTT sensor that registers alarm time when set, then calculates
# a time to start sunrise light transition before alarm time and calls transition
# function for that time.
# Requires the following components to be available in Homeassistant:
#   - sensor.mqtt_phone_alarm_<name>
#   - light.<name>
# 
# Args:
#   wakee : name of person

class AlarmRise(appapi.AppDaemon):

  def initialize(self):

    self.wakee = self.args["wakee"]

    self.sensor = "sensor.mqtt_phone_alarm_{}".format(self.wakee)
    self.log("Sensor registered: {}".format(self.sensor))
    
    self.light_name = "light.{}".format(self.wakee)
    self.log("Light registered: {}".format(self.light_name))

    # self.handle =  self.listen_state(self.sunrise_lights, entity = self.sensor)

#   def sunrise_lights(self, entity, attribute, old_state, new_state, kwargs):

    new_state = "8:29"

    self.sensor_time = datetime.datetime.strptime(new_state, "%H:%M")    
    self.log("Alarm registered: {} - {}".format(self.wakee, self.sensor_time.time()))

    self.light_time_1 = self.sensor_time - datetime.timedelta(minutes = 25)
    self.log("Sunrise 1 transition will start at {}".format(self.light_time_1.time()))
    
    self.light_time_2 = self.sensor_time - datetime.timedelta(minutes = 15)
    self.log("Sunrise 2 transition will start at {}".format(self.light_time_2.time()))
    
    self.run_once(self.transition_1, start = self.light_time_1.time())
    self.run_once(self.transition_2, start = self.light_time_2.time())

  def transition_1(self, kwargs):

    self.log("Transition 1 started")
    # self.call_service("light/turn_on", entity_id = self.light_name, kelvin = "2200", brightness_pct = "60", transition = "600")
    
  def transition_2(self, kwargs):

    self.log("Transition 2 started")
    # self.call_service("light/turn_on", entity_id = self.light_name, kelvin = "5500", brightness_pct = "100", transition = "900")