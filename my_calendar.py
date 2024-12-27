from task import Task
import matplotlib.pyplot as plt

class Calendar:
    calendar = [[[] for _ in range(31)] for _ in range(12)]
        

    def addTask(self, tasks):
       
        #trial tasks to see if the thing works ;p
        

        for task_data in tasks:
            task = Task(
            task_data["title"],
            task_data["description"],
            task_data["priority"],
            task_data["difficulty"],
            task_data["duration"],
            task_data["fuel_cost"],
            task_data["deadline"],
            task_data["start_time"],
            task_data["end_time"],
            task_data["absolute"]
            )
            start_month = int(task_data["start_time"].split("-")[1])
            start_day = int(task_data["start_time"].split("-")[2].split(" ")[0])
            
            self.calendar[start_month-1][start_day-1].append(task)
        print("Tasks added successfully!\n")
    
    def displayYearCalendar(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_title("Task Calendar")
        ax.set_xlabel("Day")
        ax.set_ylabel("Month")
        ax.set_xticks(range(31))
        ax.set_yticks(range(12))
        ax.set_xticklabels(range(1, 32))
        ax.set_yticklabels([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])

        def get_color(task_count):
            # Base skin tone color (light skin tone) in hex
            base_hex = "#add8e6"
            
            # Convert the base hex color to RGB
            r = int(base_hex[1:3], 16)
            g = int(base_hex[3:5], 16)
            b = int(base_hex[5:7], 16)
            
            # Scale the color based on task count (e.g., make the color darker as task_count increases)
            scale_factor = 1 - (task_count / 7)  # Adjust scaling factor to control how dark the color gets
            
            # Ensure scaling factor is in the range [0, 1] and scale the RGB values
            r = max(int(r * scale_factor), 0)
            g = max(int(g * scale_factor), 0)
            b = max(int(b * scale_factor), 0)
            
            # Convert the adjusted RGB values back to hex
            new_color = f"#{r:02x}{g:02x}{b:02x}"
            return new_color

        for month in range(12):
            for day in range(31):
                tasks = self.calendar[month][day]
                if tasks:
                    # Calculate the number of tasks for the day
                    task_count = len(tasks)
                    # Assign red color if the number of tasks is high (e.g., >= 5), else blue
                    color = get_color(task_count)

                    ax.scatter(day, month, color=color, s=100)

        plt.show()

        

def main():

    tasks = [
            {
                "title": "quran",
                "description": "i have to revise and then recite it to mama as well",
                "priority": 7,
                "difficulty": 6,
                "duration": 2,
                "fuel_cost": 7,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 21:59:59",
                "end_time": "2024-12-31 23:59:59",
                "absolute": False
            },
            {
                "title": "exercise",
                "description": "30 minutes of cardio",
                "priority": 5,
                "difficulty": 4,
                "duration": 0.5,
                "fuel_cost": 6,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 08:00:00",
                "end_time": "2024-02-01 08:30:00",
                "absolute": True
            },
            {
                "title": "meeting",
                "description": "team meeting",
                "priority": 8,
                "difficulty": 3,
                "duration": 1,
                "fuel_cost": 5,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 10:00:00",
                "end_time": "2024-02-02 11:00:00",
                "absolute": True
            },
            {
                "title": "shopping",
                "description": "grocery shopping",
                "priority": 4,
                "difficulty": 2,
                "duration": 2,
                "fuel_cost": 3,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-03 15:00:00",
                "end_time": "2024-02-03 17:00:00",
                "absolute": True
            },
            {
                "title": "study",
                "description": "study for exam",
                "priority": 9,
                "difficulty": 7,
                "duration": 3,
                "fuel_cost": 8,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-03 18:00:00",
                "end_time": "2024-02-04 21:00:00",
                "absolute": True
            },
            {
                "title": "coding",
                "description": "work on a coding project",
                "priority": 6,
                "difficulty": 5,
                "duration": 2,
                "fuel_cost": 4,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-03 14:00:00",
                "end_time": "2024-02-01 16:00:00",
                "absolute": True
            },
            {
                "title": "reading",
                "description": "read a book",
                "priority": 3,
                "difficulty": 2,
                "duration": 1.5,
                "fuel_cost": 2,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-01-31 18:00:00",
                "end_time": "2024-02-01 19:30:00",
                "absolute": True
            },
            {
                "title": "cooking",
                "description": "prepare dinner",
                "priority": 2,
                "difficulty": 1,
                "duration": 1,
                "fuel_cost": 1,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-02-02 19:00:00",
                "end_time": "2024-02-01 20:00:00",
                "absolute": True
            },
            {
                "title": "meditation",
                "description": "practice mindfulness",
                "priority": 1,
                "difficulty": 1,
                "duration": 0.5,
                "fuel_cost": 1,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-11-31 20:30:00",
                "end_time": "2024-02-01 21:00:00",
                "absolute": True
            },
            {
                "title": "project",
                "description": "work on a project",
                "priority": 7,
                "difficulty": 6,
                "duration": 4,
                "fuel_cost": 7,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-03-01 10:00:00",
                "end_time": "2024-03-05 14:00:00",
                "absolute": True
            },
            {
                "title": "cleaning",
                "description": "clean the house",
                "priority": 5,
                "difficulty": 4,
                "duration": 3,
                "fuel_cost": 6,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-03-10 09:00:00",
                "end_time": "2024-03-10 12:00:00",
                "absolute": True
            },
            {
                "title": "gardening",
                "description": "take care of the garden",
                "priority": 6,
                "difficulty": 5,
                "duration": 2,
                "fuel_cost": 4,
                "deadline": "2024-12-31 23:59:59",
                "start_time": "2024-03-15 14:00:00",
                "end_time": "2024-03-15 16:00:00",
                "absolute": True
            }
        ]

    calendar = Calendar()
    calendar.addTask(tasks)
    print("Calendar:")
    calendar.displayYearCalendar()
if __name__ == "__main__":
    main()