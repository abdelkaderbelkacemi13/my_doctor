#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("MY_APPOINTMENT_STORAGE_TYPE")
print(storage_t)
if storage_t == "db":
    from app.models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
    print("db initialized")
#if storage:
 #   storage.reload()
else:
    print("Storage is not initialized")
    print(storage_t)

