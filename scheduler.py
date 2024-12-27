from task import Task
from my_calendar import Calendar

class Scheduler:
    calendar = Calendar()
    written = false

    def __init__(self):
        #initialize task list
        self.tasks = []

    def add_task(self, name, description, priority, difficulty, duration, score, deadline, 
                 start_time, end_time, delayable, recurring):
        #task dictionary with all relevant factors
        
        task = Task(name, description, priority, difficulty, duration, score, deadline, start_time, end_time, delayable, recurring)
        task.calculate_weightage()
        self.tasks.append(task)
        st = start_time
        if recurring == "d" or recurring == "daily":
            while st < start_time.addMinutes(10080):
                task = Task(name, description, priority, difficulty, duration, score, deadline, st, st.addMinutes(duration * 60), delayable, recurring)
                task.calculate_weightage()
                self.tasks.append(task)
                st = st.addMinutes(1440)
        elif recurring == "w" or recurring == "weekly":
            while st < start_time.addMinutes(43830):
                task = Task(name, description, priority, difficulty, duration, score, deadline, st, st.addMinutes(duration * 60), delayable, recurring)
                task.calculate_weightage()
                self.tasks.append(task)
                st = st.addMinutes(10080)
        elif recurring == "m" or recurring == "monthly":
            while st < start_time.addMinutes(525600):
                task = Task(name, description, priority, difficulty, duration, score, deadline, st, st.addMinutes(duration * 60), delayable, recurring)
                task.calculate_weightage()
                self.tasks.append(task)
                st = st.addMinutes(43830)

    def place_task(self, task):
        month = task.start_time.month - 1
        day = task.start_time.day - 1

        tasks_on_day = self.calendar[month][day]

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

                conflicting_task = self.place_task(task)
                while conflicting_task is not None:
                    # Push the conflicting task forward
                    task.start_time = conflicting_task.end_time.addMinutes(5)
                    task.end_time = start_time.addMinutes(task.duration * 60)
                    conflicting_task = self.place_task(task)



            # Resolve conflicts iteratively


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