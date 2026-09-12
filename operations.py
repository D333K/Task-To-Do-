import os
import json
import pyfiglet
import termcolor

class TasksNotFoundError(Exception): pass

# =================================

def ask_user(task_file) -> None:
    """This Method Ask User If He Want To Add New Task If It's The First Time For Him."""

    while True:
        answer = input("Do you want to add new task? y/n:").strip().lower()

        if answer == 'y':
            add_task(task_file)
            break

        elif answer == 'n':
            break

        else:
            print("Please enter valid answer.")
            
    return

# =================================


def load_tasks(task_file) -> list:
    """This Method Will Load All Tasks From File Object And Return A List."""

    tasks_list = []

    try:
        with open(task_file, 'r', encoding="utf-8") as read_mood:
            
            for line in read_mood:
                if line.strip():
                    line_task = json.loads(line)
                    tasks_list.append(line_task)

            if not tasks_list:
                raise TasksNotFoundError

    except FileNotFoundError:
        print("This is your first time you use this program.")
        print("-" * 20)
        ask_user(task_file)
    
    except TasksNotFoundError:
        print("There is no tasks yet.")
        print("-" * 20)
        ask_user(task_file)

    except json.JSONDecodeError:
        print("Error in reading tasks from file. The file may be corrupted.")
        print("-" * 20)

    return tasks_list

# =================================

def save_tasks(tasks_list, file_object):
    """This Method Will Save Tasks After Add/Remove/Update From File Object."""

    for task in tasks_list:
        json.dump(task, file_object)
        file_object.write("\n")

# =================================

def add_task(task_file) -> None:
    """This Method Create And Add New Task In task_file File."""

    tasks_list = []

    task_name = input("Enter task name: ").strip()

    if not task_name:
        print("-" * 20)
        print("Task name cannot be empty.")
        input("Press To Continue...")
        return

    print("1- Incomplete.\n2- Complete.")

    while True:
        try:
            task_status = int(input("Choose between '1' and '2': "))
            if task_status != 1 and task_status != 2:
                raise ValueError

        except ValueError:
            print("Please enter valid number between '1' and '2'.")

        else:
            break

    try:
        with open(task_file, 'r', encoding="utf-8") as read_mood:
            
            for line in read_mood:
                if line.strip():
                    line_task = json.loads(line)
                    tasks_list.append(line_task)

            if tasks_list:
                task_id = tasks_list[len(tasks_list) - 1]["ID"] + 1

            else:
                task_id = 1
        
    except FileNotFoundError:
        task_id = 1

    except json.JSONDecodeError:
        print("Error in reading tasks from file. The file may be corrupted.")
        print("-" * 20)
        return
        
    task = {
        "ID": task_id,
        "Name": task_name,
        "Status": "Incomplete" if task_status == 1 else "Complete",
    }

    with open(task_file, 'w', encoding="utf-8") as write_mood:

        if tasks_list:
            tasks_list.append(task)
            save_tasks(tasks_list, write_mood)

        else:
            json.dump(task, write_mood)
            write_mood.write("\n")

    print("-" * 20)
    print("Add New Task Has Successfullt.")
    print("-" * 20)
    input("Press To Continue...")

    return

# =================================

def modify_task(task_file) -> None:
    """This Method Modify Or Update The Task(Name Task Or Status Task) And Save The Changes."""

    tasks_list = load_tasks(task_file)

    if not tasks_list:
        return

    print("1- Name Task.\n2- Status Task.")
    print("-" * 20)

    try:
        user_chosen = int(input("Choose between '1' and '2': "))
        if user_chosen != 1 and user_chosen != 2:
            raise ValueError

    except ValueError:
        print("-" * 20)
        print("Please enter valid number between '1' and '2' next time.")
        return

    print("-" * 20)

    try:
        task_id = int(input("Enter task id: "))

    except ValueError:
        print("-" * 20)
        print("Please enter valid number next time.")
        return

    print("-" * 20)

    flag = True

    for task in tasks_list:
        if task["ID"] == task_id:
            flag = False

            if user_chosen == 1:
                new_task_name = input("Enter new task name: ").strip()

                if not new_task_name:
                    print("-" * 20)
                    print("Task name cannot be empty.")
                    input("Press To Continue...")
                    return

                print("Task name has been updated successfully.")
                print(f"{task["Name"]} => {new_task_name}")

                task["Name"] = new_task_name
                break

            else:
                print("1- Incomplete.\n2- Complete.")
                print("-" * 20)
                
                try:
                    new_task_status = int(input("Choose between '1' and '2': "))
                    if new_task_status != 1 and new_task_status != 2:
                        raise ValueError

                    if new_task_status == 1:
                        if task["Status"] == "Incomplete":
                            print("-" * 20)
                            print("This task is already incomplete.")
                            print("-" * 20)
                            input("Press To Continue...")
                            return
                    else:
                        if task["Status"] == "Complete":
                            print("-" * 20)
                            print("This task is already completed.")
                            print("-" * 20)
                            input("Press To Continue...")
                            return

                except ValueError:
                    print("Please enter valid number between '1' and '2' next time.")
                    print("-" * 20)
                    return

                print("-" * 20)
                print(f"{task["Status"]} => {'Incomplete' if new_task_status == 1 else 'Complete'}")
                task["Status"] = "Incomplete" if new_task_status == 1 else "Complete"
                break
    if flag:
        print("There is no task with this id.")
        return

    with open(task_file, 'w', encoding="utf-8") as write_mood:
        save_tasks(tasks_list, write_mood)
        
    print("-" * 20)
    print("Update Task Has Successfully.")
    print("-" * 20)
    input("Press To Continue...")

    return

# =================================

def remove_task(task_file) -> None:
    """This Method Remove Task By Task ID."""

    tasks_list = load_tasks(task_file)

    if not tasks_list:
        return

    print("Enter '0' To Finished.")
    while True:
        try:
            task_id = int(input("Enter task id: "))

        except ValueError:
            print("Please enter valid id.")
            print("-" * 20)

        else:
            break

    if task_id == 0:
        return

    flag = True

    for index, task in enumerate(tasks_list):
        if task["ID"] == task_id:
            flag = False
            tasks_list.pop(index)
            break

    if flag:
        print("-" * 20)
        print("There is no task with this id.")
        print("-" * 20)
        input("Press To Continue...")
        return

    with open(task_file, 'w', encoding="utf-8") as write_mood:
        save_tasks(tasks_list, write_mood)

    print("-" * 20)
    print("Remove Task Has Successfully.")
    print("-" * 20)
    input("Press To Continue...")

    return

# =================================

def remove_all_tasks(task_file) -> None:
    """This Method Will Remove All Tasks From task_file."""

    tasks_list = []

    try:
        with open(task_file, 'r', encoding="utf-8") as read_mood:
            for line in read_mood:
                if line.strip():
                    line_task = json.loads(line)
                    tasks_list.append(line_task)
            
            if not tasks_list:
                raise TasksNotFoundError

    except FileNotFoundError:
        print("This is your first time you use this program.")
        print('-' * 20)
        input("Press To Continue...")
        return

    except TasksNotFoundError:
        print("There is no tasks yet.")
        print('-' * 20)
        input("Press To Continue...")
        return
    
    except json.JSONDecodeError:
        print("Error in reading tasks from file. The file may be corrupted.")
        print("-" * 20)
        return


    print("ID\tName\t\tStatus")
    print('-' * 40)

    for task in tasks_list:
        print(f"{task["ID"]}\t{task["Name"]}\t\t{task["Status"]}")

    print('-' * 40)

    answer = input("Are You Sure? y/n: ").strip().lower()

    if answer == 'y':
        with open(task_file, 'w', encoding="utf-8"):
            pass

    elif answer == 'n':
        print('-' * 20)
        input("Press To Continue...")

    else:
        print("Please enter valid answer.")
        input("Press To Continue...")

    return

# =================================

def display_completed_tasks(task_file) -> None:
    """This Method Will Display All Completed Tasks."""

    tasks_list = load_tasks(task_file)

    if not tasks_list:
        return

    print("ID\tName\t\tStatus")
    print('-' * 40)

    for task in tasks_list:
        if task["Status"] == "Complete":
            print(f"{task["ID"]}\t{task["Name"]}\t\t{task["Status"]}")

    print("-" * 20)
    input("Press To Continue...")
    return

# =================================

def display_incomplete_tasks(task_file) -> None:
    """This Method Will Display All Incomplete Tasks."""

    tasks_list = load_tasks(task_file)
    
    if not tasks_list:
        return

    print("ID\tName\t\tStatus")
    print('-' * 40)

    for task in tasks_list:
        if task["Status"] == "Incomplete":
            print(f"{task["ID"]}\t{task["Name"]}\t\t{task["Status"]}")

    print("-" * 20)
    input("Press To Continue...")
    return

# =================================

def completion_task(task_file) -> None:
    """This Method Will Let The User To Completion Any Task Is Still Incomplete."""

    tasks_list = load_tasks(task_file)
    
    if not tasks_list:
        return

    print("Enter '0' To Finished.")
    while True:
        try:
            task_id = int(input("Enter task id: "))

        except ValueError:
            print("Please enter valid id.")

        else:
            break

    if task_id == 0:
        return

    flag = True

    for task in tasks_list:
        if task["ID"] == task_id:
            if task["Status"] == "Complete":
                print("-" * 20)
                print("This task is already completed.")
                print("-" * 20)
                input("Press To Continue...")
                return

            else:
                flag = False
                task["Status"] = "Complete"
                break

    if flag:
        print("-" * 20)
        print("There is no task with this id.")
        print("-" * 20)
        input("Press To Continue...")
        return

    with open(task_file, 'w', encoding="utf-8") as write_mood:
        save_tasks(tasks_list, write_mood)

    print("-" * 20)
    print("Completion Task Has Successfully.")
    print("-" * 20)
    input("Press To Continue...")

    return

# =================================

def display_tasks(task_file) -> None:
    """This Method Will Display All Tasts."""

    tasks_list = load_tasks(task_file)
    
    if not tasks_list:
        return

    print("ID\tName\t\tStatus")
    print('-' * 40)

    for task in tasks_list:
        print(f"{task["ID"]}\t{task["Name"]}\t\t{task["Status"]}")

    print("-" * 20)
    input("Press To Continue...")
    return

# =================================

def clear_display(operation) -> None:
    """This Method Will Clear The Display And Wait User Until Press Any Key."""

    os.system("cls" if os.name == "nt" else "clear")

    print('=' * 12, end = ' ')
    print(operation, end = ' ')
    print('=' * 12, end = "\n\n")

def devloper_info() -> None:
    """This Method Will Display Developer Info."""

    os.system("cls" if os.name == "nt" else "clear")
    print(termcolor.colored(pyfiglet.figlet_format("Created By Dark Knight:-"), color="black"))
            