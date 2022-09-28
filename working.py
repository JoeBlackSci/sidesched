from sidesched import Side, Event, Scheduler
from typing import cast, Tuple, List
import pandas as pd

names = ["earlsdon", "saddleworth", "cinewood", "SB&MRTD", "jockey", "shakespere"]
spots = ["royal oak", "broomfeild", "chestnut"]
sizes = [1, 1, 1, 2, 1, 1]
sides = [Side(name, size) for name, size in zip(names, sizes)]

event = Event("bromyard", spots, sides, 3)

schedule = Scheduler(event)
timeslot = schedule._fetch_timeslot()
out = schedule._schedule_next()
print(out)