import os
import numpy as np
import cv2
import airsim

class CaptureImageService:

    # set the camera pose of the drone while flying
    @staticmethod
    def setCameraPose(client):
        camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(-1.5708, 0, 0))
        client.simSetCameraPose(1, camera_pose)

    # add real time images captured by drone to the redis stream
    @staticmethod
    def addToStream(conn,img_rgb,iteration,imagename,maxImages):
        _, data = cv2.imencode('.jpg', img_rgb)
        storedimg = data.tobytes()
        iteration.append(['imagename',imagename])
        iteration.append(['image',storedimg])
        iteration.append(['isDone','0'])
        conn.execute_command('xadd', 'inspectiondata',  'MAXLEN', '~', str(maxImages), '*', *sum(iteration, []))
    
    # get the images of the land taken by drone
    @staticmethod
    def getRealTimeImage(client,count):
        temp_dir = os.path.join(os.getcwd(), "airsim_drone")
        filepath = os.path.join(temp_dir, str(count))
        simImages = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])
        simImage = simImages[0]
        img1d = np.fromstring(simImage.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(simImage.height, simImage.width, 3)
        return img_rgb