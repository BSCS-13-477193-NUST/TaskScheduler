from task import Task
import matplotlib.pyplot as plt
from timestamp import Timestamp

class Calendar:
    #stores 60 minutes of every 24 hours of every day of every month of the year
    calendar = [[[[[] for _ in range(60)] for _ in range(24)] for _ in range(31)] for _ in range(12)]
        

    
    def addTask(self, tasks):
        for task in tasks:
            
            start_time_str = task.start_time
            start_time = self.fromString(start_time_str)
            print(start_time)

            # Access the components of the Timestamp object
            start_month = start_time.month - 1  # 0-based index for months
            print(start_month)
            start_day = start_time.day - 1      # 0-based index for days
            print(start_day)
            start_hour = start_time.hour
            print(start_hour)        # 0-based index for hours
            start_minute = start_time.minute    # 0-based index for minutes
            print(start_minute)
            
            # Append the task to the correct slot in the calendar
            self.calendar[start_month][start_day][start_hour][start_minute].append(task)

        print("Tasks added successfully!\n")
        
    
    @staticmethod
    def fromString(start_time_str: str) -> 'Timestamp':
        # Split string like "2024-01-31 21:59:59"
        date_str, time_str = start_time_str.split(' ')
        year, month, day = map(int, date_str.split('-'))
        hour, minute, _ = map(int, time_str.split(':'))
        
        # Return Timestamp object
        return Timestamp(minute, hour, day, month, year)

    def displayYearCalendar(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title("Task Calendar")
        ax.set_xlabel("Day")
        ax.set_ylabel("Month")
        ax.set_xticks(range(31))
        ax.set_yticks(range(12))
        ax.set_xticklabels(range(1, 32))
        ax.set_yticklabels([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])

        def get_color(task_count):
            # Base skin tone color (light skin tone) in hex
            base_hex = "#add8e6"
            
            # Convert the base hex color to RGB
            r = int(base_hex[1:3], 16)
            g = int(base_hex[3:5], 16)
            b = int(base_hex[5:7], 16)
            
            # Scale the color based on task count (e.g., make the color darker as task_count increases)
            scale_factor = 1 - (task_count / 7)  # Adjust scaling factor to control how dark the color gets
            
            # Ensure scaling factor is in the range [0, 1] and scale the RGB values
            r = max(int(r * scale_factor), 0)
            g = max(int(g * scale_factor), 0)
            b = max(int(b * scale_factor), 0)
            
            # Convert the adjusted RGB values back to hex
            new_color = f"#{r:02x}{g:02x}{b:02x}"
            return new_color

        for month in range(12):
            for day in range(31):
                task_count = 0  # Initialize task count for the day
                for hour in range(24):
                    for minute in range(60):
                        tasks = self.calendar[month][day][hour][minute]
                        task_count += len(tasks)  # Count the tasks for this hour and minute
                
                if task_count > 0:
                    # Assign color based on the task count
                    color = get_color(task_count)
                    ax.scatter(day, month, color=color, s=100)  # Pl

        plt.show()

def main():

    tasks = [
        Task(
            "quran",
            "i have to revise and then recite it to mama as well",
            7,
            6,
            2,
            7,
            "2024-12-31 23:59:59",
            "2024-01-31 21:59:59",
            "2024-12-31 23:59:59",
            False
        ),
        Task(
            "exercise",
            "30 minutes of cardio",
            5,
            4,
            0.5,
            6,
            "2024-12-31 23:59:59",
            "2024-01-31 08:00:00",
            "2024-02-01 08:30:00",
            True
        ),
        Task(
            "meeting",
            "team meeting",
            8,
            3,
            1,
            5,
            "2024-12-31 23:59:59",
            "2024-01-31 10:00:00",
            "2024-02-02 11:00:00",
            True
        ),
        Task(
            "shopping",
            "grocery shopping",
            4,
            2,
            2,
            3,
            "2024-12-31 23:59:59",
            "2024-01-03 15:00:00",
            "2024-02-03 17:00:00",
            True
        ),
        Task(
            "study",
            "study for exam",
            9,
            7,
            3,
            8,
            "2024-12-31 23:59:59",
            "2024-01-03 18:00:00",
            "2024-02-04 21:00:00",
            True
        ),
        Task(
            "coding",
            "work on a coding project",
            6,
            5,
            2,
            4,
            "2024-12-31 23:59:59",
            "2024-01-03 14:00:00",
            "2024-02-01 16:00:00",
            True
        ),
        Task(
            "reading",
            "read a book",
            3,
            2,
            1.5,
            2,
            "2024-12-31 23:59:59",
            "2024-01-31 18:00:00",
            "2024-02-01 19:30:00",
            True
        ),
        Task(
            "cooking",
            "prepare dinner",
            2,
            1,
            1,
            1,
            "2024-12-31 23:59:59",
            "2024-02-02 19:00:00",
            "2024-02-01 20:00:00",
            True
        ),
        Task(
            "meditation",
            "practice mindfulness",
            1,
            1,
            0.5,
            1,
            "2024-12-31 23:59:59",
            "2024-11-31 20:30:00",
            "2024-02-01 21:00:00",
            True
        ),
        Task(
            "project",
            "work on a project",
            7,
            6,
            4,
            7,
            "2024-12-31 23:59:59",
            "2024-03-01 10:00:00",
            "2024-03-05 14:00:00",
            True
        ),
        Task(
            "cleaning",
            "clean the house",
            5,
            4,
            3,
            6,
            "2024-12-31 23:59:59",
            "2024-03-10 09:00:00",
            "2024-03-10 12:00:00",
            True
        ),
        Task(
            "gardening",
            "take care of the garden",
            6,
            5,
            2,
            4,
            "2024-12-31 23:59:59",
            "2024-03-15 14:00:00",
            "2024-03-15 16:00:00",
            True
        )
    ]

    calendar = Calendar()
    calendar.addTask(tasks)
    print("Calendar:")
    calendar.displayYearCalendar()
if __name__ == "__main__":
    main()