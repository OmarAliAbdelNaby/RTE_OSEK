import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import  SWC_Parser  
def Prettify_XML(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")
def Generate_Connectors(SWCConnectors,SWCP,SWCR):
    swcR={}
    swcP={}
    temp=SWCConnectors
    autosar_org = "http://autosar.org/schema/r4.0"
    autosar_schema_instance = "http://www.w3.org/2001/XMLSchema-instance"
    autosar_schema_location = "http://autosar.org/schema/r4.0 AUTOSAR_4-3-0.xsd"
    Autosar = ET.Element("AUTOSAR",{"xmlns":autosar_org, "xmlns:xsi":autosar_schema_instance, "xsi:schemaLocation":autosar_schema_location })
    ARpackages = ET.SubElement(Autosar, "AR-PACKAGES")
    ARpackage = ET.SubElement(ARpackages, "AR-PACKAGE")
    ProjectName="Seat Heater " #TODO
    Project=ET.SubElement(ARpackage, "SHORT-NAME").text=ProjectName
    Elements=ET.SubElement(ARpackage,"ELEMENTS")
    Composition=ET.SubElement(Elements,"COMPOSITION-SW-COMPONENT-TYPE")
    CompositionName=ET.SubElement(Composition, "SHORT-NAME").text=ProjectName+"_Composition"
    Components=ET.SubElement(Composition,"COMPONENTS")
    #### software components prototypes
    for swcName in temp :
        SWC=ET.SubElement(Components,"SW-COMPONENT-PROTOTYPE")
        SWCN=ET.SubElement(SWC,"SHORT-NAME").text=swcName
        SWCTR=ET.SubElement(SWC,"TYPE-TREF",{"DEST":"APPLICATION-SW-COMPONENT-TYPE"}).text="/"+ProjectName+"/"+swcName


    #for SWCName
    Connectors=ET.SubElement(Composition,"CONNECTORS")
    for swcName in temp :
        for Port in temp[swcName] :
            if temp[swcName][Port][0]=="None":
                continue
            else :
                Conn = ET.SubElement(Connectors, "ASSEMBLY-SW-CONNECTOR")
                Connsn =ET.SubElement(Conn, "SHORT-NAME").text=Port+"_"+temp[swcName][Port][1]
                if Port in SWCP[swcName] :
                    P = ET.SubElement(Conn, "PROVIDER-IREF")
                    P1 = ET.SubElement(P, "CONTEXT-SW-COMPONENT-PROTOTYPE-REF", {
                        "DEST": "SW-COMPONENT-PROTOTYPE"}).text = "/" + ProjectName +"/"+"test_Composition"+ "/" + swcName
                    P2 = ET.SubElement(P, "P-PORT-IN-COMPOSITION-INSTANCE-REF", {
                        "DEST": "P-PORT-PROTOTYPE"}).text = "/" + ProjectName + "/" + swcName+"/"+Port
                    R=ET.SubElement(Conn, "REQUESTER-IREF")
                    R1 = ET.SubElement(R, "CONTEXT-SW-COMPONENT-PROTOTYPE-REF", {
                        "DEST": "SW-COMPONENT-PROTOTYPE"}).text = "/" + ProjectName + "/"+"test_Composition"+"/" + temp[swcName][Port][0]
                    R2 = ET.SubElement(R, "R-PORT-IN-COMPOSITION-INSTANCE-REF", {
                        "DEST": "R-PORT-PROTOTYPE"}).text = "/" + ProjectName + "/" + swcName+"/"+temp[swcName][Port][1]

                else :
                    P = ET.SubElement(Conn, "PROVIDER-IREF")
                    P1 = ET.SubElement(P, "CONTEXT-SW-COMPONENT-PROTOTYPE-REF", {
                        "DEST": "SW-COMPONENT-PROTOTYPE"}).text = "/" + ProjectName +"/"+"test_Composition"+ "/" + temp[swcName][Port][0]
                    P2 = ET.SubElement(P, "P-PORT-IN-COMPOSITION-INSTANCE-REF", {
                        "DEST": "P-PORT-PROTOTYPE"}).text = "/" + ProjectName + "/" + swcName+"/"+temp[swcName][Port][1]
                    R=ET.SubElement(Conn, "REQUESTER-IREF")
                    R1 = ET.SubElement(R, "CONTEXT-SW-COMPONENT-PROTOTYPE-REF", {
                        "DEST": "SW-COMPONENT-PROTOTYPE"}).text = "/" + ProjectName + "/"+"test_Composition"+"/" +swcName
                    R2 = ET.SubElement(R, "R-PORT-IN-COMPOSITION-INSTANCE-REF", {
                        "DEST": "R-PORT-PROTOTYPE"}).text = "/" + ProjectName + "/" + swcName+"/"+Port
                temp[temp[swcName][Port][0]][temp[swcName][Port][1]]=["None","None"]
    result=Prettify_XML(Autosar)
    header='<?xml version="1.0" encoding="UTF-8"?>'+"\n"
    file=open("Connectors.arxml","w")
    result=result.split("\n", 1)[1]
    file.write(header+result)


