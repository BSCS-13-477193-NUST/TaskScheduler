from task import Task
from my_calendar import Calendar
from timestamp import Timestamp
from task_handler import TaskHandler

class Scheduler:
    calendar = Calendar()
    written = False
    battery = 100
    task_handler = TaskHandler("tasks.json")
    mins = {
        "d": 1440,
        "w": 10080,
        "m": 43830,
        "" : 0
    }
    def __init__(self):
        #initialize task list
        self.tasks = self.task_handler.load_tasks()

    def add_task(self, name, description, priority, difficulty, duration, score, deadline, 
                 start_time, end_time, delayable, recurring, repeat):
        st = start_time
        d = deadline
        for i in range(repeat):
            task = Task(name, description, priority, difficulty, duration, score, d, st, st.addMinutes(duration * 60), delayable, recurring, repeat)
            task.calculate_weightage()
            self.tasks.append(task)
            self.task_handler.save_tasks(self.tasks)
            st = st.addMinutes(self.mins[recurring])
            d = d.addMinutes(self.mins[recurring])
            
    def place_task(self, task):
        month = task.start_time.month - 1
        day = task.start_time.day - 1

        tasks_on_day = self.calendar.calendar[month][day]
        for existing_task in tasks_on_day:
            if existing_task.start_time <= task.start_time < existing_task.end_time or \
                    existing_task.start_time < task.end_time <= existing_task.end_time or \
                    task.start_time <= existing_task.start_time < task.end_time or \
                    task.start_time < existing_task.end_time <= task.end_time:
                return existing_task

        return None

    def solve_schedule(self):
        # Sort tasks by weightage (descending order)
        self.tasks.sort(key=lambda x: x.weightage, reverse=True)

        # Get the current time
        current_time = Timestamp.getCurrentTimestamp()

        for task in self.tasks:
            # Skip completed tasks
            if task.completed:
                self.tasks.remove(task)
                continue

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

                conflicting_task = self.place_task(task)
                while conflicting_task is not None:
                    # Push the conflicting task forward
                    task.start_time = conflicting_task.end_time.addMinutes(5)
                    task.end_time = task.start_time.addMinutes(task.duration * 60)
                    conflicting_task = self.place_task(task)

            self.calendar.add_task(task)
            current_time = task.end_time.addMinutes(5)


    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.\n")
            return

        for task in self.tasks:
            print(task)
            print()