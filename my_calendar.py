from task import Task
import matplotlib.pyplot as plt

class Calendar:
    calendar = [[[] for _ in range(31)] for _ in range(12)]
        

    def addTask(self):
        # title = input("Enter title: ")
        # description = input("Describe the task: ")
        # priority = int(input("Enter priority (1-10): "))
        # difficulty = int(input("Enter difficulty (1-10): "))
        # duration = float(input("how long does it take to do the task? "))
        # fuel_cost = float(input("On a scale of 1-10 how much energy does it take?\n With 0 being no energy(you feel good after doing it)\n and 10 being a lot of energy(you feel tired after doing it) "))
        # deadline = input("Enter deadline of the task (YYYY-MM-DD HH:MM:SS): ")
        # start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
        # end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
        # delayable = input("Is the task delayable? (True/False): ")
        # delayable = True if delayable == "True" else False

        #trial tasks to see if the thing works ;p
        tasks = [
            Task(
            title="quran",
            description="i have to revise and then recite it to mama as well",
            priority=7,
            difficulty=6,
            duration=2,
            fuel_cost=7,
            deadline="2024-12-31 23:59:59",
            start_time="2024-01-31 21:59:59",
            end_time="2024-12-31 23:59:59",
            delayable=False
            ),
            Task(
            title="exercise",
            description="30 minutes of cardio",
            priority=5,
            difficulty=4,
            duration=0.5,
            fuel_cost=6,
            deadline="2024-12-31 23:59:59",
            start_time="2024-02-01 08:00:00",
            end_time="2024-02-01 08:30:00",
            delayable=True
            ),
            Task(
            title="meeting",
            description="team meeting",
            priority=8,
            difficulty=3,
            duration=1,
            fuel_cost=5,
            deadline="2024-12-31 23:59:59",
            start_time="2024-02-05 10:00:00",
            end_time="2024-02-05 11:00:00",
            delayable=True
            ),
            Task(
            title="shopping",
            description="grocery shopping",
            priority=4,
            difficulty=2,
            duration=2,
            fuel_cost=3,
            deadline="2024-12-31 23:59:59",
            start_time="2024-12-03 15:00:00",
            end_time="2024-02-03 17:00:00",
            delayable=True
            ),
            Task(
            title="study",
            description="study for exam",
            priority=9,
            difficulty=7,
            duration=3,
            fuel_cost=8,
            deadline="2024-12-31 23:59:59",
            start_time="2024-02-04 18:00:00",
            end_time="2024-02-04 21:00:00",
            delayable=True
            )
        ]

        for task in tasks:
            start_month = int(task.start_time.split("-")[1])
            start_day = int(task.start_time.split("-")[2].split(" ")[0])
            self.calendar[start_month-1][start_day-1].append(task)
        print("Tasks added successfully!\n")
    
    def printCalendar(self):
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

        for month in range(12):
            for day in range(31):
                tasks = self.calendar[month][day]
                if tasks:
                    task_priorities = [task.priority for task in tasks]
                    color = "red" if max(task_priorities) >= 7 else "blue"
                    ax.scatter(day, month, color=color, s=100)

        plt.show()

        

def main():
    calendar = Calendar()
    calendar.addTask()
    print("Calendar:")
    calendar.printCalendar()
if __name__ == "__main__":
    main()