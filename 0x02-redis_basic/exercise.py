#!/usr/bin/env python3
"""
Redis basic.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any, Optional
from functool import wraps


def count_calls(method: Callable) -> Callable:
    """
    Creates and returns function that increments the count
    for that key every time the method is called and returns
    the value returned by the original method
    """
    @wraps(method)
    def incr_wrapper(self,*args, **kwargs):
        counter_name = method.__qualname__
        self._redis.incr(counter_name)
        return method(self,*args, **kwargs)
    return incr_wrapper


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function.
    """
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache:
  """Basic cache in redis."""

  def __init__(self):
    """
    Store an instance of the Redis client as a private variable named _redis.

    (using redis.Redis()) and flush the instance using flushdb.
    """
    self._redis = redis.Redis()
    self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
    """Store the input data in Redis using the random key and return the key."""
    id: str = str(uuid4())
    if not isinstance(data, (str, bytes, int, float)):
      raise TypeError("unsuported datat type")
    self._redis.set(id, data)
    return id

  def get(self, key: str, fn: Optional[Callable]) -> any:
      """Get stored value with a key

      convert the data to a desired format if 'fn' is provided
      """
      val = self._redis.get(key)
      if val is None or fn is None:
          return val
      return fn(val)

  def get_str(self, key: str) ->str:
      """Get stored string converted as string format."""
      return self.get(key, str)

  def get_int(self, key: int) ->int:
      """Get stored int converted as int format."""
      return self.get(key, int)
