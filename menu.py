from scheduler import Scheduler
from timestamp import Timestamp
from my_calendar import Calendar

def menu():
    scheduler = Scheduler()
    print(r"""
     __          ________ _      _____ ____  __  __ ______   _______ ____          
     \ \        / /  ____| |    / ____/ __ \|  \/  |  ____| |__   __/ __ \         
      \ \  /\  / /| |__  | |   | |   | |  | | \  / | |__       | | | |  | |        
       \ \/  \/ / |  __| | |   | |   | |  | | |\/| |  __|      | | | |  | |         _____   __   __
        \  /\  /  | |____| |___| |___| |__| | |  | | |____     | | | |__| |        |_   _| |  \ /  |
  _  __  \/  \/   |______|______\_____\____/|_|  |_|______|    |_|  \____/  __  __   | |   | | V | |
 | |/ /    /\        /\   |  \/  | |__   __|/\   |  \/  |   /\        /\   |  \/  |  |_|   |_|   |_|
 | ' /    /  \      /  \  | \  / |    | |  /  \  | \  / |  /  \      /  \  | \  / |
 |  <    / /\ \    / /\ \ | |\/| |    | | / /\ \ | |\/| | / /\ \    / /\ \ | |\/| |
 | . \  / ____ \  / ____ \| |  | |    | |/ ____ \| |  | |/ ____ \  / ____ \| |  | |
 |_|\_\/_/    \_\/_/    \_\_|  |_|    |_/_/    \_\_|  |_/_/    \_\/_/    \_\_|  |_|
""")
    while True:
        print("\n1️⃣  Add Task ➕")
        print("2️⃣  Edit Task ✏")
        print("3️⃣  Complete Task ✅")
        print("4️⃣  Display Tasks 📜")
        print("5️⃣  Refresh Schedule 🔄 ")
        print("6️⃣  Display Calendar 📆")
        print("7️⃣  Clear Calendar 🗑")
        print("8️⃣  Exit 🚪")
        choice = input("Enter your choice: ")


        if choice == "1":
            try:
                try:
                    name = input("📝 Enter task name: ")
                    description = input("📝 Enter task description: ")
                    priority = int(input("⚡ Enter priority level (0-10): "))
                    if priority < 0 or priority > 10:
                        print("❌ Invalid input. Please try again.")
                        continue
                    difficulty = int(input("🛠 Enter difficulty level (0-10): "))
                    if difficulty < 0 or difficulty > 10:
                        print("❌ Invalid input. Please try again.")
                        continue
                    duration = float(input("⏳ Enter task duration in hours: "))
                    if duration < 0:
                        print("❌ Invalid input. Please try again.")
                        continue

                    deadline = Timestamp.getDate(input("📅 Enter deadline (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if deadline is None:
                        continue

                    start_time = Timestamp.getDate(input("🕒 Enter start time (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if start_time is None:
                        continue

                except ValueError:
                    print("❌ Invalid input. Please try again.")
                    continue

                delayable_input = input("⏳ Is task delayable? (y/n): ")
                if delayable_input == "y":
                    delayable = True
                elif delayable_input == "n":
                    delayable = False
                else:
                    print("❌ Invalid input. Task will be considered delayable by default.")
                    delayable = True

                repeat = 1
                r_input = input("🔄 Is task recurring? (y/n): ")
                if r_input == "y":
                    recurring = ""
                    while recurring != "d" and recurring != "w" and recurring != "m":
                        recurring = input("🔁 Enter recurring interval (daily (d), weekly (w), monthly (m)): ")
                        if recurring != "d" and recurring != "w" and recurring != "m":
                            print("❌ Invalid input. Please try again.")
                    repeat = int(input("🔢 How many times should the task repeat? >"))
                    if repeat < 1:
                        print("❌ Invalid input. Task will be considered non-recurring by default.")
                        repeat = 1
                    elif repeat > 100:
                        repeat = 100
                elif r_input == "n":
                    recurring = ""
                else:
                    print("❌ Invalid input. Task will be considered non-recurring by default.")
                    recurring = ""

                scheduler.add_task(name, description, priority, difficulty, duration, 
                                deadline, start_time, start_time.addMinutes(duration*60), delayable, recurring, repeat)

                print("✅ Task added successfully!\n")
                scheduler.task_handler.save_tasks(scheduler.tasks)
            except ValueError or IndexError or KeyError or AttributeError or TypeError or EOFError:
                print("❌ Invalid input. Please try again.")
                continue
        elif choice == "2":
            try:
                if not scheduler.tasks:
                    print("📋 No tasks to edit.\n")
                    continue
                try:
                    task_id = int(input("🔢 Enter task ID to edit: "))
                except ValueError:
                    print("❌ Invalid input. Please try again.")
                    continue

                task = scheduler.get_task(task_id)
                if task is None:
                    print("🔍 Task not found. Please try again.")
                    continue

                print("✅ Task found:")
                print(task)
                print("✏ Edit task:")
                print("1. Name 📝")
                print("2. Description 📝")
                print("3. Priority ⚡")
                print("4. Difficulty 🛠")
                print("5. Duration ⏳")
                print("6. Deadline 📅")
                print("7. Start Time 🕒")
                print("8. Delayable ⏳")
                print("9. Recurring 🔄")
                print("10. Cancel ❌")
                edit_choice = input("➡ Enter your choice: ")

                if edit_choice == "1":
                    name = input("📝 Enter new task name: ")
                    task.set_name(name)
                    print("✅ Task name updated successfully!\n")

                elif edit_choice == "2":
                    description = input("📝 Enter new task description: ")
                    task.description = description
                    print("✅ Task description updated successfully!\n")

                elif edit_choice == "3":
                    try:
                        priority = int(input("⚡ Enter new priority level (1-10): "))
                    except ValueError:
                        print("❌ Invalid input. Please try again.")
                        continue
                    task.set_priority(priority)
                    print("✅ Task priority updated successfully!\n")

                elif edit_choice == "4":
                    try:
                        difficulty = int(input("🛠 Enter new difficulty level (1-10): "))
                    except ValueError:
                        print("❌ Invalid input. Please try again.")
                        continue
                    task.set_difficulty(difficulty)
                    print("✅ Task difficulty updated successfully!\n")

                elif edit_choice == "5":
                    try:
                        duration = float(input("⏳ Enter new task duration in hours: "))
                    except ValueError:
                        print("❌ Invalid input. Please try again.")
                        continue
                    task.set_duration(duration)
                    print("✅ Task duration updated successfully!\n")

                elif edit_choice == "6":
                    deadline = Timestamp.getDate(input("📅 Enter new deadline (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if deadline is None:
                        continue
                    task.set_deadline(deadline)
                    print("✅ Task deadline updated successfully!\n")

                elif edit_choice == "7":
                    start_time = Timestamp.getDate(input("🕒 Enter new start time (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if start_time is None:
                        continue
                    task.set_start_time(start_time)
                    print("✅ Task start time updated successfully!\n")

                elif edit_choice == "8":
                    delayable_input = input("⏳ Is task delayable? (y/n): ")
                    if delayable_input == "y":
                        delayable = True
                    elif delayable_input == "n":
                        delayable = False
                    else:
                        print("❌ Invalid input. Task will be considered delayable by default.")
                        delayable = True
                    task.set_delayable(delayable)
                    print("✅ Task delayable status updated successfully!\n")

                elif edit_choice == "9":
                    repeat = 1
                    r_input = input("🔄 Is task recurring? (y/n): ")
                    if r_input == "y":
                        recurring = ""
                        while recurring != "d" and recurring != "w" and recurring != "m":
                            recurring = input("🔁 Enter new recurring interval (daily (d), weekly (w), monthly (m)): ")
                            if recurring != "d" and recurring != "w" and recurring != "m":
                                print("❌ Invalid input. Please try again.")
                        repeat = int(input("🔢 How many times should the task repeat? >"))
                        if repeat < 1:
                            print("❌ Invalid input. Task will be considered non-recurring by default.")
                            repeat = 1
                        elif repeat > 1000:
                            repeat = 1000
                    elif r_input == "n":
                        recurring = ""
                    else:
                        print("❌ Invalid input. Task will be considered non-recurring by default.")
                        recurring = ""
                    task.set_repeat(repeat)
                    task.set_recurring(recurring)
                    print("✅ Task recurring status updated successfully!\n")

                elif edit_choice == "10":
                    print("❌ Edit cancelled.\n")

                scheduler.task_handler.save_tasks(scheduler.tasks)

            except ValueError or IndexError or KeyError or AttributeError or TypeError or EOFError:
                print("Invalid input. Please try again.")
                continue
        elif choice == "3":
            if not scheduler.tasks:
                print("No tasks to complete.\n")
                continue
            try:
                task_id = int(input("Enter task ID to complete: "))
            except ValueError or TypeError:
                print("Invalid input. Please try again.")
                continue

            task = scheduler.get_task(task_id)
            if task is None:
                print("Task not found. Please try again.")
                continue

            task.set_completed(True)
            scheduler.remove_task(task)
            scheduler.calendar.removeTask(task)
            scheduler.task_handler.save_tasks(scheduler.tasks)
            print("Task completed successfully!\n")
        elif choice == "4":
            scheduler.display_tasks()

        elif choice == "5":
            scheduler.solve_schedule()
            scheduler.task_handler.save_tasks(scheduler.tasks)

        elif choice == "6":
            try:
                if not scheduler.tasks:
                    print("📋 No tasks to display.\n")
                    continue

                print("🔄 Optimising schedule...")
                scheduler.solve_schedule()

                while True:
                    print("📅 Schedule Options:")
                    print("1. Display day schedule 📆")
                    print("2. Display month schedule 🗓")
                    print("3. Display year schedule 🗓")
                    choice = input("➡ Enter your choice: ")

                    if choice == "1":
                        day = int(input("📆 Enter day to display (1-31): "))
                        month = int(input("🗓 Enter month to display (1-12): "))
                        scheduler.calendar.displayDailyTasks(month, day)
                        break
                    elif choice == "2":
                        month = int(input("🗓 Enter month to display (1-12): "))
                        scheduler.calendar.displayMonthlyCalendar(month)
                        break
                    elif choice == "3":
                        scheduler.calendar.displayYearlyCalendar()
                        break
                    else:
                        print("❌ Invalid choice. Please try again.")

            except ValueError or IndexError or KeyError or AttributeError or TypeError or EOFError:
                print("Invalid input. Please try again.")
                continue

        elif choice == "7":
            scheduler.tasks = []
            scheduler.calendar.clearCalendar()
            scheduler.task_handler.save_tasks(scheduler.tasks)
            print("🗑 Calendar cleared.\n")

        elif choice == "8":
            print("👋 Exiting the Task Management System. Goodbye! 🚪")
            break
        else:
            print("❌ Invalid choice. Please try again. 🔄\n")