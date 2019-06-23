# from os_tool import *
from Print_OS_XML import *

# from xml.etree import ElementTree as ET


if __name__ == '__main__':
    parsexml = ParseArxml("Ga3foor.xml")

    Task, Task_values = (parsexml.GetTaskList())

    Counter, _ = (parsexml.GetCounterList())

    Event, _ = (parsexml.GetEventList())

    Resource, _ = (parsexml.GetResourceList())

    Alarm = (parsexml.GetAlarmList())

f = open("AutoSARConfig.c", "w")
n_tasks = len(Task)
n_resources = 0
NUMBER_OF_EVENTS = 0
NUMBER_OF_EXTENDEDTASK = 0

for i in range(n_tasks):
    n_resources += Task_values[i][8]

for i in range(n_tasks):
    NUMBER_OF_EVENTS += Task_values[i][7]

for i in range(n_tasks):
    if (Task_values[i][5] == 'EXTENDED'):
        NUMBER_OF_EXTENDEDTASK += 1

NUMBER_OF_COUNTER = len(Counter)
NUMBER_OF_ALARM = len(Alarm)

f.write('#include "AutoSARConfig.h"\n')
f.write('UBaseType_t const volatile Null;\n')
f.write('OsResource GlobalRes;\n\n\n')

for i in range(n_tasks):
    for j in range(Task_values[i][7]):
        f.write('#ifndef TASK_' + str(i + 1) + '_EVENT_' + str(j + 1) + '\n')
        f.write('    #define TASK_' + str(i + 1) + '_EVENT_' + str(j + 1) + '       Null' + '\n')
        f.write('#endif' + '\n\n')

for i in range(n_tasks):
    for j in range(Task_values[i][8]):
        f.write('#ifndef TASK_' + str(i + 1) + '_RESOURCE_' + str(j + 1) + '\n')
        f.write('    #define TASK_' + str(i + 1) + '_RESOURCE_' + str(j + 1) + '       Null' + '\n')
        f.write('#endif' + '\n\n')

for i in range(n_resources):
    f.write('#define _' + str(n_resources - i) + '_RESOURCES_IN_TASK(ExtTaskID) \    \n')
    f.write('      OsResource * ResourcesInTask_##ExtTaskID[' + str(n_resources - i) + '] = {\ \n')
    for j in range(n_resources - i):
        f.write(
            '                                                                   (OsResource *) &TASK_## ExtTaskID ##_RESOURCE_' + str(
                j + 1))
        if (i != n_resources - 1):
            f.write(', \ \n')
    f.write('                                                                      };')

    f.write('\n\n\n')

f.write('#define _0_RESOURCES_IN_TASK(ExtTaskID) \ \n')
f.write('         OsResource * ResourcesInTask_##ExtTaskID = (OsResource *) &GlobalRes;\n\n');
f.write('#if NUMBER_OF_RESOURCES > 0 \n\n')
for i in range(n_resources):
    f.write('#ifndef RESOURCE_LINKEDRESOURCE_' + str(i + 1) + '\n')
    f.write('    #define RESOURCE_LINKEDRESOURCE_' + str(i + 1) + '   Null\n')
    f.write('#endif\n\n\n')

f.write('OsResource ResourceStruct[NUMBER_OF_RESOURCES];\n\n')
f.write('/* Create Resource Handle (ID) for all Resources. The handle can be used to\n')
f.write('GetResource, ReleaseResource.*/\n\n')
f.write('UBaseType_t const RESOURCE_NAME_1 = (UBaseType_t) &ResourceStruct[0];\n\n')
for i in range(1, n_resources):
    f.write('#if NUMBER_OF_RESOURCES >= ' + str(i + 1) + '\n')
    f.write('UBaseType_t const volatile RESOURCE_NAME_' + str(i + 1) + ' = (UBaseType_t) &ResourceStruct[' + str(
        i) + '];\n')
    f.write('#endif\n\n')

f.write('/*************************** Resource struct ******************************************/\n\n\n')
f.write('OsResource ResourceStruct[NUMBER_OF_RESOURCES] = {\n')
f.write('                                     {\n')
f.write('                                               .ResourceProperty = RESOURCE_PROPERTY_1,\n')
f.write(
    '                                               .LinkedResource = (OsResourceContainer *) &RESOURCE_LINKEDRESOURCE_1,\n')
f.write('                                               .CeilingPriority = NULL,\n')
f.write('                                               .Availability = TRUE,\n')
f.write('                                              }' + ',\n')
for i in range(1, n_resources):
    f.write('#if NUMBER_OF_RESOURCES >= ' + str(i + 1) + '\n')
    f.write('                                     {\n')
    f.write(
        '                                               .ResourceProperty = RESOURCE_PROPERTY_' + str(i + 1) + ',\n')
    f.write(
        '                                               .LinkedResource = (OsResourceContainer *) &RESOURCE_LINKEDRESOURCE_' + str(
            i + 1) + ',\n')
    f.write('                                               .CeilingPriority = NULL,\n')
    f.write('                                               .Availability = TRUE,\n')
    f.write('                                              }' + ',\n')
    f.write('#endif\n')
f.write('}; \n #endif\n')

f.write('/* Declaration of ResourcesInTask */\n')
f.write('#if NUMBER_OF_EXTENDEDTASK > 0\n\n')
for i in range(NUMBER_OF_EXTENDEDTASK):
    for j in range(Task_values[i][8]):
        if (i != 0):
            f.write('#if NUMBER_OF_EXTENDEDTASK >= ' + str(i + 1) + '\n')
        f.write('    #if TASK_' + str(i + 1) + '_NUMBER_OF_RES_IN_TASK == ' + str(j) + '\n')
        f.write('        _' + str(j) + '_RESOURCES_IN_TASK( ' + str(i + 1) + ' );' + '\n')
        f.write('    #endif' + '\n')
        if (j == NUMBER_OF_EXTENDEDTASK):
            f.write('#endif' + '\n')
f.write('#endif\n')
f.write('#endif\n\n\n\n')

f.write('#if NUMBER_OF_EVENTS > 0\n\n')

f.write("/* Create Event Handle (ID) for all Events. The handle can be used to SetEvent, WaitEvent, GetEvent, etc.*/\n")

f.write('UBaseType_t const volatile OS_EVENT_NAME_1 = (1 << ' + str((i - 2) + 1) + ');\n')
for i in range(1, NUMBER_OF_EVENTS):
    f.write('#if NUMBER_OF_EVENTS >= ' + str(i + 1) + '\n')
    f.write('UBaseType_t const volatile OS_EVENT_NAME_' + str(i + 1) + ' = (1 << ' + str((i - 1) + 1) + ');\n')
    f.write('#endif\n')
f.write('\n OsEvent EventStruct[NUMBER_OF_EVENTS] = {\n')
f.write('                                {\n')
f.write('                                  .Mask = (UBaseType_t) &EventStruct[0],\n')
f.write('                                },\n')

for i in range(1, NUMBER_OF_EVENTS):
    f.write('#if NUMBER_OF_EVENTS >= ' + str(i + 1) + '\n')
    f.write('                                {\n')
    f.write('                                  .Mask = (UBaseType_t) &EventStruct[' + str(i) + '],\n')
    f.write('                                },\n')
    f.write('#endif\n')

f.write('};\n')
f.write('#endif\n\n\n')
f.write('#if NUMBER_OF_EVENTS > 0\n')
f.write('TaskEventsRef EventsInTask[NUMBER_OF_EXTENDEDTASK] = {\n')

for i in range(NUMBER_OF_EXTENDEDTASK):
    if (i != 0):
        f.write('#if NUMBER_OF_EXTENDEDTASK >= ' + str(i + 1) + '\n')
    f.write('                                {\n')
    for j in range(Task_values[i][7]):
        f.write('                                 .event' + str(j + 1) + ' = (UBaseType_t) &TASK_' + str(
            i + 1) + '_EVENT_' + str(j + 1) + ',\n')

    f.write('                                },\n')
    if (i != 0):
        f.write('#endif\n')
f.write('};\n')
f.write('#endif\n\n\n')
f.write('/******************************* Task Struct *********************************************/\n')
f.write('/* declare Task stack for each task */\n')
f.write('static StackType_t IdleStack[IDLETASK_STACK_SIZE];\n')
for i in range(n_tasks):
    f.write('#if NUMBER_OF_TASKS >= ' + str(i + 1) + '\n')
    f.write('static StackType_t TaskStack' + str(i + 1) + ' [OS_TASK_SIZE_' + str(i + 1) + '];\n');
    f.write('#endif\n')
f.write('\n\n\n OsTask TaskStruct[NUMBER_OF_TASKS + 1] = {\n')
f.write('                                 {\n')
f.write('                                  .StackRef = IdleStack,\n')
f.write('                                  .StackSize = IDLETASK_STACK_SIZE,\n')
f.write('                                  .TaskCode = (TaskFunction_t) IdleTask,\n')
f.write('                                  .Priority = NULL,\n')
f.write('                                  .StartingPriority = NULL,\n')
f.write('                                  .Activation = 1,\n')
f.write('                                  .Schedule = FULL,\n')
f.write('                                  .AutoStart = TRUE,\n')
f.write('                                  .TaskType = BASIC,\n')
f.write('                                   },\n')
for i in range(n_tasks):
    f.write('#if NUMBER_OF_TASKS >= ' + str(i + 1) + '\n')

    f.write('                                      {\n')
    f.write('                                       .StackRef = TaskStack' + str(i + 1) + ',\n')
    f.write('                                       .StackSize = OS_TASK_SIZE_' + str(i + 1) + ',\n')
    f.write(
        '                                       .TaskCode = (TaskFunction_t) TASK_FUNCTION_NAME(OS_TASK_NAME_' + str(
            i + 1) + '),\n')
    f.write('                                       .Priority =  OS_TASK_PRIORITY_' + str(i + 1) + ',\n')
    f.write('                                       .StartingPriority = OS_TASK_PRIORITY_' + str(i + 1) + ',\n')
    f.write('                                       .Activation = OS_TASK_ACTIVATION_' + str(i + 1) + ',\n')
    f.write('                                       .Schedule = OS_TASK_SCHEDULE_' + str(i + 1) + ',\n')
    f.write('                                       .AutoStart = OS_TASK_AUTOSTART_' + str(i + 1) + ',\n')
    f.write('                                       .TaskType = OS_TASK_TYPE_' + str(i + 1) + ',\n')
    f.write('                                      },\n')
    f.write('#endif\n')
f.write('};\n\n')
f.write('/* Create Task Handle (ID) for all Tasks. The handle can be used to\n')
f.write('ActivateTask, ChainTask, GetTaskState etc.*/\n\n')
for i in range(n_tasks):
    f.write('#if NUMBER_OF_TASKS >= ' + str(i + 1) + '\n')
    f.write('TaskType const OS_TASK_NAME_' + str(i + 1) + ' = (TaskType) &TaskStruct[' + str(i + 1) + '];\n');
    f.write('#endif\n')
f.write('/***************************** Counter Structs ***************************************/\n\n')
f.write('#if NUMBER_OF_COUNTER\n')
f.write('OsCounter CounterStruct[NUMBER_OF_COUNTER] = { \n')
for i in range(NUMBER_OF_COUNTER):
    f.write('#if NUMBER_OF_COUNTER >= ' + str(i + 1) + '\n')
    f.write('                                        { \n');
    f.write('                                          .MaxAllowedValue = OS_COUNTER_MAX_ALLOWED_VALUE_' + str(
        i + 1) + ',\n');
    f.write(
        '                                          .TicksPerBase = OS_COUNTER_TICKS_PER_BASE_' + str(i + 1) + ',\n');
    f.write('                                          .MinCycle = OS_COUNTER_MIN_CYCLE_' + str(i + 1) + ',\n');
    f.write('                                        },\n');
    f.write('#endif\n')
f.write('};\n')
f.write('#endif\n\n\n')

f.write('\n\n\n /***************************** Alarm Structs ***************************************/\n\n')
f.write('#if NUMBER_OF_ALARM != 0 \n')
f.write('OsAlarm AlarmStruct[NUMBER_OF_ALARM] = { \n')
for i in range(NUMBER_OF_ALARM):

    if (i != 0):
        f.write('#if NUMBER_OF_ALARM >= ' + str(i + 1) + '\n')

    f.write('                                    {\n')
    f.write(
        '                                     .pCounterID = (OsCounter *) &CounterStruct[OS_ALARM_COUNTER_REF_' + str(
            i + 1) + '],\n')
    f.write('                                     .Action = OS_ALARM_ACTION_' + str(i + 1) + ',\n')
    f.write('                                     .TaskID = (UBaseType_t *) &OS_ALARM_ACTION_TASK_REF_' + str(
        i + 1) + ',\n')
    f.write('#if OS_ALARM_ACTION_' + str(i + 1) + ' == SETEVENT\n')
    f.write('                                     .EventID = (UBaseType_t *) &OS_ALARM_ACTION_EVENT_REF_' + str(
        i + 1) + ',\n')
    f.write('#endif\n')
    f.write('                                     .AlarmTime = ALARM_TIME_' + str(i + 1) + ' - 1,\n')
    f.write('                                     .CycleTime = CYCLE_TIME_' + str(i + 1) + ',\n')
    f.write('                                     .AutoStart = AUTOSTART_' + str(i + 1) + ',\n')
    f.write('                                    #if ALARM_CALLBACK\n')
    f.write(
        '                                     .AlarmCallBackFunc = (AlarmCallBackFunction_t) ALARM_CALLBACK_FUNCTION_' + str(
            i + 1) + ',\n')
    f.write('                                    #endif\n')
    f.write('                                    },\n')
    if (i != 0):
        f.write('#endif\n')
f.write('};\n')
f.write('#endif\n\n\n')
for i in range(NUMBER_OF_ALARM):
    f.write('#if NUMBER_OF_ALARM >= ' + str(i + 1) + '\n')
    f.write('AlarmType const OS_ALARM_NAME_' + str(i + 1) + ' = (AlarmType) &AlarmStruct[' + str(i) + '];\n');
    f.write('#endif\n')

f.close()
