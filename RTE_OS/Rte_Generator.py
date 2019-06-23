import xml.etree.ElementTree as ET
import os
from SWC_Parser import *
from DataType_Interfaces_Parser import *
from Runnables_Events_Parser import *
from Runnables_Events_Parser import *
def Get_Ports_Connections(xmlFilePath):
    tree = ET.parse(xmlFilePath)
    software_component_names_array = []
    connectors_array = []
    schema = "{http://autosar.org/schema/r4.0}"
    for node in tree.iter():  # iterate on all tree nodes
        if (node.tag == schema + "COMPONENTS"):
            for child in node:
                if (child.tag == schema + "SW-COMPONENT-PROTOTYPE"):
                    for child2 in child:
                        if (child2.tag == schema + "SHORT-NAME"):
                            software_component_names_array.append(child2.text)
        elif (node.tag == schema + "CONNECTORS"):
            for child in node:
                if (child.tag == schema + "ASSEMBLY-SW-CONNECTOR"):
                    array = []
                    for child2 in child:
                        if (child2.tag == schema + "PROVIDER-IREF"):
                            for PROVIDER in child2:
                                if (PROVIDER.tag == schema + "CONTEXT-SW-COMPONENT-PROTOTYPE-REF"):
                                    # append SWC name
                                    array.append(PROVIDER.text.split("/")[-1])
                                elif (PROVIDER.tag == schema + "P-PORT-IN-COMPOSITION-INSTANCE-REF"):
                                    # append port name
                                    array.append(PROVIDER.text.split("/")[-1])
                        elif (child2.tag == schema + "REQUESTER-IREF"):
                            for REQUESTER in child2:
                                if (REQUESTER.tag == schema + "CONTEXT-SW-COMPONENT-PROTOTYPE-REF"):
                                    # append SWC name
                                    array.append(REQUESTER.text.split("/")[-1])
                                elif (REQUESTER.tag == schema + "R-PORT-IN-COMPOSITION-INSTANCE-REF"):
                                    # append port name
                                    array.append(REQUESTER.text.split("/")[-1])
                    connectors_array.append(array)

    return [software_component_names_array, connectors_array]


def Generate_Read_Data_Element_Function(DEName, DEType, PortName, Events):
    functionName = "Rte_Read_"+ PortName + "_" + DEName
    functionArguments = DEType + "* data"
    functionBody = ""
    for event in Events:
        functionBody = functionBody + "\t\tSetEvent(" +"RTE_"+event + ") ;\n"
    functionBody = functionBody + "\t\t" + "* data" + " = " + DEName+" ;"
    returnLine="\t\t"+"return RTE_E_OK ;"
    function = "Std_ReturnType" + " " + functionName + " (" + functionArguments + ")" + "\n\t{\n" + functionBody +"\n"+returnLine+ "\n\t}\n"
    prototype="Std_ReturnType" + " " + functionName + " (" + functionArguments + ");\n"
    return function,prototype


def Generate_Write_Data_Element_Function(DEName, DEType, PortName):
    functionName = "Rte_Write_"+ PortName + "_" + DEName
    functionArguments = DEType + " data"
    functionBody = "\t\t" + DEName + " = " + "data ;"
    returnLine="\t\t"+"return RTE_E_OK ;"
    function = "Std_ReturnType" + " " + functionName + " (" + functionArguments + ")" + "\n\t{\n" + functionBody+"\n"+returnLine + "\n\t}\n"
    prototype="Std_ReturnType" + " " + functionName + " (" + functionArguments + ");\n" 
    return function,prototype
def Generate_DataTypes_Definition():
    definitions="typedef "+"unsigned char "+"Boolean ;"+"\n"+\
                "typedef "+"unsigned char "+"UnsignedInteger_8 ;"+"\n"+\
                "typedef "+"signed char "+"SignedInteger_8 ;"+"\n"+\
                "typedef "+"unsigned short "+"UnsignedInteger_16 ;"+"\n"+\
                "typedef "+"short "+"SignedInteger_16 ;"+"\n"+\
                "typedef "+"unsigned int "+"UnsignedInteger_32 ;"+"\n"+\
                "typedef "+"int "+"SignedInteger_32 ;"+"\n"+\
                "typedef "+"unsigned int "+"Std_ReturnType ;"+"\n"
    return definitions            
def Generate_VariableAccess_Macro(RunnableName,DEName,PortName,Read_Write,Replacment_bool):#Read_Write="Read" or "Write"
    functionName="Rte_I"+Read_Write+"_"+RunnableName+"_"+PortName+"_"+DEName
    replacment=""
    if(Replacment_bool):
        replacment="Rte_"+Read_Write+"_"+PortName+"_"+DEName
        replacment="\\\n"+replacment+"(data)"
    macro="#define "+functionName+"(data)"+replacment+"\n"
    return macro 
def Generate_Rte_Ports_Functions(ConnectorsList,globalDatatypesandInterfacesFilePath,globalSwcsFilePaths):#returns DElements Defination,PortsFunctions,PortsPrototypes
    functions=""
    prototypes=""
    DEdefinition=""
    swcDictRports = {}
    swcDictPports = {}
    swcDataRecievedEvents = {}
    dataelements = Port_Interface_Parser(globalDatatypesandInterfacesFilePath).Get_SR_Data_Elements()
    for swcName in ConnectorsList[0]:
        filepath=globalSwcsFilePaths[swcName]
        swcDictRports[swcName] = SWC_Parser(filepath).Get_R_PortsFromComponent()
        swcDictPports[swcName] = SWC_Parser(filepath).Get_P_PortsFromComponent()
        swcDataRecievedEventsList=Component(filepath).Get_Data_Recieved_Events()
        if swcDataRecievedEventsList==[]:
            swcDataRecievedEvents[swcName] = []
        else :
            swcDataRecievedEvents[swcName] = swcDataRecievedEventsList[0]
    for Connector in ConnectorsList[1]:
        # Connector[0]: (Provider swc name),#Connector[2]: (Required swc name),
        ##Connector[1]: (Provider Port name),#Connector[3]: (Required Port name).
        Interface = swcDictPports[Connector[0]][Connector[1]]
        InterfaceType = Interface[0]
        if InterfaceType == "C/S":
            continue
        InterfaceName = Interface[1]
        for DE in dataelements[InterfaceName]:
            # DE[0]:(name) #DE[1](type)
            DEdefinition=DEdefinition+DE[1]+" "+Connector[1]+"_"+DE[0]+" ;"+"\n"
            DEdefinition=DEdefinition+DE[1]+" "+Connector[3]+"_"+DE[0]+" ;"+"\n"
            functionw,prototypew=Generate_Write_Data_Element_Function(DE[0], DE[1], Connector[1])
            functions=functions+functionw+"\n"
            prototypes=prototypes+prototypew+"\n"
            DataelementEvents = []
            if not(Connector[2] in swcDataRecievedEvents) :
                continue
            for Event in swcDataRecievedEvents[Connector[2]]:
                if swcDataRecievedEvents[Connector[2]][Event][1] == DE[0]:
                    DataelementEvents.append(Event)
            functionr,prototyper=Generate_Read_Data_Element_Function(DE[0], DE[1], Connector[3],DataelementEvents)
            functions=functions+functionr+"\n"
            prototypes=prototypes+prototyper+"\n"
    return DEdefinition,functions,prototypes        
def Generate_Rte_Runnables_VariableAccess_Macros(ConnectorsList,globalDatatypesandInterfacesFilePath,globalSwcsFilePaths) :
    result=""
    swcDictRports = {}
    swcDictPports = {}
    swcRunnables={}
    PconnectorsTemp=[] #list containing P connected ports
    RconnectorsTemp=[] #list containing R connected ports
    dataelements = Port_Interface_Parser(globalDatatypesandInterfacesFilePath).Get_SR_Data_Elements()
    for swcName in ConnectorsList[0]:
        filepath=globalSwcsFilePaths[swcName]
        swcDictRports[swcName] = SWC_Parser(filepath).Get_R_PortsFromComponent()
        swcDictPports[swcName] = SWC_Parser(filepath).Get_P_PortsFromComponent()
        swcRunnables[swcName]=Component(filepath).Get_Runnables()
    for Connector in ConnectorsList[1]:
        # Connector[0]: (Provider swc name),#Connector[2]: (Required swc name),
        ##Connector[1]: (Provider Port name),#Connector[3]: (Required Port name).
        PconnectorsTemp.append(Connector[1])
        RconnectorsTemp.append(Connector[3])
    for swcName in ConnectorsList[0]:
        for runnable in swcRunnables[swcName] :
            RunnablePortsAccess=swcRunnables[swcName][runnable][0]
            RunnableVariableAccess=swcRunnables[swcName][runnable][1]
            for i in range(len(RunnablePortsAccess)):
                if(RunnablePortsAccess[i] in PconnectorsTemp):
                    result=result+Generate_VariableAccess_Macro(runnable,RunnableVariableAccess[i],RunnablePortsAccess[i],"Write",True)+"\n"
                elif(RunnablePortsAccess[i] in RconnectorsTemp) :
                    result=result+Generate_VariableAccess_Macro(runnable,RunnableVariableAccess[i],RunnablePortsAccess[i],"Read",True)+"\n"
                elif(RunnablePortsAccess[i] in swcDictPports[swcName]):
                    result=result+Generate_VariableAccess_Macro(runnable,RunnableVariableAccess[i],RunnablePortsAccess[i],"Write",False)+"\n"
                else: 
                    result=result+Generate_VariableAccess_Macro(runnable,RunnableVariableAccess[i],RunnablePortsAccess[i],"Read",False)+"\n"
    return result 
def Generate_SWCs_HFiles_CFiles(ConnectorsList,globalProjectName,globalDatatypesandInterfacesFilePath,globalSwcsFilePaths) :
    result=""
    swcDictRports = {}
    swcDictPports = {}
    swcRunnables={}
    dataelements = Port_Interface_Parser(globalDatatypesandInterfacesFilePath).Get_SR_Data_Elements()
    for swcName in ConnectorsList[0]:
        filepath=globalSwcsFilePaths[swcName]
        swcDictRports[swcName] = SWC_Parser(filepath).Get_R_PortsFromComponent()
        swcDictPports[swcName] = SWC_Parser(filepath).Get_P_PortsFromComponent()
        swcRunnables[swcName]=Component(filepath).Get_Runnables()
    for swcName in ConnectorsList[0]:
        if not os.path.exists(globalProjectName):
              os.mkdir(globalProjectName)
        filec = open(globalProjectName+"/Rte_"+swcName+".c", "w")
        filec.write("#include \"Rte.h\"\n")
        filec.write("#include \"Rtetypes.h\"\n")
        filec.write("#include \""+"Rte_"+swcName+".h"+"\"")
        filec.write("\n\n\n")
        fileh = open(globalProjectName+"/Rte_"+swcName+".h", "w")
        guardName="RTE_"+swcName.upper()+"_HEADER_H_"
        guard="#ifndef "+guardName+"\n"+"#define "+guardName+"\n\n"
        fileh.write(guard)                           
        for runnable in swcRunnables[swcName] :
            filec.write("void "+runnable+"(\t)\n\t{\n\n\n\t}")
            filec.write("\n\n\n") 
            fileh.write("void "+runnable+"(\t);\n")
            RunnablePortsAccess=swcRunnables[swcName][runnable][0]
            RunnableVariableAccess=swcRunnables[swcName][runnable][1]
            temp=False 
            for i in range(len(RunnablePortsAccess)):
                if RunnablePortsAccess[i] in swcDictPports[swcName]:
                    Interface = swcDictPports[swcName][RunnablePortsAccess[i]]
                    temp=True
                else :
                    Interface = swcDictRports[swcName][RunnablePortsAccess[i]]
                    temp=False 
                InterfaceType = Interface[0]
                if InterfaceType == "C/S":
                    continue
                InterfaceName = Interface[1]
                for DE in dataelements[InterfaceName]:
                    # DE[0]:(name) #DE[1](type)
                    if DE[0]==RunnableVariableAccess[i]:
                        if temp:
                            result=result+"Std_ReturnType "+"Rte_IWrite"+"_"+runnable+"_"+RunnablePortsAccess[i]+"_"+RunnableVariableAccess[i]+"("+DE[1]+" data);"+"\n"
                        else :
                            result=result+"Std_ReturnType "+"Rte_IRead"+"_"+runnable+"_"+RunnablePortsAccess[i]+"_"+RunnableVariableAccess[i]+"("+DE[1]+" *data);"+"\n" 
                        break
        fileh.write("#endif")                                                      
    return result 
def OtherDefinations():
    definitions="#define RTE_E_OK     (Std_ReturnType)0"+"\n"+\
                "#define RTE_E_NOT_OK (Std_ReturnType)1"+"\n"
    return definitions 
def Generate_Rte_CandH_Files(ConnectorsList,globalProjectName,globalDatatypesandInterfacesFilePath,globalSwcsFilePaths):
    print(globalProjectName)
    if not os.path.exists(globalProjectName):
        os.mkdir(globalProjectName)
    filec = open(globalProjectName+"/Rte.c", "w")
    Includes=""
    Includes=Includes+"#include <stdio.h>"+"\n"
    Includes=Includes+"#include <time.h>"+"\n"
    Includes=Includes+'#include "Rte.h"'+"\n"
    Includes=Includes+'#include "Rtetypes.h"'+"\n"
    DEdefinition,functions,prototypes=Generate_Rte_Ports_Functions(ConnectorsList,globalDatatypesandInterfacesFilePath,globalSwcsFilePaths)
    filec.write(Includes)
    filec.write("\n\n\n")
    filec.write(DEdefinition)
    filec.write("\n\n\n")
    filec.write(functions) 
    fileh=open(globalProjectName+"/Rte.h", "w")
    guardName="RTE_HEADER_H_"
    guard="#ifndef "+guardName+"\n"+"#define "+guardName+"\n\n"
    fileh.write(guard)
    fileh.write('#include "Rtetypes.h"')
    fileh.write("\n\n\n")
    fileh.write(prototypes)
    fileh.write("\n\n\n")
    fileh.write("\n\n\n")
    fileh.write("#endif")
def Generate_RtetypesH_File(ConnectorsList,globalProjectName) :
    if not os.path.exists(globalProjectName):
        os.mkdir(globalProjectName)
    file = open(globalProjectName+"/Rtetypes.h", "w")
    guardName="RTETYPES_HEADER_H_"
    guard="#ifndef "+guardName+"\n"+"#define "+guardName+"\n\n"
    file.write(guard)
    file.write("\n\n\n")
    file.write(Generate_DataTypes_Definition())
    file.write("\n\n\n")
    #file.write(Generate_Rte_Runnables_VariableAccess_Macros(ConnectorsList))
    #file.write("\n\n\n")
    file.write(OtherDefinations())
    file.write("\n\n\n")
    file.write("#endif")
def main():
    ConnectorsList=Get_Ports_Connections("Connectors.arxml")
    print(ConnectorsList)
    Generate_Rte_CandH_Files(ConnectorsList,"globalProjectName")
    Generate_RtetypesH_File(ConnectorsList,"globalProjectName")
    Generate_SWCs_HFiles_CFiles(ConnectorsList,"globalProjectName")
if __name__ == '__main__':
    main()



