from Print_OS_XML import *
from Amr_Component import *
import math
import Print_OS_XML

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


dict1 = {"T1": [10, 15, 100, 200],
         "T2": [5, 9, 15]}
print(isSynched(dict1))


def isBasic(taskName, tasksList):
    for eachTaskList in tasksList:
        if eachTaskList[0] == taskName:
            if eachTaskList[5] == "BASIC":
                return True
    return False


parsexml2 = ParseArxml ( "Ga3foor.xml" )
_, taskListAll = parsexml2.GetTaskList()
taskList = []
alarmID = 0
cnt = 0
for element in taskListAll:
    taskList.append(element[0])
print(taskListAll)
#print(isBasic("T2", taskListAll))



c1=Component("swc1.arxml")
c1.Get_Runnables()
#print(c1.Get_Runnables().keys())

listRunnables = list(c1.Get_Runnables().keys())
#print(listRunnables)
firstListRunnables = listRunnables[0:2]
secondListRunnables= listRunnables[2:5]
Task2RunDict = dict((el,0) for el in taskList)
RunSynchDict = dict((el,[]) for el in taskList)
Task2RunDict['T1'] = firstListRunnables
Task2RunDict['T2'] = secondListRunnables
print(Task2RunDict)

#------------------------------------------------------------------------------------------
#----------- As simulation for the output from the GUI Task2RunnablesMapping  -------------
#----------- Dictionary of key is the task and the value is list of runnables -------------
#------------------------------------------------------------------------------------------

print(c1.Get_Triggers())
#print(c1.Get_Runnables())


    # print(parsexml.GetGeneralConfig())
#print (parsexml.GetTaskList())

NewXML = CreateArxml ( 'Ga3foor.xml' )
NewXML.CreateOS ( 'ActiveEcuC' )

for everyTask in taskListAll:
    print(everyTask)

    newTask = [everyTask[0], everyTask[1], everyTask[4], everyTask[2], everyTask[6], everyTask[5], everyTask[3], everyTask[7], everyTask[8], everyTask[9], everyTask[10]]
    print(newTask)
    NewXML.AddTask(newTask)

#------------------- Init Triggers ---------------
for everyDict in c1.Get_Triggers()[0]:
    eventName = "RTE_Event_" + list(everyDict.keys())[0]
    NewXML.AddEvent([eventName, 300])
#------------------- Periodic Triggers -----------
for everyDict in c1.Get_Triggers()[1]:
    alarmID = alarmID + 1
    alarmName = "RTE_Alarm_alarm" + alarmID.__str__()
    eventName = "RTE_Event_" + list(everyDict.keys())[0]
    NewXML.AddEvent([eventName, 300])
    if alarmID % 2 != 0:
        cnt = cnt + 1
        counterName = "RTE_Counter_counter" + cnt.__str__()
        NewXML.AddCounter([counterName, 'HARDWARE' , 0.000000001 , 65535 , 1 , 0])   #ns   #ms
    alarmTime = list(everyDict.values())[0][0]

    for task, runnables in Task2RunDict.items():
        for everyRunnable in runnables:
            if everyRunnable == list(everyDict.values())[0][1]:
                specTask = task
    #NewXML.AddAlarm([alarmName, "TRUE", alarmTime, "NULL", counterName, "NULL", "SETEVENT", specTask, eventName]) #alarmTime is out of scale
    NewXML.AddAlarm([alarmName, "TRUE", alarmTime, "NULL", counterName, specTask, "SETEVENT", specTask, eventName])
    RunSynchDict[specTask].append(alarmTime)

#------------------- operation Invoked Triggers ----------
for everyDict in c1.Get_Triggers()[3]:
    eventName = "RTE_Event_" +  list(everyDict.keys())[0]
    NewXML.AddEvent([eventName, 300])
#---------------------------------------------------------

