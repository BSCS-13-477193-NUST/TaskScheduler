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
        #----in development-------
        # Calculate weightage for each task
        for task in self.tasks:
            task.calculate_weightage()

        # Sort tasks by weightage in descending order
        self.tasks.sort(key=lambda x: x.weightage, reverse=True)

        current_time = Timestamp.getCurrentTimestamp()

        for task in self.tasks:
            if task.completed:
                continue
            if not task.delayable:
                if task.start_time < current_time:
                    if task.end_time > current_time:
                        task.start_time = current_time
                        task.duration = task.end_time.getDifference(current_time) / 60.0

                      
            else: #task is delayable

                if task.start_time < current_time:
                    task.start_time = current_time
            if self.calendar.is_conflict(task.start_time, task.end_time):
            
            task.end_time = task.start_time.addMinutes(task.duration * 60)
            
            self.calendar.add_tasks(task)
            current_time = task.end_time.addMinutes(5)  # Update current time to the end time of the last scheduled task

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