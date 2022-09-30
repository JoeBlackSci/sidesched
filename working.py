from pprint import pprint
from typing import List, Tuple, cast
import logging

import pandas as pd

from sidesched import Event, Scheduler, Side

logging.basicConfig(level=logging.DEBUG)

names = ["earlsdon", "saddleworth", "cinewood", "SB&MRTD", "jockey", "shakespere"]
spots = ["royal oak", "broomfeild", "chestnut"]
sizes = [1, 1, 1, 2, 1, 1]
sides = [Side(name, size) for name, size in zip(names, sizes)]

event = Event("bromyard", spots, sides, 3)

schedule = Scheduler(event)
schedule.side_priority = "spot"

out = schedule._prioritise_sides()
pprint(out)
out = schedule.side_metrics()
pprint(out)
print()

schedule._schedule_next()
out = schedule._prioritise_sides()
pprint(out)
out = schedule.side_metrics()
pprint(out)
print()

schedule._schedule_next()
out = schedule._prioritise_sides()
pprint(out)
out = schedule.side_metrics()
pprint(out)
print()

schedule._schedule_next()
out = schedule._prioritise_sides()
pprint(out)
out = schedule.side_metrics()
pprint(out)
print()


print(event.freq_side)
print(event.freq_spot)
