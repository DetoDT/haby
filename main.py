# TODO: gui
# TODO: plot graph

import yaml
import datetime


with open('tasks.yml', 'r') as file:
    tasks = yaml.safe_load(file)

current_date = datetime.date.today()
print(current_date)


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


def check_date():
    with open("date_of_last_save.yml", "r") as file:
        last_date = yaml.safe_load(file)
    file.close()

    if current_date > last_date:
        return last_date
    return None


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
            for i in tasks:
                data[f'{date}']['tasks'][f'Task{j}'] = {
                    'name': i.getName(), 'points': i.getPoints(), 'completed': i.getCompleted()}
                j += 1
            yaml.dump(data, file)
            file.close()
        else:
            file.close()


def find_score_by_date(date):
    with open('recap_days.yml', 'r') as file:
        data = yaml.safe_load(file)
        score = data[date]['score']
        file.close()
    return score


# create a task and assign name and points
def createTask():
    taskName = input("Name of the task: ")
    taskPoints = int(input("Points: "))
    return Task(taskName, taskPoints, False)


def save(taskList):
    print("Saving...")
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

    file.close

    print("Saved!")


def performAction(action, taskList, score):
    match action:
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

        case 'a':
            print('\n')
            task = createTask()
            taskList.append(task)
            print('\n')
            return False, score

        case 's':
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

            print('\n')
            return False, score

        case 'f':
            print()
            with open('recap_days.yml', 'r') as file:
                data = yaml.safe_load(file)
                if data is None:
                    print("No saved score found")
                    return False, score
                print("Choose one of the dates: below")
                for k in data:
                    print(f'- {k}')
                date = input()
                old_score = find_score_by_date(date)
                print(old_score)
                file.close()
            return False, score

        case 'q':
            save(taskList)
            return True, score


def main():
    score = 0
    # exampleTask = Task("Coding", 100, False)
    actionList1 = ['l', 'a', 's', 'f', 'q']
    taskList = []

    if tasks is not None:
        for k in tasks:
            # task = Task(tasks[k][0], tasks[k][1], tasks[k][2])
            attributes = tasks[k]
            loadedTask = Task(
                attributes['name'], attributes['points'], attributes['completed'])
            if loadedTask.getCompleted():
                score += loadedTask.getPoints()
            taskList.append(loadedTask)
    file.close()

    last_date = check_date()
    print(last_date)
    if last_date is not None:
        print("Saving past day data...")
        save_score(score, taskList, last_date)
        print("Done!\n")
        score = 0
        for k in taskList:
            k.setNotCompleted()

    print("Haby.\n")
    while True:
        print('--------------------------------------------------------------')
        print(f'Score: {score}')
        print("l: list tasks         | a: add task           | s: set completed |")
        print("f: find score by date | q: quit")
        action = input()
        if action in actionList1:
            quit, score = performAction(action, taskList, score)
            if quit:
                break
        else:
            print("Please try again.")


if __name__ == '__main__':
    main()
