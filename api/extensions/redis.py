import redis
from config.redis_config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_DECODE_RESPONSES
security_redis  = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=REDIS_DECODE_RESPONSES)