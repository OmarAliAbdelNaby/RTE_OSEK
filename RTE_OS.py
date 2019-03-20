from Print_OS_XML import *
from Amr_Component import *


parsexml2 = ParseArxml ( "Farag_MagdyOS.xml" )
taskListAll = parsexml2.GetTaskList()
taskList = []
alarmID = 0
cnt = 0
for element in taskListAll:
    taskList.append(element[0])
#print (taskList)

c1=Component("swc1.arxml")
c1.Get_Runnables()
#print(c1.Get_Runnables().keys())

listRunnables = list(c1.Get_Runnables().keys())
#print(listRunnables)
firstListRunnables = listRunnables[0:2]
secondListRunnables= listRunnables[2:5]
Task2RunDict = dict((el,0) for el in taskList)
Task2RunDict['T1'] = firstListRunnables
Task2RunDict['T2'] = secondListRunnables
print(Task2RunDict.values())

#------------------------------------------------------------------------------------------
#----------- As simulation for the output from the GUI Task2RunnablesMapping  -------------
#----------- Dictionary of key is the task and the value is list of runnables -------------
#------------------------------------------------------------------------------------------

print(c1.Get_Triggers())
#print(c1.Get_Runnables())

parsexml = ParseArxml ( "Farag_MagdyOS.xml" )
    # print(parsexml.GetGeneralConfig())
print (parsexml.GetTaskList())

NewXML = CreateArxml ( 'Ga3foor.xml' )
NewXML.CreateOS ( 'ActiveEcuC' )

#------------------- Init Triggers ---------------
for everyDict in c1.Get_Triggers()[0]:
    eventName = list(everyDict.keys())[0]
    NewXML.AddEvent([eventName, 300])
#-------------------------------------------------

#------------------- Periodic Triggers -----------
for everyDict in c1.Get_Triggers()[1]:
    alarmID = alarmID + 1
    alarmName = "alarm" + alarmID.__str__()
    eventName = list(everyDict.keys())[0]
    NewXML.AddEvent([eventName, 300])
    if cnt % 2 == 0:
        counterName = "counter" + (alarmID - cnt).__str__()
        NewXML.AddCounter([counterName, 'HARDWARE' , 0.000000001 , 65535 , 1 , 0])   #ns   #ms
    alarmTime = list(everyDict.values())[0]
    '''
    for everyListOfRunnables in list(Task2RunDict.values()):
        for everyRunnable in everyListOfRunnables:
            if everyRunnable == list(everyDict.values())[1]:
                everyListOfRunnables
    #NewXML.AddAlarm([alarmName, "FALSE", 0, "TRUE", alarmTime, "NULL", "SETEVENT", ,eventName]) #alarmTime is out of scale
    '''
    cnt = cnt + 1
#---------------------------------------------------

#------------------- operation Invoked Triggers ----------
for everyDict in c1.Get_Triggers()[3]:
    eventName = list(everyDict.keys())[0]
    NewXML.AddEvent([eventName, 300])
#---------------------------------------------------------

