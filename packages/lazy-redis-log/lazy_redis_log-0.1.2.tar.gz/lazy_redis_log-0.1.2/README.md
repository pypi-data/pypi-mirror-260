# Lazy Redis Log
Like `print(...)`, but also writes to Redis Streams.

# Installation
```
pip install lazy-redis-log
```

# How to Use

```py
from redis import Redis
from lazy_redis_log import LazyRedisLog

LOG = LazyRedisLog()

LOG.redis = Redis(...)
LOG.key = 'logs:example'
LOG.field = 'example'
LOG.do_console = True # Print on the console.
LOG.do_redis = True # Write to Redis.

LOG('Hello World!')

LOG(
    'Hello World!',
    redis=False, # Don't write to Redis.
)

LOG(
    'Hello World!',
    console=False, # Don't print on the console.
)

LOG(
    'Hello World!',
    field='example2'
    # Write on this field on the stream.
    # This will always write to Redis,
    # even if `do_redis` is `False`.
)

LOG(
    'Hello',
    'World!',
    LazyRedisLog,
    sep=', ',
    end=' END ',
    # Functions similarly to `print(...)`.
)
```
