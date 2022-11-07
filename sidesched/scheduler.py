import logging as log
import pprint as pp
from dataclasses import dataclass, field
from random import choice, seed
from typing import (Any, Callable, Dict, List, Optional, Sequence, Set, Tuple)

import pandas as pd

from sidesched.classes import Event, Side

# TODO:
#   Mode: priotiy vs score 
#   Seed

class Scheduler:
    """_summary_
    """
    def __init__(self, event: Event) -> None:
        self.event: Event = event
        self.cur_time: int = 0
        self.side_decider: Callable = min  # Suggested: [min, sum]
        self.feature_priority: List[str] = ["side", "spot", "load"]
        self._feature_func_dict: Dict[str, Callable] = {
            "load": self._get_load,
            "spot": self._get_freq_spot,
            "side": self._get_freq_side,
        }
        self.side_priority: str = "both"  # Options ["both", "side", "spot"]
        
        log.info("Scheduler Initialised")

    def _fetch_timeslot(self, time: Optional[int] = None) -> Dict[str, List]:
        """Fetch timeslot for given time from Event.

        Parameters
        ----------
        time : Optional[int], optional
            Position of timeslot, by default None

        Returns
        -------
        Dict[str, List]
            The timetable of sides at given time in format: {spot: [sides]}.
        """
        
        if not time:
            time = self.cur_time
        log.info(f"fetching timeslot {time}")
        return self.event.get_timeslot(time)

    def _get_load(self, timeslot: Dict[str, List], *_, **__) -> Dict[str, int]:
        """Load (occupacy/fullness) of all spots for given timeslot.

        Parameters
        ----------
        timeslot : Dict[str, List]
            Timetable of sides at spots for a given time. {spot: [sides]}.

        Returns
        -------
        Dict[str, int]
            Number of sides currently at spots with. {spot: load}
        """

        # Extra addition of len accounts for lonely large teams
        return {
            spot: sum(side.size for side in sides) + len(sides)  # type: ignore [custom Side]
            for spot, sides in timeslot.items()
        }

    def _get_freq_spot(
        self, timeslot: Dict[str, List], side: Side, *_, **__
    ) -> Dict[str, int]:
        """Frequency of times side has been assigned each spot

        Parameters
        ----------
        timeslot : Dict[str, List]
            Timetable of sides at spots for a given time. {spot: [sides]}.
        side : Side
            Side to get frequency for.

        Returns
        -------
        Dict[str, int]
            Freqency side has previously been assigned spots. {spot: freq}
        """
        freq_spot = self.event.freq_spot
        return {
            spot: freq_spot.loc[side, spot]  # type: ignore [custom index Side]
            for spot in timeslot
        }

    def _get_freq_side(
        self, timeslot: Dict[str, List], side: Side, func: Optional[Callable] = None
    ) -> Dict[str, int]:
        """Frequency side has previously been co-assigned spots with present sides.

        Parameters
        ----------
        timeslot : Dict[str, List]
            Timetable of sides at spots for a given time. {spot: [sides]}.
        side : Side
            Side to get frequency for.
        func : Optional[Callable], optional
            Function used to determine optimal assignment for the side.
            Suggested: [min, sum]. minimal returned value is given priority.
            None defaults to Sheduler.side_decider, by default: min.

        Returns
        -------
        Dict[str, int]
            Frequency side has been co-assinged with sides at spots. {spot: freq}
        """

        if not func:
            func = self.side_decider
        freq_side = self.event.freq_side

        return {
            spot: func(freq_side.loc[side, c_side] for c_side in sides) if sides else 0  # type: ignore [custom index Side]
            for spot, sides in timeslot.items()
        }

    def side_metrics(self, from_min: bool = False) -> Dict[str, Any]:
        """Freqency sides have been assigned to spots and co-assigned with sides.

        Parameters
        ----------
        from_min : bool, optional
            Frequency is determined from zero rather than current global
            minimum, by default False

        Returns
        -------
        Dict[str, Any]
            Metrics of side frequency of assigned spot and co-assigned sides.
        """
        freq_spot = self.event.freq_spot
        min_spots = freq_spot.to_numpy().min() if from_min else 0
        spots_at = [
            sum(freq_spot.loc[side] > min_spots) for side in self.event.sides  # type: ignore [custom index Side]
        ]

        freq_side = self.event.freq_side
        min_sides = freq_side.to_numpy().min() if from_min else 0
        sides_with = [
            sum(freq_side.loc[side] > min_sides) for side in self.event.sides  # type: ignore [custom index Side]
        ]

        return {
            "sides": self.event.sides,
            "spots_at": spots_at,
            "sides_with": sides_with,
        }

    def _prioritise_sides(self, prio: Optional[str] = None) -> List[Side]:
        """Get current priority of sides

        Parameters
        ----------
        prio : Optional[str], optional
            Method of determining priority. Options: ['both', 'side', 'spot'],
            None defaults to Sheduler.feature_priority, default "both".

        Returns
        -------
        List[Side]
            List of sides in order of assignment priority.

        Raises
        ------
        ValueError
            On invalid priority.
        """
        if not prio:
            prio = self.side_priority

        metrics = self.side_metrics()

        if prio == "side":
            scores = metrics["sides_with"]
        elif prio == "spot":
            scores = metrics["spots_at"]
        elif prio == "both":
            scores = [
                spots + sides
                for spots, sides in zip(metrics["spots_at"], metrics["sides_with"])
            ]
        else:
            raise ValueError(
                (
                    f"Side priority is {self.side_priority}"
                    "must be one of 'both', 'spot' or 'side'."
                )
            )
        score_dict = {side: score for side, score in zip(metrics["sides"], scores)}
        score_list = sorted(score_dict, key=lambda side: score_dict[side])
        log.debug(f"prio scores:\n{pp.pformat(score_dict)}\n")
        log.debug(f"prio order:\n{pp.pformat(score_list)}\n")
        return sorted(score_dict, key=lambda side: score_dict[side])


    def _valid_options(
        self, timeslot: Dict[str, List], side: Side, options: Sequence
    ) -> Set[str]:
        """Set of valid spots to allocate side to. """
        selection = set(options)
        for feature in self.feature_priority:
            scores = self._feature_func_dict[feature](timeslot, side, self.side_decider)
            
            log.debug(f"{feature} scores: {scores}")

            prev_selection = selection.copy()

            for spot, val in scores.items():
                if val != min(scores.values()):
                    selection.discard(spot)

            if not selection:
                selection = prev_selection.copy()
        
        log.debug(f"selection: {selection}")
        return selection


    def _assign_side(
        self, timeslot: Dict[str, List], side: Side, allocation: str
    ) -> None:
        """Assign side to spot at timeslot."""
        timeslot[allocation].append(side)


    def _schedule_next(self) -> None:
        log.info("Schedule Next")
        
        timeslot = self._fetch_timeslot()
        prio_sides = self._prioritise_sides()
        spots = self.event.spots

        while prio_sides:
            side = prio_sides.pop(0)
            log.debug(f"side: {side.name.upper()}\n")
            
            selection = self._valid_options(timeslot, side, spots)
            allocation = choice(list(selection))
            self._assign_side(timeslot, side, allocation)
            log.debug(f"{side} assigned to {allocation}\n")
            
        self.event.update_freqs()
        self.cur_time = self.cur_time + 1
        
        log.debug(f"side frequency:\n{self.event.freq_side}\n")
        log.debug(f"spot frequency:\n{self.event.freq_spot}\n")
        log.debug(f"timeslot:\n{pp.pformat(timeslot)}\n")
    
    def schedule(self) -> None:
        log.info("Scheduling Begin")
        
        while self.cur_time < self.event.slots:
            self._schedule_next()
            
        log.info("Scheduling End")
        
