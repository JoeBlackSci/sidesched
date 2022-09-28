from typing import List

from sidesched.classes import Side, Event

names: List[str] = ["bbb", "aaa"]
sizes: List[int] = [1, 2]
spots: List[str] = ["BBB", "AAA"]

side1: Side = Side(names[0], size=sizes[0])
side2: Side = Side(names[1], size=sizes[1])

event: Event = Event(
    "event_name",
    1,
    spots=spots,
    sides=[side1, side2]
)

class TestSide:
    def test_name(self) -> None:
        assert side1.name == "bbb"
    
    def test_size_1(self) -> None:
        assert side1.size == 1
    
    def test_size_2(self) -> None:
        assert side2.size == 2
        
    def test_sorting(self) -> None: 
        assert sorted([side1, side2]) == [side2, side1]

class TestEvent:
    
    def test_side_order(self) -> None:
        assert event.sides[0].name < event.sides[1].name  # type: ignore
        
    def test_add_spot(self) -> None:
        event.add_spot("BBA") 
        assert event.spots == ["AAA", "BBA", "BBB"]
    
    def test_add_side(self) -> None:  
        event.add_side(Side("bba"))
        side_names = [side.name for side in event.sides]
        assert side_names == ["aaa", "bba", "bbb"]
        
        
