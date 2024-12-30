from task import Task
from my_calendar import Calendar
from timestamp import Timestamp
from task_handler import TaskHandler
import copy

class Scheduler:
    calendar = Calendar()
    battery = 100
    task_handler = TaskHandler("tasks.json")

    def __init__(self):
        #initialize task list
        self.tasks = self.task_handler.load_tasks()

    def add_task(self, name, description, priority, difficulty, duration, deadline, 
                 start_time, end_time, delayable, recurring, repeat):
        st = start_time
        d = deadline
        for i in range(repeat):
            task = Task(name, description, priority, difficulty, duration, d, st, st.addMinutes(duration * 60), delayable, recurring, repeat)
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
            
    def check_conflicts(self, task):
        month = task.start_time.month - 1
        day = task.start_time.day - 1

        tasks_on_day = self.calendar.calendar[month][day]
        for existing_task in tasks_on_day:
            #constraint: task cannot overlap with another task
            if (existing_task.start_time.isBefore(task.start_time) and task.start_time.isBefore(existing_task.end_time)) or \
               (existing_task.start_time.isBefore(task.end_time) and task.end_time.isBefore(existing_task.end_time)) or \
               (task.start_time.isBefore(existing_task.start_time) and existing_task.start_time.isBefore(task.end_time)) or \
               (task.start_time.isBefore(existing_task.end_time) and existing_task.end_time.isBefore(task.end_time)):
                return existing_task
        return None

    #recursive function to ensure absolute task is assigned appropriate time
    def place_absolute_task(self, task, tasks):
        current_time = Timestamp.getCurrentTimestamp()
        if task.end_time.isBefore(current_time): #if task is already over, remove it
            tasks.remove(task)
            return
        elif task.start_time.isBefore(current_time) and current_time.isBefore(task.end_time): #if task is ongoing, set start time to current time
            task.start_time = current_time.addMinutes(1)
            task.duration = task.end_time.getDifference(task.start_time) / 60
            self.place_absolute_task(task, tasks)
        else:
            #check if task conflicts with an existing task
            conflicting_task = self.check_conflicts(task)
            while conflicting_task is not None:
                #if task conflicts, still add task but with a shortened duration but still within same time
                if task.end_time.isBefore(conflicting_task.end_time):
                    if task.start_time.isBefore(conflicting_task.start_time): #case 3
                        task.end_time = conflicting_task.start_time.addMinutes(1)
                        task.duration = task.end_time.getDifference(task.start_time) / 60
                        self.place_absolute_task(task, tasks)
                    else: #case 1
                        tasks.remove(task)
                        return None
                elif conflicting_task.end_time.isBefore(task.end_time):
                    if task.start_time.isBefore(conflicting_task.start_time): #case 4
                        task2 = copy.deepcopy(task)
                        task2.end_time = conflicting_task.start_time.addMinutes(1)
                        task2.duration = task2.end_time.getDifference(task2.start_time) / 60
                        task2.id = Task.i
                        Task.i += 1

                        task.start_time = conflicting_task.end_time.addMinutes(1)
                        task.duration = task.end_time.getDifference(task.start_time) / 60

                        tasks.append(task2)
                        self.place_absolute_task(task, tasks)
                        self.place_absolute_task(task2, tasks)

                    else: #case 2
                        task.start_time = conflicting_task.end_time.addMinutes(1)
                        task.duration = task.end_time.getDifference(task.start_time) / 60
                        self.place_absolute_task(task, tasks)

    #recursive function to ensure unabsolute task is properly assigned time
    def place_unabsolute_task(self, task, tasks):
        current_time = Timestamp.getCurrentTimestamp()
        if task.deadline.isBefore(current_time):  # if task is already over, remove it
            tasks.remove(task)
            return
        if task.start_time.isBefore(current_time):  # if task is ongoing, set start time to current time
            task.start_time = current_time.addMinutes(1)
            task.duration = task.end_time.getDifference(task.start_time) / 60
            self.place_unabsolute_task(task, tasks)
        else:
            # Ensure the task does not start before the original start time
            if current_time.isBefore(task.start_time):
                task.start_time = task.start_time
            else:
                task.start_time = current_time
                #ensure task does not start before original start time
                if current_time.isBefore(task.start_time):
                    task.start_time = task.start_time
                else:
                    task.start_time = current_time

            # Ensure the task does not end after the deadline
            task.end_time = min(task.start_time.addMinutes(task.duration * 60), task.deadline)

            # Check if task conflicts with an existing task
            conflicting_task = self.check_conflicts(task)
            while conflicting_task is not None:
                # Push the conflicting task forward
                task.start_time = conflicting_task.end_time.addMinutes(5)
                task.end_time = min(task.start_time.addMinutes(task.duration * 60), task.deadline)

                # If the task cannot be completed before the deadline, remove it
                if task.end_time.isAfter(task.deadline):
                    tasks.remove(task)
                    return

                conflicting_task = self.check_conflicts(task)

            tasks.append(task)


    def solve_schedule(self): #------------------- in development ---------------------------
        absolute_tasks = []
        unabsolute_tasks = []

        self.calendar.clearCalendar() #clear calendar

        for task in self.tasks:
            if task.completed: #remove if completed
                self.tasks.remove(task)
                continue
            if task.delayable:
                unabsolute_tasks.append(task)
            else:
                absolute_tasks.append(task)
        
        #sort both lists by weightage (descending)
        absolute_tasks.sort(key=lambda x: x.weightage, reverse=True) #constraint: weightage
        unabsolute_tasks.sort(key=lambda x: x.weightage, reverse=True) #constraint: weightage

        for task in absolute_tasks: #strict constraints
            self.place_absolute_task(task, absolute_tasks)
        self.calendar.addTasks(absolute_tasks)

                    
        for task in unabsolute_tasks: #dynamic constraints
            # For delayable tasks, start from the later of current time or original start time
            if current_time.isBefore(task.start_time):
                task.start_time = task.start_time
            else:
                task.start_time = current_time
            task.end_time = task.start_time.addMinutes(task.duration * 60)

            conflicting_task = self.check_conflicts(task)
            while conflicting_task is not None:
                # Push the conflicting task forward
                task.start_time = conflicting_task.end_time.addMinutes(5)
                task.end_time = task.start_time.addMinutes(task.duration * 60)
                conflicting_task = self.check_conflicts(task)

            current_time = task.end_time.addMinutes(5)
        #merge both arrays in self.tasks
        self.tasks = absolute_tasks + unabsolute_tasks
        self.task_handler.save_tasks(self.tasks)
        self.calendar.addTasks(self.tasks)


    def display_tasks(self):
        if not self.tasks:
            print("No tasks to display.\n")
            return

        for task in self.tasks:
            print(task)
            print()