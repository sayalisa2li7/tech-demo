import redis

def test_redis_connection():
    try:
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        client.ping()
        print("Connected to Redis")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

test_redis_connection()
