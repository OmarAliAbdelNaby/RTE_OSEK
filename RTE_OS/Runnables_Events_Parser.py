import xml.etree.ElementTree as ET

class Component:
    PportsOfDataWriteElementsList = []
    def __init__(self, XmlFilePath):
       self.XmlFilePath = XmlFilePath

    def Get_SWC(self):
        SWC_List= []
        SWC_List.append(self.Get_Runnables())
        #SWC_List.append(self.Get_Ports())



        return SWC_List



    def Get_Runnables(self):
        tree = ET.parse(self.XmlFilePath)   #parse the file
        root = tree.getroot()
        Runnable_Name = ""
        Output_Dictionary = {}
        DataElementsPerRunnable = []
        PortsPerRunnable = []
        ListperRunnable = []
        RUNNABLES_LIST=[]
        for node in tree.iter():
            #check if the current node's tag is RUNNABLES
            if(node.tag == "{http://autosar.org/schema/r4.0}RUNNABLES"):
            # iterate on all the children
                for child in node:
                # iterate on all grandchildren because the needed tags are grand children of RUNNABLES and not children
                    DataElementsPerRunnable = []
                    PortsPerRunnable = []
                    for grandchild in child:
                        # if the SHORT-NAME tag is found return the name value
                        if(grandchild.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                            Runnable_Name = grandchild.text
                            #print(grandchild.text)
                        # if the CAN-BE-INVOKED-CONCURRENTLY tag is found --> return the value as a dictionary value and the runnable name as a key
                        if((grandchild.tag == "{http://autosar.org/schema/r4.0}DATA-RECEIVE-POINT-BY-VALUES") #EDITED
                          or (grandchild.tag == "{http://autosar.org/schema/r4.0}DATA-SEND-POINTS")
                          or (grandchild.tag == "{http://autosar.org/schema/r4.0}DATA-WRITE-ACCESSS") #EDITED
                          or (grandchild.tag == "{http://autosar.org/schema/r4.0}DATA-READ-ACCESSS")): #EDITED
                            for xgrandchild in grandchild:
                                for xxgrandchild in xgrandchild:
                                    for xxxgrandchild in xxgrandchild:
                                        #del ListperRunnable[:]
                                        '''DataElementsPerRunnable = []
                                        PortsPerRunnable = []
                                        ListperRunnable = []'''
                                        for xxxxgrandchild in xxxgrandchild:
                                            if(xxxxgrandchild.tag == "{http://autosar.org/schema/r4.0}PORT-PROTOTYPE-REF"):
                                                PortsPerRunnable.append(xxxxgrandchild.text.split("/")[3])
                                            if(xxxxgrandchild.tag == "{http://autosar.org/schema/r4.0}TARGET-DATA-PROTOTYPE-REF"):
                                                DataElementsPerRunnable.append(xxxxgrandchild.text.split("/")[4]) #EDITED
                    ListperRunnable.append(PortsPerRunnable)
                    ListperRunnable.append(DataElementsPerRunnable)
                    #Each Runnable has a dictionary of it short name as its key and a list of 2 lists [[Ports],[DataElements]]
                    Output_Dictionary[Runnable_Name]= ListperRunnable
                    DataElementsPerRunnable = []
                    PortsPerRunnable = []
                    ListperRunnable = []

        return Output_Dictionary
    def Get_Timing_Events_Name_And_Period(self):
         tree = ET.parse(self.XmlFilePath)   #parse the file
         root = tree.getroot()
         ShortName = ""
         TIMING_LIST=["PERIOD","START-ON-EVENT-REF"]
         List_of_Dictionaries=[]
         for node in tree.iter():
            if(node.tag == "{http://autosar.org/schema/r4.0}TIMING-EVENT"):
               Output_Dictionary = {}
               TIMING_LIST=["",""]
               # iterate on all the children because the needed tags are children of TIMING-EVENT
               for child in node:
                  if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                      ShortName = child.text
                  if(child.tag == "{http://autosar.org/schema/r4.0}START-ON-EVENT-REF"):
                         TIMING_LIST[1] = child.text.split("/")[4]
                  if(child.tag == "{http://autosar.org/schema/r4.0}PERIOD"):
                      # add the timing event name as key to the dictionary and the period as a value to the key
                      TIMING_LIST[0]=child.text
               Output_Dictionary[ShortName] = TIMING_LIST
               List_of_Dictionaries.append(Output_Dictionary)
         return List_of_Dictionaries

    def Get_Init_Events(self):
         tree = ET.parse(self.XmlFilePath)   #parse the file
         root = tree.getroot()
         ShortName = ""
         List_of_Dictionaries=[]
         INIT_LIST="START-ON-EVENT-REF"
         Output_Dictionary = {}
         for node in tree.iter():

            if (node.tag == "{http://autosar.org/schema/r4.0}INIT-EVENT"):
                  INIT_LIST=[""]
                  Output_Dictionary = {}
                  # iterate on all the children because the needed tags are children of INIT-EVENT
                  for child in node:
                      if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                         ShortName = child.text
                      if(child.tag == "{http://autosar.org/schema/r4.0}START-ON-EVENT-REF"):
                         INIT_LIST = child.text.split("/")[4]
                  Output_Dictionary[ShortName] = INIT_LIST #################see how to use this later
                  List_of_Dictionaries.append(Output_Dictionary)
         return List_of_Dictionaries


    def Get_Data_Recieved_Events(self):
         tree = ET.parse(self.XmlFilePath)   #parse the file
         root = tree.getroot()
         ShortName = ""
         List_of_Dictionaries=[]
         DATA_RECEIVED_LIST=["CONTEXT_R_PORT_REF" , "TARGET_DATA_ELEMENT_REF","START-ON-EVENT-REF"]
         Output_Dictionary = {}
         for node in tree.iter():
            if((node.tag == "{http://autosar.org/schema/r4.0}DATA-RECEIVED-EVENT")
              or(node.tag == "{http://autosar.org/schema/r4.0}DATA-RECEIVE-ERROR-EVENT")) : #EDITED
               Output_Dictionary = {}
               DATA_RECEIVED_LIST=["","",""]
               # iterate on all the children because the needed tags are children of DATA-RECEIVED-EVENT
               for child in node:
                  if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                      ShortName = child.text
                  if(child.tag == "{http://autosar.org/schema/r4.0}START-ON-EVENT-REF"):
                      DATA_RECEIVED_LIST[2] = child.text.split("/")[4]
                  if(child.tag == "{http://autosar.org/schema/r4.0}DATA-IREF"):
                      for grandchild in child:
                         if(grandchild.tag == "{http://autosar.org/schema/r4.0}CONTEXT-R-PORT-REF"):
                            # add the R-port as the First value to DATA_RECEIVED_LIST
                            DATA_RECEIVED_LIST[0] = grandchild.text.split("/")[3]
                         if(grandchild.tag == "{http://autosar.org/schema/r4.0}TARGET-DATA-ELEMENT-REF"):
                            # add the Data-elment as the second value to DATA_RECEIVED_LIST
                            DATA_RECEIVED_LIST[1] = grandchild.text.split("/")[4] #EDITED

                  # add the short name as key to the dictionary and the DATA_RECEIVED_LIST of Type, Data-elment , R-port and Runnable as a value to the key
               Output_Dictionary[ShortName] = DATA_RECEIVED_LIST
               List_of_Dictionaries.append(Output_Dictionary)
         return List_of_Dictionaries

    def Get_Operation_Invoked_Events(self):
         tree = ET.parse(self.XmlFilePath)   #parse the file
         root = tree.getroot()
         ShortName = ""

         List_of_Dictionaries=[]
         OPERATION_INVOKED_LIST= ["CONTEXT_P_PORT_REF","TARGET_PROVIDED_OPERATION_REF","START-ON-EVENT-REF"]

         Output_Dictionary = {}

         for node in tree.iter():
            if(node.tag == "{http://autosar.org/schema/r4.0}OPERATION-INVOKED-EVENT"):
               Output_Dictionary = {}
               OPERATION_INVOKED_LIST= ["","",""]

               # iterate on all the children because the needed tags are children of OPERATION-INVOKED-EVENT
               for child in node:

                  if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                      ShortName = child.text

                  if(child.tag == "{http://autosar.org/schema/r4.0}START-ON-EVENT-REF"):
                      OPERATION_INVOKED_LIST[2] = child.text.split("/")[4]
                  if(child.tag == "{http://autosar.org/schema/r4.0}OPERATION-IREF"):
                      for grandchild in child:
                         if(grandchild.tag == "{http://autosar.org/schema/r4.0}CONTEXT-P-PORT-REF"):
                            # add the P-port as the First value to OPERATION_INVOKED_LIST
                            OPERATION_INVOKED_LIST[0] = grandchild.text.split("/")[3]
                         if(grandchild.tag == "{http://autosar.org/schema/r4.0}TARGET-PROVIDED-OPERATION-REF"):
                            # add the Client-server-operetaion as the second value to OPERATION_INVOKED_LIST
                            OPERATION_INVOKED_LIST[1] = grandchild.text.split("/")[4] #EDITED

                  # add the short name as key to the dictionary and the OPERATION_INVOKED_LIST of Type, Client-server-operetaion, P-port and Runnable as a value to the key
               Output_Dictionary[ShortName] = OPERATION_INVOKED_LIST
               List_of_Dictionaries.append(Output_Dictionary)
         return List_of_Dictionaries

    def Get_Triggers(self):
        TRIGGERS_LIST = []
        TRIGGERS_LIST.append(self.Get_Init_Events())
        TRIGGERS_LIST.append(self.Get_Timing_Events_Name_And_Period())
        TRIGGERS_LIST.append(self.Get_Data_Recieved_Events())
        TRIGGERS_LIST.append(self.Get_Operation_Invoked_Events())
        return TRIGGERS_LIST




    def Get_Data_Read_Elements(self):
       tree = ET.parse(self.XmlFilePath)   #parse the file
       root = tree.getroot()
       DataReadElementsList = []
       for node in tree.iter():
          if(node.tag == "{http://autosar.org/schema/r4.0}DATA-SEND-POINTS"):
             for child in node:
                for grandchild in child:
                    for xgrandchild in grandchild:
                       for xxgrandchild in xgrandchild:
                          if(xxgrandchild.tag == "{http://autosar.org/schema/r4.0}TARGET-DATA-PROTOTYPE-REF"):
                             #get the substring after the 4th "/"
                             DataReadElementsList.append(xxgrandchild.text.split("/")[4])
       return DataReadElementsList



    def Get_Data_Write_Elements(self):
       tree = ET.parse(self.XmlFilePath)   #parse the file
       root = tree.getroot()
       DataWriteElementsList = []

       for node in tree.iter():
          if(node.tag == "{http://autosar.org/schema/r4.0}DATA-RECEIVE-POINTS"):
             for child in node:
                for grandchild in child:
                    for xgrandchild in grandchild:
                       for xxgrandchild in xgrandchild:
                          if(xxgrandchild.tag == "{http://autosar.org/schema/r4.0}TARGET-DATA-PROTOTYPE-REF"):
                             #get the substring after the 4th "/"
                             DataWriteElementsList.append(xxgrandchild.text.split("/")[4])
       return DataWriteElementsList


    def Get_R_Ports_Of_Data_Read_Elements(self):
       tree = ET.parse(self.XmlFilePath)   #parse the file
       root = tree.getroot()
       RportsOfDataReadElementsList = []

       for node in tree.iter():
          if(node.tag == "{http://autosar.org/schema/r4.0}DATA-RECEIVE-POINTS"):
             for child in node:
                for grandchild in child:
                    for xgrandchild in grandchild:
                       for xxgrandchild in xgrandchild:
                          if(xxgrandchild.tag == "{http://autosar.org/schema/r4.0}PORT-PROTOTYPE-REF"):
                             #get the substring after the 4th "/"
                             RportsOfDataReadElementsList.append(xxgrandchild.text.split("/")[3])
       return RportsOfDataReadElementsList


    def Get_P_Ports_Of_Data_Write_Elements(self):
       tree = ET.parse(self.XmlFilePath)   #parse the file
       root = tree.getroot()
       PportsOfDataWriteElementsList = []

       for node in tree.iter():
          if(node.tag == "{http://autosar.org/schema/r4.0}DATA-SEND-POINTS"):
             for child in node:
                for grandchild in child:
                    for xgrandchild in grandchild:
                       for xxgrandchild in xgrandchild:
                          if(xxgrandchild.tag == "{http://autosar.org/schema/r4.0}PORT-PROTOTYPE-REF"):
                             #get the substring after the 4th "/"
                             PportsOfDataWriteElementsList.append(xxgrandchild.text.split("/")[3])
       return PportsOfDataWriteElementsList


#########################################################################################################################################################
    def Get_Runnable_Name_And_If_It_Can_Be_Invoked_Concurrently(self): #EDITED add minimum start interval
       tree = ET.parse(self.XmlFilePath)   #parse the file
       root = tree.getroot()
       Runnable_Name = ""
       Invoked=""
       Minimum=""
       Output_Dictionary = {}
       for node in tree.iter():
          #check if the current node's tag is RUNNABLES
          if(node.tag == "{http://autosar.org/schema/r4.0}RUNNABLES"):
             # iterate on all the children
             for child in node:
                # iterate on all grandchildren because the needed tags are grand children of RUNNABLES and not children
                for grandchild in child:
                    # if the SHORT-NAME tag is found return the name value
                    if(grandchild.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                       Runnable_Name = grandchild.text
                    # if the CAN-BE-INVOKED-CONCURRENTLY tag is found --> return the value as a dictionary value and the runnable name as a key
                    if(grandchild.tag == "{http://autosar.org/schema/r4.0}CAN-BE-INVOKED-CONCURRENTLY"):
                       Invoked = grandchild.text
                    if(grandchild.tag == "{http://autosar.org/schema/r4.0}MINIMUM-START-INTERVAL"):
                       Minimum = grandchild.text
                Output_Dictionary[Runnable_Name] = [Invoked,Minimum]
       return Output_Dictionary

    def Get_Runnables_TEST(self):
        tree = ET.parse(self.XmlFilePath)   #parse the file
        root = tree.getroot()
        Runnable_Name = ""
        Output_Dictionary = {}
        RUNNABLES_LIST=[]
        PORTS_LIST = []
        for node in tree.iter():
            #check if the current node's tag is RUNNABLES
            if(node.tag == "{http://autosar.org/schema/r4.0}RUNNABLES"):
            # iterate on all the children
                for child in node:
                # iterate on all grandchildren because the needed tags are grand children of RUNNABLES and not children
                    for grandchild in child:
                        # if the SHORT-NAME tag is found return the name value
                        if(grandchild.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                            Runnable_Name = grandchild.text
                        self.Get_P_Ports_Of_Data_Write_Elements()
                        PportsOfDataWriteElementsList = PORTS_LIST
                        Output_Dictionary[Runnable_Name]= PORTS_LIST
        RUNNABLES_LIST.append(Output_Dictionary)
        return RUNNABLES_LIST
def main():
  c1=Component("swc1.arxml")
  print (c1.Get_Triggers())
  print (c1.Get_Runnables())
  print (c1.Get_Timing_Events_Name_And_Period())
  print (c1.Get_Data_Recieved_Events())
  print (c1.Get_Operation_Invoked_Events())
  print (c1.Get_Init_Events())

if __name__ == '__main__':
    main()




