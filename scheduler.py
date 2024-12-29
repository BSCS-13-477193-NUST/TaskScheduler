from task import Task
from my_calendar import Calendar
from timestamp import Timestamp
from task_handler import TaskHandler

class Scheduler:
    calendar = Calendar()
    battery = 100
    task_handler = TaskHandler("tasks.json")

    def __init__(self):
        #initialize task list
        self.tasks = self.task_handler.load_tasks()

    def add_task(self, name, description, priority, difficulty, duration, fuel_cost, deadline, 
                 start_time, end_time, delayable, recurring, repeat):
        st = start_time
        d = deadline
        for i in range(repeat):
            task = Task(name, description, priority, difficulty, duration, fuel_cost, d, st, st.addMinutes(duration * 60), delayable, recurring, repeat)
            task.calculate_weightage()
            self.tasks.append(task)
            if recurring == "d":
                st = st.addDays(1)
                d = d.addDays(1)
            elif recurring == "w":
                st = st.addDays(7)
                d = d.addDays(7)
            elif recurring == "m":
                st = st.addMonths(1)
                d = d.addMonths(1)

    def remove_task(self, task):
        self.tasks.remove(task)
        self.task_handler.save_tasks(self.tasks)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
            
    def place_task(self, task):
        month = task.start_time.month - 1
        day = task.start_time.day - 1

        tasks_on_day = self.calendar.calendar[month][day]
        for existing_task in tasks_on_day:
            if (existing_task.start_time.isBefore(task.start_time) and task.start_time.isBefore(existing_task.end_time)) or \
               (existing_task.start_time.isBefore(task.end_time) and task.end_time.isBefore(existing_task.end_time)) or \
               (task.start_time.isBefore(existing_task.start_time) and existing_task.start_time.isBefore(task.end_time)) or \
               (task.start_time.isBefore(existing_task.end_time) and existing_task.end_time.isBefore(task.end_time)):
                return existing_task

        return None

    def solve_schedule(self):
        absolute_tasks = []
        unabsolute_tasks = []

        current_time = Timestamp.getCurrentTimestamp()

        for task in self.tasks:
            if task.completed:
                self.tasks.remove(task)
                continue
            if task.delayable:
                unabsolute_tasks.append(task)
            else:
                absolute_tasks.append(task)
        
        #sort both lists by weightage (descending)
        absolute_tasks.sort(key=lambda x: x.weightage, reverse=True)
        unabsolute_tasks.sort(key=lambda x: x.weightage, reverse=True)

        for task in absolute_tasks: #strict constraints
            if task.end_time.isBefore(current_time):
                self.tasks.remove(task)
                continue
            elif task.start_time.isBefore(current_time) and current_time.isBefore(task.end_time):
                task.start_time = current_time
                task.duration = current_time.addMinutes(task.end_time.getMinutesLeft())
            else:
                #check if task conflicts with an existing task
                conflicting_task = self.place_task(task)
                if conflicting_task is not None:
                    #if task conflicts, still add task but with a shortened duration but still within same time
                    task.duration = task.start_time.addMinutes(conflicting_task.start_time.getMinutesLeft())
                    continue
            


        for task in unabsolute_tasks: #dynamic constraints
            # For delayable tasks, start from the later of current time or original start time
            if current_time.isBefore(task.start_time):
                task.start_time = task.start_time
            else:
                task.start_time = current_time
            task.end_time = task.start_time.addMinutes(task.duration * 60)

            conflicting_task = self.place_task(task)
            while conflicting_task is not None:
                # Push the conflicting task forward
                task.start_time = conflicting_task.end_time.addMinutes(5)
                task.end_time = task.start_time.addMinutes(task.duration * 60)
                conflicting_task = self.place_task(task)

            current_time = task.end_time.addMinutes(5)
        self.calendar.addTask(self.tasks)
        self.task_handler.save_tasks(self.tasks)

    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.\n")
            return

        for task in self.tasks:
            print(task)
            print()
