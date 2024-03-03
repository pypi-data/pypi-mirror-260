import time
import numpy as np
from timer_score.ts_checkpoint import TSCheckpoint


class TSTimer:
    """
    Generalized timer class that generates a score from 0 to 1

    :attribute target: the target duration
    :attribute start: start time marked when class instantiated
    :attribute finish: finish time set with stop method
    :attribute checkpoints: list of named checkpoints with time stamps

    :method reset(): clears all checkpoints and captures new start
    :method stop(): captures final checkpoint
    :method checkpoint(): checkpoints a specific time while timer runs
    :method duration(): duration of specific checkpoint or total time
    :method score(): returns score from 0 to 1 of specific checkpoint or total time
    """
    def __init__(self, target=None) -> None:
        """
        Initiates the class and marks the start time
        """
        self.target = target
        self.start = time.time()
        self.checkpoints: list[TSCheckpoint] = []
        self.__finished = False

    @property
    def finish(self) -> float | None:
        """
        Returns the time of the final checkpoint
        """
        if self.__finished:
            return self.checkpoints[len(self.checkpoints) - 1].time
        return None

    def reset(self) -> None:
        """
        Resets the timer
        """
        self.checkpoints = []
        self.__finished = False
        self.start = time.time()

    def stop(self) -> None:
        """
        Stops the timer amd marks the finish time as the final checkpoint
        """
        self.checkpoint(name="finish")
        self.__finished = True

    def sleep(self, seconds):
        """
        Sleep avoids importing time everywhere
        """
        time.sleep(seconds)

    def checkpoint(self, name=None, target=None) -> TSCheckpoint | None:
        """
        Adds another checkpoint

        :param name: (optional) name of the checkpoint
        :param target: (optional) target to use for score of checkpoint

        :return: TSCheckpoint
        """
        if self.__finished:
            return None

        if name and self.__find_checkpoint(name):
            raise ValueError("Duplicate checkpoint name")

        time_now = time.time()
        target = target if target else self.target
        duration = time_now - self.start
        checkpoint = TSCheckpoint(
            name = name,
            target = target,
            time = time_now,
            duration = duration
        )
        self.checkpoints.append(checkpoint)
        return checkpoint

    def __find_checkpoint(self, name=None):  # TODO Add return value
        """
        Find checkpoint by name or index

        :param index: (optional) index of checkpoint
        :param name: (optional) name of checkpoint

        :return: TSCheckpoint or none if not found
        """
        for checkpoint in self.checkpoints:
            if checkpoint.name == name:
                return checkpoint

        return None

    def duration(self, name=None) -> float:
        """
        Calculates total time spent from start to a check point or finish

        :param name: (optional) name of checkpoint
        """
        if name:
            checkpoint = self.__find_checkpoint(name)
            if checkpoint:
                return checkpoint.duration

        if name and not checkpoint:
            raise ValueError("Invalid checkpoint name provided")

        if not self.finish:
            return time.time() - self.start

        return self.finish - self.start

    def score(self, name=None) -> tuple:
        """
        Calculate score as a percentage using a sigmoid function.
        The score approaches 1 as the performance gets better as measured
        by the duration against the target duration.
        The score approaches 0 as performance gets worse.

        :param name: (optional) name of checkpoint to use in calculation

        :return score: Score ranging from 0 to 1
        :return duration: Duration used to calculate score
        :return target: Target duration used to calculate score
        """
        checkpoint = self.__find_checkpoint(name)

        if name and not checkpoint:
            raise ValueError("Invalid checkpoint name provided")

        if checkpoint:
            duration = checkpoint.duration
            target = checkpoint.target
        else:
            target = self.target
            duration = self.duration()

        if not target:
            raise ValueError("No target provided")

        # Slope more aggressive for low targets and less aggressive for high targets
        if target < 1.5:
            k = 2.0
        elif target > 5:
            k = 0.5
        else:
            k = 1.0

        score = 1 - (1 / (1 + np.exp(-k * (duration - target))))
        return score, duration, target

    def execute(self, func, *args, **kwargs) -> tuple:
        """
        Calculate score, duration to execute the function.

        :param func: function to execute to calcuate the score and duration
        :param args: positional arguments to pass to function
        :param kwargs: named arguments to pass to function

        :return score: Score ranging from 0 to 1
        :return duration: Duration used to calculate score
        :return target: Target duration used to calculate score
        """
        func(*args, **kwargs)
        self.stop()
        return self.score()
