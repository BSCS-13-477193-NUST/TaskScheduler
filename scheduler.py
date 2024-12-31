from task import Task
from my_calendar import Calendar
from timestamp import Timestamp
from task_handler import TaskHandler
import copy

class Scheduler:
    calendar = Calendar()
    battery = 100
    task_handler = TaskHandler("tasks.json")
    absolute_tasks = []
    unabsolute_tasks = []

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

    def remove_task(self, taskID):
        self.tasks = [task for task in self.tasks if task.id != taskID]
        self.task_handler.save_tasks(self.tasks)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_task_index(self, task_id):
        for i in range(len(self.tasks)):
            if self.tasks[i].id == task_id:
                return i
        return None
            
    def check_conflicts(self, task):
        month = task.start_time.month - 1
        day = task.start_time.day - 1

        tasks_on_day = self.calendar.calendar[month][day]
        for existing_task in tasks_on_day:
            #constraint: task cannot overlap with another task
            if (existing_task.start_time <= task.start_time < existing_task.end_time) or \
               (existing_task.start_time < task.end_time <= existing_task.end_time) or \
               (task.start_time <= existing_task.start_time < task.end_time) or \
               (task.start_time < existing_task.end_time <= task.end_time):
                return existing_task
        return None

    #recursive function to ensure absolute task is assigned appropriate time
    def place_absolute_task(self, task):
        current_time = Timestamp.getCurrentTimestamp()
        if task.end_time <= current_time: #if task is already over, remove it
            return
        elif task.start_time < current_time < task.end_time: #if task is ongoing, set start time to current time
            task.start_time = current_time.addMinutes(1)
            task.duration = task.end_time.getDifference(task.start_time) / 60
            self.place_absolute_task(task)
        else:
            #check if task conflicts with an existing task
            print("in da else")
            conflicting_task = self.check_conflicts(task)
            if conflicting_task is not None:

                #if task conflicts, still add task but with a shortened duration but still within same time
                if task.end_time <= conflicting_task.end_time:
                    if task.start_time < conflicting_task.start_time: #case 3
                        task.end_time = conflicting_task.start_time
                        task.duration = task.end_time.getDifference(task.start_time) / 60
                        print("case 3")
                        self.place_absolute_task(task)
                    else: #case 1
                        print("case 1")
                        return
                elif conflicting_task.end_time < task.end_time:
                    if task.start_time <= conflicting_task.start_time: #case 4
                        #break case 4 into two tasks, case 2 and 3
                        
                        task2 = copy.deepcopy(task)
                        task2.end_time = conflicting_task.start_time.addMinutes(1)
                        task2.duration = task2.end_time.getDifference(task2.start_time) / 60
                        task2.title = task.title + " (1)"
                        task2.id  = Task.i
                        Task.i += 1

                        task.start_time = conflicting_task.end_time.addMinutes(1)
                        task.duration = task.end_time.getDifference(task.start_time) / 60
                        task.title = task.title + " (2)"

                        if task2.duration <= 1 or task.duration <= 1:
                            return
                        if conflicting_task.description == "night sleep": #if conflicting task is sleep, remove task
                            return

                        self.absolute_tasks.append(task2)
                        print(f"{task.title}: case 4")
                        self.place_absolute_task(task)
                        print("da break")
                        self.place_absolute_task(task2)

                    else: #case 2
                        task.start_time = conflicting_task.end_time.addMinutes(1)
                        task.duration = task.end_time.getDifference(task.start_time) / 60
                        print("case 2")
                        self.place_absolute_task(task)
            self.absolute_tasks.append(task)
            self.calendar.addTask(task)


    #recursive function to ensure unabsolute task is properly assigned time
    def place_unabsolute_task(self, task):
        if task is None:
            return
        current_time = Timestamp.getCurrentTimestamp()
        if task.deadline <= current_time:  # if task is already over, increase its weightage
            task.deadline = current_time.addMinutes(task.duration * 60)
            task.weightage += 3
        
        if task.start_time.addMinutes(task.duration * 60) >= task.deadline:  # if task should be ongoing, increase weightage slightly
            task.weightage += 2
        #check conflicts
        conflicting_task = self.check_conflicts(task)
        while conflicting_task is not None:
            #check if task should replace existing task
            if task.weightage > conflicting_task.weightage and conflicting_task.delayable:
                self.calendar.removeTask(conflicting_task.id)
                self.unabsolute_tasks.remove(conflicting_task)
                conflicting_task.start_time = task.end_time.addMinutes(3)
                conflicting_task.end_time = conflicting_task.start_time.addMinutes(conflicting_task.duration * 60)
                break
            task.start_time = conflicting_task.end_time.addMinutes(3)
            task.end_time = task.start_time.addMinutes(task.duration * 60)
            conflicting_task = self.check_conflicts(task)
        self.unabsolute_tasks.append(task)
        self.calendar.addTask(task)
        self.place_unabsolute_task(conflicting_task)

    def solve_schedule(self):
        self.absolute_tasks = []
        self.unabsolute_tasks = []

        self.calendar.clearCalendar() #clear calendar

        for task in self.tasks:
            if task.completed or task.duration <= 0: #remove if completed or duration is 0
                self.tasks.remove(task)
                continue
            if task.delayable:
                self.unabsolute_tasks.append(task)
            else:
                self.absolute_tasks.append(task)
        
        #sort both lists by weightage (descending)
        self.absolute_tasks.sort(key=lambda x: x.weightage, reverse=True) #constraint: weightage
        self.unabsolute_tasks.sort(key=lambda x: x.duration / (x.deadline.getDifference(x.start_time) / 60), reverse=True) #constraint: completionRatio

        absolute_tasks = copy.deepcopy(self.absolute_tasks)
        unabsolute_tasks = copy.deepcopy(self.unabsolute_tasks)

        self.absolute_tasks = []
        self.unabsolute_tasks = []

        for task in absolute_tasks: #strict constraints
            self.place_absolute_task(task)
                    
        for task in unabsolute_tasks: #dynamic constraints
            self.place_unabsolute_task(task)

        #merge both arrays in self.tasks
        self.tasks = self.absolute_tasks + self.unabsolute_tasks
        #sort self.tasks by start time
        self.tasks.sort(key=lambda x: x.start_time)
        self.task_handler.save_tasks(self.tasks)
        self.calendar.clearCalendar()
        for task in self.tasks:
            self.calendar.addTask(task)

    def set_sleep_schedule(self, start_time, duration):
        current_time = Timestamp.getCurrentTimestamp()
        for task in self.tasks:
            if task.description == "night sleep":
                self.remove_task(task)
        if duration <= 0:
            self.task_handler.save_tasks(self.tasks)
            return
        end_time = start_time.addMinutes(duration)
        self.add_task("Sleep", "night sleep", 0, 10, duration, end_time.addMinutes(1), start_time, end_time, False, "d", 365)
        self.task_handler.save_tasks(self.tasks)


    # def __init__(title:  description:priority:difficulty:                duration: float, deadline: Timestamp, start_time: Timestamp, end_time: Timestamp, delayable: bool, recurring: str, repeat: int) -> None:

    def display_tasks(self):
        #ask user which day tasks to display
        while True:
            try:
                print("Enter the date you want to display tasks for: ")
                month = int(input("Month (1-12): "))
                day = int(input("Day (1-31): "))
                if 1 <= month <= 12 and 1 <= day <= Timestamp.days_in_month[month]:
                    break
                else:
                    print(f"Invalid input. Please enter a valid month (1-12) and day (1-{Timestamp.days_in_month[month]}).")
            except (ValueError, KeyError):
                print("Invalid input. Please enter correct values for month and day.")

        tasks_on_day = self.task_handler.load_tasks()
        tasks_on_day = [task for task in tasks_on_day if task.start_time.month == month and task.start_time.day == day]
        if len(tasks_on_day) == 0:
            print("No tasks to display.\n")
            return

        print("📜 Tasks:")
        for task in tasks_on_day:
            #dont print sleep task
            if task.description == "night sleep":
                continue
            print(task)
            print()