#!/usr/bin/env python3
"""Provide some stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


def nginx_stat():
    """
    Provide some stats about Nginx logs stored in MongoDB.

    First line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents 
    with the method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order 
    one line with the number of documents with:
    method=GET
    path=/status
    """
    client = MongoClient()
    nginx_logs = client.logs.nginx

    total_logs = nginx_logs.count_documents()
    print(f"{total_logs} logs")
    print("Methods:")
    for m in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_logs.count_documents({"method": m})
    print(f"\tmethod {m}: {count}")
    status_check = nginx_logs.count_documents({"path": "/status"})
    print(f"{status_check} status check")
    client.close()


if __name__ == "__main__":
    """Execute."""
    nginx_stat()
