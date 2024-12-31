from timestamp import Timestamp
from settings import weights

class Task:
    id: int
    title: str
    description: str
    priority: int
    difficulty: int
    duration: float         #hours
    deadline: Timestamp
    start_time: Timestamp
    end_time: Timestamp
    delayable: bool
    completed: bool
    recurring: int
    repeat: int
    weightage: float
    i = 1
    def __init__(self, title: str, description: str, priority: int, difficulty: int, duration: float, deadline: Timestamp, start_time: Timestamp, end_time: Timestamp, delayable: bool, recurring: str, repeat: int) -> None:
        self.id = self.i
        Task.i += 1
        self.title = title
        self.description = description
        self.priority = priority
        self.difficulty = difficulty
        self.duration = duration
        self.deadline = deadline
        self.start_time = start_time
        self.end_time = end_time
        self.delayable = delayable
        self.recurring = recurring
        self.repeat = repeat
        self.completed = False
        self.weightage = 0

    def calculate_weightage(self):
        completionRatio = self.duration / (self.deadline.getDifference(self.start_time) / 60)

        self.weightage = (
            - weights['priority'] * self.priority +
            weights['difficulty'] * self.difficulty +
            weights['completion ratio'] * completionRatio
        )

    def __str__(self) -> str:
        return f"Task ID {self.id}: {self.title}\nDescription: {self.description}\nPriority: {self.priority}\nDifficulty: {self.difficulty}\nDuration: {self.duration} hours\nDeadline: {self.deadline}\nStart Time: {self.start_time}\nEnd Time: {self.end_time}\nDelayable: {self.delayable}\nCompleted: {self.completed}\nWeightage: {self.weightage:.2f}"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'difficulty': self.difficulty,
            'duration': self.duration,
            'deadline': self.deadline.to_dict(),
            'start_time': self.start_time.to_dict(),
            'end_time': self.end_time.to_dict(),
            'delayable': self.delayable,
            'completed': self.completed,
            'weightage': self.weightage,
            'recurring': self.recurring,
            'repeat': self.repeat
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['title'],
            data['description'],
            data['priority'],
            data['difficulty'],
            data['duration'],
            Timestamp.from_dict(data['deadline']),
            Timestamp.from_dict(data['start_time']),
            Timestamp.from_dict(data['end_time']),
            data['delayable'],
            data['recurring'],
            data['repeat'],
        )

    def set_title(self, title: str):
        self.title = title

    def get_title(self) -> str:
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

    def get_id(self) -> int:
        return self.id

    def get_recurring(self) -> int:
        return self.recurring
    
    def set_recurring(self, recurring: int):
        self.recurring = recurring
    
    def get_repeat(self) -> int:
        return self.repeat
    
    def set_repeat(self, repeat: int):
        self.repeat = repeat

    def get_description(self) -> str:
        return self.description
    
    def set_description(self, description: str):
        self.description = description
    
    def get_weightage(self) -> float:
        return self.weightage

    def set_weightage(self, weightage: float):
        self.weightage = weightage