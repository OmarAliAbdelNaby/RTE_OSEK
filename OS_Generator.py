from Print_OS_XML import *

Head = "/* This file is Auto-Generated to configure the AUTOSAR OS */\n\n\n"
gcfg = "\n/************************** GENERAL CONFIGURATION ***************************/\n"
tcfg = "\n/**************************** TASK CONFIGURATION ****************************/"
acfg = "\n/*************************** ALARM CONFIGURATION ****************************/"
ccfg = "\n/************************* COUNTER CONFIGURATION ****************************/"
ecfg = "\n/*************************** EVENT CONFIGURATION ****************************/"
rcfg = "\n/************************ RESOURCE CONFIGURATION ****************************/"
icfg = "\n*****************************ISR CONFIGURATION*******************************/"

class OsGenerator:
    XmlFile = None
    configOs = None
    FileName = ""
    def __init__(self, XmlFilePath, HeaderFilePath):
        self.FileName = str(HeaderFilePath)
        self.XmlFile = ParseArxml(str(XmlFilePath))
        with open(self.FileName, mode="w+") as self.configOs:
            self.configOs.write(Head)

    def GenerateGeneral_Config_H_(self,General_config):
        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(gcfg)
            self.configOs.write("\n#define CPU_CLOCK_HZ\t\t\t\t\t" + "16000000")
            self.configOs.write("\n#define OSTICKDURATION\t\t\t\t\t" + "1000")
            self.configOs.write("\n#define NUMBER_OF_EXTENDEDTASK\t\t\t" +  str(General_config[0]))
            self.configOs.write("\n#define NUMBER_OF_BASICTASK\t\t\t\t"  +  str(General_config[1]))
            self.configOs.write("\n#define NUMBER_OF_PRIORITES\t\t\t\t"  +  str(General_config[0]))
            self.configOs.write("\n#define NUMBER_OF_EVENTS\t\t\t\t"     +  str(General_config[2]))
            self.configOs.write("\n#define NUMBER_OF_RESOURCES\t\t\t\t"  +  str(General_config[3]))
            self.configOs.write("\n#define NUMBER_OF_COUNTER\t\t\t\t"    +  str(General_config[4]))
            self.configOs.write("\n#define NUMBER_OF_ALARM\t\t\t\t\t"    +  str(General_config[5]))
            self.configOs.write("\n#define NUMBER_OF_ISR\t\t\t\t\t"      +  str(General_config[6]))
            self.configOs.write("\n#define NUMBER_OF_CALLBACK_FUNCTION\t\t" + "0")
            self.configOs.write("\n\n#define ALARM_CALLBACK\t\t\t\t\t" + "0")
            self.configOs.write("\n#define IDLETASK_STACK_SIZE\t\t\t\t" + "128")


    def Task_Config_H_(self):
        TaskList,Taskvalues = self.XmlFile.GetTaskList()
        tID = 0    # ID TASK
        etID = 0   # Special ID for EXTENDED TASK


        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(tcfg)
            for Task in Taskvalues:
                tID += 1

                self.configOs.write("\n\n#define OS_TASK_NAME_" + str(tID) + "\t\t\t\t\t" + Task[0])
                self.configOs.write("\n#define OS_TASK_PRIORITY_" + str(tID) + "\t\t\t\t" + Task[1])
                self.configOs.write("\n#define OS_TASK_SCHEDULE_" + str(tID) + "\t\t\t\t" + Task[4])
                self.configOs.write("\n#define OS_TASK_ACTIVATION_" + str(tID) + "\t\t\t" + Task[2])
                self.configOs.write("\n#define OS_TASK_AUTOSTART_" + str(tID) + "\t\t\t\t" + Task[6])
                self.configOs.write("\n#define OS_TASK_TYPE_" + str(tID) + "\t\t\t\t\t" + Task[5])
                self.configOs.write("\n#define OS_TASK_SIZE_" + str(tID) + "\t\t\t\t\t" + Task[3])

                # This part for Reference and not handed yet
                #task1 = ['T1', 3, 'FULL', 1, 'TRUE', 'EXTENDED', 128, 2, 3, ['Ev1', 'Null'], ['Res1', 'Null', 'Null']]

                if len(Task) > 7:
                    evID = 0  # ID for Event in task
                    resID = 0  # ID for Res in task
                    etID += 1
                    self.configOs.write("\n#define TASK_" + str(etID) + "_NUMBER_OF_EVENT_IN_TASK\t" +str(Task[7]))
                    self.configOs.write("\n#define TASK_" + str(etID) + "_NUMBER_OF_RES_IN_TASK\t" + str(Task[8]))
                    for Event in Task[9]:
                        evID += 1
                        self.configOs.write("\n#define TASK_" + str(etID) + "_EVENT_" + str(evID) + "\t\t\t\t\t" + Event)
                    for Res in Task[10]:
                        resID += 1
                        self.configOs.write("\n#define TASK_" + str(etID) + "_RESOURCE_" + str(resID) + "\t\t\t\t" + Res)

    def Alarm_Config_H_(self):
        AlarmList = self.XmlFile.GetAlarmList()
        aID = 0  # ID Alarm
        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(acfg)
            for alarm in AlarmList:
                aID += 1
                self.configOs.write("\n\n#define OS_ALARM_NAME_" + str(aID) +  "\t\t\t\t\t" + alarm[0])
                self.configOs.write("\n#define AUTOSTART_" + str(aID) + "\t\t\t\t\t\t" + alarm[1])
                self.configOs.write("\n#define ALARM_TIME_" + str(aID) +  "\t\t\t\t\t" + alarm[2])
                self.configOs.write("\n#define CYCLE_TIME_" + str(aID) +  "\t\t\t\t\t" + alarm[3])
                self.configOs.write("\n#define OS_ALARM_COUNTER_REF_" + str(aID) + "\t\t\t" + alarm[4])
                self.configOs.write("\n#define OS_ALARM_ACTIVATE_TASK_REF_" + str(aID) +  "\t" + alarm[5])
                self.configOs.write("\n#define OS_ALARM_CALLBACK_NAME_" + str(aID) + "\t\t" + alarm[8])
                self.configOs.write("\n#define OS_ALARM_SET_EVENT_REF_" + str(aID) +  "\t\t" + alarm[7])
                self.configOs.write("\n#define OS_ALARM_SET_EVENT_TASK_REF_" + str(aID) +  "\t" + alarm[6])
                # self.configOs.write("\n#define ALARM_ACTION_CALLBACK_FUNC_" + str(aID) + "\t\t" + alarm[9])

    def Counter_Config_H_(self):
        CounterList,Countervalues = self.XmlFile.GetCounterList()
        cID = 0     # ID Counter
        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(ccfg)
            for counter in Countervalues:
                cID += 1
                self.configOs.write("\n\n#define OS_COUNTER_Name_" + str(cID) + "\t\t\t\t\t" + counter[0])
                self.configOs.write("\n#define OS_COUNTER_TYPE_" + str(cID) + "\t\t\t\t\t" + counter[1])
                self.configOs.write("\n#define OS_SECONDS_PER_TICK_" + str(cID) + "\t\t\t\t" + counter[2])
                self.configOs.write("\n#define OS_COUNTER_MAX_ALLOWED_VALUE_" + str(cID) + "\t\t" + counter[3])
                self.configOs.write("\n#define OS_COUNTER_TICKS_PER_BASE_" + str(cID) + "\t\t\t" + counter[4])
                self.configOs.write("\n#define OS_COUNTER_MIN_CYCLE_" + str(cID) + "\t\t\t\t" + counter[5])

    def Event_Config_H_(self):
        EventList,Eventvalues = self.XmlFile.GetEventList()
        eID = 0     # ID Event
        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(ecfg)
            for event in Eventvalues:
                eID += 1
                self.configOs.write("\n\n#define OS_EVENT_NAME_" + str(eID) + "\t\t\t\t\t" + event[0])
                self.configOs.write("\n#define OS_EVENT_MASK_" + str(eID) + "\t\t\t\t\t" + event[1])

    def Resource_Config_H_(self):
        ResList,Resvalue = self.XmlFile.GetResourceList()
        rID = 0     # ID Resource
        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(rcfg)
            for res in Resvalue:
                rID += 1
                self.configOs.write("\n\n#define OS_RESOURCE_NAME_" + str(rID) + "\t\t\t\t\t" + res[0])
                self.configOs.write("\n#define OS_RESOURCE_PROPERTY_" + str(rID) + "\t\t\t\t" + res[1])
                #self.configOs.write("\n#define OsResourceLinkedResourceRef" + str(rID) + "\t\t\t\t" + res[2])


    def Isr_Config_H_(self):
        ISRList,ISRvalue = self.XmlFile.GetISRList()
        iID = 0     # ID ISR
        with open(self.FileName, mode="a") as self.configOs:
            self.configOs.write(icfg)
            for isr in ISRvalue:
                iID += 1
                self.configOs.write ( "\n\n#define ISR_NAME_" + str ( iID ) + "\t\t\t\t\t\t\t" + isr [ 0 ] )
                self.configOs.write ( "\n#define OS_ISR_RESOURCE_REF_" + str ( iID ) + "\t\t\t\t" + isr [ 1 ] )
                #self.configOs.write ( "\n#define OsIsrResourceRef"  + str (iID) + "\t\t\t\t" +  )
'''
                if res[2] == "LINKED":
                    self.configOs.write("\n#define OS_RESOURCE_LINKED_RESOURCE_REF_" + str(rID) + "\t" + res[2])
'''
# This main for test only #


if __name__ == '__main__':

    newfile = OsGenerator("Farag_MagdyOS.xml", "Farag_Magdy.h")
    #newfile.GenerateGeneral_Config_H_()
    newfile.Task_Config_H_()
    newfile.Alarm_Config_H_()
    newfile.Counter_Config_H_()
    newfile.Event_Config_H_()
    newfile.Resource_Config_H_()
    #newfile.Isr_Config_H_()
