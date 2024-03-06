from redis import Redis


class LazyRedisLog:
    def __init__(self):
        self.key: str = "log"
        """
        The Redis key.
        """
        self.field: str = "default"
        """
        The field name in the Redis stream.
        """
        self.redis: Redis = None  # type: ignore
        self.do_console: bool = True
        """
        If the logger should print on the console by default.
        """
        self.do_redis: bool = True
        """
        If the logger should write to Redis by default.
        """

    def __call__(
        self,
        *values: object,
        sep: str = " ",
        end: str = "\n",
        field: str = None,  # type: ignore
        redis: bool = None,  # type: ignore
        console: bool = None,  # type: ignore
    ):
        """
        :param field: The field name in the Redis stream. If provided, it will always write to Redis, even if `do_redis` and `redis` is `False`.
        :param redis: If this should be written in Redis.
        :param console: If this should be printed on the console.
        """
        text = sep.join(str(value) for value in values)

        if redis == None:
            redis = self.do_redis

        if console == None:
            console = self.do_console

        if field != None:
            redis = True

        if field == None:
            field = self.field

        if redis and self.redis != None:
            self.redis.xadd(
                self.key,
                {
                    field: text,
                },
            )

        if console:
            print(
                *values,
                sep=sep,
                end=end,
            )

        return text
