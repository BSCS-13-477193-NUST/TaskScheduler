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
        temp = self
        temp.minute += minutes
        while temp.minute >= 60:
            temp.minute -= 60
            temp.hour += 1
        while temp.hour >= 24:
            temp.hour -= 24
            temp.day += 1
        while temp.day > Timestamp.days_in_month[temp.month]:
            #adjust for leap year
            if temp.month == 2 and temp.day > 28:
                if (temp.year % 4 == 0 and temp.year % 100 != 0) or (temp.year % 400 == 0):
                    if temp.day > 29:
                        temp.day -= 29
                        temp.month += 1
                    else:
                        break
                else:
                    temp.day -= 28
                    temp.month += 1
            else:
                temp.day -= Timestamp.days_in_month[temp.month]
                temp.month += 1
            if temp.month > 12:
                temp.month = 1
                temp.year += 1

    
    def __str__(self) -> str:
        return f"{self.hour:02}:{self.minute:02} {self.day:02}/{self.month:02}/{self.year}" 