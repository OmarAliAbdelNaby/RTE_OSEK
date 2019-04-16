from RTE_OS import *

def getRunnableEvent(runnableName):
    for everyList in c1.Get_Triggers():
        for everyDict in everyList:
            for event, trigValues in everyDict.items():
                if everyList == c1.Get_Triggers()[0]:
                    if runnableName == trigValues:
                        return event
                else:
                    if runnableName == list(everyDict.values())[0][len(list(everyDict.values())[0]) - 1]:
                        return event



def getTaskEvents(taskName):
    taskEvents = []
    for task, runnables in Task2RunDict.items():
        if(task == taskName):
            for everyRunnable in runnables:
                taskEvents.append(getRunnableEvent(everyRunnable))

    return taskEvents
#print(getRunnableEvent('R1'))
#print(getTaskEvents('T1'))

f = open("taskBodies.c", "w+")
for everyTask in taskList:
    f.write("TASK(" + everyTask + ")\n")
    f.write("{\n")
    f.write("\tEventMaskType NewEvents;\n")
    f.write("\twhile(true)\n\t{\n")
    f.write("\t\tWaitEvent(")
    events = getTaskEvents(everyTask)
    for everyEvent in events:
        if everyEvent == events[len(events) - 1]:
            f.write(everyEvent.__str__() + ");\n")
        else:
            f.write(everyEvent.__str__() + " | ")
    f.write("\t\tGetEvent(" + everyTask + ", &NewEvents);\n")
    f.write("\t\tClearEvent(NewEvents);\n")
    #f.write("if(NewEvent &" +  + ")")
    for task, runnables in Task2RunDict.items():
        if(task == everyTask):
            for everyRunnable in runnables:
                eventName = getRunnableEvent(everyRunnable)
                f.write("\t\tif(NewEvent & " + eventName.__str__() + ")\n\t\t{\n\t\t\t")
                f.write(everyRunnable + "();\n\t\t}\n")
    f.write("\t}\n}\n")
