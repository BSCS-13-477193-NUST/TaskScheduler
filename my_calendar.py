from task import Task
import matplotlib.pyplot as plt
from timestamp import Timestamp

class Calendar:
    #stores 60 minutes of every 24 hours of every day of every month of the year
    calendar = [[[] for _ in range(31)] for _ in range(12)]

    def addTask(self, tasks):

            # Append the task to the correct slot in the calendar
        self.calendar[task.start_time.month][task.start_time.day].append(task)

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
                tasks = self.calendar[month][day]
                if tasks:
                    # Calculate the number of tasks for the day
                    task_count = len(tasks)
                    # Assign red color if the number of tasks is high (e.g., >= 5), else blue
                    color = get_color(task_count)

                    ax.scatter(day, month, color=color, s=100)

        plt.show()

        

def main():

    tasks = [
            {
                "title": "quran",
                "description": "i have to revise and then recite it to mama as well",
                "priority": 7,
                "difficulty": 6,
                "duration": 2,
                "fuel_cost": 7,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 21:59:59",
                "end_time": "2024-12-31 23:59:59",
                "absolute": False
            },
            {
                "title": "exercise",
                "description": "30 minutes of cardio",
                "priority": 5,
                "difficulty": 4,
                "duration": 0.5,
                "fuel_cost": 6,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 08:00:00",
                "end_time": "2024-02-01 08:30:00",
                "absolute": True
            },
            {
                "title": "meeting",
                "description": "team meeting",
                "priority": 8,
                "difficulty": 3,
                "duration": 1,
                "fuel_cost": 5,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 10:00:00",
                "end_time": "2024-02-02 11:00:00",
                "absolute": True
            },
            {
                "title": "shopping",
                "description": "grocery shopping",
                "priority": 4,
                "difficulty": 2,
                "duration": 2,
                "fuel_cost": 3,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-03 15:00:00",
                "end_time": "2024-02-03 17:00:00",
                "absolute": True
            },
            {
                "title": "study",
                "description": "study for exam",
                "priority": 9,
                "difficulty": 7,
                "duration": 3,
                "fuel_cost": 8,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-03 18:00:00",
                "end_time": "2024-02-04 21:00:00",
                "absolute": True
            },
            {
                "title": "coding",
                "description": "work on a coding project",
                "priority": 6,
                "difficulty": 5,
                "duration": 2,
                "fuel_cost": 4,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-03 14:00:00",
                "end_time": "2024-02-01 16:00:00",
                "absolute": True
            },
            {
                "title": "reading",
                "description": "read a book",
                "priority": 3,
                "difficulty": 2,
                "duration": 1.5,
                "fuel_cost": 2,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 18:00:00",
                "end_time": "2024-02-01 19:30:00",
                "absolute": True
            },
            {
                "title": "cooking",
                "description": "prepare dinner",
                "priority": 2,
                "difficulty": 1,
                "duration": 1,
                "fuel_cost": 1,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-02-02 19:00:00",
                "end_time": "2024-02-01 20:00:00",
                "absolute": True
            },
            {
                "title": "meditation",
                "description": "practice mindfulness",
                "priority": 1,
                "difficulty": 1,
                "duration": 0.5,
                "fuel_cost": 1,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-11-31 20:30:00",
                "end_time": "2024-02-01 21:00:00",
                "absolute": True
            },
            {
                "title": "project",
                "description": "work on a project",
                "priority": 7,
                "difficulty": 6,
                "duration": 4,
                "fuel_cost": 7,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-03-01 10:00:00",
                "end_time": "2024-03-05 14:00:00",
                "absolute": True
            },
            {
                "title": "cleaning",
                "description": "clean the house",
                "priority": 5,
                "difficulty": 4,
                "duration": 3,
                "fuel_cost": 6,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-03-10 09:00:00",
                "end_time": "2024-03-10 12:00:00",
                "absolute": True
            },
            {
                "title": "gardening",
                "description": "take care of the garden",
                "priority": 6,
                "difficulty": 5,
                "duration": 2,
                "fuel_cost": 4,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-03-15 14:00:00",
                "end_time": "2024-03-15 16:00:00",
                "absolute": True
            }
        ]

    calendar = Calendar()
    calendar.addTask(tasks)
    print("Calendar:")
    calendar.displayYearCalendar()
if __name__ == "__main__":
    main()