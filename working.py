from pprint import pprint
from typing import List, Tuple, cast

import pandas as pd

from sidesched import Event, Scheduler, Side

names = ["earlsdon", "saddleworth", "cinewood", "SB&MRTD", "jockey", "shakespere"]
spots = ["royal oak", "broomfeild", "chestnut"]
sizes = [1, 1, 1, 2, 1, 1]
sides = [Side(name, size) for name, size in zip(names, sizes)]

event = Event("bromyard", spots, sides, 3)

schedule = Scheduler(event)
schedule.schedule()

print(event.freq_side)
print(event.freq_spot)



