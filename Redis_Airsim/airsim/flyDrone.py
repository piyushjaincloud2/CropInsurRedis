import airsim
import argparse
from flyDroneService import FlyDroneService

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--level', help='Game Level', type=int, default=1)
    args = parser.parse_args()
    
    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    FlyDroneService.initializeAirSimClient(client)

    gameLevel = args.level
    print(gameLevel)
    
    # simulate flying of drone in x,y and z coordinates
    if gameLevel == 3:
        print('Level 3')
        client.simEnableWeather(True)
        FlyDroneService.setFlyingCoordsForDroneAtThirdLevel(client)
    elif gameLevel == 2:
        print('Level 2')
        client.simEnableWeather(True)
        FlyDroneService.setFlyingCoordsForDroneAtSecondLevel(client)
    else:
        print('Level 1')
        client.simEnableWeather(True)
        client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 1)
        FlyDroneService.setFlyingCoordsForDroneAtFirstLevel(client)
        
    #stop and return the simulator to initial state
    FlyDroneService.resetAirSimClient(client)

