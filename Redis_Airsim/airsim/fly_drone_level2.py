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
client.moveToPositionAsync(0,-102, -2, 8).join()

client.moveToPositionAsync(-28,-92,-2, 8).join()
client.moveToPositionAsync(-28, -5, -2,8).join()

client.moveToPositionAsync(-39, -5, -2, 8).join()
client.moveToPositionAsync(-39, -90, -2,8).join()

client.moveToPositionAsync(-59, -90, -2, 8).join()
client.moveToPositionAsync(-59, -5, -2, 8).join()

client.moveToPositionAsync(-78, -5, -2, 8).join()
client.moveToPositionAsync(-78, -90, -2, 8).join()

client.moveToPositionAsync(-88, -90, -2, 8).join()
client.moveToPositionAsync(-88, -5, -2, 8).join()

client.moveToPositionAsync(-98, -5, -2, 8).join()
client.moveToPositionAsync(-98, -90, -2, 8).join()

#stop and return the simulator to initial state
client.hoverAsync().join()
client.armDisarm(False)
client.reset()
client.enableApiControl(False)
