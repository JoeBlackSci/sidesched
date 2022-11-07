from pprint import pprint
from typing import List, Tuple, cast
import logging

import pandas as pd

from sidesched import Event, Scheduler, Side

logging.basicConfig(level=logging.DEBUG, filename="log.txt", filemode="w+", )

names = ["earlsdon", "saddleworth", "cinewood", "SB&MRTD", "jockey", "shakespere"]
spots = ["royal oak", "broomfeild", "chestnut"]
sizes = [1, 1, 1, 2, 1, 1]
sides = [Side(name, size) for name, size in zip(names, sizes)]

event = Event("bromyard", spots, sides, 5)
schedule = Scheduler(event)
schedule.side_priority = "side"
schedule.side_decider = min
schedule.feature_priority = ["load", "side", "spot"]

schedule.schedule()

print(event.freq_side)
print("\n")
print(event.freq_spot)
