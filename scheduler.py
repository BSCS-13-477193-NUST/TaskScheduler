from task import Task
from my_calendar import Calendar

class Scheduler:
    calendar = Calendar()
    written = false

    def __init__(self):
        #initialize task list
        self.tasks = []

    def add_task(self, name, description, priority, difficulty, duration, score, deadline_importance, 
                 start_time, end_time, delayable):
        #task dictionary with all relevant factors
        task = Task(name, description, priority, difficulty, duration, score, deadline_importance, start_time, end_time, delayable)
        task.calculate_weightage()
        self.tasks.append(task)


    def solve_schedule(self):
        # Calculate weightage for each task
        for task in self.tasks:
            task.calculate_weightage()

        # Sort tasks by weightage in descending order
        self.tasks.sort(key=lambda x: x.weightage, reverse=True)

        current_time = Timestamp.getCurrentTimestamp()

        for task in self.tasks:
            task.start_time = current_time
            task.end_time = task.start_time.addMinutes(task.duration * 60)
            task.completed = True
            self.calendar.add_tasks(task)
            current_time = task.end_time  # Update current time to the end time of the last scheduled task

    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.\n")
            return

        for i, task in enumerate(self.tasks, 1):
            print(f"Task {i}:")
            for task in self.tasks:
                print()
                print(task)
                
            print()