import setup_path 
import airsim
import numpy as np
import os
import tempfile
import pprint
import cv2

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

state = client.getMultirotorState()
s = pprint.pformat(state)
print("state: %s" % s)

imu_data = client.getImuData()
s = pprint.pformat(imu_data)
print("imu_data: %s" % s)

barometer_data = client.getBarometerData()
s = pprint.pformat(barometer_data)
print("barometer_data: %s" % s)

magnetometer_data = client.getMagnetometerData()
s = pprint.pformat(magnetometer_data)
print("magnetometer_data: %s" % s)

gps_data = client.getGpsData()
s = pprint.pformat(gps_data)
print("gps_data: %s" % s)

airsim.wait_key('Press any key to takeoff')
client.takeoffAsync().join()

state = client.getMultirotorState()
print("state: %s" % pprint.pformat(state))

airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
client.simEnableWeather(True)
client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 1)

# simulate flying of drone in x,y and z coordinates
client.moveToPositionAsync(0,-85, 0, 10).join()

client.moveToPositionAsync(-14,-85,0, 10).join()
client.moveToPositionAsync(-14, -9, 0, 10).join()

client.moveToPositionAsync(-30, -9, 0, 10).join()
client.moveToPositionAsync(-30, -78, 0, 10).join()

client.moveToPositionAsync(-48, -78, 0, 10).join()
client.moveToPositionAsync(-48, -9, 0, 10).join()

client.moveToPositionAsync(-65, -9, 0, 10).join()
client.moveToPositionAsync(-65, -78, 0, 10).join()

client.moveToPositionAsync(-80, -78, 0, 10).join()
client.moveToPositionAsync(-80, -9, 0, 10).join()

client.moveToPositionAsync(-98, -9, 0, 10).join()
client.moveToPositionAsync(-98, -78, 0, 10).join()

#stop and return the simulator to initial state
client.hoverAsync().join()
client.armDisarm(False)
client.reset()
client.enableApiControl(False)
