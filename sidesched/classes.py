from dataclasses import dataclass, field
from typing import Optional, List, Dict
from bisect import insort
import pandas as pd


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
    spots: Optional[List[str]] = field(default_factory=list)
    sides: Optional[List[Side]] = field(default_factory=list)
    freq_side: Optional[pd.DataFrame] = field(default_factory=pd.DataFrame)
    freq_spot: Optional[pd.DataFrame] = field(default_factory=pd.DataFrame)
    shedule: Optional[List[Dict[str, List[Side]]]] = field(default_factory=list)


    def __init__(
        self, 
        name: str, 
        slots: int = 0,
        spots: Optional[List[str]] = None, 
        sides: Optional[List[Side]] = None
    ) -> None:

        self.name = name
        self.slots = slots

        if spots == None:
            self.spots = []
        else:
            self.spots = sorted(list(spots))

        if sides == None:
            self.sides = []
        else:
            self.sides = sorted(list(sides))

        self.freq_side = None
        self.freq_spot = None
        self.shedule = None
    

    def add_spot(self, spot: str) -> None:
        insort(self.spots, spot)  # type: ignore
  

    def add_side(self, side: Side) -> None:
        insort(self.sides, side)  # type: ignore

