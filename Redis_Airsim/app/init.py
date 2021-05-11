import redis
import argparse
from urllib.parse import urlparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Redis URL', type=str, default='redis://127.0.0.1:6379')
    args = parser.parse_args()
    
    url = urlparse(args.url)
    conn = redis.Redis(host=url.hostname, port=url.port)

    with open('gearconsumer.py', 'rb') as f:
        gear = f.read()
        res = conn.execute_command('RG.PYEXECUTE', gear)
        print(res)