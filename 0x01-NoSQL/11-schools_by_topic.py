#!/usr/bin/env python3
"""
Filter the list of school having a specific topic.


"""


def schools_by_topic(mongo_collection, topic):
  """
  Filter the list of school having a specific topic.
  topic (string) will be topic searched

  Returns:
    list: list of school having a specific topic:
  """
  mongo_collection.find({"topic":topic})