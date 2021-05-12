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

client.moveToPositionAsync(0,-90, -1, 10).join()

client.moveToPositionAsync(-20,-90,-1, 10).join()
client.moveToPositionAsync(-20, -9, -1,10).join()

client.moveToPositionAsync(-40, -9, -1, 10).join()
client.moveToPositionAsync(-40, -80, -1,10).join()

client.moveToPositionAsync(-54, -80, -1, 10).join()
client.moveToPositionAsync(-54, -9, -1, 10).join()

client.moveToPositionAsync(-74, -9, -1, 10).join()
client.moveToPositionAsync(-74, -80, -1, 10).join()

client.moveToPositionAsync(-88, -80, -1, 10).join()
client.moveToPositionAsync(-88, -9, -1, 10).join()

client.moveToPositionAsync(-98, -9, -1, 10).join()
client.moveToPositionAsync(-98, -80, -1, 10).join()

#stop and return the simulator to initial state
client.hoverAsync().join()
client.armDisarm(False)
client.reset()
client.enableApiControl(False)
