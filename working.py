from sidesched import Side, Event, Scheduler
from typing import cast, Tuple, List

names = ["earlsdon", "saddleworth", "cinewood", "SB&MRTD", "jockey", "shakespere"]
spots = ["royal oak", "broomfeild", "chestnut"]
sizes = [1, 1, 1, 2, 1, 1]
sides = [Side(name, size) for name, size in zip(names, sizes)]

event = Event("bromyard", spots, sides, 3)

schedule = Scheduler(event)

# print(schedule._prioritise_sides())

metrics = {"sides": [1,2,3,4], "spots": [5,6,7,8]}
print(
    [
        sides + spots 
        for sides, spots 
        in zip(metrics["sides"], metrics["spots"])
    ]
)