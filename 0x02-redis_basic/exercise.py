#!/usr/bin/env python3
"""
Redis basic.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Any, Optional

class Cache:
  """Basic cache in redis."""

  def __init__(self):
    """
    Store an instance of the Redis client as a private variable named _redis.

    (using redis.Redis()) and flush the instance using flushdb.
    """
    self._redis = redis.Redis()
    self._redis.flushdb()

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
