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
        """
        Schedules tasks by assigning start and end times, prioritizing tasks with higher weightage first.
        Resolves conflicts iteratively and ensures no overlapping tasks in the schedule.
        """
        # Sort tasks by weightage (descending order)
        self.tasks.sort(key=lambda x: x.weightage, reverse=True)

        # Get the current time
        current_time = Timestamp.getCurrentTimestamp()

        for task in self.tasks:
            # Skip completed tasks
            if task.completed:
                self.tasks.remove(task)
                continue

            # Set task start time based on whether it's delayable
            if not task.delayable:
                # For non-delayable tasks, ensure they are scheduled within their constraints
                if task.end_time < current_time:
                    # Task has already started and ended, skip it
                    self.tasks.remove(task)
                    continue
                elif task.start_time < current_time and task.end_time > current_time:
                    task.start_time = current_time
                    task.duration = current_time.addMinutes(getMinutesLeft(task.end_time))
            else:
                # For delayable tasks, start from the current time
                task.start_time = current_time
                task.end_time = task.start_time.addMinutes(task.duration * 60)

            # Resolve conflicts iteratively
            conflicting_task = self.place_task(task)
            while conflicting_task is not None:
                # Push the conflicting task forward
                task.start_time = conflicting_task.end_time.addMinutes(5)  # Add a buffer time
                task.end_time = task.start_time.addMinutes(task.duration * 60)
                conflicting_task = self.place_task(task)

            # Check for calendar conflicts
            while self.calendar.is_conflict(task.start_time, task.end_time):
                task.start_time = task.start_time.addMinutes(5)  # Increment start time to avoid conflict
                task.end_time = task.start_time.addMinutes(task.duration * 60)

            # Add the task to the calendar
            self.calendar.add_tasks(task)

            # Update the current time to the end of the scheduled task
            current_time = task.end_time.addMinutes(5)


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