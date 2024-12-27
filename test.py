from constraint import Problem
from datetime import datetime, timedelta


class Task:
    def __init__(self, name, priority, duration, deadline, delayable, weightage=0):
        self.name = name
        self.priority = priority
        self.duration = duration  # Duration in minutes
        self.deadline = deadline  # Deadline as a datetime object
        self.delayable = delayable
        self.weightage = weightage
        self.start_time = None
        self.end_time = None

    def __str__(self):
        return f"Task({self.name}, Priority: {self.priority}, Duration: {self.duration}, " \
               f"Deadline: {self.deadline}, Delayable: {self.delayable})"


class SchedulerCSP:
    def __init__(self):
        self.tasks = []
        self.problem = Problem()

    def add_task(self, task: Task):
        self.tasks.append(task)

    def solve_schedule(self):
        # Define variables and domains
        for task in self.tasks:
            # Define the domain for each task's start time
            if task.delayable:
                start_time_domain = [
                    task.deadline - timedelta(minutes=task.duration * i)
                    for i in range((task.deadline - datetime.now()).seconds // 60)
                ]
            else:
                # Non-delayable tasks have a fixed start time domain
                start_time_domain = [datetime.now()]
            
            # Add the task and its domain to the CSP
            self.problem.addVariable(task.name, start_time_domain)

        # Define constraints
        def no_overlap(t1_start, t2_start, t1_duration, t2_duration):
            t1_end = t1_start + timedelta(minutes=t1_duration)
            t2_end = t2_start + timedelta(minutes=t2_duration)
            return t1_end <= t2_start or t2_end <= t1_start

        # Add pairwise no-overlap constraints
        for i, task1 in enumerate(self.tasks):
            for j, task2 in enumerate(self.tasks):
                if i != j:
                    self.problem.addConstraint(
                        lambda t1_start, t2_start, t1=task1, t2=task2: 
                        no_overlap(t1_start, t2_start, t1.duration, t2.duration),
                        (task1.name, task2.name)
                    )

        # Add deadline constraints
        for task in self.tasks:
            self.problem.addConstraint(
                lambda start_time, t=task: start_time + timedelta(minutes=t.duration) <= t.deadline,
                (task.name,)
            )

        # Solve the CSP
        solution = self.problem.getSolution()
        if solution:
            for task in self.tasks:
                task.start_time = solution[task.name]
                task.end_time = task.start_time + timedelta(minutes=task.duration)
            return True
        return False

    def display_schedule(self):
        if not self.tasks:
            print("No tasks to schedule.")
            return

        for task in self.tasks:
            print(f"Task: {task.name}")
            print(f"  Start Time: {task.start_time}")
            print(f"  End Time: {task.end_time}")
            print()


# Example usage
if __name__ == "__main__":
    scheduler = SchedulerCSP()

    # Example tasks
    task1 = Task("Task1", priority=5, duration=30, deadline=datetime.now() + timedelta(hours=2), delayable=False)
    task2 = Task("Task2", priority=3, duration=60, deadline=datetime.now() + timedelta(hours=3), delayable=True)
    task3 = Task("Task3", priority=1, duration=45, deadline=datetime.now() + timedelta(hours=4), delayable=True)

    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)

    if scheduler.solve_schedule():
        scheduler.display_schedule()
    else:
        print("No valid schedule found.")