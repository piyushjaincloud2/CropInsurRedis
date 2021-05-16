import redis
import argparse
from urllib.parse import urlparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Redis URL', type=str, default='redis://127.0.0.1:6379')
    args = parser.parse_args()
    
    url = urlparse(args.url)
    conn = redis.Redis(host=url.hostname, port=url.port)

    # Load the AI model in the redis
    with open('models/model.pb', 'rb') as f:
        model = f.read()
        res = conn.execute_command('AI.MODELSET', 'customvisionmodel', 'TF', 'CPU', 'INPUTS', 'image_tensor', 'OUTPUTS', 'detected_boxes','detected_scores','detected_classes','BLOB', model)
        print(res)

    # Load the Gear to register with the inspectiondata stream
    with open('gearconsumer.py', 'rb') as f:
        gear = f.read()
        res = conn.execute_command('RG.PYEXECUTE', gear)
        print(res)