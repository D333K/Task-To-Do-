import operations

the_file = "Task_To_Do.json"
    
# =================================

while True:
    operations.clear_display("To Do List")

    print("1. Add Task")
    print("2. Modify Task")
    print("3. Remove Task")
    print("4. Remove All Task")
    print("5. Display Completed Task")
    print("6. Display Incomplete Task")
    print("7. Completion Task")
    print("8. Display All Task")
    print("0. Exit")

    print('_' * 12)


    try:
        user_selection = int(input("Choose An Operation: "))

        if user_selection < 0:
            raise ValueError

        if user_selection == 1:
            operations.clear_display("ADD TASK")
            operations.add_task(the_file)

        elif user_selection == 2:
            operations.clear_display("MODIFY TASK")
            operations.modify_task(the_file)

        elif user_selection == 3:
            operations.clear_display("REMOVE TASK")
            operations.remove_task(the_file)

        elif user_selection == 4:
            operations.clear_display("REMOVE ALL TASK")
            operations.remove_all_tasks(the_file)

        elif user_selection == 5:
            operations.clear_display("COMPLETED TASKS")
            operations.display_completed_tasks(the_file)

        elif user_selection == 6:
            operations.clear_display("INCOMPLETE TASKS")
            operations.display_incomplete_tasks(the_file)

        elif user_selection == 7:
            operations.clear_display("COMPLETION TASK")
            operations.completion_task(the_file)

        elif user_selection == 8:
            operations.clear_display("ALL TASKS")
            operations.display_tasks(the_file)

        elif user_selection == 0:
            operations.devloper_info()
            break

    except ValueError:
        print("Error in input!\nPlease enter a valid number.")
        input("Press To Continue...")