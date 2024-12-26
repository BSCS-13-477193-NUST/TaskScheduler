import time

class Timestamp:
    minute: int
    hour: int
    day: int
    month: int
    year: int

    def __init__(self, minute: int, hour: int, day: int, month: int, year: int):
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year
    
    def getCurrentTimestamp() -> 'Timestamp':
        current_time = time.localtime()
        return Timestamp(current_time.tm_min, current_time.tm_hour, current_time.tm_mday, current_time.tm_mon, current_time.tm_year)
    
    def getDifference(self, timestamp: 'Timestamp') -> int:
        return (self.year - timestamp.year) * 525600 + (self.month - timestamp.month) * 43800 + (self.day - timestamp.day) * 1440 + (self.hour - timestamp.hour) * 60 + (self.minute - timestamp.minute)

    def getMinutesLeft(self) -> int:
        time1 = Timestamp.getCurrentTimestamp()
        return self.getDifference(time1)

    
    def __str__(self) -> str:
        return f"{self.hour:02}:{self.minute:02} {self.day:02}/{self.month:02}/{self.year}" 