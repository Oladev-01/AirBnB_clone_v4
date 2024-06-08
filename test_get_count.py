#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("Amenity objects: {}".format(storage.count(Amenity)))
print("User objects: {}".format(storage.count(User)))


first_state_id = list(storage.all(State).values())[0].id
print(first_state_id)
print("First state: {}".format(storage.get(State, first_state_id)))
