import appdaemon.appapi as appapi
import datetime

# Trigger morning sunrise in bedroom based on phone alarm times.
# Listens to MQTT sensor that registers alarm time when set, then calculates
# a time to start sunrise light transition before alarm time and calls transition
# function for that time. Finally, publishes a message to clear the sensor so if no 
# alarm is set, no lighs come on the following day.
#
# Requires the following components to be available in Homeassistant:
#   - sensor.mqtt_phone_alarm_<name>
#   - light.<name>
# 
# Args:
#   wakee : name of person

class AlarmRise(appapi.AppDaemon):

  def initialize(self):

    # create and log the required variables from the kwargs.
    # mqtt, sensor and light for each wakee
    self.wakee = self.args["wakee"]    
    self.mqtt_topic = "phone/alarm/{}".format(self.wakee)
    self.sensor = "sensor.mqtt_phone_alarm_{}".format(self.wakee)
    self.log("Sensor registered: {}".format(self.sensor))
    self.light_name = "light.{}".format(self.wakee)
    self.log("Light registered: {}".format(self.light_name))

    # tasker submits the alarm time at 3:59 via mqtt which is detected by sensor
    # appdaemon then runs sunrise_lights if mqtt sensor has a valid time
    self.handle = self.run_daily(self.sunrise_lights, datetime.time(4, 0, 0))

  def sunrise_lights(self, kwargs):

    self.sensor_value = self.get_state(self.sensor)

    if self.sensor_value != "":
      self.sensor_time = datetime.datetime.strptime(self.sensor_value, "%H:%M")    
      self.log("Alarm registered: {} - {}".format(self.wakee, self.sensor_time.time()))

      self.light_time_1 = self.sensor_time - datetime.timedelta(minutes = 20)
      self.log("Sunrise 1 transition will start at {}".format(self.light_time_1.time()))
      
      self.light_time_2 = self.sensor_time - datetime.timedelta(minutes = 10)
      self.log("Sunrise 2 transition will start at {}".format(self.light_time_2.time()))
      
      self.run_once(self.transition_1, start = self.light_time_1.time())
      self.run_once(self.transition_2, start = self.light_time_2.time())

      self.call_service("mqtt/publish", topic = self.mqtt_topic, payload = "")

  def transition_1(self, kwargs):

    self.log("Transition 1 started")
    self.call_service("light/turn_on", entity_id = self.light_name, kelvin = "2200", brightness_pct = "50", transition = "599")
    
  def transition_2(self, kwargs):

    self.log("Transition 2 started")
    self.call_service("light/turn_on", entity_id = self.light_name, kelvin = "5500", brightness_pct = "100", transition = "600")