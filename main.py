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

# TODO: daily score update 
def changeScore(task):
    if task.completed == True:
        score += task.points
    else:
        score -= task.points

# create a task and assign name and points
def createTask():
    taskName = input("Name of the task: ")
    taskPoints = int(input("Points: "))
    return Task(taskName, taskPoints, False)

# manages listing, adding, setting status of tasks and quitting out
def performAction(action, taskList, score):
    match action:
        case 'l':
            print("\n")
            for i in taskList:
                status = "Not Completed"
                if i.getCompleted():
                    status = "Completed"
                print(f'- {i.getName()}, value: {i.getPoints()}, status: {status}')
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
            if taskList[index].getCompleted() == True:
                taskList[index].setNotCompleted()
                score -= taskList[index].getPoints()
            else:
                taskList[index].setCompleted() 
                score += taskList[index].getPoints()

            print('\n')
            return False, score
        case 'q':
            return True, score

# TODO: save config file
# TODO: daily tracking
# TODO: gui
# TODO: plot graph

def main():
    score = 0
    exampleTask = Task("Coding", 100, False)
    actionList1 = ['l', 'a', 's', 'q']
    taskList = [exampleTask]
    name = exampleTask.getName()
    print(f'{name}')
    print("Haby.\n")
    while True:
        print ('----------------------------------------------------------------')
        print(f'Score: {score}')
        print("l: list tasks | a: add task | s: set completed | q: quit")
        action = input()
        if action in actionList1:
            quit, score = performAction(action, taskList, score)
            if quit:
                break
        else:
            print("Please try again.")


    

if __name__ == '__main__':
    main()
