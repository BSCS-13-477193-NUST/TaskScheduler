from scheduler import Scheduler
from timestamp import Timestamp

def menu():
    scheduler = Scheduler()

    while True:
        print("\nTask Management System")
        print("1. Add Task")
        print("2. Display Tasks")
        print("3. Solve Schedule")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter task name: ")
            priority = int(input("Enter priority level (1-10): "))
            difficulty = int(input("Enter difficulty level (1-10): "))
            duration = float(input("Enter task duration in hours: "))
            score = float(input("Enter task score (1-10): "))
            
            deadline_input = input("Enter deadline (YYYY-MM-DD HH:MM): ")
            deadline = Timestamp(*deadline_parts)

            start_time_input = input("Enter start time (days:hours:minutes): ")
            start_time_parts = list(map(int, start_time_input.split(':')))
            start_time = Timestamp(*start_time_parts)

            end_time_input = input("Enter end time (days:hours:minutes): ")
            end_time_parts = list(map(int, end_time_input.split(':')))
            end_time = Timestamp(*end_time_parts)
 
            delayable = float(input("Enter delayable factor (1-10): "))

            scheduler.add_task(name, priority, difficulty, duration, score, 
                               deadline, start_time, end_time, delayable)
            print("Task added successfully!\n")

        elif choice == "2":
            scheduler.display_tasks()

        elif choice == "3":
            scheduler.solve_schedule()

        elif choice == "4":
            print("Exiting the Task Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    menu()