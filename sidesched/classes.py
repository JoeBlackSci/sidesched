from dataclasses import dataclass, field
from typing import List, Dict
import pandas as pd
import numpy as np
import logging as log


@dataclass(frozen=True, order=True)
class Side:
    """Side Class, represents agents."""
    name: str
    size: int = 1
    
    def __repr__(self) -> str:
        return  self.name


@dataclass
class Event:
    """Event consisting of sides, spots and timeslots."""
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
    
    def _update_freq_side(self) -> None:
        log.info("Updating side frequency")
        _freq_side: pd.DataFrame = pd.DataFrame(
            np.zeros([len(self.sides)] * 2, dtype="int"),
            index=self.sides,
            columns=self.sides
        )
        
        all_groups = [group for slot in self.timetable for group in slot.values()]
        
        for side in self.sides:
            for grouping in all_groups:
                for c_side in grouping:
                    if c_side in grouping and side in grouping:
                        _freq_side.loc[side, c_side] += 1  # type: ignore [Custom index Side]
                    
        self.freq_side = _freq_side
            
    
    def _update_freq_spot(self) -> None:
        log.info("Updating spot frequency")
        _freq_spot: pd.DataFrame = pd.DataFrame(
            np.zeros((len(self.sides), len(self.spots)), dtype="int"),
            index=self.sides,
            columns=self.spots
        )
        
        for side in self.sides:
            for timeslot in self.timetable:
                for spot, sides in timeslot.items():
                    if side in sides:
                        _freq_spot.loc[side, spot] += 1  # type: ignore [Custom index Side]
        
        self.freq_spot = _freq_spot
        
    
    def update_freqs(self) -> None:
        """Update frequency metrics."""
        self._update_freq_side()
        self._update_freq_spot()
