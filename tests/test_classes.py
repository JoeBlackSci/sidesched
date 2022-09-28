from typing import List

from sidesched.classes import Side, Event

names: List[str] = ["bb", "aa", "ab"]
sizes: List[int] = [1, 2, 1]
spots: List[str] = ["BB", "AA"]
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
        
    def test_side_sorting(self) -> None: 
        assert sorted(sides) == [sides[1], sides[2], sides[0]]

class TestEvent:
    
    def test_side_order(self) -> None:
        assert event.sides == [sides[1], sides[2], sides[0]]
    
    def test_freq_spot(self) -> None:
        assert event.freq_spot.shape == (3,2)
        assert event.freq_spot.index.to_list() == event.sides
        assert event.freq_spot.columns.to_list() == event.spots
        
    def test_freq_side(self) -> None:
        assert event.freq_side.shape == (3,3)
        assert event.freq_side.index.to_list() == event.sides
        assert event.freq_side.columns.to_list() == event.sides
    
    def test_timetable(self) -> None:
        assert len(event.timetable) == len(range(event.slots))
        assert all(
            len(event.timetable[i]) == len(event.spots)
            for i in range(event.slots)
        )
    