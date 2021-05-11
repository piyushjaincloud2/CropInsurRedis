import redis

conn = redis.Redis(host='localhost', port=6379)
res = conn.execute_command('xread','Block', 10000000,'STREAMS', 'airsim:0', '$')

print(res)