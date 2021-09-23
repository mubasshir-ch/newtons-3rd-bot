import datetime
import pickle


days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class CClass:
    def __init__(self,weekDay,classTime):
        self.weekDay = weekDay
        self.classTime = classTime
    def __str__(self) :
        return self.weekDay+" at "+ self.classTime + "(UTC+6)"
    def __repr__(self):
        return str(self)
    def __eq__(self,other):
        if self.weekDay != other.weekDay or self.classTime != other.classTime:
            return False
        return True

def loadClasses():
    global classes
    classes = pickle.load(open("classes.dat","rb"))

def classRemove(idx):
    idx=idx-1
    print("remove ",idx)
    if idx<0 or idx>=len(classes):
        return "Please enter a valid index"
    else:
        cl = classes[idx]
        del classes[idx]
        print(classes)
        return str(cl)+" removed"

def classAdd(weekDay,classTime):
    weekDay = weekDay.capitalize()
    if weekDay not in days:
        return "Please enter a valid weekday"
    try:
        datetime.datetime.strptime(classTime, '%H:%M')
    except ValueError:
        return "Please enter time in HH:MM 24-hour format(UTC+6)"
    temp = CClass(weekDay,classTime)
    if temp in classes:
        return "Class already exists"
    else:
        classes.append(temp)
        return "Added class, "+str(temp)


if __name__=="__main__":
    loadClasses()
    # print(classAdd("saturday","20:00"))
    # print(classAdd("wednesday","20:00"))

# print(classes)
# print(classRemove(1))
# if __name__=="__main__":