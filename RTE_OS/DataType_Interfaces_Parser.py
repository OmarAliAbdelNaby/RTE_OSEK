import xml.etree.ElementTree as ET

Elements = []

class DE_AND_IF_Parser:

    def __init__(self, XmlFilePath):
        self.XmlFilePath = XmlFilePath

    def GetDataTypes(self):
        tree = ET.parse(self.XmlFilePath)   #parse the file
        for node in tree.iter():    #iterate on all tree nodes
            if(node.tag == "{http://autosar.org/schema/r4.0}ELEMENTS"):
                for child in node:
                    if(child.tag == "{http://autosar.org/schema/r4.0}APPLICATION-PRIMITIVE-DATA-TYPE"):
                        for grandchild in child:
                            Element = {}
                            if(grandchild.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                                Type = grandchild.text
                                Value = 0    #EDITED
                                Element.update({ Type:  Value})
                        Elements.append(Element)
        return Elements


class Port_Interface_Parser:

    def __init__(self, XmlFilePath):
        self.XmlFilePath = XmlFilePath


    def Get_Ports(self):
        tree = ET.parse(self.XmlFilePath)
        Client_Server_Ports_List = []
        Sender_Receiver_Ports_List =[]
        iterations = 0
        for node in tree.iter():
            if(node.tag == "{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE"):
                for child in node: #for grandchild in child:
                    if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                        #print (child.text)
                        Client_Server_Ports_List.append(child.text)
                        #print (Client_Server_Ports_List)
                        #print (iterations)
                        if (iterations==0)or(iterations ==1): #skip the first and second iterations as we need only the third
                            iterations+=1
                            continue

            elif(node.tag == "{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE"):
                for child in node: #for grandchild in child:
                    if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                        #print (child.text)
                        Sender_Receiver_Ports_List.append(child.text)
                        #print (Sender_Receiver_Ports_List)
                        #print (iterations)
                        if (iterations==0)or(iterations ==1): #skip the first and second iterations as we need only the third
                            iterations+=1
                            continue

        Ports_List = [['S/R',Sender_Receiver_Ports_List], ['C/S',Client_Server_Ports_List]]
        return Ports_List

    def Get_CS_Operations(self):
        tree = ET.parse(self.XmlFilePath)
        all_arguments_list = []
        Operations_List = []
        operation_dec = {}
        each_operation_dec = {}
        arguments_list = []
        value = 0
        for node in tree.iter():
            if(node.tag == "{http://autosar.org/schema/r4.0}CLIENT-SERVER-INTERFACE"):
                operation_dec = {}
                each_operation_dec = {}
                arguments_list = []
                for child in node:
                    if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                        operation_dec_key = child.text

                    if(child.tag == "{http://autosar.org/schema/r4.0}OPERATIONS"):
                        for CLIENT_SERVER_OPERATIONs in child:
                            if(CLIENT_SERVER_OPERATIONs.tag == "{http://autosar.org/schema/r4.0}CLIENT-SERVER-OPERATION"):
                                for CLIENT_SERVER_OPERATIONs_childs in CLIENT_SERVER_OPERATIONs:
                                    if(CLIENT_SERVER_OPERATIONs_childs.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                                        each_operation_dec_key = CLIENT_SERVER_OPERATIONs_childs.text
                                    if(CLIENT_SERVER_OPERATIONs_childs.tag == "{http://autosar.org/schema/r4.0}ARGUMENTS"):
                                        for ARGUMENTs_childs in CLIENT_SERVER_OPERATIONs_childs:
                                            single_argument_list = []
                                            if(ARGUMENTs_childs.tag == "{http://autosar.org/schema/r4.0}ARGUMENT-DATA-PROTOTYPE"):
                                                for ARGUMENT_DATA_PROTOTYPE_childs in ARGUMENTs_childs:
                                                    if(ARGUMENT_DATA_PROTOTYPE_childs.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                                                        single_argument_list.append(ARGUMENT_DATA_PROTOTYPE_childs.text)
                                                    if(ARGUMENT_DATA_PROTOTYPE_childs.tag == "{http://autosar.org/schema/r4.0}TYPE-TREF"):
                                                        single_argument_list.append(ARGUMENT_DATA_PROTOTYPE_childs.text.split("/")[3])
                                                        for data_elements_dict in Elements:
                                                            for Type , Value in data_elements_dict.items():
                                                                if((single_argument_list[1]) == Type):
                                                                    value = data_elements_dict.get(Type)
                                                        single_argument_list.append(value)
                                                    if(ARGUMENT_DATA_PROTOTYPE_childs.tag == "{http://autosar.org/schema/r4.0}DIRECTION"):
                                                        for dir_tag in ARGUMENT_DATA_PROTOTYPE_childs:
                                                            if(dir_tag.tag == "{http://autosar.org/schema/r4.0}DIRECTION"):
                                                                single_argument_list.append(dir_tag.text)
                                            arguments_list.append(single_argument_list)
                                        all_arguments_list.append(arguments_list)

                                        each_operation_dec.update({each_operation_dec_key : arguments_list})

                        operation_dec.update({operation_dec_key : each_operation_dec})
                        Operations_List.append(operation_dec)

        return Operations_List

    def Get_SR_Data_Elements(self):
        tree = ET.parse(self.XmlFilePath)
        Sender_Receiver_Key = {}
        Sender_Receiver_Interface = {}
        value = 0

        for node in tree.iter():
            if(node.tag == "{http://autosar.org/schema/r4.0}SENDER-RECEIVER-INTERFACE"):
                for child in node:
                    if(child.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                        All_DE_List = []
                        Sender_Receiver_Key = child.text
                    if(child.tag == "{http://autosar.org/schema/r4.0}DATA-ELEMENTS"):
                        for grandchild in child:
                            if(grandchild.tag == "{http://autosar.org/schema/r4.0}VARIABLE-DATA-PROTOTYPE"):
                                DE_List = []
                                for grandgrandchild in grandchild:
                                    if(grandgrandchild.tag == "{http://autosar.org/schema/r4.0}SHORT-NAME"):
                                        DE_List.append(grandgrandchild.text)
                                    if(grandgrandchild.tag == "{http://autosar.org/schema/r4.0}TYPE-TREF"):
                                        DE_List.append(grandgrandchild.text.split("/")[3])
                                        for data_elements_dict in Elements:
                                            for Type , Value in data_elements_dict.items():
                                                if((DE_List[1]) == Type):
                                                    value = data_elements_dict.get(Type)
                                        DE_List.append(value)
                                All_DE_List.append(DE_List)
                                Sender_Receiver_Interface.update({Sender_Receiver_Key : All_DE_List})

        return Sender_Receiver_Interface
def main():
    c1=Port_Interface_Parser("DataTypesAndInterfaces.arxml")
    c2=DE_AND_IF_Parser("DataTypesAndInterfaces.arxml")
    print(c2.GetDataTypes()) #DataTypes
    print(c1.Get_Ports()) #PortInterfaces
    print(c1.Get_SR_Data_Elements()) #SRInterface :DataElements

if __name__ == '__main__':
    main()


