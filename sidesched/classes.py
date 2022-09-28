from dataclasses import dataclass, field
from typing import List, Dict
import pandas as pd
import numpy as np


@dataclass(frozen=True, order=True)
class Side:
    """Morris Side Class."""
    name: str
    size: int = 1


@dataclass
class Event:
    """Festival dance program."""
    name: str
    slots: int = 1
    spots: List[str] = field(default_factory=list)
    sides: List[Side] = field(default_factory=list)
    freq_side: pd.DataFrame = field(default_factory=pd.DataFrame)
    freq_spot: pd.DataFrame = field(default_factory=pd.DataFrame)
    shedule: List[Dict[str, List[Side]]] = field(default_factory=list)
    

    def __init__(
        self, 
        name: str, 
        spots: List[str], 
        sides: List[Side],
        slots: int
    ) -> None:

        self.name = name
        self.slots = slots
        self.spots = sorted(list(spots))
        self.sides = sorted(list(sides))
        
        self.freq_side = pd.DataFrame(
            np.zeros([len(self.sides)] * 2, dtype="int"),
            index=self.sides,
            columns=self.sides
        )
        self.freq_spot = pd.DataFrame(
            np.zeros((len(self.sides), len(self.spots)), dtype="int"),
            index=self.sides,
            columns=self.spots
        )

        self.timetable = [
            {spot: [] for spot in self.spots} 
            for _ in range(slots)
        ]
    
    def get_timeslot(self, time: int) -> Dict[str, List]:
        return self.timetable[time]
