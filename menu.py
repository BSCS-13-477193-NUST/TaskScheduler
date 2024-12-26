from scheduler import Scheduler
from timestamp import Timestamp

def parseString(text) -> 'Timestamp':
    #(YYYY-MM-DD HH:MM)
    parts = text.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2][:2])
    
    parts = parts[3].split(':')
    hour = int(parts[0])
    minute = int(parts[1])
    #validation checks
    if year < 2024 or month < 1 or month > 12 or day < 1 or day > 31 or hour < 0 or hour > 23 or minute < 0 or minute > 59:
        print("Invalid date/time format. Please try again.")
        return None
    return Timestamp(minute, hour, day, month, year)

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
            
            deadline = if parseString(input("Enter deadline (YYYY-MM-DD HH:MM): ")) == None:
                continue

            start_time = if parseString(input("Enter deadline (YYYY-MM-DD HH:MM): ")) == None:
                continue

            end_time = if parseString(input("Enter deadline (YYYY-MM-DD HH:MM): ")) == None:
                continue
 
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