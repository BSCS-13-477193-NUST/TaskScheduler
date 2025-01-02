from scheduler import Scheduler
from timestamp import Timestamp
from my_calendar import Calendar
import copy


def menu():
    scheduler = Scheduler()
    print("👋 Welcome to the Kaam Tamaam System! 🚪")
    print(r"""
                                                                                    _____   __   __
                                                                                   |_   _| |  \ /  |
  _  __                    __  __   _______       __  __                    __  __   | |   | | V | |
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
        print("4️⃣  Update Sleep Schedule 🛌")
        print("5️⃣  Display Tasks 📜")
        print("6️⃣  Refresh Schedule 🔄")
        print("7️⃣  Display Calendar 📆")
        print("8️⃣  Clear Calendar 🗑")
        print("0️⃣  Exit 🚪")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                current_time = Timestamp.getCurrentTimestamp()
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
                if duration <= 0:
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

                start_time = Timestamp.getDate(input("🕒 Enter start time (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                if start_time is None:
                    continue
                if start_time < current_time and recurring == "":
                    print("❌ Invalid input. Start time cannot be before current time. Please try again.")
                    continue
                
                if delayable:
                    deadline = Timestamp.getDate(input("📅 Enter deadline (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if deadline is None:
                        continue
                else:
                    deadline = start_time.addMinutes(duration*60).addMinutes(1)

                if start_time > deadline:
                    print("❌ Invalid input. Deadline cannot be before start time. Please try again.")
                    continue

                scheduler.add_task(name, description, priority, difficulty, duration, 
                                deadline, start_time, start_time.addMinutes(duration*60), delayable, recurring, repeat)

                print("✅ Task added successfully!\n")
                scheduler.task_handler.save_tasks(scheduler.tasks)
            except (ValueError, IndexError, KeyError, AttributeError, TypeError, EOFError):
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

                i = scheduler.get_task_index(task_id)
                if i is None:
                    print("🔍 Task not found. Please try again.")
                    continue
                print("✅ Task found:\n")
                print(scheduler.tasks[i])
                print()
                print("✏ Edit task:")
                print("1️⃣  Name 📝")
                print("2️⃣  Description 📝")
                print("3️⃣  Priority ⚡")
                print("4️⃣  Difficulty 🛠")
                print("5️⃣  Duration ⏳")
                print("6️⃣  Deadline 📅")
                print("7️⃣  Start Time 🕒")
                print("8️⃣  Delayable ⏳")
                print("9️⃣  Recurring 🔄")
                print("🔟  Cancel ❌")
                edit_choice = input("➡ Enter your choice: ")

                if edit_choice == "1":
                    name = input("📝 Enter new task name: ")
                    scheduler.tasks[i].name = name
                    print("✅ Task name updated successfully!\n")

                elif edit_choice == "2":
                    description = input("📝 Enter new task description: ")
                    scheduler.tasks[i].description = description
                    print("✅ Task description updated successfully!\n")

                elif edit_choice == "3":
                    try:
                        priority = int(input("⚡ Enter new priority level (1-10): "))
                    except ValueError:
                        print("❌ Invalid input. Please try again.")
                        continue
                    scheduler.tasks[i].priority = priority
                    scheduler.tasks[i].calculate_weightage()
                    print("✅ Task priority updated successfully!\n")

                elif edit_choice == "4":
                    try:
                        difficulty = int(input("🛠 Enter new difficulty level (1-10): "))
                    except ValueError:
                        print("❌ Invalid input. Please try again.")
                        continue
                    scheduler.tasks[i].difficulty = difficulty
                    scheduler.tasks[i].calculate_weightage()
                    print("✅ Task difficulty updated successfully!\n")

                elif edit_choice == "5":
                    try:
                        duration = float(input("⏳ Enter new task duration in hours: "))
                    except ValueError:
                        print("❌ Invalid input. Please try again.")
                        continue
                    scheduler.tasks[i].duration = duration
                    scheduler.tasks[i].end_time = scheduler.tasks[i].start_time.addMinutes(duration*60)
                    print("✅ Task duration updated successfully!\n")

                elif edit_choice == "6":
                    deadline = Timestamp.getDate(input("📅 Enter new deadline (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if deadline is None:
                        continue
                    scheduler.tasks[i].deadline = deadline
                    print("✅ Task deadline updated successfully!\n")

                elif edit_choice == "7":
                    start_time = Timestamp.getDate(input("🕒 Enter new start time (YYYY-MM-DD HH:MM or HH:MM or YYYY-MM-DD): "))
                    if start_time is None:
                        continue
                    scheduler.tasks[i].start_time = start_time
                    scheduler.tasks[i].end_time = start_time.addMinutes(scheduler.tasks[i].duration*60)
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
                    scheduler.tasks[i].delayable = delayable
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
                    scheduler.tasks[i].repeat = repeat
                    scheduler.tasks[i].recurring = recurring
                    print("✅ Task recurring status updated successfully!\n")

                elif edit_choice == "10":
                    print("❌ Edit cancelled.\n")
                    continue
                scheduler.task_handler.save_tasks(scheduler.tasks)

            except (ValueError, IndexError, KeyError, AttributeError, TypeError, EOFError) as e:
                print("Invalid input. Please try again.")
                continue
        elif choice == "3":
            if not scheduler.tasks:
                print("No tasks to complete.\n")
                continue
            try:
                task_id = int(input("Enter task ID to complete: "))
            except (ValueError, TypeError):
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
        elif choice == '4':
            try:
                sleep_start = Timestamp.getDate(input("🌙 Enter sleep start time (HH:MM): "))
                sleep_duration = float(input("🌙 Enter sleep duration in hours: "))
                if sleep_start is None or sleep_duration is None:
                    print("❌ Invalid input. Please try again.")
                    continue
                if sleep_duration < 0:
                    print("❌ Invalid input. Please try again.")
                    continue
                if sleep_start < Timestamp.getCurrentTimestamp():
                    sleep_start = sleep_start.addDays(1)
                scheduler.set_sleep_schedule(sleep_start, sleep_duration)
                print("✅ Sleep schedule updated successfully!\n")
            except (ValueError, IndexError, KeyError, AttributeError, TypeError, EOFError):
                print("Invalid input. Please try again.")
                continue

        elif choice == "5":
            scheduler.display_tasks()

        elif choice == "6":
            scheduler.solve_schedule()
            scheduler.task_handler.save_tasks(scheduler.tasks)
            print("🔄 Schedule refreshed successfully!\n")

        elif choice == "7":
            try:
                if not scheduler.tasks:
                    print("📋 No tasks to display.\n")
                    continue

                print("🔄 Optimising schedule...")
                scheduler.solve_schedule()

                while True:
                    print("📅 Schedule Options:")
                    print("1️⃣  Display day schedule 📆")
                    print("2️⃣  Display month schedule 🗓")
                    print("3️⃣  Display year schedule 🗓")
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

            except (ValueError, IndexError, KeyError, AttributeError, TypeError, EOFError):
                print("Invalid input. Please try again.")
                continue

        elif choice == "8":
            scheduler.tasks = []
            scheduler.calendar.clearCalendar()
            scheduler.task_handler.save_tasks(scheduler.tasks)
            sleep_start, sleep_duration = scheduler.calendar.getSleepTimes()
            print("🗑 Calendar cleared.\n")
            if sleep_start is not None and sleep_end is not None:
                scheduler.set_sleep_schedule(sleep_start, sleep_duration)

        elif choice == "0":
            print("👋 Exiting the Kaam Tamaam System. Goodbye! 🚪")
            break
        else:
            print("❌ Invalid choice. Please try again. 🔄\n")
