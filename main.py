# TODO: error handling
# TODO: check for days when the app has not been opened to set score to 0
# TODO: list tasks by alphabetical order (maybe)
# TODO: improve plot
# TODO: gui

import yaml
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use('_mpl-gallery')
current_date = datetime.date.today()


# Create config files if they don't exist
def create_config():
    if not os.path.exists('./tasks.yml'):
        os.mknod('./tasks.yml')
    if not os.path.exists('./recap_days.yml'):
        os.mknod('./recap_days.yml')
    if not os.path.exists('./date_of_last_save.yml'):
        os.mknod('./date_of_last_save.yml')


# Main object of the project is the Task: it contains
# the name, the points and the daily status of the class
class Task():
    def __init__(self, name, points, completed):
        self.name = name
        self.points = points
        self.completed = completed

    def setCompleted(self):
        self.completed = True

    def setNotCompleted(self):
        self.completed = False

    def setPoints(self, x):
        self.points = x

    def setName(self, s):
        self.name = s

    def getCompleted(self):
        return self.completed

    def getPoints(self):
        return self.points

    def getName(self):
        return self.name


# this class contains the list of tasks with their status of a particular date
# and the total score for that day
class Daily_Task():
    def __init__(self, score, tasks, date):
        self.score = score
        self.tasks = tasks
        self.date = date

    def setScore(self, score):
        self.score = score

    def setTasks(self, tasks):
        self.tasks = tasks

    def setDate(self, date):
        self.date = date

    def getScore(self):
        return self.score

    def getTasks(self):
        return self.tasks

    def getDate(self):
        return self.date


# unused for now, could be useful later
# draws a graph of all the tasks on the x and their relative points
def draw_tasks_plot(taskList):
    x_array = []
    y_array = []
    for i in range(0, len(taskList)):
        x_array.append(i)

    x_labels = []
    for t in taskList:
        y_array.append(t.getPoints())
        x_labels.append(t.getName())

    x = np.array(x_array)
    y = np.array(y_array)
    plt.xticks(x, x_labels)
    plt.bar(x, y)
    plt.show()


# draws a plot to compare the score obtained day by day
def draw_daily_plot(today_score):
    x_array = []
    y_array = []
    x_labels = []
    with open('recap_days.yml', 'r') as file:
        data = yaml.safe_load(file)
    file.close()

    i=0
    if data is not None:
        for date in data:
            x_labels.append(date)
            x_array.append(i)
            i += 1
            y_array.append(data[date]['score'])

    x_labels.append("Today")
    x_array.append(i)
    y_array.append(today_score)
    x = np.array(x_array)
    y = np.array(y_array)
    plt.xticks(x, x_labels)
    plt.plot(x, y)
    plt.show()


# compares today date with the date of the last save
# if it's a different day returns the date of last save to use it
# otherwise returns None
def check_date():
    with open("date_of_last_save.yml", "r") as file:
        last_date = yaml.safe_load(file)
    file.close()

    if last_date is None:
        return None

    if current_date > last_date:
        return last_date
    return None


# saves the score and tasks progress of each day of use
def save_score(score, tasks, date):
    daily_task = Daily_Task(score, tasks, date)
    with open('recap_days.yml', 'a+') as file:
        data = yaml.safe_load(file)
        if data is None:
            data = {}
        if date not in data.keys():
            data[f'{date}'] = {'score': daily_task.getScore(
            ), 'date': daily_task.getDate(), 'tasks': {}}
            j = 0
            if tasks is not None:
                for i in tasks:
                    data[f'{date}']['tasks'][f'Task{j}'] = {
                        'name': i.getName(), 'points': i.getPoints(), 'completed': i.getCompleted()}
                    j += 1
            else:
                data[f'{date}']['score'] = 0;
            yaml.dump(data, file)
            file.close()
        else:
            file.close()


# unused, finds the score of a given day
def find_score_by_date(date):
    with open('recap_days.yml', 'r') as file:
        data = yaml.safe_load(file)
        score = data[date]['score']
        file.close()
    return score


# create a task and assign name and points
def createTask():
    print("Name of the task: ")
    taskName = input("> ")
    print("Points: ")
    taskPoints = int(input("> "))
    return Task(taskName, taskPoints, False)


# saves the current status of the tasks for today
def save(taskList):
    i = 0
    dict = {}
    for task in taskList:
        dict[f'Task{i}'] = {'name': task.getName(
        ), 'points': task.getPoints(), 'completed': task.getCompleted()}
        i += 1

    with open('tasks.yml', 'w') as file:
        yaml.dump(dict, file)

    file.close()
    with open('date_of_last_save.yml', 'w') as file:
        yaml.dump(current_date, file)

    file.close()


# manages what to do when users chooses what he wants to do
def performAction(action, taskList, score):
    match action:
        # list all tasks
        case 'l':
            print("\n")
            for i in taskList:
                status = "Not Completed"
                if i.getCompleted():
                    status = "Completed"
                print(
                    f'- {i.getName()}, value: {i.getPoints()}, status: {status}')
            print("\n")
            return False, score

        # add a new task to the list
        case 'a':
            print('\n')
            task = createTask()
            taskList.append(task)
            print('\n')
            return False, score

        # change a task status to completed or not completed
        # and changes score accordingly
        case 's':
            if not taskList:
                print("No task found.")
                print()
                return False, score
            print('\n')
            print("Select task by indicating number: ")
            for i in range(1, len(taskList)+1):
                print(f'{i}. {taskList[i-1].getName()}')
            index = int(input("\nEnter number: ")) - 1
            if taskList[index].getCompleted():
                taskList[index].setNotCompleted()
                score -= taskList[index].getPoints()
            else:
                taskList[index].setCompleted()
                score += taskList[index].getPoints()

            print()
            return False, score

        # edit a task (delete, change name, change score)
        case 'e':
            if not taskList:
                print("No task found.")
                print()
                return False, score
            print()
            print("Do you want to delete the task or change the name/points?")
            choice = input("d/c: ")
            while True:
                if choice == 'd':
                    print("Select task by indicating number: ")
                    for i in range(1, len(taskList)+1):
                        print(f'{i}. {taskList[i-1].getName()}')
                    index = int(input("\nEnter number: ")) - 1
                    taskList.pop(index)
                    save(taskList)
                    break

                elif choice == 'c':
                    print("Select task by indicating number: ")
                    for i in range(1, len(taskList)+1):
                        print(f'{i}. {taskList[i-1].getName()}')
                    index = int(input("\nEnter number: ")) - 1
                    new_name = input(
                        "> New name (leave blank to keep the old value): ")
                    new_points = input(
                        "> New points(leave blank to keep the old value): ")
                    if new_name != '':
                        taskList[index].setName(new_name)
                    if new_points != '':
                        new_points = int(new_points)
                        point_diff = new_points - taskList[index].getPoints()
                        taskList[index].setPoints(new_points)
                    if taskList[index].getCompleted() and new_points != '':
                        score += point_diff
                    break
                else:
                    print("Retry")
            print()
            return False, score

        # draw a plot of daily scores
        case 'p':
            draw_daily_plot(score)
            return False, score

        # # find the score obtained on specific day
        # case 'f':
        #     print()
        #     with open('recap_days.yml', 'r') as file:
        #         data = yaml.safe_load(file)
        #         if data is None:
        #             print("No saved score found")
        #             return False, score
        #         print("Choose one of the dates: below")
        #         for k in data:
        #             print(f'- {k}')
        #         date = input("> ")
        #         old_score = find_score_by_date(date)
        #         print(f'Score: {old_score}')
        #         file.close()
        #     return False, score

        # save and quit
        case 'q':
            print("Saving...")
            save(taskList)
            print("Saved!")
            return True, score

        # manages mistype
        case _:
            print("Retry.")
            return False, score


def main():
    create_config()
    with open('tasks.yml', 'r') as file:
        tasks = yaml.safe_load(file)

    score = 0
    # exampleTask = Task("Coding", 100, False)
    actionList1 = ['l', 'a', 's', 'e', 'p', 'q']
    taskList = []

    if tasks is not None:
        for k in tasks:
            # task = Task(tasks[k][0], tasks[k][1], tasks[k][2])
            attributes = tasks[k]
            loadedTask = Task(
                attributes['name'],
                attributes['points'],
                attributes['completed'])
            if loadedTask.getCompleted():
                score += loadedTask.getPoints()
            taskList.append(loadedTask)
    file.close()

    last_date = check_date()
    if last_date is not None:
        delta = current_date - last_date
        for i in range(delta.days):
            day = last_date + datetime.timedelta(days=i)
            if day != last_date:
                save_score(0, None, day)
        print("Saving past day data...")
        save_score(score, taskList, last_date)
        print("Done!\n")
        score = 0
        for k in taskList:
            k.setNotCompleted()

    logo = r"""
 ██╗  ██╗ █████╗ ██████╗ ██╗   ██╗
 ██║  ██║██╔══██╗██╔══██╗╚██╗ ██╔╝
 ███████║███████║██████╔╝ ╚████╔╝ 
 ██╔══██║██╔══██║██╔══██╗  ╚██╔╝  
 ██║  ██║██║  ██║██████╔╝   ██║   
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝    ╚═╝   
                                  """
    print(logo)

    actions = r"""
 ████████████████████████████████████████████████████████████
 ██                                                        ██
 ██  l:list tasks   | a: add task     | s:set completed    ██
 ██  p: plot scores | e: edit task    | q:quit             ██
 ██                                                        ██
 ████████████████████████████████████████████████████████████"""
    while True:
        print(f'Score: {score}')
        print(actions)
        print()
        action = input("> ")
        if action in actionList1:
            quit, score = performAction(action, taskList, score)
            if quit:
                break
        else:
            print("Please try again.")


if __name__ == '__main__':
    main()
