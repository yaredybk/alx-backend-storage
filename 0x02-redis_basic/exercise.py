#!/usr/bin/env python3
"""
Redis basic.
"""
import redis
from uuid import uuid4

class Cache:
  """Basic cache in redis."""

  def __init__(self):
    """
    Store an instance of the Redis client as a private variable named _redis.

    (using redis.Redis()) and flush the instance using flushdb.
    """
    self._redis = redis.Redis()
    self._redis.flushdb()

  def store(self, data: str|bytes|int|float) -> str:
    """Store the input data in Redis using the random key and return the key."""
    id = uuid4()
    if not isinstance(data, (str, bytes, int, float)):
      raise TypeError("unsuported datat type")
    self._redis.store(id, data)
    return id