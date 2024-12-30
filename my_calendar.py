import calendar
from task import Task
import matplotlib.pyplot as plt
from timestamp import Timestamp
import matplotlib.patches as patches

class Calendar:
    # stores 60 minutes of every 24 hours of every day of every month of the year
    calendar = [[[] for _ in range(31)] for _ in range(12)]
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # Number of days in each month
    
    def addTask(self, tasks):
        for task in tasks:
            start_time_str = task.start_time
            start_time = self.fromString(start_time_str)

            # Access the components of the Timestamp object
            start_month = start_time.month - 1  # 0-based index for months
            start_day = start_time.day - 1      # 0-based index for days
            
            # Append the task to the correct slot in the calendar
            self.calendar[start_month][start_day].append(task)

        print("Tasks added successfully!\n")
        
    @staticmethod
    def fromString(start_time_str: str) -> 'Timestamp':
        # Split string like "2024-01-31 21:59:59"
        date_str, time_str = start_time_str.split(' ')
        year, month, day = map(int, date_str.split('-'))
        hour, minute, _ = map(int, time_str.split(':'))
        
        # Return Timestamp object
        return Timestamp(minute, hour, day, month, year)

    def displayDailyTasks(self, month, day):
        # Check if the day is valid for the given month
        month = month - 1
        day = day - 1
        if day >= self.days_in_month[month]:
            print(f"Error: Day {day + 1} is out of range for month {month + 1}.")
            return

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title(f"Tasks for {day + 1}/{month + 1}/2025", fontweight = 'bold')
        ax.set_xlabel("Minute")
        ax.set_ylabel("Hour")
        
        # Set background color to black
        ax.set_facecolor('white')

        # Define Y-axis labels (hours)
        ax.set_yticks(range(24))
        ax.set_yticklabels([f"{i}:00" for i in range(24)])

        # Define X-axis labels (minutes)
        ax.set_xticks(range(0, 60, 5))  # Display every 5th minute
        ax.set_xticklabels([f"{i:02d}" for i in range(0, 60, 5)])

        # Draw the grid
        ax.grid(True, which='both', axis='both', color='white', linestyle='-', linewidth=0)


        tasks = self.calendar[month][day]
        if tasks:
            # Place an elongated shape for each task
            for task in tasks:
                # Change from string to timestamp object
                start_time_str = task.start_time
                start_time = self.fromString(start_time_str)

                # Storing details of the task
                minute = start_time.minute
                hour = start_time.hour
                duration = task.duration * 60  # Convert duration to minutes
                
                # Calculate the number of full hours and remaining minutes
                remaining_duration = duration
                current_hour = hour
                current_minute = minute
                
                while remaining_duration > 0:
                    # Calculate time remaining in the current hour
                    minutes_in_current_hour = 60 - current_minute
                    
                    # Determine the duration to display in the current hour
                    duration_in_this_hour = min(remaining_duration, minutes_in_current_hour)
                    
                    # Plot the task segment in the current hour
                    ax.plot(
                        [current_minute, current_minute + duration_in_this_hour],
                        [current_hour, current_hour],
                        color='#add8e6',
                        linewidth=5
                    )
                    ax.scatter(
                        current_minute,
                        current_hour,
                        color='#add8e6',
                        s=100,
                        edgecolor='#add8e6',
                        label="Task" if current_minute == minute and current_hour == hour else ""
                    )
                    ax.text(
                        current_minute,
                        current_hour,
                        task.title,
                        color='black',
                        fontsize=12,
                        fontfamily='cursive',
                        ha='left',
                        va='center'
                    )
                    
                    # Update remaining duration and move to the next hour if needed
                    remaining_duration -= duration_in_this_hour
                    current_hour += 1  # Move to the next hour
                    current_minute = 0  # Reset minute to the start of the next hour


        # Display the plot
        plt.show()
    
    def displayYearlyCalendar(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title("Task Calendar", fontweight = 'bold')
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
                task_count = len(self.calendar[month][day])
                if task_count > 0:
                    # Assign color based on the task count
                    color = get_color(task_count)
                    ax.scatter(day, month, color=color, s=100)  # Pl

        plt.show()

    def displayMonthlyCalendar(self, month):
    
        # Check if the month is valid
        month = month - 1
        if month < 0 or month >= 12:
            print(f"Error: Month {month + 1} is out of range.")
            return

        # Get the number of days in the month and the starting weekday
        year = 2025
        days_in_month = calendar.monthrange(year, month + 1)[1]
        start_weekday = calendar.monthrange(year, month + 1)[0]  # Monday = 0, Sunday = 6

        # Set up the calendar grid (days on x-axis, weeks on y-axis)
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_title(f"Task Calendar for {calendar.month_name[month + 1]} {year}", fontweight='bold')
        
        # Define x-axis labels (days of the week)
        ax.set_xticks(range(7))
        ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fontsize=10)

        # Define y-axis labels (weeks)
        num_weeks = (days_in_month + start_weekday + 6) // 7  # Calculate required number of weeks
        ax.set_yticks(range(num_weeks))
        ax.set_yticklabels([f"Week {i + 1}" for i in range(num_weeks)], fontsize=10)

        # Set grid and invert the y-axis for top-to-bottom alignment
        ax.set_xlim(-0.5, 6.5)
        ax.set_ylim(-0.5, num_weeks - 0.5)
        ax.invert_yaxis()  # Invert y-axis to display weeks top-to-bottom
        ax.set_facecolor("white")

        # Fetch the tasks for the given month
        tasks_for_month = self.calendar[month]

        # Map each day to its (week, day) coordinates
        day_to_coordinates = {}
        week = 0
        for day in range(1, days_in_month + 1):
            weekday = (start_weekday + day - 1) % 7
            if weekday == 0 and day != 1:
                week += 1  # Move to the next week
            day_to_coordinates[day] = (week, weekday)

        # Plot the calendar
        for day in range(1, days_in_month + 1):
            week, weekday = day_to_coordinates[day]
            
            # Display the date in the top-left corner of the grid cell
            ax.text(
                weekday + 0.3, week + 0.4,  # Adjust the position slightly
                str(day),
                fontsize=8,
                color="black",
                bbox=dict(facecolor='#add8e6', edgecolor='black', boxstyle='round,pad=0.1'),  # Light blue background with black border
                ha="left",
                va="center"
            )

            # Add a background rectangle for the grid cell
            rect = patches.Rectangle(
                (weekday - 0.45, week - 0.4),  # Bottom-left corner of the rectangle
                width=0.9,        # Width of the rectangle
                height=0.9,       # Height of the rectangle
                facecolor="#e0f7fa",  # Light cyan color for the rectangle
                alpha=0.3,        # Transparency
                edgecolor="grey", # Border color
                linewidth=0.5,    # Border width
            )
            ax.add_patch(rect)


            # Fetch tasks for the current day
            tasks = tasks_for_month[day - 1]
            if tasks:
                # Limit the number of tasks to 5
                tasks = tasks[:4]
                for i, task in enumerate(tasks):
                    # Get task details
                    start_time_str = task.start_time
                    start_time = self.fromString(start_time_str)
                    duration = task.duration
                    # Plot a rectangle for the task
                    rect = patches.Rectangle(
                        (weekday - 0.4, week + i * 0.2 - 0.4),  # Adjust position to stack tasks within the same day
                        width=0.8,  # Rectangle width
                        height=0.15,  # Rectangle height
                        facecolor="#add8e6",  # Task color
                        edgecolor="grey",
                        alpha=0.8,
                    )
                    ax.add_patch(rect)
                    # Add task title within the rectangle
                    ax.text(
                        weekday, week + i * 0.2 - 0.3,
                        task.title,
                        fontsize=8,
                        color="black",
                        verticalalignment="center",
                        horizontalalignment="center",
                    )
                # Add dots to indicate more tasks
                if len(tasks_for_month[day - 1]) > 4:
                    ax.text(
                        weekday, week + 0.4,
                        "...",
                        fontsize=8,
                        color="black",
                        verticalalignment="center",
                        horizontalalignment="center",
                    )

        plt.show()

    def clearCalendar(self):
        self.calendar = [[[] for _ in range(31)] for _ in range(12)]
        print("Calendar cleared successfully!\n")

    def removeTask(self, taskTitle):
        for month in range(12):
            for day in range(31):
                if self.calendar[month][day]:
                    for task in self.calendar[month][day]:
                        if task.title == taskTitle:
                            self.calendar[month][day].remove(task)
                            print(f"Task '{task.title}' removed successfully!\n")
                        else:
                            print(f"Task '{taskTitle}' not found in the calendar.\n")
        return


def main():
    tasks = [
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
        ),
        Task(
            "writing",
            "write a blog post",
            4,
            3,
            2,
            5,
            "2024-12-31 23:59:59",
            "2024-02-01 13:00:00",
            "2024-02-01 15:00:00",
            True
        ),
        Task(
            "music",
            "practice playing the guitar",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-01 16:30:00",
            "2024-02-01 18:00:00",
            True
        ),
        Task(
            "workout",
            "strength training",
            5,
            4,
            1,
            6,
            "2024-12-31 23:59:59",
            "2024-02-01 19:30:00",
            "2024-02-01 20:30:00",
            True
        ),
        Task(
            "cooking",
            "try a new recipe",
            2,
            1,
            2,
            2,
            "2024-12-31 23:59:59",
            "2024-02-01 21:30:00",
            "2024-02-01 23:30:00",
            True
        ),
        Task(
            "shopping",
            "buy new clothes",
            4,
            3,
            2,
            4,
            "2024-12-31 23:59:59",
            "2024-02-02 10:00:00",
            "2024-02-02 12:00:00",
            True
        ),
        Task(
            "cleaning",
            "clean the car",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-02 14:00:00",
            "2024-02-02 15:30:00",
            True
        ),
        Task(
            "meeting",
            "client meeting",
            6,
            5,
            1,
            7,
            "2024-12-31 23:59:59",
            "2024-02-02 16:00:00",
            "2024-02-02 17:00:00",
            True
        ),
        Task(
            "reading",
            "read a newspaper",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-03 08:00:00",
            "2024-02-03 09:00:00",
            True
        ),
        Task(
            "study",
            "learn a new programming language",
            8,
            7,
            4,
            9,
            "2024-12-31 23:59:59",
            "2024-02-03 10:00:00",
            "2024-02-04 14:00:00",
            True
        ),
        Task(
            "exercise",
            "yoga",
            3,
            2,
            1,
            4,
            "2024-12-31 23:59:59",
            "2024-02-03 16:00:00",
            "2024-02-03 17:00:00",
            True
        ),
        Task(
            "cooking",
            "bake a cake",
            4,
            3,
            2,
            5,
            "2024-12-31 23:59:59",
            "2024-02-03 18:00:00",
            "2024-02-03 20:00:00",
            True
        ),
        Task(
            "shopping",
            "buy groceries",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-04 09:00:00",
            "2024-02-04 10:30:00",
            True
        ),
        Task(
            "gardening",
            "plant flowers",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-04 14:00:00",
            "2024-02-04 15:00:00",
            True
        ),
        Task(
            "meeting",
            "project meeting",
            5,
            4,
            1.5,
            6,
            "2024-12-31 23:59:59",
            "2024-02-04 16:00:00",
            "2024-02-04 17:30:00",
            True
        ),
        Task(
            "study",
            "read a textbook",
            4,
            3,
            2,
            5,
            "2024-12-31 23:59:59",
            "2024-02-05 10:00:00",
            "2024-02-05 12:00:00",
            True
        ),
        Task(
            "exercise",
            "go for a run",
            3,
            2,
            1,
            4,
            "2024-12-31 23:59:59",
            "2024-02-05 14:00:00",
            "2024-02-05 15:00:00",
            True
        ),
        Task(
            "cooking",
            "try a new recipe",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-05 16:00:00",
            "2024-02-05 17:00:00",
            True
        ),
        Task(
            "shopping",
            "buy new clothes",
            4,
            3,
            2,
            4,
            "2024-12-31 23:59:59",
            "2024-02-06 09:00:00",
            "2024-02-06 11:00:00",
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
            "2024-02-06 14:00:00",
            "2024-02-06 17:00:00",
            True
        ),
        Task(
            "gardening",
            "trim the hedges",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-07 10:00:00",
            "2024-02-07 11:30:00",
            True
        ),
        Task(
            "meeting",
            "team meeting",
            6,
            5,
            1,
            7,
            "2024-12-31 23:59:59",
            "2024-02-07 14:00:00",
            "2024-02-07 15:00:00",
            True
        ),
        Task(
            "reading",
            "read a novel",
            4,
            3,
            2,
            5,
            "2024-12-31 23:59:59",
            "2024-02-07 16:00:00",
            "2024-02-07 18:00:00",
            True
        ),
        Task(
            "study",
            "prepare for a presentation",
            5,
            4,
            3,
            6,
            "2024-12-31 23:59:59",
            "2024-02-08 09:00:00",
            "2024-02-08 12:00:00",
            True
        ),
        Task(
            "exercise",
            "30 minutes of cardio",
            3,
            2,
            1,
            4,
            "2024-12-31 23:59:59",
            "2024-02-08 14:00:00",
            "2024-02-08 15:00:00",
            True
        ),
        Task(
            "cooking",
            "try a new recipe",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-08 16:00:00",
            "2024-02-08 17:00:00",
            True
        ),
        Task(
            "shopping",
            "buy groceries",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-09 09:00:00",
            "2024-02-09 10:30:00",
            True
        ),
        Task(
            "gardening",
            "plant flowers",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-09 14:00:00",
            "2024-02-09 15:00:00",
            True
        ),
        Task(
            "meeting",
            "project meeting",
            5,
            4,
            1.5,
            6,
            "2024-12-31 23:59:59",
            "2024-02-09 16:00:00",
            "2024-02-09 17:30:00",
            True
        ),
        Task(
            "study",
            "read a textbook",
            4,
            3,
            2,
            5,
            "2024-12-31 23:59:59",
            "2024-02-10 10:00:00",
            "2024-02-10 12:00:00",
            True
        ),
        Task(
            "exercise",
            "go for a run",
            3,
            2,
            1,
            4,
            "2024-12-31 23:59:59",
            "2024-02-10 14:00:00",
            "2024-02-10 15:00:00",
            True
        ),
        Task(
            "cooking",
            "try a new recipe",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-10 16:00:00",
            "2024-02-10 17:00:00",
            True
        ),
        Task(
            "shopping",
            "buy new clothes",
            4,
            3,
            2,
            4,
            "2024-12-31 23:59:59",
            "2024-02-11 09:00:00",
            "2024-02-11 11:00:00",
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
            "2024-02-11 14:00:00",
            "2024-02-11 17:00:00",
            True
        ),
        Task(
            "gardening",
            "trim the hedges",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-12 10:00:00",
            "2024-02-12 11:30:00",
            True
        ),
        Task(
            "meeting",
            "team meeting",
            6,
            5,
            1,
            7,
            "2024-12-31 23:59:59",
            "2024-02-12 14:00:00",
            "2024-02-12 15:00:00",
            True
        ),
        Task(
            "reading",
            "read a novel",
            4,
            3,
            2,
            5,
            "2024-12-31 23:59:59",
            "2024-02-12 16:00:00",
            "2024-02-12 18:00:00",
            True
        ),
        Task(
            "study",
            "prepare for a presentation",
            5,
            4,
            3,
            6,
            "2024-12-31 23:59:59",
            "2024-02-13 09:00:00",
            "2024-02-13 12:00:00",
            True
        ),
        Task(
            "exercise",
            "30 minutes of cardio",
            3,
            2,
            1,
            4,
            "2024-12-31 23:59:59",
            "2024-02-13 14:00:00",
            "2024-02-13 15:00:00",
            True
        ),
        Task(
            "cooking",
            "try a new recipe",
            2,
            1,
            1,
            2,
            "2024-12-31 23:59:59",
            "2024-02-01 16:00:00",
            "2024-02-13 17:00:00",
            True
        ),
        Task(
            "shopping",
            "buy groceries",
            3,
            2,
            1.5,
            3,
            "2024-12-31 23:59:59",
            "2024-02-01 09:00:00",
            "2024-02-14 10:30:00",
            True
        )
    ]
    calendar = Calendar()
    calendar.addTask(tasks)

    # Display tasks for a specific day
    # calendar.displayDailyTasks(month=2, day=1)  # Example: Display tasks for January 31st
    # calendar.displayYearlyCalendar()  # Display the yearly calendar
    calendar.displayMonthlyCalendar(month=2)  # Example: Display tasks for February
    print(calendar.calendar[1])
    calendar.removeTask('exercise')  # Remove the first task
    print(calendar.calendar[1])
    calendar.displayMonthlyCalendar(month=2)  # Display tasks for February after removing the first task
    
if __name__ == "__main__":
    main()


def advanceTime(self, gameState):
    # Tracks updated beliefs after one time step
    updatedBeliefs = util.Counter()

    # Loop through all prior positions with non-zero belief
    for priorPosition in self.legalPositions:
        if self.beliefs[priorPosition] > 0:
            # Get the distribution over possible new positions for the ghost
            potentialNewPositionDist = self.getPositionDistribution(self.setGhostPosition(gameState, priorPosition))

            # Update beliefs for each possible new position
            for newPosition, transitionProbability in potentialNewPositionDist.items():
                updatedBeliefs[newPosition] += self.beliefs[priorPosition] * transitionProbability

    # Normalize the updated beliefs and apply them to the class's beliefs
    updatedBeliefs.normalize()
    self.beliefs = updatedBeliefs
