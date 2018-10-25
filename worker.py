import config as cf
import redis
from rq import Worker, Queue, Connection

while True:
	try:
		redis_url = cf.REDIS_URL
		conn = redis.from_url(redis_url)
		break
	except:
		pass

listen = [cf.REDIS_QUEUE_NAME]

if __name__ == '__main__':
	with Connection(conn):
		worker = Worker(list(map(Queue, listen)))
		worker.work()