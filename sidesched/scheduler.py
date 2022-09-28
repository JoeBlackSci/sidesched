from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable

from sidesched.classes import Event, Side


class Scheduler:
    def __init__(self, event: Event) -> None:
        self.event = event
        self.cur_time: int = 0
        self.side_decider: Callable = min
        self.feature_priority: List[str] = ["load", "spot", "side"]
        self._feature_func_dict: Dict[str, Callable] = {
            "load": self._get_load,
            "spot": self._get_freq_spot,
            "side": self._get_freq_side
        }

    def _fetch_timeslot(self, time: Optional[int] = None) -> Dict[str, List]:
        if not time:
            time = self.cur_time
        return self.event.get_timeslot(time)

    def _get_load(self, timeslot: Dict[str, List], *_, **__) -> Dict[str, int]:
        return {spot: len(sides) for spot, sides in timeslot.items()}

    def _get_freq_spot(
        self, timeslot: Dict[str, List], side: Side, *_, **__
    ) -> Dict[str, int]:
        freq_spot = self.event.freq_spot
        return {
            spot: freq_spot.loc[side, spot]  # type: ignore [custom index Side]
            for spot in timeslot
        }

    def _get_freq_side(
        self, timeslot: Dict[str, List], side: Side, func: Optional[Callable] = None
    ) -> Dict[str, int]:
        
        if not func:
            func = self.side_decider
        freq_side = self.event.freq_side
        
        return {
            spot: sum(freq_side.loc[side, c_side] for c_side in sides)  # type: ignore [custom index Side]
            for spot, sides in timeslot.items()
        }

    # def _shedule_next(self) -> None:

    #     timeslot = {spot: [] for spot in self.spots}
    #     fill = {spot: 0 for spot in self.spots}
    #     unassigned = rand.sample(self.sides.copy(), k=len(self.sides))

    #     while unassigned:
    #         side = unassigned.pop()

    #         allocated = rand.choice([
    #             spot for i, spot in enumerate(timeslot)
    #             if fill[spot] == min(fill.values())
    #         ])

    #     # Extra 1 accounts for lonely teams when there's a low team count.
    #     fill[allocated] += side.size + 1
    #     timeslot[allocated].append(side)

    #     self.shedule = [timeslot]
    #     self._initalise_freqs()
    #     self._update_freqs(timeslot)
