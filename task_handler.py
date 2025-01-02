from task import Task
from timestamp import Timestamp
import json

class TaskHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_tasks(self):
        try:
            with open(self.file_path, 'r') as file:
                tasks = json.load(file)
                loaded_tasks = []
                for task in tasks:
                    loaded_task = Task.from_dict(task)
                    #take care of id, completed, and weightage attributes since they werent in from_dict
                    loaded_task.id = task['id']
                    loaded_task.completed = task['completed']
                    loaded_task.weightage = task['weightage']
                    loaded_tasks.append(loaded_task)
                return loaded_tasks
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_tasks(self, tasks):
        with open(self.file_path, 'w') as file:
            file.truncate(0)  #empty file
            task_dicts = []
            for task in tasks:
                task_dicts.append(task.to_dict())
            json.dump(task_dicts, file, indent=4)