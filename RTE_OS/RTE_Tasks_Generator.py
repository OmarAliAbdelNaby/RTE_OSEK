from RTE_OS import *

f = open("taskBodies.c", "w+")

eventsListAll = []
for everyTask in taskList:
    f.write("DeclareTask(" + everyTask + ");\n")
    eventsListAll.append(getTaskEvents(everyTask))

f.write("\n")

for everyEventList in eventsListAll:
    for everyEvent in everyEventList:
        f.write("DeclareEvent(" + everyEvent + ");\n")

f.write("\n")

for everyTask in taskList:
    f.write("TASK(" + everyTask + ")\n")
    f.write("{\n")
    f.write("\tEventMaskType NewEvent;\n")
    f.write("\twhile(true)\n\t{\n")
    f.write("\t\tWaitEvent(")
    events = getTaskEvents(everyTask)
    for everyEvent in events:
        if everyEvent == events[len(events) - 1]:
            f.write(everyEvent.__str__() + ");\n")
        else:
            f.write(everyEvent.__str__() + " | ")
    f.write("\t\tGetEvent(" + everyTask + ", &NewEvent);\n")
    f.write("\t\tClearEvent(NewEvent);\n")
    #f.write("if(NewEvent &" +  + ")")
    for task, runnables in Task2RunDict.items():
        if(task == everyTask):
            for everyRunnable in runnables:
                eventName = getRunnableEvent(everyRunnable)
                f.write("\t\tif(NewEvent & " + eventName.__str__() + ")\n\t\t{\n\t\t\t")
                f.write(everyRunnable + "();\n\t\t}\n")
    f.write("\t\tTerminateTask();\n\t}\n}\n")