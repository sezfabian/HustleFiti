#!/usr/bin/env python3
from models import storage

all_objects = storage.all()
print(f"Number of objects: {len(all_objects)}")
for key, obj in all_objects.items():
    print(f"Object: {key}, Type: {type(obj)}, {obj}")


