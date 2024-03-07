import redis


class Redis:
    def __init__(self, host: str, port: int = 6379, password: str = None, db: int = 0, prefix: str = None, decode_responses: bool = True):
        self.redis_client = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=decode_responses,
        )
        self.prefix = prefix

    def prefixed(self, key: str):
        return f"{self.prefix}:{key}" if self.prefix else key

    def get(self, key: str):
        return self.redis_client.get(self.prefixed(key))

    def set(self, key: str, value: str, ex=None, px=None):
        self.redis_client.set(self.prefixed(key), value, ex=ex, px=px)
