import airsim
import time
import os
import numpy as np
import cv2
import redis


def SetCameraPose(client):
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(-1.5708, 0, 0))
    client.simSetCameraPose(1, camera_pose)


def main():
    client = airsim.VehicleClient()
    client.confirmConnection()
    count=1

    SetCameraPose(client)
    conn = redis.Redis(host='localhost', port=6379)
    MAX_IMAGES = 50
    temp_dir = os.path.join(os.getcwd(), "airsim_drone")

    while(client.isApiControlEnabled()):
        
        filepath = os.path.join(temp_dir, str(count))
        imagename = str(count) + '.jpg'
        simImages = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])
        simImage = simImages[0]
        img1d = np.fromstring(simImage.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(simImage.height, simImage.width, 3)

        filepath = os.path.join(temp_dir, str(count))
        cv2.imwrite(os.path.normpath(filepath + '.jpg'), img_rgb)

        _, data = cv2.imencode('.jpg', img_rgb)
        storedimg = data.tobytes()
        msg = {
            'imagename': imagename,
            'image': storedimg
        }
        conn.execute_command('xadd', 'airsimrunner',  'MAXLEN', '~', str(MAX_IMAGES), '*','imagename', msg['imagename'], 'image', msg['image'])
        time.sleep(2)
        print(count)
        count += 1

if __name__ == '__main__':
    main()


