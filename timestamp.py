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
    
    @staticmethod
    def getCurrentTimestamp() -> 'Timestamp':
        current_time = time.localtime()
        return Timestamp(current_time.tm_min, current_time.tm_hour, current_time.tm_mday, current_time.tm_mon, current_time.tm_year)
    
    def getDifference(self, timestamp: 'Timestamp') -> int:
        return (self.year - timestamp.year) * 525600 + (self.month - timestamp.month) * 43800 + (self.day - timestamp.day) * 1440 + (self.hour - timestamp.hour) * 60 + (self.minute - timestamp.minute)

    def isBefore(self, timestamp: 'Timestamp') -> bool:
        if self.year < timestamp.year:
            return True
        elif self.year == timestamp.year:
            if self.month < timestamp.month:
                return True
            elif self.month == timestamp.month:
                if self.day < timestamp.day:
                    return True
                elif self.day == timestamp.day:
                    if self.hour < timestamp.hour:
                        return True
                    elif self.hour == timestamp.hour:
                        if self.minute < timestamp.minute:
                            return True
        return False

    def getMinutesLeft(self) -> int:
        time1 = Timestamp.getCurrentTimestamp()
        return self.getDifference(time1)

    def addMinutes(self, minutes: int) -> 'Timestamp':
        temp = self.__class__(self.minute, self.hour, self.day, self.month, self.year)
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
        return temp

    def addDays(self, days: int) -> 'Timestamp':
        temp = self.__class__(self.minute, self.hour, self.day, self.month, self.year)
        temp.day += days
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
        return temp

    def addMonths(self, months: int) -> 'Timestamp':
        temp = self.__class__(self.minute, self.hour, self.day, self.month, self.year)
        temp.month += months
        while temp.month > 12:
            temp.month -= 12
            temp.year += 1
        # Adjust the day if it exceeds the maximum days in the resulting month
        if temp.day > Timestamp.days_in_month[temp.month]:
            if temp.month == 2 and temp.day > 28:
                if (temp.year % 4 == 0 and temp.year % 100 != 0) or (temp.year % 400 == 0):
                    if temp.day > 29:
                        temp.day = 29
                else:
                    temp.day = 28
            else:
                temp.day = Timestamp.days_in_month[temp.month]
        return temp

    @staticmethod
    def getDate(text) -> 'Timestamp':
        temp = Timestamp.getCurrentTimestamp()
        if text == "now":
            return temp
        try:
            if '-' not in text:
                #time only format (HH:MM)
                parts = text.split(':')
                hour = int(parts[0])
                minute = int(parts[1])
                day = temp.day
                month = temp.month
                year = temp.year
            elif ':' not in text:
                #date only format (YYYY-MM-DD)
                parts = text.split('-')
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2][:2])
                minute = 59
                hour = 23
            else:
                #date and time format (YYYY-MM-DD HH:MM)
                parts = text.split('-')
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2][:2])
                parts = parts[2][2:].split(':')
                hour = int(parts[0])
                minute = int(parts[1])
        except ValueError or IndexError:
            print("Invalid date/time format. Please try again.")
            return None
        #validation check
        if year < 2024 or month < 1 or month > 12 or day < 1 or day > 31 or hour < 0 or hour > 23 or minute < 0 or minute > 59:
            print("Invalid date/time format. Please try again.")
            return None
        return Timestamp(minute, hour, day, month, year)

    def __str__(self) -> str:
        return f"{self.hour:02}:{self.minute:02} {self.day:02}/{self.month:02}/{self.year}" 

    def to_dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'hour': self.hour,
            'minute': self.minute
        }

    @staticmethod
    def from_dict(data):
        return Timestamp(data['minute'], data['hour'], data['day'], data['month'], data['year'])