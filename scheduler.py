from task import Task

class Scheduler:

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
        #calculate weightage for each task
        for task in self.tasks:
            task.calculate_weightage()

        #sort tasks by weightage in descending order
        self.tasks.sort(key=lambda x: x.weightage, reverse=True)

        # print("\nScheduled Tasks (sorted by weightage):")
        # for i, task in enumerate(self.tasks, 1):
        #     print(f"{i}. {task.name} - Weightage: {task.weightage:.2f}, Duration: {task.duration} hours")

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