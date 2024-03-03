from datetime import datetime
from dataclasses import dataclass


@dataclass
class TSCheckpoint:
    """
    Checkpoint class to track various durations duing a time test

    :attribute name: name of the checkpoint, random name generated if none provided
    :attribute target: target duration, default timer target provided if no checkpoint specific target
    :attribute time: time the checkpoint was marked
    :attribute duration: elapsed time in seconds from when the timer was started
    """
    name = None
    target = None
    time = None
    duration = None

    def __init__(self, name=None, target=None, time=None, duration=None):
        if name:
            self.name = name
        else:
            self.name = f"cp{datetime.now().strftime('%m%d%H%M%S%f')}"  # Adding time for uniqueness
        self.target = target
        self.time = time
        self.duration = duration
