from scheduler import Scheduler
from timestamp import Timestamp
from my_calendar import Calendar

def getDate(text) -> 'Timestamp':
    temp = Timestamp.getCurrentTimestamp()
    if text == "now":
        return temp
    try:
        if '-' not in text:
            #time only format (HH:MM)
            parts = text.split(':')
            hour = int(parts[0])
            minute = int(parts[1])
            day = temp.day
            month = temp.month
            year = temp.year
        elif ':' not in text:
            #date only format (YYYY-MM-DD)
            parts = text.split('-')
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2][:2])
            minute = 59
            hour = 23
        else:
            #date and time format (YYYY-MM-DD HH:MM)
            parts = text.split('-')
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2][:2])
            parts = parts[2][2:].split(':')
            hour = int(parts[0])
            minute = int(parts[1])
    except ValueError or IndexError:
        print("Invalid date/time format. Please try again.")
        return None
    #validation check
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
        print("4. Display Calendar")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                priority = int(input("Enter priority level (1-10): "))
                difficulty = int(input("Enter difficulty level (1-10): "))
                duration = float(input("Enter task duration in hours: "))
                score = float(input("Enter task score (1-10): "))
                
                deadline = getDate(input("Enter deadline (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                if deadline is None:
                    continue
            
                start_time = getDate(input("Enter start time (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                if start_time is None:
                    continue

            except ValueError:
                print("Invalid input. Please try again.")
                continue

            delayable_input = input("Is task delayable? (y/n): ")
            if delayable_input == "y":
                delayable = True
            elif delayable_input == "n":
                delayable = False
            else:
                print("Invalid input. Task will be considered delayable by default.")
                delayable = True

            repeat = 1
            r_input = input("Is task recurring? (y/n): ")
            if r_input == "y":
                recurring = ""
                while recurring != "d" and recurring != "w" and recurring != "m":
                    recurring = input("Enter recurring interval (daily (d), weekly (w), monthly (m)): ")
                    if recurring != "d" and recurring != "w" and recurring != "m":
                        print("Invalid input. Please try again.")
                repeat = int(input("How many times should the task repeat? >"))


                
            elif recurring_input == "n":
                recurring = ""
            else:
                print("Invalid input. Task will be considered non-recurring by default.")
                recurring = ""

            scheduler.add_task(name, description, priority, difficulty, duration, score, 
                               deadline, start_time, start_time.addMinutes(duration*60), delayable, recurring, repeat)
            
            print("Task added successfully!\n")

        elif choice == "2":
            scheduler.display_tasks()

        elif choice == "3":
            scheduler.solve_schedule()

        elif choice == "4":
            if not scheduler.tasks:
                print("No tasks to display.\n")
                continue
            if not scheduler.written:
                print("Optimising schedule...")
                scheduler.solve_schedule()
                scheduler.written = true
            print("Displaying calendar...")
            scheduler.calendar.printCalendar()
        elif choice == "5":
            print("Exiting the Task Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    menu()