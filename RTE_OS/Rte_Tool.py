import sys
from PyQt4 import QtGui, QtCore
import ntpath

from DataType_Interfaces_Parser import *
from pathlib import Path
from SWC_Parser import *
from Runnables_Events_Parser import *
#from RTE_OS import *
from Print_OS_XML import *
from Connectors_Generator import Generate_Connectors
from Rte_Generator import *
import json

globalallFilePaths={}
globalnoOfRunnables=[]
globalallFilePaths["globalSwcsFilePaths"]={}
FileNames=[]
SWCsPports = {}
SWCsRports = {}
Data_Elements = []
SWCsRunnables = {}
SWCsConnectors = {}
RunnablesTasksDict={}
PortsComboBoxDict={}
taskList = []
positionList=[]
ComSignals = {}  # TODO

personDict = {
  'bill': 'tech',
  'federer': 'tennis',
  'ronaldo': 'football',
  'woods': 'golf',
  'ali': 'boxing'
}
app_json = json.dumps(personDict, sort_keys=True)
print(app_json)
class ComboBox(QtGui.QWidget):
   def __init__(self,id1,Index,parent,Portbool,List1,List2): #Portbool True : 1 combobox---  False Runnable :2 combobox
      super(ComboBox, self).__init__(parent)
      self.cb1 = QtGui.QComboBox()
      self.cb2 = QtGui.QComboBox()
      self.List1=List1
      self.List2=List2
      self.id1=id1  
      self.type=""
      self.parent=parent
      self.Index=Index
      self.cb1.addItems(self.List1)
      self.cb1.currentIndexChanged.connect(self.selectionchange)
      if Portbool==True:
              self.type="Port"
              self.parent.setItemWidget(self.Index, 1, self.cb1)
      else :
              self.type="Runnable"
              self.cb2.addItems(self.List2)
              self.cb2.currentIndexChanged.connect(self.selectionchange)              
              hbox = QtGui.QHBoxLayout()
              hbox.addWidget(self.cb1)
              hbox.addWidget(self.cb2) 
              layout = QtGui.QWidget()
              layout.setLayout(hbox) 
              parent.setItemWidget(Index, 1, layout)
   def selectionchange(self,i):
      if self.type=="Port":
          connected=self.cb1.currentText().split(":")
          if connected[0]!="None":
              connectedSWC=connected[0]
              connectedPort=connected[1]
          else :
              connectedSWC="None"
              connectedPort="None"
          current=self.id1.split(":")
          currentSWC=current[0]
          currentPort=current[1]
          if connected[0]=="None":
              if SWCsConnectors[currentSWC][currentPort][0]=='None':
                  SWCsConnectors[currentSWC][currentPort] = ["None", "None"]
              elif SWCsConnectors[currentSWC][currentPort][0]=='Signal':
                  SWCsConnectors[currentSWC][currentPort] = ["None", "None"]
              else :
                  SWCsConnectors[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]]=["None","None"]
                  index1 =  PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.findText("None", QtCore.Qt.MatchFixedString)
                  if index1 >= 0:
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][
                          SWCsConnectors[currentSWC][currentPort][1]].cb1.blockSignals(True)
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.setCurrentIndex(index1)
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][
                          SWCsConnectors[currentSWC][currentPort][1]].cb1.blockSignals(False)
                  SWCsConnectors[currentSWC][currentPort] = ["None", "None"]
          elif   connectedSWC=="Signal":
              if SWCsConnectors[currentSWC][currentPort][0]=='None':
                  SWCsConnectors[currentSWC][currentPort] = [connectedSWC, connectedPort]
              elif SWCsConnectors[currentSWC][currentPort][0]=='Signal':
                  SWCsConnectors[currentSWC][currentPort] = [connectedSWC, connectedPort]
              else :
                  SWCsConnectors[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]]=["None","None"]
                  index1 =  PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.findText("None", QtCore.Qt.MatchFixedString)
                  if index1 >= 0:
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][
                          SWCsConnectors[currentSWC][currentPort][1]].cb1.blockSignals(True)
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.setCurrentIndex(index1)
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][
                          SWCsConnectors[currentSWC][currentPort][1]].cb1.blockSignals(False)
                  SWCsConnectors[currentSWC][currentPort] = ["None", "None"]
          elif SWCsConnectors[connectedSWC][connectedPort][0]=="None" :
              if SWCsConnectors[currentSWC][currentPort][0]=='None':
                  SWCsConnectors[currentSWC][currentPort] = [connectedSWC, connectedPort]
                  SWCsConnectors[connectedSWC][connectedPort] = [currentSWC, currentPort]
                  index = self.cb1.findText(connectedSWC+":"+connectedPort, QtCore.Qt.MatchFixedString)
                  if index >= 0:
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(True)
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.setCurrentIndex(index)
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(False)
              elif SWCsConnectors[currentSWC][currentPort][0]=='Signal':
                  SWCsConnectors[currentSWC][currentPort] = [connectedSWC, connectedPort]
                  SWCsConnectors[connectedSWC][connectedPort] = [currentSWC, currentPort]
                  index = self.cb1.findText(connectedSWC+":"+connectedPort, QtCore.Qt.MatchFixedString)
                  if index >= 0:
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(True)
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.setCurrentIndex(index)
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(False)
              else :
                  SWCsConnectors[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]]=["None","None"]
                  index1 =  PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.findText("None", QtCore.Qt.MatchFixedString)
                  if index1 >= 0:
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][
                          SWCsConnectors[currentSWC][currentPort][1]].cb1.blockSignals(True)
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.setCurrentIndex(index1)
                      PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][
                          SWCsConnectors[currentSWC][currentPort][1]].cb1.blockSignals(False)
                  SWCsConnectors[currentSWC][currentPort] = [connectedSWC, connectedPort]
                  SWCsConnectors[connectedSWC][connectedPort] = [currentSWC, currentPort]
                  index2 = self.cb1.findText(connectedSWC + ":" + connectedPort, QtCore.Qt.MatchFixedString)
                  if index2 >= 0:
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(True)
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.setCurrentIndex(index2)
                      PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(False)
          else :
                QtGui.QMessageBox.warning(self, "Warning", "Port is already Connected")
                index = PortsComboBoxDict[SWCsConnectors[currentSWC][currentPort][0]][SWCsConnectors[currentSWC][currentPort][1]].cb1.findText("None", QtCore.Qt.MatchFixedString)
                if index >= 0:
                       PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(True)
                       PortsComboBoxDict[connectedSWC][connectedPort].cb1.setCurrentIndex(index)
                       PortsComboBoxDict[connectedSWC][connectedPort].cb1.blockSignals(False)
      else :
          Task=self.cb1.currentText()
          Pos=self.cb2.currentText()
          Runnable=self.id1
          RunnablesTasksDict[Runnable]=[Task,int(Pos)]


        ##TODO

class connection(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(connection, self).__init__(parent)
        # Main Screen Window
        self.mainUI()
        self.initializaion()
        self.tree()
        self.center()
        self.generateButton()
        # 1- add SWC (key of any swc dictionary)

        self.show()
    def initializaion(self):
        # Initializate SWCsConnectors
        noOfRunnables = 0
        for SwcComponentName in SWCsRunnables :
            SWCsConnectors[SwcComponentName] = {}
            for Rport in SWCsRports[SwcComponentName]:
                if SWCsRports[SwcComponentName][Rport][0] != 'S/R':
                    continue
                SWCsConnectors[SwcComponentName][Rport] = ["None","None"]
            for Pport in SWCsPports[SwcComponentName]:
                if SWCsPports[SwcComponentName][Pport][0] != 'S/R':
                    continue
                SWCsConnectors[SwcComponentName][Pport] = ["None","None"]
            for Runnable in SWCsRunnables[SwcComponentName] :
                RunnablesTasksDict[Runnable]=[taskList[0],1]
                noOfRunnables += 1
        globalnoOfRunnables.append(noOfRunnables)

    def mainUI(self):
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("RTE Tool")
        self.center()
    def GenerateRte(self):
        try:
            Generate_Connectors(SWCsConnectors,SWCsPports,SWCsRports)
            print(globalallFilePaths["globalProjectName"])
            ConnectorsList=Get_Ports_Connections("Connectors.arxml")
            Generate_Rte_CandH_Files(ConnectorsList,globalallFilePaths["globalProjectName"],globalallFilePaths["globalDatatypesandInterfacesFilePath"],globalallFilePaths["globalSwcsFilePaths"])
            Generate_RtetypesH_File(ConnectorsList,globalallFilePaths["globalProjectName"])
            Generate_SWCs_HFiles_CFiles(ConnectorsList,globalallFilePaths["globalProjectName"],globalallFilePaths["globalDatatypesandInterfacesFilePath"],globalallFilePaths["globalSwcsFilePaths"])
            print(RunnablesTasksDict)
            with open('RunnablesandTasks.txt', 'w') as json_file:
                json.dump(RunnablesTasksDict, json_file)
            QtGui.QMessageBox.about(self,"Message","Generation Done Sucssesfully ")
        except:
            QtGui.QMessageBox.about(self,"Warning","Something Went Wrong!!")
    def generateButton(self):
            # RTE Tool
            generate_btn = QtGui.QPushButton("Rte Generate", self)
            generate_btn.clicked.connect(self.GenerateRte)
            generate_btn.resize(100, 50)
            generate_btn.move(1200, 50)
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
    def tree(self):
        # Tree Geometry
        swcListBox = QtGui.QTreeWidget(self)
        swcListBox.setGeometry(50,50,1100,600)

        # Column width
        swcListBox.setColumnWidth(0, 100)
        swcListBox.header().setResizeMode(0,QtGui.QHeaderView.Stretch|QtGui.QHeaderView.Interactive)

        # Header
        header = QtGui.QTreeWidgetItem(["Tree", "Connect To"])
        swcListBox.setHeaderItem(header)

        # Fill Tree
        root = QtGui.QTreeWidgetItem(swcListBox, ["Software Components"])

        for SwcComponentName in SWCsRunnables :
            swc = QtGui.QTreeWidgetItem(root, [SwcComponentName])
            Ports = QtGui.QTreeWidgetItem(swc,["Ports"])
            Runnables = QtGui.QTreeWidgetItem(swc, ["Runnables"])
            PortsComboBoxDict[SwcComponentName]={}
            for Rport in SWCsRports[SwcComponentName]:
                if SWCsRports[SwcComponentName][Rport][0] != 'S/R':
                    continue
                ComboList=["None"]
                RportGUI = QtGui.QTreeWidgetItem(Ports, [Rport])
                for ConnectedSwcComponentName in SWCsRunnables :
                    if ConnectedSwcComponentName==SwcComponentName :
                        continue
                    for ConnectedPport in SWCsPports[ConnectedSwcComponentName]:
                        if SWCsPports[ConnectedSwcComponentName][ConnectedPport][0] != 'S/R':
                            continue
                        elif SWCsPports[ConnectedSwcComponentName][ConnectedPport][1] != SWCsRports[SwcComponentName][Rport][1] :
                            continue
                        elif SWCsConnectors[ConnectedSwcComponentName][ConnectedPport][0]!='None':
                            continue
                        else :
                            ComboList.append(ConnectedSwcComponentName+":"+ConnectedPport)

                PortsComboBoxDict[SwcComponentName][Rport]=ComboBox(SwcComponentName+":"+Rport,RportGUI,swcListBox,True,ComboList,[])


                #comboBox.mousePressEvent(QtCore.QEvent.Show)

            for Pport in SWCsPports[SwcComponentName]:
                if SWCsPports[SwcComponentName][Pport][0] != 'S/R':
                    continue
                ComboList=["None"]
                PportGUI = QtGui.QTreeWidgetItem(Ports, [Pport])
                for ConnectedSwcComponentName in SWCsRunnables :
                    if ConnectedSwcComponentName==SwcComponentName :
                        continue
                    for ConnectedRport in SWCsRports[ConnectedSwcComponentName]:
                        if SWCsRports[ConnectedSwcComponentName][ConnectedRport][0] != 'S/R':
                            continue
                        elif SWCsRports[ConnectedSwcComponentName][ConnectedRport][1] != SWCsPports[SwcComponentName][Pport][1] :
                            continue
                        elif SWCsConnectors[ConnectedSwcComponentName][ConnectedRport][0]!='None':
                            continue
                        else :
                            ComboList.append(ConnectedSwcComponentName+":"+ConnectedRport)
                PortsComboBoxDict[SwcComponentName][Pport]=ComboBox(SwcComponentName+":"+Pport,PportGUI,swcListBox,True,ComboList,[])
                #comboBox.mousePressEvent(QtCore.QEvent.Show)
            for Runnable in SWCsRunnables[SwcComponentName] :
                RunnableGui = QtGui.QTreeWidgetItem(Runnables, [Runnable])
                positionList = [str(i) for i in range(1, globalnoOfRunnables[-1] + 1)]
                combo=ComboBox(Runnable,RunnableGui,swcListBox,False,taskList,positionList)
            ''' for Rport in SWCsRports[SwcComponentName]:
                SWCsConnectors[SwcComponentName][Rport] = ["None","None"]
            for Pport in SWCsPports[SwcComponentName]:
                SWCsConnectors[SwcComponentName][Pport] = ["None","None"]
            '''

        #swc = QtGui.QTreeWidgetItem(root, ["SWC 1"])
        # barA = QtGui.QTreeWidgetItem(A, ["bar", "i", "ii"])
        # bazA = QtGui.QTreeWidgetItem(A, ["baz", "a", "b"])

        #Port1 = QtGui.QTreeWidgetItem(swc)
        # swcListBox.setSizeHint ( 0, QtCore.QSize(100, 1000))
        comboBox = QtGui.QComboBox()
        comboBox.addItem("motif")
        comboBox.addItem("Windows")
        comboBox.addItem("cde")
        comboBox.addItem("Plastique")
        comboBox.addItem("Cleanlooks")
        comboBox.addItem("windowsvista")
        # barA.setData()
        #Port1.setText(0, "port 1")

        #swcListBox.setItemWidget(Port1, 1, comboBox)


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # Main Screen Window
        self.mainUI()

        # Right SWC Listview
        self.listView = QtGui.QTextEdit(self)
        self.verticalLayoutWidget = QtGui.QWidget(self)
        self.connect_pushButton = QtGui.QPushButton("Connect", self.verticalLayoutWidget)

        self.SWCList(self.listView)

        # Buttons
        self.Buttons()


        # Software Component TreeView
        # self.SwcTreeView()
        # Application Button
        # Add swc Button
        # self.addSwc()
        self.show()


    def SWCList(self,listView):
        listView.setGeometry(QtCore.QRect(470, 120, 400, 192))
        #listView.setObjectName(_fromUtf8("ListView"))

    def Buttons(self):
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 371, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)

        # Add SWC Button
        add_swc_pushButton = QtGui.QPushButton("Add ARXML File",self.verticalLayoutWidget)
        self.verticalLayout.addWidget(add_swc_pushButton)
        add_swc_pushButton.setIcon(QtGui.QIcon("attach.png"))
        add_swc_pushButton.clicked.connect(self.file_open)

        # Connect SWC Button

        #connect_pushButton.setObjectName("Connect")
        self.verticalLayout.addWidget(self.connect_pushButton)
        self.connect_pushButton.setIcon(QtGui.QIcon("select5.png"))
        self.connect_pushButton.setEnabled(False)
        self.connect_pushButton.clicked.connect(self.openRteWindow)

    # Main Screen Window UI
    def mainUI(self):
        self.resize(900, 480)
        self.setWindowTitle("RTE Tool")
        self.center()
    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    # Tree View Test
    def SwcTreeView(self):
        pointListBox = QtGui.QTreeWidget(self)
        pointListBox.setColumnWidth(0,250)
        pointListBox.header().setResizeMode(0, QtGui.QHeaderView.Stretch | QtGui.QHeaderView.Interactive)
        #pointListBox.setColumnWidth(2000, 100)
        header = QtGui.QTreeWidgetItem(["Tree", "Connect To"])
        # ...
        pointListBox.setHeaderItem(header)  # Another alternative is setHeaderLabels(["Tree","First",...])
        pointListBox.setGeometry(10,10,600,300)
        root = QtGui.QTreeWidgetItem(pointListBox, ["Software Components"])
        A = QtGui.QTreeWidgetItem(root, ["SWC 1"])
        # barA = QtGui.QTreeWidgetItem(A, ["bar", "i", "ii"])
        # bazA = QtGui.QTreeWidgetItem(A, ["baz", "a", "b"])

        Port1 = QtGui.QTreeWidgetItem(A)
        # pointListBox.setSizeHint ( 0, QtCore.QSize(100, 1000))
        comboBox = QtGui.QComboBox()
        comboBox.addItem("port2")
        comboBox.addItem("port3")
        comboBox.addItem("port4")
        comboBox.addItem("port5")
        comboBox.addItem("port6")
        comboBox.addItem("port8")
        # barA.setData()
        Port1.setText(0, "port 1")

        pointListBox.setItemWidget(Port1, 1, comboBox)

    # Open File
    def file_open(self):
        #path = QtGui.QFileDialog.getOpenFileName(None, 'Open File')
        filter = "ARXML (*.arxml)"
        #file_name = QtGui.QFileDialog
        #file_name.setFileMode(QFileDialog.ExistingFiles)
        paths = QtGui.QFileDialog.getOpenFileNamesAndFilter(self, "Open files","C\\Desktop" , filter)[0]
        #print ( ntpath.split(paths[0])[1])
        # file = open(path, 'r')
        # print(file)
        # global head, tail

        for path in paths:
           head, tail = ntpath.split(path)
           fileName=tail.split(".")[0]
           if fileName in FileNames :
                QtGui.QMessageBox.warning(self, "Warning", "You Already add "+ fileName+".arxml")
           else :
                FileNames.append(fileName)
                self.addItemToListView(fileName,Path(path))
                self.checkCompleteSchema()
        '''
        if len(path)!=0:
            head, tail = ntpath.split(path[0])
            print(head)
            print(tail)
            fileName=tail.split(".")[0]
            fileType=tail.split(".")[-1]
            if fileType!="arxml" and fileType!="xml"   :
                QtGui.QMessageBox.warning(self, "Warning", "Add Only xml Files ")
            elif fileName in FileNames :
                QtGui.QMessageBox.warning(self, "Warning", "You Already add this File")
            else :
                FileNames.append(fileName)
                self.addItemToListView(fileName,Path(path))
            # parser(name)
                self.checkCompleteSchema()
         '''
    def addItemToListView(self,filename,path):

        if filename=="DataTypesAndInterfaces":
            try:
                if len(Data_Elements) == 0:
                    Data_Elements.append(Port_Interface_Parser(path).Get_SR_Data_Elements())
                self.listView.append(str('%s - Data Types and Interfaces File' % filename))
                globalallFilePaths["globalDatatypesandInterfacesFilePath"] = path
            except:
                QtGui.QMessageBox.warning(self,"Warning","Not a correct Data Types File")
        elif filename=="Com" :
            #TODO
            #globalallFilePaths["globalComFilePath"]=path
            #try:
                #ComSignals = Com_Parser()
            self.listView.append(str('%s - Com File' % filename))
        elif filename=="OS" :
            try:
                parsexml2 = ParseArxml(path)
                _, taskListAll = parsexml2.GetTaskList()
                for element in taskListAll:
                    taskList.append(element[0])
                self.listView.append(str('%s - Os File' % filename))
                globalallFilePaths["globalOSFilePath"]=path
            except:
                QtGui.QMessageBox.warning(self,"Warning","Not a correct OS File")

        else :
            try:
                Software_Component = SWC_Parser(path)
                Runnables = Component(path)
                # print(Software_Component.Get_P_PortsFromComponent())
                SWCsPports[filename] = Software_Component.Get_P_PortsFromComponent()
                SWCsRports[filename] = Software_Component.Get_R_PortsFromComponent()
                SWCsRunnables[filename] = Runnables.Get_Runnables()
                self.listView.append(str('%s - Software Component File' % filename))
                globalallFilePaths["globalSwcsFilePaths"][filename]= path
                if "globalProjectName" not in globalallFilePaths :
                    globalallFilePaths["globalProjectName"]=(Software_Component.GetProjectName())
            except:
                QtGui.QMessageBox.warning(self,"Warning","Not a correct AutoSar File")


    # Check that OS, SWCs , DataTypesandInterfaces, COM arxml files are added
    def checkCompleteSchema(self):

        if len(SWCsRunnables) > 1 and len(Data_Elements) > 0 and len(taskList) > 0 :  # TODO : Com Signals
            self.connect_pushButton.setEnabled(True)
    def openRteWindow(self):
        dialog=connection(self)

        dialog.show()
        self.hide()

    def addSwc (self):
        # RTE Tool
        btn = QtGui.QPushButton("Add swc", self)
        btn.resize(100,50)
        btn.move(20,320)

def main():
    app= QtGui.QApplication(sys.argv)
    QtGui.qApp = app
    GUI= Window()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()