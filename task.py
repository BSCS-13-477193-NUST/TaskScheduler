from timestamp import Timestamp
from settings import weights

class Task:
    title: str
    description: str
    priority: int
    difficulty: int
    duration: float
    fuel_cost: float
    deadline: Timestamp
    start_time: Timestamp
    end_time: Timestamp
    absolute: bool
    completed: bool
    weightage: float

    def __init__(self, title: str, description: str, priority: int, difficulty: int, duration: float, score: float, deadline: Timestamp, start_time: Timestamp, end_time: Timestamp, absolute: bool):
        self.title = title
        self.description = description
        self.priority = priority
        self.difficulty = difficulty
        self.duration = duration
        self.fuel_cost = score
        self.deadline = deadline
        self.start_time = start_time
        self.end_time = end_time
        self.absolute = absolute
        self.completed = False
        self.weightage = 0

    def calculateWeightage(self):
        deadlineMins = self.deadline.getMinutesLeft()
        completionWindow = self.end_time.getDifference(self.start_time)

        self.weightage = (
            weights['w1'] * self.priority +
            weights['w2'] * self.difficulty -
            weights['w3'] * self.duration -
            weights['w4'] * self.fuel_cost -
            weights['w5'] * deadlineMins -
            weights['w6'] * completionWindow
        )

    def set_name(self, name: str):
        self.title = name

    def get_name(self) -> str:
        return self.title

    def set_priority(self, priority: int):
        self.priority = priority

    def get_priority(self) -> int:
        return self.priority

    def set_difficulty(self, difficulty: int):
        self.difficulty = difficulty

    def get_difficulty(self) -> int:
        return self.difficulty

    def set_duration(self, duration: float):
        self.duration = duration

    def get_duration(self) -> float:
        return self.duration

    def set_score(self, score: float):
        self.fuel_cost = score

    def get_score(self) -> float:
        return self.fuel_cost

    def set_deadline(self, deadline: Timestamp):
        self.deadline = deadline

    def get_deadline(self) -> Timestamp:
        return self.deadline

    def set_start_time(self, start_time: Timestamp):
        self.start_time = start_time

    def get_start_time(self) -> Timestamp:
        return self.start_time

    def set_end_time(self, end_time: Timestamp):
        self.end_time = end_time

    def get_end_time(self) -> Timestamp:
        return self.end_time

    def set_delayable(self, delayable: bool):
        self.absolute = delayable

    def get_delayable(self) -> bool:
        return self.absolute

    def set_completed(self, completed: bool):
        self.completed = completed

    def get_completed(self) -> bool:
        return self.completed

    def set_weightage(self, weightage: float):
        self.weightage = weightage

    def get_weightage(self) -> float:
        return self.weightage