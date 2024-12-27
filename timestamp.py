import time

class Timestamp:
    minute: int
    hour: int
    day: int
    month: int
    year: int

    days_in_month = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

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

    def addMinutes(self, minutes: int):
        self.minute += minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
        while self.day > Timestamp.days_in_month[self.month]:
            #adjust for leap year
            if self.month == 2 and self.day > 28:
                if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0):
                    if self.day > 29:
                        self.day -= 29
                        self.month += 1
                    else:
                        break
                else:
                    self.day -= 28
                    self.month += 1
            else:
                self.day -= Timestamp.days_in_month[self.month]
                self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1

    
    def __str__(self) -> str:
        return f"{self.hour:02}:{self.minute:02} {self.day:02}/{self.month:02}/{self.year}" 