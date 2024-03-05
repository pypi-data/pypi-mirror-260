"""
A timing library for python. Record basic stats for arbitrary timed operations and compute average times
for repeated invocations.
"""
import sys
import os
import hashlib
from pathlib import Path


TASKSTATS_DIR_NAME = ".taskstats/"
TASKSTATS_DIR_ENV = "TASKSTATS_DIR"
TASKSTATS_MAX_HISTORY = 5


class TaskStat:
    """The timing history of a task"""
    def __init__(self):
        self.name = None
        self.timings = []

    def mean(self) -> float:
        """Get the mean time of this tasks"""
        total = sum(self.timings)
        if len(self.timings) > 0:
            return total / len(self.timings)
        return 0

    def max(self) -> float:
        """Get the longest recorded time"""
        found = 0
        for t in self.timings:
            if t > found:
                found = t
        return found


def get_taskstats_dir() -> Path:
    """Get the path to the taskstats folder"""
    dir_override = os.environ.get(TASKSTATS_DIR_ENV, None)
    if dir_override is not None:
        folder = Path(dir_override)
    else:
        folder = Path.home() / TASKSTATS_DIR_NAME
    return folder


def _get_task_index(name) -> str:
    """Make a sha1 string from name to use as a task index"""
    sha1 = hashlib.sha1(str(name).encode("ascii"))
    return sha1.hexdigest()


def record_task_timing(name: str, duration: int) -> TaskStat:
    """Record how long the task took in seconds."""
    task_index = _get_task_index(name)
    task_file = get_taskstats_dir() / task_index
    try:
        task_file.parent.mkdir(parents=True, exist_ok=True)
        with task_file.open("a") as outfile:
            outfile.write(f"{duration}\n")

        # read back to check max lines
        timing = get_task_timing(name)
        if len(timing.timings) > TASKSTATS_MAX_HISTORY:
            # replace the file if it is too big
            timing.timings = timing.timings[TASKSTATS_MAX_HISTORY * -1:]
            with task_file.open("w") as outfile:
                for duration in timing.timings:
                    outfile.write(f"{duration}\n")
    except Exception as err:
        sys.stderr.write(f"cannot record task timing for {name}: {err}\n")
        timing = get_task_timing(name)

    return timing


def get_task_timing(name: str) -> TaskStat:
    """Get the timings for a task if possible"""
    timing = TaskStat()
    timing.name = name
    try:
        filename = _get_task_index(name)
        taskfile = get_taskstats_dir() / filename
        if taskfile.exists():
            lines = taskfile.read_text().splitlines()
            for item in lines:
                value = float(item)
                timing.timings.append(value)
    except Exception as err:
        sys.stderr.write(f"cannot read task timing for {name}: {err}\n")

    return timing
