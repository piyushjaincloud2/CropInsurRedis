import airsim
import pprint
import time

class FlyDroneService:

    # initializes the airsim client and waits for the api control to be enabled, which is done on receiving the signal from the front end app when inspection is started
    @staticmethod
    def initializeAirSimClient(client):

        while not client.isApiControlEnabled():
            print("Client is waiting to take off")
            time.sleep(1)

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

        client.takeoffAsync().join()

        state = client.getMultirotorState()
        print("state: %s" % pprint.pformat(state))
        
    # reset the drone to the initial state
    @staticmethod
    def resetAirSimClient(client):
        client.hoverAsync().join()
        client.armDisarm(False)
        client.reset()
        client.enableApiControl(False)
    
    # set the flying coordinates for the drone at Level 1
    @staticmethod
    def setFlyingCoordsForDroneAtFirstLevel(client):
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

    # set the flying coordinates for the drone at Level 2
    @staticmethod
    def setFlyingCoordsForDroneAtSecondLevel(client):
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
    
    # set the flying coordinates for the drone at Level 3
    @staticmethod
    def setFlyingCoordsForDroneAtThirdLevel(client):
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