from Print_OS_XML import *
from Amr_Component import *
import os
import json

def isMultiples(numbers):
    leastNumber = min(n for n in numbers)
    for num in numbers:
        if num % leastNumber != 0:
            return False
    return True
#-------------------

def isSynched(RunSynchDict):
    taskSynchStates = dict((el,0) for el in list(RunSynchDict.keys()))
    for taskName, periods in RunSynchDict.items():
        if isMultiples(periods):
            taskSynchStates[taskName] = "Synched"
        else:
            taskSynchStates[taskName] = "Not Synched"
    return taskSynchStates

'''
#Testing function
dict1 = {"T1": [10, 15, 100, 200],
         "T2": [5, 9, 15]}
#print(isSynched(dict1))
'''

#-------------------------------------

def isBasic(taskName, tasksList):
    for eachTaskList in tasksList:
        if eachTaskList[0] == taskName:
            if eachTaskList[5] == "BASIC":
                return True
    return False


parsexml2 = ParseArxml ( "OS.xml" )
_, taskListAll = parsexml2.GetTaskList()
taskList = []
alarmID = 0
cnt = 0
numExtendedTasks = 0
numBasicTasks = 0
numEvents = 0
listPriorities = []
numPriorities = 0
generalConfigList = []
for element in taskListAll:
    taskList.append(element[0])
#--------------------------------------------------

allTriggers = []
allRunnables = []

path = 'E:\\Projects\RTE_OSEK-master\RTE_OS\SWCs'
for filename in os.listdir(path):
    if not filename.endswith('.arxml'): continue
    fullname = os.path.join(path, filename)
    c1 = Component(fullname)
    #print(fullname)
    listRunnables = list(c1.Get_Runnables().keys())
    allRunnables.append(listRunnables)
    allTriggers.append(c1.Get_Triggers())
    #print(listRunnables)
    #print(c1.Get_Triggers())

#print(allRunnables)
#print(allTriggers)
#--------------------------------------------------

#--------------------------------------------------
def mapping(oldTask2RunDict):
    Task2RunDict =  dict((el, []) for el in taskList)
    for everyKey, everyValue in oldTask2RunDict.items():
        Task2RunDict[everyValue[0]].append(everyKey)
    return Task2RunDict


with open("RunnablesandTasks.txt") as json_file:
    oldTask2RunDict = json.load(json_file)


Task2RunDict = mapping(oldTask2RunDict)
RunSynchDict = dict((el, []) for el in taskList)
#Task2RunDict['T1'] = ['HeatRegulatorRunnable', 'SeatHeaterRunnable', 'UpdateHeating']
#Task2RunDict['T2'] = ['SeatSensorRunnableLeft', 'SeatSensorRunnableRight']
#print(Task2RunDict)
#
#--------------------------------------------------

def getRunnableEvent(runnableName):
    for everyListTriggers in allTriggers:
        for everyList in everyListTriggers:
            for everyDict in everyList:
                for event, trigValues in everyDict.items():
                    if everyList == everyListTriggers[0]:
                        if runnableName == trigValues:
                            return "RTE_Event_" + event
                    else:
                        if runnableName == list(everyDict.values())[0][len(list(everyDict.values())[0]) - 1]:
                            return "RTE_Event_" + event


def getTaskEvents(taskName):
    taskEvents = []
    for task, runnables in Task2RunDict.items():
        if(task == taskName):
            for everyRunnable in runnables:
                taskEvents.append(getRunnableEvent(everyRunnable))

    return taskEvents


def getEventTask(eventName):
    #eventName = eventName.replace("RTE_Event_", '')
    for everyTask in taskList:
        everyTaskEvents = getTaskEvents(everyTask)
        for everyEvent in everyTaskEvents:
            if(eventName == everyEvent):
                return everyTask

#print(getEventTask('RTE_Event_E3'))

#AlarmList = parsexml2.GetAlarmList()
#print(AlarmList)
#print(AlarmList[0][7])



#------------------------------------------------------------------------------------------
#----------- As simulation for the output from the GUI Task2RunnablesMapping  -------------
#----------- Dictionary of key is the task and the value is list of runnables -------------
#------------------------------------------------------------------------------------------

#print(c1.Get_Triggers())

NewXML = CreateArxml ( 'OS.xml' )
NewXML.CreateOS ( 'ActiveEcuC' )

for everyTask in taskListAll:
    listPriorities.append(everyTask[1])

    if (isBasic(everyTask[0],taskListAll)):
        numBasicTasks += 1
    else:
        numExtendedTasks += 1
    taskEventsList = getTaskEvents(everyTask[0])
    #elly na2sa mkan true hea everyTask[6]
    newTask = [everyTask[0], everyTask[1], everyTask[4], everyTask[2], "TRUE" , everyTask[5], everyTask[3], len(taskEventsList), everyTask[8], taskEventsList, everyTask[10]]
    NewXML.AddTask(newTask)

numPriorities = len(list(set(listPriorities)))

eventLists = []
counterLists = []
alarmLists = []

#------------------- Init Triggers ---------------
for everyListTriggers in allTriggers:
    for everyDict in everyListTriggers[0]:
        eventName = "RTE_Event_" + list(everyDict.keys())[0]
        #NewXML.AddEvent([eventName, 300])
        eventLists.append([eventName, 300])
        numEvents += 1
#-------------------------------------------------

#------------------- Periodic Triggers -----------
for everyListTriggers in allTriggers:
    for everyDict in everyListTriggers[1]:
        alarmID = alarmID + 1
        alarmName = "RTE_Alarm_alarm" + alarmID.__str__()
        eventName = "RTE_Event_" + list(everyDict.keys())[0]
        #NewXML.AddEvent([eventName, 300])
        eventLists.append([eventName, 300])
        numEvents += 1
        if alarmID % 2 != 0:
            cnt = cnt + 1
            counterName = (cnt-1).__str__() #"RTE_Counter_counter" + cnt.__str__()
            #NewXML.AddCounter([counterName, 'HARDWARE' , 0.000000001 , 65535 , 1 , 0])   #ns   #ms
            counterLists.append([counterName, 'HARDWARE' , 0.000000001 , 65535 , 1 , 0])
            #print([counterName, 'HARDWARE' , 0.000000001 , 65535 , 1 , 0])
        alarmTime = list(everyDict.values())[0][0]

        for task, runnables in Task2RunDict.items():
            for everyRunnable in runnables:
                if everyRunnable == list(everyDict.values())[0][1]:
                    specTask = task

        alarmLists.append([alarmName, "TRUE", "NULL", alarmTime, counterName, specTask, "SETEVENT", specTask, eventName])
        #print([alarmName, "TRUE", 400, alarmTime, counterName, specTask, "SETEVENT", specTask, eventName])
        RunSynchDict[specTask].append(alarmTime)
#-------------------------------------------------

#------------------- operation Invoked Triggers ----------
for everyListTriggers in allTriggers:
    for everyDict in everyListTriggers[3]:
        eventName = "RTE_Event_" +  list(everyDict.keys())[0]
        #NewXML.AddEvent([eventName, 300])
        eventLists.append([eventName, 300])
        numEvents += 1
#---------------------------------------------------------

#------------------- Data Recieved Triggers ----------
for everyListTriggers in allTriggers:
    for everyDict in everyListTriggers[2]:
        eventName = "RTE_Event_" +  list(everyDict.keys())[0]
        #NewXML.AddEvent([eventName, 300])
        eventLists.append([eventName, 300])
        numEvents += 1
#---------------------------------------------------------

generalConfigList = [numExtendedTasks, numBasicTasks, numPriorities, numEvents, 0, cnt, alarmID, 0, 0]

for everyEvent in eventLists:
    NewXML.AddEvent(everyEvent)

for everyCounter in counterLists:
    NewXML.AddCounter(everyCounter)

for everyAlarm in alarmLists:
    NewXML.AddAlarm(everyAlarm)

def tasksGenerator(oldDictionary):

    f = open("taskBodies.c", "r+")

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
        # f.write("if(NewEvent &" +  + ")")
        for task, runnables in Task2RunDict.items():
            if (task == everyTask):
                orderedRunnables = list((el) for el in runnables)
                for everyRunnable in runnables:
                    #print(runnables)
                    position = oldDictionary[everyRunnable][1]
                    #print(everyRunnable, position)
                    orderedRunnables[position - 1] = everyRunnable

                #print(orderedRunnables)
                for everyRunnable in orderedRunnables:
                    eventName = getRunnableEvent(everyRunnable)
                    f.write("\t\tif(NewEvent & " + eventName.__str__() + ")\n\t\t{\n\t\t\t")
                    f.write(everyRunnable + "();\n\t\t}\n")
        f.write("\t\tTerminateTask();\n\t}\n}\n")

    #print(f.read())
    f.close()
    f1 = open("taskBodies.c", "r+")
    return f1.read()

#print(oldTask2RunDict)
taskBodyString = tasksGenerator(oldTask2RunDict)
