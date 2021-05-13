import airsim
import pprint

class FlyDroneService:

    @staticmethod
    def initializeAirSimClient(client):
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

    @staticmethod
    def resetAirSimClient(client):
        client.hoverAsync().join()
        client.armDisarm(False)
        client.reset()
        client.enableApiControl(False)
    
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