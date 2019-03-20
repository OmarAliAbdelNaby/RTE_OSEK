from xml.etree import ElementTree as ET

autosar_org = "http://autosar.org/schema/r4.0"
autosar_schema_instance = "http://www.w3.org/2001/XMLSchema-instance"
autosar_schema_location = "http://autosar.org/schema/r4.0 AUTOSAR_4-2-1.xsd"


def indent(elem , level=0) :
    i = "\n" + level * "  "
    if len ( elem ) :
        if not elem.text or not elem.text.strip () :
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip () :
            elem.tail = i
        for elem in elem :
            indent ( elem , level + 1 )
        if not elem.tail or not elem.tail.strip () :
            elem.tail = i
    else :
        if level and (not elem.tail or not elem.tail.strip ()) :
            elem.tail = i


class CreateArxml :
    tree = ET.ElementTree
    directory = ''

    def __init__(self , directory) :
        self.directory = directory

    def CreateDefaultARXML(self) :
        ET.register_namespace ( "" , autosar_schema_instance )
        root = ET.Element ( "AUTOSAR" , { "xmlns" : autosar_org , "xmlns:xsi" : autosar_schema_instance ,
                                          "xsi:schemaLocation" : autosar_schema_location } )

        TopLevel = ET.SubElement ( root , "AR-PACKAGES" )
        ArPackage = ET.SubElement ( TopLevel , "AR-PACKAGE" )

        self.tree = ET.ElementTree ( root )

    def CreateOS(self , ActiveEcuC_Name) :
        self.CreateDefaultARXML ()
        root = self.tree.getroot ()
        ArPackage = root.find ( "AR-PACKAGES/AR-PACKAGE" )

        top = root.find ( "AR-PACKAGES" )
        # print(ArPackage)
        ActiveEcuC = ET.SubElement ( ArPackage , "SHORT-NAME" )
        ActiveEcuC.text = ActiveEcuC_Name
        Elements = ET.SubElement ( ArPackage , "ELEMENTS" )
        ECUC_MODULE_CONFIGURATION_VALUES = ET.SubElement ( Elements , "ECUC-MODULE-CONFIGURATION-VALUES" )
        os = ET.SubElement ( ECUC_MODULE_CONFIGURATION_VALUES , "SHORT-NAME" )
        os.text = "Os"

        containers = ET.SubElement ( ECUC_MODULE_CONFIGURATION_VALUES , "CONTAINERS" )
        # cont1 = ET.SubElement(containers, "ECUC-CONTAINER-VALUE")
        # cont1name = ET.SubElement(cont1, "SHORT-NAME")
        # cont1name.text = "OsTask"

        # cont2 = ET.SubElement(containers, "ECUC-CONTAINER-VALUE")
        # cont2name = ET.SubElement(cont2, "SHORT-NAME")
        # cont2name.text = "OsCounter"

        # cont3 = ET.SubElement(containers, "EECUC-CONTAINER-VALUE")
        # cont3name = ET.SubElement(cont3, "SHORT-NAME")
        # cont3name.text = "OsAlarm"

        # cont4 = ET.SubElement(containers, "ECUC-CONTAINER-VALUE")
        # cont4name = ET.SubElement(cont4, "SHORT-NAME")
        # cont4name.text = "OsResource"

        # cont5 = ET.SubElement(containers, "ECUC-CONTAINER-VALUE")
        # cont5name = ET.SubElement(cont5, "SHORT-NAME")
        # cont5name.text = "OsEvent"

        # cont6 = ET.SubElement(containers, "ECUC-CONTAINER-VALUE")
        # cont6name = ET.SubElement(cont6, "SHORT-NAME")
        # cont6name.text = "OsISR"

        indent ( root )
        self.tree.write ( self.directory )

    def AddMaxElement(self , MaxElemName , value) :
        root = self.tree.getroot ()
        flag = False
        MaxElems = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES" )

        for node in MaxElems.iter () :
            for child in node :
                if child.text == MaxElemName :
                    flag = True
                    continue
                if flag :
                    child.text = str ( value )
                    flag = False
        self.tree.write ( "nawaf.xml" )

    def AddIdleTaskSize(self , size) :
        root = self.tree.getroot ()
        idletask = root.find ( "AR-PACKAGES/AR-PACKAGE/CONFIG-BASE/IDLE-TASK-SIZE" )
        idletask.text = str ( size )
        self.tree.write ( self.directory )

    def AddCallBack(self , state) :
        root = self.tree.getroot ()
        callback = root.find ( "AR-PACKAGES/AR-PACKAGE/CONFIG-BASE/CALLBACK" )
        callback.text = str ( state )
        self.tree.write ( self.directory )

    # task1 = ['T1', 3, 'FULL', 1, 'TRUE', 'EXTENDED', 128, 2, 3, ['Ev1', 'Null'], ['Res1', 'Null', 'Null']]
    def AddTask(self , tasklist) :
        root = self.tree.getroot ()
        containers = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES/CONTAINERS" )
        cont1_for_name = ET.SubElement ( containers , "ECUC-CONTAINER-VALUE" )
        cont1name_for_name = ET.SubElement ( cont1_for_name , "SHORT-NAME" )
        cont1name_for_name.text = str ( tasklist [ 0 ] ) + "OsTask"

        # Block for PARAMETRES#
        PARAMETERS = ET.SubElement ( cont1_for_name , "PARAMETER-VALUES" )

        # Block for OsTaskPriority#
        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        taskpri = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        taskpri.text = "OsTaskPriority"
        Value_taskpri = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_taskpri.text = str ( tasklist [ 1 ] )

        # Block for OsTaskActivation#
        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        taskact = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        taskact.text = "OsTaskActivation"
        Value_taskact = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_taskact.text = str ( tasklist [ 3 ] )

        # Block for OsTaskSize#
        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        tasksize = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        tasksize.text = "OsTaskSize"
        Value_tasksize = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_tasksize.text = str ( tasklist [ 6 ] )

        # Block for OsTaskSchedule#
        ECUC_ENUMERATION_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        tasksched = ET.SubElement ( ECUC_ENUMERATION_PARAM , "SHORT-NAME" )
        tasksched.text = "OsTaskSchedule"
        Value_OsTaskSchedule = ET.SubElement ( ECUC_ENUMERATION_PARAM , "VALUE" )
        Value_OsTaskSchedule.text = str ( tasklist [ 2 ] )

        # Block for OsTaskType#
        ECUC_ENUMERATION_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        tasktype = ET.SubElement ( ECUC_ENUMERATION_PARAM , "SHORT-NAME" )
        tasktype.text = "OsTaskType"
        Value_OsTaskType = ET.SubElement ( ECUC_ENUMERATION_PARAM , "VALUE" )
        Value_OsTaskType.text = str ( tasklist [ 5 ] )

        # Block for OsTaskAutostart#
        ECUC_ENUMERATION_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        tasktype = ET.SubElement ( ECUC_ENUMERATION_PARAM , "SHORT-NAME" )
        tasktype.text = "OsTaskAutostart"
        Value_OsTaskAutostart = ET.SubElement ( ECUC_ENUMERATION_PARAM , "VALUE" )
        Value_OsTaskAutostart.text = str ( tasklist [ 4 ] )

        # Block for Reference#
        REFERENCE_VALUES = ET.SubElement ( cont1_for_name , "REFERENCE-VALUES" )

        # OsTaskEventRef#
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsTaskEventRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsTaskEventRef.text = "OsTaskEventRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsEvent"'''

        # OsTaskResourceRef#
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsTaskResourceRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsTaskResourceRef.text = "OsTaskResourceRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsResource"'''

        indent ( root )
        self.tree.write ( self.directory )

    def AddCounter(self , countertable) :
        root = self.tree.getroot ()
        containers = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES/CONTAINERS" )
        cont2_for_name = ET.SubElement ( containers , "ECUC-CONTAINER-VALUE" )
        cont2name_for_name = ET.SubElement ( cont2_for_name , "SHORT-NAME" )
        cont2name_for_name.text = str ( countertable [ 0 ] ) + "OsCounter"

        '''
        counter1 = [counter_name',type_of_counter,OsSecondsPerTick,
                     OsCounterMaxAllowedValue,OsCounterTicksPerBase,OsCounterMinCycle] 
        Ex: counter1 = ['Counter_1','HARDWARE',2, 65535, 7, 128]  # we remove id '''

        PARAMETERS = ET.SubElement ( cont2_for_name , "PARAMETER-VALUES" )

        ECUC_ENUMERATION_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        OsCounterType = ET.SubElement ( ECUC_ENUMERATION_PARAM , "SHORT-NAME" )
        OsCounterType.text = "OsCounterType"
        Value_OsCounterType = ET.SubElement ( ECUC_ENUMERATION_PARAM , "VALUE" )
        Value_OsCounterType.text = str ( countertable [ 1 ] )

        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        OsSecondsPerTick = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        OsSecondsPerTick.text = "OsSecondsPerTick"
        Value_OsSecondsPerTick = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_OsSecondsPerTick.text = str ( countertable [ 2 ] )

        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        OsCounterMaxAllowedValue = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        OsCounterMaxAllowedValue.text = "OsCounterMaxAllowedValue"
        Value_OsCounterMaxAllowedValue = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_OsCounterMaxAllowedValue.text = str ( countertable [ 3 ] )

        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        OsCounterTicksPerBase = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        OsCounterTicksPerBase.text = "OsCounterTicksPerBase"
        Value_OsCounterTicksPerBase = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_OsCounterTicksPerBase.text = str ( countertable [ 4 ] )

        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        OsCounterMinCycle = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        OsCounterMinCycle.text = "OsCounterMinCycle"
        Value_OsCounterMinCycle = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_OsCounterMinCycle.text = str ( countertable [ 5 ] )

        indent ( root )
        self.tree.write ( self.directory )

    def AddAlarm(self , alarmtable) :
        root = self.tree.getroot ()
        containers = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES/CONTAINERS" )
        cont3_for_name = ET.SubElement ( containers , "ECUC-CONTAINER-VALUE" )
        cont3name_for_name = ET.SubElement ( cont3_for_name , "SHORT-NAME" )
        cont3name_for_name.text = str ( alarmtable [ 0 ] ) + "OsAlarm"

        # Block for Parameters
        PARAMETERS = ET.SubElement ( cont3_for_name , "PARAMETER-VALUES" )

        # OsAlarmAutostart
        ECUC_INTEGER_PARAM_VALUE = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        alarmtype = ET.SubElement ( ECUC_INTEGER_PARAM_VALUE , "SHORT-NAME" )
        alarmtype.text = "AUTOSTART"
        Value_alarmtype = ET.SubElement ( ECUC_INTEGER_PARAM_VALUE , "VALUE" )
        Value_alarmtype.text = str ( alarmtable [ 1 ] )

        # Block for Reference
        REFERENCE_VALUES = ET.SubElement ( cont3_for_name , "REFERENCE-VALUES" )

        # OsAlarmCounterRef
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsAlarmCounterRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsAlarmCounterRef.text = "OsAlarmCounterRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsCounter"'''

        # Block for Sub-Containers
        SUB_CONTAINERS = ET.SubElement ( cont3_for_name , "SUB-CONTAINERS" )

        # Block for OsAlarmAction
        ECUC_CONTAINER_VALUE = ET.SubElement ( SUB_CONTAINERS , "ECUC-CONTAINER-VALUE" )
        OsAlarmAction = ET.SubElement ( ECUC_CONTAINER_VALUE , "SHORT-NAME" )
        OsAlarmAction.text = "OsAlarmAction"

        # Block for SUB-CONTAINERS in OsAlarmAction
        SUB_CONTAINERS = ET.SubElement ( ECUC_CONTAINER_VALUE , "SUB-CONTAINERS" )

        # Block for OsAlarmActivateTask
        ECUC_CONTAINER_VALUE = ET.SubElement ( SUB_CONTAINERS , "ECUC-CONTAINER-VALUE" )
        OsAlarmActivateTask = ET.SubElement ( ECUC_CONTAINER_VALUE , "SHORT-NAME" )
        OsAlarmActivateTask.text = "OsAlarmActivateTask"

        # Block for Reference in OsAlarmActivateTask
        REFERENCE_VALUES = ET.SubElement ( ECUC_CONTAINER_VALUE , "REFERENCE-VALUES" )

        # Block for OsAlarmActivateTaskRef
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsAlarmActivateTaskRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsAlarmActivateTaskRef.text = "OsAlarmActivateTaskRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST= "AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsTask"'''

        # Block for OsAlarmCallback
        ECUC_CONTAINER_VALUE = ET.SubElement ( SUB_CONTAINERS , "ECUC-CONTAINER-VALUE" )
        OsAlarmCallback = ET.SubElement ( ECUC_CONTAINER_VALUE , "SHORT-NAME" )
        OsAlarmCallback.text = "OsAlarmCallback"

        # Block for parameters
        PARAMETERS = ET.SubElement ( ECUC_CONTAINER_VALUE , "PARAMETER-VALUES" )

        # Block for OsAlarmCallbackName
        ECUC_ENUMERATION_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        OsAlarmCallbackName = ET.SubElement ( ECUC_ENUMERATION_PARAM , "SHORT-NAME" )
        OsAlarmCallbackName.text = "OsAlarmCallbackName"
        Value_OsAlarmCallbackName = ET.SubElement ( ECUC_ENUMERATION_PARAM , "VALUE" )
        Value_OsAlarmCallbackName.text = str ( alarmtable [ 2 ] )

        # Block for OsAlarmSetEvent
        ECUC_CONTAINER_VALUE = ET.SubElement ( SUB_CONTAINERS , "ECUC-CONTAINER-VALUE" )
        OsAlarmSetEvent = ET.SubElement ( ECUC_CONTAINER_VALUE , "SHORT-NAME" )
        OsAlarmSetEvent.text = "OsAlarmSetEvent"

        # Block for references in OsAlarmSetEvent
        REFERENCE_VALUES = ET.SubElement ( ECUC_CONTAINER_VALUE , "REFERENCE-VALUES" )

        # Block for OsAlarmSetEventRef
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsAlarmSetEventRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsAlarmSetEventRef.text = "OsAlarmSetEventRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsEvent"'''

        # Block for OsAlarmSetEventTaskRef
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsAlarmSetEventTaskRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsAlarmSetEventTaskRef.text = "OsAlarmSetEventTaskRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsTask"'''

        indent ( root )
        self.tree.write ( self.directory )

    def AddResource(self , Resourcetable) :
        root = self.tree.getroot ()
        containers = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES/CONTAINERS" )
        cont4_for_name = ET.SubElement ( containers , "ECUC-CONTAINER-VALUE" )
        cont4name_for_name = ET.SubElement ( cont4_for_name , "SHORT-NAME" )
        cont4name_for_name.text = str ( Resourcetable [ 0 ] ) + "OsResource"

        PARAMETERS = ET.SubElement ( cont4_for_name , "PARAMETER-VALUES" )

        ECUC_ENUMERATION_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        resprop = ET.SubElement ( ECUC_ENUMERATION_PARAM , "SHORT-NAME" )
        resprop.text = "OsResourceProperty"
        Value_OsResourceProperty = ET.SubElement ( ECUC_ENUMERATION_PARAM , "VALUE" )
        Value_OsResourceProperty.text = str ( Resourcetable [ 1 ] )

        if Resourcetable [ 1 ] == "LINKED" :
            # Block for Reference#
            REFERENCE_VALUES = ET.SubElement ( cont4_for_name , "REFERENCE-VALUES" )

            # OsTaskEventRef#
            ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
            OsTaskEventRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
            OsTaskEventRef.text = "OsResourceLinkedResourceRef"
            VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
            VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\\''' + \
                             Resourcetable [ 2 ] + '''"'''

        indent ( root )
        self.tree.write ( self.directory )

    def AddEvent(self , eventtable) :
        root = self.tree.getroot ()
        containers = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES/CONTAINERS" )

        cont5_for_name = ET.SubElement ( containers , "ECUC-CONTAINER-VALUE" )
        cont5name_for_name = ET.SubElement ( cont5_for_name , "SHORT-NAME" )
        cont5name_for_name.text = str ( eventtable [ 0 ] ) + "OsEvent"

        PARAMETERS = ET.SubElement ( cont5_for_name , "PARAMETER-VALUES" )

        ECUC_INTEGER_PARAM = ET.SubElement ( PARAMETERS , "ECUC-NUMERICAL-PARAM-VALUE" )
        eventmask = ET.SubElement ( ECUC_INTEGER_PARAM , "SHORT-NAME" )
        eventmask.text = "OsEventMask"
        Value_eventmask = ET.SubElement ( ECUC_INTEGER_PARAM , "VALUE" )
        Value_eventmask.text = str ( eventtable [ 1 ] )

        indent ( root )
        self.tree.write ( self.directory )

    def AddISR(self , isrtable) :
        root = self.tree.getroot ()
        containers = root.find ( "AR-PACKAGES/AR-PACKAGE/ELEMENTS/ECUC-MODULE-CONFIGURATION-VALUES/CONTAINERS" )
        cont6_for_name = ET.SubElement ( containers , "ECUC-CONTAINER-VALUE" )
        cont6name_for_name = ET.SubElement ( cont6_for_name , "SHORT-NAME" )
        cont6name_for_name.text = str ( isrtable [ 0 ] ) + "OsISR"

        # Block for parameter
        PARAMETERS = ET.SubElement ( cont6_for_name , "PARAMETER-VALUES" )

        # Block for OsIsrCategory
        ECUC_NUMERICAL_PARAM = ET.SubElement ( PARAMETERS , "ECUC-TEXTUAL-PARAM-VALUE" )
        OsIsrCategory = ET.SubElement ( ECUC_NUMERICAL_PARAM , "SHORT-NAME" )
        OsIsrCategory.text = "OsIsrCategory"
        Value_OsIsrCategory = ET.SubElement ( ECUC_NUMERICAL_PARAM , "VALUE" )
        Value_OsIsrCategory.text = str ( isrtable [ 1 ] )

        # Block for reference
        REFERENCE_VALUES = ET.SubElement ( cont6_for_name , "REFERENCE-VALUES" )

        # Block for OsIsrResourceRef
        ECUC_REFERENCE_VALUE = ET.SubElement ( REFERENCE_VALUES , "ECUC-REFERENCE-VALUE" )
        OsIsrResourceRef = ET.SubElement ( ECUC_REFERENCE_VALUE , "SHORT-NAME" )
        OsIsrResourceRef.text = "OsIsrResourceRef"
        VALUE_REF = ET.SubElement ( ECUC_REFERENCE_VALUE , "VALUE-REF" )
        VALUE_REF.text = '''DEST="AUTOSAR\AR-PACKAGES\AR-PACKAGE\ELEMENTS\ECUC-MODULE-CONFIGURATION-VALUES\OsResource"'''

        indent ( root )
        self.tree.write ( self.directory )


class ParseArxml :
    tree = ET.parse

    def __init__(self , XmlFilePath) :
        self.tree = ET.parse ( XmlFilePath )

    def GetGeneralConfig(self) :
        GeneralConfigDict = { }
        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}CONFIG-BASE" :
                for child in node :
                    if child.tag == "{http://autosar.org/schema/r4.0}MAX-NUMBER-OF-ELEMENTS" :
                        for grandchild in child :
                            if grandchild.tag == "{http://autosar.org/schema/r4.0}MAX-NUMBER-OF-ELEMENT" :
                                for max in grandchild :
                                    if max.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                        key = max.text
                                    if max.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                        num = max.text
                                        GeneralConfigDict [ key ] = num
                    elif child.tag == "{http://autosar.org/schema/r4.0}IDLE-TASK-SIZE" :
                        GeneralConfigDict [ "IDLE_TASK_SIZE" ] = child.text
                    elif child.tag == "{http://autosar.org/schema/r4.0}CALLBACK" :
                        GeneralConfigDict [ "ALARM_CALLBACK" ] = child.text
        return GeneralConfigDict

    def GetTaskList(self) :
        # tasklist = []
        # taskparameters = []
        # eventlist = []
        # reslist = []

        Tasklist = [ ]
        Taskvalues = [ ]

        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" :
                for child1 in node :
                    if child1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" and "OsTask" in child1.text :
                        Tasklist_temp = [ 'TaskName' ]
                        Taskvalues_temp = [ ]
                        Taskvalues_temp.append ( child1.text [ :-6 ] )  # for name
                        for child2 in node :
                            if child2.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :
                                for gchild1 in child2 :
                                    if gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-TEXTUAL-PARAM-VALUE" or gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-NUMERICAL-PARAM-VALUE" :
                                        for ggchild1 in gchild1 :
                                            if ggchild1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Tasklist_temp.append ( ggchild1.text )
                                            elif ggchild1.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                Taskvalues_temp.append ( ggchild1.text )


                            elif child2.tag == "{http://autosar.org/schema/r4.0}REFERENCE-VALUES" :
                                for gchild2 in child2 :
                                    if gchild2.tag == "{http://autosar.org/schema/r4.0}ECUC-REFERENCE-VALUE" :
                                        for ggchild2 in gchild2 :
                                            if ggchild2.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Tasklist_temp.append ( ggchild2.text )
                                            elif ggchild2.tag == "{http://autosar.org/schema/r4.0}VALUE-REF" :
                                                Taskvalues_temp.append ( ggchild2.text )

                        Tasklist.append ( Tasklist_temp )
                        Taskvalues.append ( Taskvalues_temp )

        return Taskvalues
        #Tasklist is removed

        '''
        for node in self.tree.iter():
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE":
                for child in node:
                    if taskparameters:
                        x = []
                        x.extend(taskparameters)
                        tasklist.append(x)
                        print(taskparameters)
                    taskparameters[:] = []
                    eventlist[:] = []
                    reslist[:] = []
                    if child.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES":
                        for grandchild in child:
                            if grandchild.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME":
                                taskparameters.append(grandchild.text)
                                continue
                            elif grandchild.tag == "{http://autosar.org/schema/r4.0}PRIORITY":
                                taskparameters.append(grandchild.text)
                                continue
                            elif grandchild.tag == "{http://autosar.org/schema/r4.0}SCHEDULE":
                                taskparameters.append(grandchild.text)
                                continue
                            elif grandchild.tag == "{http://autosar.org/schema/r4.0}ACTIVATION":
                                taskparameters.append(grandchild.text)
                                continue
                            elif grandchild.tag == "{http://autosar.org/schema/r4.0}AUTOSTART":
                                taskparameters.append(grandchild.text)
                                continue
                            elif grandchild.tag == "{http://autosar.org/schema/r4.0}TASK-TYPE":
                                taskparameters.append(grandchild.text)
                                continue
                            elif grandchild.tag == "{http://autosar.org/schema/r4.0}TASK-SIZE":
                                taskparameters.append(grandchild.text)
                                continue
                            if taskparameters[5] == "EXTENDED":
                                if grandchild.tag == "{http://autosar.org/schema/r4.0}MAX-OF-EVENT-IN-TASK":
                                    taskparameters.append(grandchild.text)
                                    continue
                                elif grandchild.tag == "{http://autosar.org/schema/r4.0}MAX-OF-RESOURCE-IN-TASK":
                                    taskparameters.append(grandchild.text)
                                    continue
                                elif grandchild.tag == "{http://autosar.org/schema/r4.0}EVENT":
                                    for event in grandchild:
                                        eventlist.append(event.text)
                                        if len(eventlist) == int(taskparameters[7]):
                                            y = []
                                            y.extend(eventlist)
                                            taskparameters.append(y)
                                    continue
                                elif grandchild.tag == "{http://autosar.org/schema/r4.0}RESOURCE":
                                    for res in grandchild:
                                        reslist.append(res.text)
                                        if len(reslist) == int(taskparameters[8]):
                                            y = []
                                            y.extend(reslist)
                                            taskparameters.append(y)

        return tasklist
'''

    def GetCounterList(self) :
        counterlist = [ ]
        countervalues = [ ]
        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" :
                for child1 in node :
                    if child1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" and "OsCounter" in child1.text :

                        for child2 in node :
                            if child2.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :
                                counterlist_temp = [ 'counterName' ]
                                countervalues_temp = [ ]
                                countervalues_temp.append ( child1.text [ :-9 ] )  # for name
                                for gchild1 in child2 :
                                    if gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-TEXTUAL-PARAM-VALUE" or gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-NUMERICAL-PARAM-VALUE" :
                                        for ggchild1 in gchild1 :
                                            if ggchild1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                counterlist_temp.append ( ggchild1.text )
                                            elif ggchild1.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                countervalues_temp.append ( ggchild1.text )

                                counterlist.append ( counterlist_temp )
                                countervalues.append ( countervalues_temp )

        return counterlist , countervalues

    def GetEventList(self) :
        Eventlist = [ ]
        Eventvalues = [ ]
        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" :
                for child1 in node :
                    if child1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" and "OsEvent" in child1.text :  # kda a7na d5lna fl event mazboot
                        for child2 in node :
                            if child2.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :  # kda d5lna gwa al parameters
                                Eventlist_temp = [ 'EventName' ]
                                Eventvalues_temp = [ ]
                                Eventvalues_temp.append ( child1.text [ :-7 ] )  # for name
                                for child3 in child2 :
                                    if child3.tag == "{http://autosar.org/schema/r4.0}ECUC-NUMERICAL-PARAM-VALUE" :
                                        for child4 in child3 :
                                            if child4.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Eventlist_temp.append ( child4.text )
                                            if child4.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                Eventvalues_temp.append ( child4.text )

                                Eventlist.append ( Eventlist_temp )
                                Eventvalues.append ( Eventvalues_temp )

        return Eventlist , Eventvalues

    def GetResourceList(self) :
        Resourcelist = [ ]
        Resourcevalues = [ ]
        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" :
                for child1 in node :
                    if child1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" and "OsResource" in child1.text :
                        Resourcelist_temp = [ 'ResourceName' ]
                        Resourcevalues_temp = [ ]
                        Resourcevalues_temp.append ( child1.text [ :-10 ] )  # for name
                        for child2 in node :
                            if child2.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :

                                for gchild1 in child2 :
                                    if gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-TEXTUAL-PARAM-VALUE" :
                                        for ggchild1 in gchild1 :
                                            if ggchild1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Resourcelist_temp.append ( ggchild1.text )
                                            elif ggchild1.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                Resourcevalues_temp.append ( ggchild1.text )


                            elif child2.tag == "{http://autosar.org/schema/r4.0}REFERENCE-VALUES" :
                                for gchild2 in child2 :
                                    if gchild2.tag == "{http://autosar.org/schema/r4.0}ECUC-REFERENCE-VALUE" :
                                        for ggchild2 in gchild2 :
                                            if ggchild2.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Resourcelist_temp.append ( ggchild2.text )
                                            elif ggchild2.tag == "{http://autosar.org/schema/r4.0}VALUE-REF" :
                                                Resourcevalues_temp.append ( ggchild2.text [ 79 :-1 ] )

                        Resourcelist.append ( Resourcelist_temp )
                        Resourcevalues.append ( Resourcevalues_temp )

        return Resourcelist , Resourcevalues

    def GetAlarmList(self) :

        Alarmlist = [ ]
        Alarmvalues = [ ]
        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" :
                for child1 in node :
                    if child1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" and "OsAlarm" in child1.text :
                        Alarmlist_temp = [ 'AlarmName' ]
                        Alarmvalues_temp = [ ]
                        Alarmvalues_temp.append ( child1.text [ :-7 ] )

                        for child2 in node :
                            if child2.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :
                                for gchild1 in child2 :
                                    if gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-NUMERICAL-PARAM-VALUE" :
                                        for ggchild1 in gchild1 :
                                            if ggchild1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Alarmlist_temp.append ( ggchild1.text )
                                            elif ggchild1.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                Alarmvalues_temp.append ( ggchild1.text )

                            elif child2.tag == "{http://autosar.org/schema/r4.0}REFERENCE-VALUES" :
                                for gchild2 in child2 :
                                    if gchild2.tag == "{http://autosar.org/schema/r4.0}ECUC-REFERENCE-VALUE" :
                                        for ggchild2 in gchild2 :
                                            if ggchild2.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Alarmlist_temp.append ( ggchild2.text )
                                            elif ggchild2.tag == "{http://autosar.org/schema/r4.0}VALUE-REF" :
                                                Alarmvalues_temp.append ( ggchild2.text )

                            elif child2.tag == "{http://autosar.org/schema/r4.0}SUB-CONTAINERS" :
                                for child3 in child2 :
                                    if child3.tag == " {http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE " :
                                        for gchild3 in child3 :
                                            if gchild3.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                Alarmlist_temp.append ( gchild3.text )
                                            elif gchild3.tag == "{http://autosar.org/schema/r4.0} SUB-CONTAINERS" :
                                                for ggchild3 in gchild3 :
                                                    if ggchild3.tag == " {http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE " :
                                                        for gggchild3 in ggchild3 :
                                                            if gggchild3.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                                Alarmlist_temp.append ( gggchild3.text )
                                                            elif gggchild3.tag == "{http://autosar.org/schema/r4.0}REFERENCE-VALUES" :
                                                                for ggggchild3 in ggggchild3 :
                                                                    if ggggchild3.tag == "{http://autosar.org/schema/r4.0}ECUC-REFERENCE-VALUE" :
                                                                        for gggggchild3 in ggggchild3 :
                                                                            if gggggchild3.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                                                Alarmlist_temp.append ( gggggchild3.text )
                                                                            elif gggggchild3.tag == "{http://autosar.org/schema/r4.0}VALUE-REF" :
                                                                                Alarmvalues_temp.append ( gggggchild3.text )
                                                            elif gggchild3.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :
                                                                for ggggchild3 in gggchild3 :
                                                                    if ggggchild3.tag == "{http://autosar.org/schema/r4.0}ECUC-TEXTUAL-PARAM-VALUE" :
                                                                        for gggggchild3 in ggggchild3 :
                                                                            if gggggchild3.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                                                Alarmlist_temp.append ( gggggchild3.text )
                                                                            elif gggggchild3.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                                                Alarmvalues_temp.append ( gggggchild3.text )

                        Alarmlist.append ( Alarmlist_temp )
                        Alarmvalues.append ( Alarmvalues_temp )

        return Alarmlist , Alarmvalues

    def GetISRList(self) :
        ISRlist = [ ]
        ISRvalues = [ ]

        for node in self.tree.iter () :
            if node.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" :
                for child1 in node :
                    if child1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" and "OsISR" in child1.text :
                        ISRlist_temp = [ 'ISRName' ]
                        ISRvalues_temp = [ ]
                        ISRvalues_temp.append ( child1.text [ :-5 ] )

                        for child2 in node :
                            if child2.tag == "{http://autosar.org/schema/r4.0}PARAMETER-VALUES" :
                                for gchild1 in child2 :
                                    if gchild1.tag == "{http://autosar.org/schema/r4.0}ECUC-TEXTUAL-PARAM-VALUE" :
                                        for ggchild1 in gchild1 :
                                            if ggchild1.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                ISRlist_temp.append ( ggchild1.text )
                                            elif ggchild1.tag == "{http://autosar.org/schema/r4.0}VALUE" :
                                                ISRvalues_temp.append ( ggchild1.text )
                            elif child2.tag == "{http://autosar.org/schema/r4.0}REFERENCE-VALUES" :
                                for gchild2 in child2 :
                                    if gchild2.tag == "{http://autosar.org/schema/r4.0}ECUC-REFERENCE-VALUE" :
                                        for ggchild2 in gchild2 :
                                            if ggchild2.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME" :
                                                ISRlist_temp.append ( ggchild2.text )
                                            elif ggchild2.tag == "{http://autosar.org/schema/r4.0}VALUE-REF" :
                                                ISRvalues_temp.append ( ggchild2.text )

                        ISRlist.append ( ISRlist_temp )
                        ISRvalues.append ( ISRvalues_temp )

        return ISRlist , ISRvalues


if __name__ == '__main__' :
    # task = [name , priortity, activation ,size , schedule , type , autostart]
    task1 = [ 'T1' , 3 , 'FULL' , 1 , 'TRUE' , 'EXTENDED' , 128 , 2 , 3 , [ 'Ev1' , 'Null' ] ,
              [ 'Res1' , 'Null' , 'Null' ] ]
    task2 = [ 'T2' , 2 , 'FULL' , 1 , 'FALSE' , 'EXTENDED' , 128 , 1 , 1 , [ 'Ev2' ] , [ 'Res2' ] ]

    # COUNTER_NAWAF[0, 65535, 7, 128]
    # counter1 = [counter_name',type_of_counter,OsSecondsPerTick, OsCounterMaxAllowedValue,OsCounterTicksPerBase,OsCounterMinCycle]
    counter1 = [ 'Counter_1' , 'HARDWARE' , 2 , 65535 , 7 , 128 ]  # we remove id
    counter2 = [ 'Counter_2' , 'SOFTWARE' , 5 , 65539 , 3 , 122 ]  # we remove id

    # ALARM_NAWAF =["periodic", 0, "TRUE", 500, 3, "SETEVENT", "T1", "Ev1"]
    alarm1 = [ "alarm1" , "TRUE" , "FUNCTION_NAME" , "TRUE" , 500 , 3 , "SETEVENT" , "T1" , "Ev1" ]
    alarm2 = [ "alarm2" , "False" , 0 , "FALSE" , 600 , 5 , "ACTIVATETASK" , "T2" ]
    #alarm3 = []
    #---------name-----

    # RESOURCE_NAWAF = ["Res1", "STANDARD"]
    resource1 = [ "Resource1" , "INTERNAL" ]
    resource2 = [ "Resource2" , "LINKED" , "Resource1" ]

    event1 = [ "Ev1" , 200 ]
    event2 = [ "Ev2" , 5 ]

    Isr1 = [ "ISR1" , "CATEGORY_1" ]
    Isr2 = [ "ISR2" , "CATEGORY_2" ]

    NewXML = CreateArxml ( 'Farag_MagdyOS.xml' )
    # NewXML.CreateDefaultARXML()
    NewXML.CreateOS ( 'ActiveEcuC' )
    # NewXML.AddMaxElement("NUM_OF_ALARM", 1)
    # NewXML.AddMaxElement("NUM_OF_EVENT", 3)           # hna al mfrod n7t fn
    # NewXML.AddMaxElement("NUM_OF_ISR", 4)
    # NewXML.AddMaxElement("NUM_OF_COUNTER", 1)
    # NewXML.AddMaxElement("NUM_OF_BASIC", 3)
    # NewXML.AddMaxElement("NUM_OF_CALLBACK", 0)
    # NewXML.AddMaxElement("NUM_OF_EXTENDED", 2)
    # NewXML.AddMaxElement("NUM_OF_RESOURCE", 4)
    # NewXML.AddIdleTaskSize(128)
    # NewXML.AddCallBack(0)
    NewXML.AddTask ( task1 )
    NewXML.AddTask ( task2 )
    NewXML.AddCounter ( counter1 )
    NewXML.AddCounter ( counter2 )
    NewXML.AddAlarm ( alarm1 )
    NewXML.AddAlarm ( alarm2 )
    NewXML.AddResource ( resource1 )
    NewXML.AddResource ( resource2 )
    NewXML.AddEvent ( event1 )
    #NewXML.AddEvent([key, 200])
    NewXML.AddEvent ( event2 )
    NewXML.AddISR ( Isr1 )
    NewXML.AddISR ( Isr2 )

    #parsexml = ParseArxml ( "Farag_MagdyOS.xml" )
    # print(parsexml.GetGeneralConfig())
    #print (parsexml.GetTaskList())
    #print ( parsexml.GetCounterList () )
    #print ( parsexml.GetEventList () )
    #print ( parsexml.GetResourceList () )
    #print(parsexml.GetAlarmList())
    #print ( parsexml.GetISRList () )
