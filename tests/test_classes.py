from typing import List

from sidesched.classes import Side, Event

names: List[str] = ["bb", "aa", "ab"]
sizes: List[int] = [1, 2, 1]
spots: List[str] = ["BB", "AA", "AB"]
sides: List[Side] = [Side(name, size) for name, size in zip(names, sizes)]

event: Event = Event(
    "event_name",
    spots=spots,
    sides=sides,
    slots=3
)

class TestSide:
    def test_name(self) -> None:
        assert sides[0].name == "bb"
    
    def test_size_1(self) -> None:
        assert sides[0].size == 1
    
    def test_size_2(self) -> None:
        assert sides[1].size == 2
        
    def test_sorting(self) -> None: 
        assert sorted(sides) == [sides[1], sides,[2], sides[0]]

class TestEvent:
    
    def test_side_order(self) -> None:
        assert event.sides == [sides[1], sides,[2], sides[0]]
        
        
        
