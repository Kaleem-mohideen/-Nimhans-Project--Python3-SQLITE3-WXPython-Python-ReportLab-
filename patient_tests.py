import os
import wx  
import wx.lib.agw.thumbnailctrl as TC
from PIL import Image
import datetime
import wx.adv
import wx.lib.scrolledpanel as scrolled
import dbManager as db

filename="regis.jpeg"
class MyApp(wx.App):
    def __init__(self):
        super().__init__()

        frame = MyFrame(parent=None, title="Menu Bar App")
        frame.Show()


class MyFrame(wx.Frame):         
    def __init__(self, parent, title): 
        super().__init__(parent, title = title, size = (500, 400))  
        self.InitUI()
        # wx.Frame.__init__(self, None, wx.ID_ANY, "Choose Dot in Picture", size=(700,500))
        self.panel = wx.Panel(self, wx.ID_ANY)
        jpeg = wx.Image(filename, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image=wx.StaticBitmap(self.panel, -1, jpeg, (150, 80), (jpeg.GetWidth(), jpeg.GetHeight()))
        #print(image.GetScaleMode())
        image.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
        self.Show(True)

    def on_clic(self, evt):
        PatientDetails(self, title = 'ENTER PATIENT DETAILS')
        x, y=evt.GetPosition()
        #print("clicked at", x, y)


    def InitUI(self):   
        #self.text = wx.TextCtrl(parent=self, id=wx.ID_ANY, style = wx.EXPAND|wx.TE_MULTILINE) 
        menuBar = wx.MenuBar() 

        reportsMenu = ReportsMenu(parentFrame=self)
        menuBar.Append(reportsMenu, '&Reports') 

        masterMenu = MasterMenu(parentFrame=self)
        menuBar.Append(masterMenu, '&Master')

        self.SetMenuBar(menuBar) 

        #self.Bind(wx.EVT_MENU, self.MenuHandler)
        self.Centre() 
        self.Show(True)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
class ReportsMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame
    
    def OnInit(self):
        generateItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Generate', kind=wx.ITEM_NORMAL)
        self.Append(generateItem)
        self.Bind(wx.EVT_MENU, handler=self.onGenerate, source=generateItem)

        viewItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text="&View", helpString="Save your file", kind=wx.ITEM_NORMAL)
        self.Append(viewItem)
        self.Bind(wx.EVT_MENU, handler=self.onView, source=viewItem)


        
        quitItem = wx.MenuItem(parentMenu=self, id=wx.ID_EXIT, text='&Quit\tCtrl+Q') 
        self.Append(quitItem)
        self.Bind(wx.EVT_MENU, handler=self.onQuit, source=quitItem)

    def onGenerate(self, event):
        app = wx.App(redirect=False)
        frame = GeneratePanel(None, 'TESTS GENERATE')
        frame.SetSize((800, 580))
        frame.Show()
        app.MainLoop()

    def onView(self, event):
        dialog = wx.FileDialog(self.parentFrame, message="Save your data", 
                            defaultFile="Untitled.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return None
        
        path = dialog.GetPath()
        data = self.parentFrame.text.GetValue()
        print(data)
        data = data.split('\n')
        print(data)
        with open(path, "w+") as myfile:
            for line in data:
                myfile.write(line+"\n")


    def onQuit(self, event):
        self.parentFrame.Close()

#---------------------------------------------------------------------------------------------------------------------------------------------

class MasterMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame

    def OnInit(self):
        testMasterItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Test Master', kind=wx.ITEM_NORMAL)
        self.Append(testMasterItem)
        self.Bind(wx.EVT_MENU, handler=self.onTestMaster, source=testMasterItem) 

    def onTestMaster(self, event):
        app = wx.App(redirect=False)
        frame = TestMasterPanel(None, 'Test Master')
        frame.SetSize((800, 580))
        frame.Show()
        app.MainLoop()
        #pass

#---------------------------------------------------------------------------------------------------------------------------------------------

class TestMasterPanel(wx.Frame):
    def __init__(self, parent, title):
        super(TestMasterPanel, self).__init__(parent, title = title)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()      
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)
        self.test_itemsid = {dict_value['Name'] : dict_key  for lst_items in db.getAssayList() for dict_key, dict_value in lst_items.items()}
        if len(self.test_itemsid)==1 and list(self.test_itemsid.keys())[0] == None and list(self.test_itemsid.values())[0] == None:
            self.test_items = []
            self.test_itemsid = {}
        else:
            self.test_items = [i for i in self.test_itemsid]
        print(self.test_itemsid)
        self.testsList = wx.ListBox(self.panel, choices=self.test_items, size=(270, 250), style=wx.LB_MULTIPLE)
        #self.testsList.SetSelection(0)
        sizer.Add(self.testsList, pos = (0,0), flag = wx.ALL|wx.EXPAND, border = 5)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.testsList)

        self.antibodiesBtn = wx.Button(self.panel, label = "Antibody", size=(90, 28)) 
        self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))



        sizer.Add(self.antibodiesBtn, pos = (2,0), flag = wx.LEFT, border = 50)
        sizer.Add(self.discardBtn, pos = (1,3), flag = wx.RIGHT, border = 50)
        sizer.Add(addBtn, pos = (8,0), flag = wx.LEFT, border = 50)

        self.antibodiesBtn.Bind(wx.EVT_BUTTON, self.onAntibodiesClick)
        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)
        addBtn.Bind(wx.EVT_BUTTON, self.onAdd)

        if not self.test_items:
            self.discardBtn.Disable()
            self.antibodiesBtn.Disable()
        else:
            self.discardBtn.Enable()
            self.antibodiesBtn.Enable()

        sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(sizer)

    def onListboxSelection(self, evt):
        #pass
        self.index = evt.GetSelection()
        

    def onDiscard(self, evt):
        if self.index != None:
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                self.selectedString = str(self.testsList.GetString(self.index))
                #print(self.selectedString)
                print(self.test_itemsid[self.selectedString])
                if db.disableAssay(self.test_itemsid[self.selectedString]):
                    del self.test_itemsid[self.selectedString] 
                    self.test_items.remove(self.selectedString)
                    if not self.test_items:
                        self.antibodiesBtn.Disable()
                        self.discardBtn.Disable()
                    self.testsList.Deselect(self.index)
                    self.index = None
                    self.testsList.Set(self.test_items)
                    print(self.test_itemsid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.testsList.Deselect(self.index)
            self.index = None
        dlg = MyDialog(self)
        print(self.test_itemsid)
        dlg.Destroy()

    def onAntibodiesClick(self, evt):
        if self.index != None:
            selectedString = str(self.testsList.GetString(self.index))
            app = wx.App(redirect=False)
            Antibdy_Frame = AntibodyMasterPanel(None, 'Antibody Master', selectedString, self.test_itemsid)
            self.testsList.Deselect(self.index)
            self.index = None
            Antibdy_Frame.SetSize((800, 580))
            Antibdy_Frame.Show()
            app.MainLoop()

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog(wx.Dialog, TestMasterPanel):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the test name that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.addtext.SetFont(font)
        self.addtext.SetForegroundColour('#848484') 
        self.addtext.SetHint("Enter the test name")  # This text is grey, and disappears when you type
        self.addPanel.SetFocus()

        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.text, 0, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.addtext, 1, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.addBtn, 2, wx.ALL, 5)
        self.addPanel.SetSizer(self.panel_sizer)

        self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.addtext.Bind(wx.EVT_TEXT_ENTER,self.onAdd)
        self.addtext.Bind(wx.EVT_TEXT,self.onFirstClick)  



        self.ShowModal()
        #wx.CallAfter(self.panel_sizer.Layout)

    def onFirstClick(self, evt):
        if self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        testInput = None
        if self.addtext.GetValue(): testInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 


        if testInput is not None and testInput not in self.parent.test_items:
            addedAssayId = db.addAssay(testInput)
            if addedAssayId != -1:
                self.parent.test_itemsid[testInput] = addedAssayId
                self.parent.test_items.append(testInput)
                self.parent.testsList.Set(self.parent.test_items)
                self.parent.discardBtn.Enable()
                self.parent.antibodiesBtn.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif testInput is not None:
            msgBox = wx.MessageBox('The Test had already exists, Try Adding New Test', 'Existing Error', wx.OK| wx.ICON_WARNING)
            # print(msgBox)
            # print(wx.OK)
            if msgBox == wx.OK:
                self.addtext.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the test name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class AntibodyMasterPanel(wx.Frame):
    def __init__(self, parent, title, selectedString, assayIdDict):
        super(AntibodyMasterPanel, self).__init__(parent, title = title)
        self.parentFrame = parent
        self.testName = selectedString
        self.assayId = assayIdDict[self.testName]
        self.Antibdy_index = None 
        self.Result_index = None  
        self.choices = []
        self.flag = 1
        self.InitUI()
        self.Centre() 
        self.Show()      

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(0,0)

        self.test_name = wx.StaticText(self.panel, label = self.testName + ':', size = (20, 100)) 
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.test_name.SetFont(font)
        self.sizer.Add(self.test_name, pos = (0,0), flag = wx.TOP|wx.LEFT|wx.EXPAND, border = 4)

        self.antibdy_itemsid = {antibody['Name'] : anti_id  for anti_id, antibody in db.getAntiBodies(self.assayId).items()}
        #print(self.antibdy_itemsid)
        if len(self.antibdy_itemsid)==1 and list(self.antibdy_itemsid.keys())[0] == None and list(self.antibdy_itemsid.values())[0] == None:
            self.Antibdy_items = []
            self.antibdy_itemsid = {}
        else:
            self.Antibdy_items = [antibodyNames for antibodyNames in self.antibdy_itemsid if antibodyNames]
        self.AntibdyList = wx.ListBox(self.panel, choices=self.Antibdy_items, size=(270, 100), style=wx.LB_MULTIPLE)
        print(self.antibdy_itemsid)
        #self.AntibdyList.SetSelection(0)
        self.sizer.Add(self.AntibdyList, pos = (1,0), flag = wx.BOTTOM|wx.LEFT|wx.EXPAND, border = 40)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.AntibdyList)

        self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        self.addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))

        self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.discardBtn.Bind(wx.EVT_BUTTON, self.onMsg)

        self.sizer.Add(self.discardBtn, pos = (2,3), flag = wx.RIGHT, border = 50)
        self.sizer.Add(self.addBtn, pos = (5,0), flag = wx.LEFT|wx.BOTTOM, border = 50)

        if not self.Antibdy_items:
            self.discardBtn.Disable()
        else:
            self.discardBtn.Enable()

        self.sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(self.sizer)

    def onMsg(self, evt):
        if self.Antibdy_index == None and self.Result_index == None:
            wx.MessageBox('None of them Choosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onListboxSelection(self, evt):
        self.Antibdy_index = evt.GetSelection()

        if self.Result_index != None:
            self.listResult.Deselect(self.Result_index)
            self.Result_index = None

        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)

        self.antibdy_selectedText = str(self.AntibdyList.GetString(self.Antibdy_index))
        self.antiId = self.antibdy_itemsid[self.antibdy_selectedText]
        #print(self.assayId)
        getAntibdyDict = db.getAntiBodies(self.assayId)
        #print(self.antiId)
        #print(getAntibdyDict)
        self.choicesid ={choice: choiceId for choiceId, choice in getAntibdyDict[self.antiId]['Options'].items()}
        print(self.choicesid)

        if not self.choices and self.flag:
            if len(self.choicesid)==1 and list(self.choicesid.keys())[0] == None and list(self.choicesid.values())[0] == None:
                self.choices = []
                self.flag = 0
            else:
                self.choices= [choice for choice in self.choicesid if choice]
            self.listResult = wx.ListBox(self.panel, choices= self.choices, size=(270, 100), style=wx.LB_MULTIPLE)
            self.addBtnResult = wx.Button(self.panel, label = "Add", size=(90, 28))
            font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            self.antibdytitletResult = wx.StaticText(self.panel, label = self.antibdy_selectedText)
            self.antibdytitletResult.SetFont(font)
            #self.listResult.SetSelection(0)
            self.sizer.Add(self.antibdytitletResult, pos = (0,5), flag = wx.TOP|wx.RIGHT|wx.EXPAND, border = 40)
            self.sizer.Add(self.listResult, pos = (1,5), flag = wx.BOTTOM|wx.RIGHT|wx.EXPAND, border = 40)
            self.sizer.Add(self.addBtnResult, pos = (5,5), flag = wx.BOTTOM|wx.RIGHT, border = 50)
            self.sizer.AddGrowableCol(5)

        else:
            if len(self.choicesid)==1 and list(self.choicesid.keys())[0] == None and list(self.choicesid.values())[0] == None:
                self.choices = []
                self.choicesid = {}
                self.flag = 0
            else:
                self.choices= [choice for choice in self.choicesid if choice]
            self.antibdytitletResult.SetLabel(self.antibdy_selectedText)
            self.listResult.Set(self.choices)
            self.addBtnResult.Enable()
        self.Bind(wx.EVT_LISTBOX, self.onListbox1Selection, self.listResult)
        self.addBtnResult.Bind(wx.EVT_BUTTON, self.onAddResult)
        self.panel.SetSizerAndFit(self.sizer)
        
    def onListbox1Selection(self, evt):
        self.Result_index = evt.GetSelection()

        if self.Antibdy_index != None:
            self.AntibdyList.Deselect(self.Antibdy_index)
            self.Antibdy_index = None

        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscardResult)

    def onDiscard(self, evt):
        if self.Antibdy_index != None:
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard Antibody->{0} from Test->{1}?'.format(self.antibdy_selectedText, self.testName), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                print(self.antibdy_itemsid[self.antibdy_selectedText])
                if db.disableAntiBody(self.assayId, self.antibdy_itemsid[self.antibdy_selectedText]):
                    del self.antibdy_itemsid[self.antibdy_selectedText]
                    self.Antibdy_items.remove(self.antibdy_selectedText)
                    self.AntibdyList.Deselect(self.Antibdy_index)
                    self.Antibdy_index = None
                    if not self.Antibdy_items:
                        self.discardBtn.Disable()
                    self.AntibdyList.Set(self.Antibdy_items)
                    self.listResult.Clear()
                    self.antibdytitletResult.SetLabel('')
                    self.addBtnResult.Disable()
                    print(self.antibdy_itemsid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.Antibdy_index != None:
            self.AntibdyList.Deselect(self.Antibdy_index)
            self.Antibdy_index = None
            self.listResult.Clear()
            self.antibdytitletResult.SetLabel('')
            self.addBtnResult.Disable()
        dlg1 = MyDialog1(self)
        print(self.antibdy_itemsid)
        dlg1.Destroy()

    def onDiscardResult(self, evt):
        if self.Result_index != None:
            self.selected_String1 = str(self.listResult.GetString(self.Result_index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard Option->{0} from Antibody->{1}?'.format(self.selected_String1, self.antibdy_selectedText), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                optionId = self.choicesid[self.selected_String1]
                print(optionId)
                ret_value = db.disableOption(self.assayId, self.antiId, optionId)
                if ret_value != -1:
                    del self.choicesid[self.selected_String1]
                    self.choices.remove(self.selected_String1)
                    if not self.choices:
                        self.flag = 0
                    self.listResult.Deselect(self.Result_index)
                    self.Result_index = None
                    self.listResult.Set(self.choices)
                    print(self.choicesid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAddResult(self, evt):
        if self.Result_index != None:
            self.listResult.Deselect(self.Result_index)
            self.Result_index = None

        dlg2 = MyDialog2(self)
        print(self.choicesid)
        dlg2.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog1(wx.Dialog, AntibodyMasterPanel):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.text = wx.StaticText(self.addPanel, -1, 'Enter the Antibody name that you want to Add in Test->{0}:'.format(self.parent.testName), pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.addtext.SetFont(font)
        self.addtext.SetForegroundColour('#848484') 
        self.addtext.SetHint("Enter the Antibody name")  # This text is grey, and disappears when you type
        self.addPanel.SetFocus()

        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.text, 0, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.addtext, 1, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.addBtn, 2, wx.ALL, 5)
        self.addPanel.SetSizer(self.panel_sizer)

        self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.addtext.Bind(wx.EVT_TEXT_ENTER,self.onAdd)
        self.addtext.Bind(wx.EVT_TEXT,self.onFirstClick)  



        self.ShowModal()
        #wx.CallAfter(self.panel_sizer.Layout)

    def onFirstClick(self, evt):
        if self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        testInput = None
        if self.addtext.GetValue(): testInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 
        if testInput is not None and testInput not in self.parent.Antibdy_items:
            addedAntibdyId = db.addAntiBody(self.parent.assayId, testInput)
            if addedAntibdyId != -1 and type(addedAntibdyId) == int:
                self.parent.antibdy_itemsid[testInput] = addedAntibdyId
                self.parent.Antibdy_items.append(testInput)
                self.parent.AntibdyList.Set(self.parent.Antibdy_items)
                self.parent.discardBtn.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif testInput is not None:
            msgBox = wx.MessageBox('The Antibody had already exists, Try Adding New Antibody', 'Existing Error', wx.OK| wx.ICON_WARNING)
            #msg = msgBox.ShowModal()
            # print(msgBox)
            # print(wx.OK)
            if msgBox == wx.OK:
                self.addtext.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Antibody name")  # This text is grey, and disappears when you type

#---------------------------------------------------------------------------------------------------------------------------------------------

class MyDialog2(wx.Dialog, AntibodyMasterPanel):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.text1 = wx.StaticText(self.addPanel, -1,'Enter the Option that you want to Add in Antibody->{0}:'.format(self.parent.antibdy_selectedText), pos=(10, 12))
        self.addtext1 = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn1 = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.addtext1.SetFont(font)
        self.addtext1.SetForegroundColour('#848484') 
        self.addtext1.SetHint("Enter the Option name")  # This text is grey, and disappears when you type
        self.addPanel.SetFocus()

        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.text1, 0, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.addtext1, 1, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.addBtn1, 2, wx.ALL, 5)
        self.addPanel.SetSizer(self.panel_sizer)

        self.addBtn1.Bind(wx.EVT_BUTTON, self.onAdd1)
        self.addtext1.Bind(wx.EVT_TEXT_ENTER,self.onAdd1)
        self.addtext1.Bind(wx.EVT_TEXT,self.onFirstClick1)  



        self.ShowModal()
        #wx.CallAfter(self.panel_sizer.Layout)

    def onFirstClick1(self, evt):
        if self.addtext1.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour(wx.BLACK)

    def onAdd1(self, evt):
        testInput = None
        if self.addtext1.GetValue(): testInput =self.addtext1.GetValue()
        if self.addtext1.GetValue() and self.addtext1.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour('#848484') 
        if testInput is not None and testInput not in self.parent.choices:
            addedChoiceId = db.addOption(self.parent.assayId, self.parent.antiId, testInput)
            if addedChoiceId and type(addedChoiceId) == int:
                self.parent.choicesid[testInput] = addedChoiceId
                self.parent.choices.append(testInput)
                self.parent.listResult.Set(self.parent.choices)
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif testInput is not None:
            msgBox = wx.MessageBox('The Option had already exists, Try Adding New Option', 'Existing Error', wx.OK| wx.ICON_WARNING)
            #msg = msgBox.ShowModal()
            # print(msgBox)
            # print(wx.OK)
            if msgBox == wx.OK:
                self.addtext1.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.addtext1.SetFont(font)
                self.addtext1.SetForegroundColour('#848484')
                self.addtext1.SetHint("Enter the Option name")  # This text is grey, and disappears when you type

#---------------------------------------------------------------------------------------------------------------------------------------------
class PatientDetails(wx.Frame): 
    def __init__(self, parent, title):
        super(PatientDetails, self).__init__(parent, title = title, size = (700, 500)) 
        #self = parent
        self.parentFrame = parent  
        self.InitUI() 
        self.Centre() 
        self.Show()      
         
    def InitUI(self): 
       
        panel = wx.Panel(self) 
        sizer = wx.GridBagSizer(0,0)
            
        text = wx.StaticText(panel, label = "UHID:") 
        sizer.Add(text, pos = (0, 0), flag = wx.ALL, border = 5)
            
        self.tc = wx.TextCtrl(panel) 
        sizer.Add(self.tc, pos = (0, 1), flag = wx.ALL|wx.EXPAND, border = 5)

        text1 = wx.StaticText(panel, label = "Referring Hospital:")
        sizer.Add(text1, pos = (0, 2), flag = wx.ALL, border = 5)

        self.tc1 = wx.TextCtrl(panel) 
        sizer.Add(self.tc1, pos = (0,3),flag = wx.EXPAND|wx.ALL, border = 5)
         
        text2 = wx.StaticText(panel, label = "MRD No:") 
        sizer.Add(text2, pos = (1, 0), flag = wx.ALL, border = 5)
            
        self.tc2 = wx.TextCtrl(panel) 
        sizer.Add(self.tc2, pos = (1,1), flag = wx.ALL|wx.EXPAND, border = 5) 

        text3 = wx.StaticText(panel,label = "Referring Dept:") 
        sizer.Add(text3, pos = (1, 2), flag = wx.ALL, border = 5)

        self.tc3 = wx.TextCtrl(panel) 
        sizer.Add(self.tc3, pos = (1,3),flag = wx.EXPAND|wx.ALL, border = 5)
         
        text4 = wx.StaticText(panel,label = "Patient Name:") 
        sizer.Add(text4, pos = (2, 0), flag = wx.ALL, border = 5) 
            
        self.tc4 = wx.TextCtrl(panel) 
        sizer.Add(self.tc4, pos = (2,1), flag = wx.ALL|wx.EXPAND, border = 5) 
            
        text5 = wx.StaticText(panel,label = "Sample Collection Date:") 
        sizer.Add(text5, pos = (2, 2), flag = wx.ALL, border = 5)
            
        self.tc5 = wx.TextCtrl(panel) 
        sizer.Add(self.tc5, pos = (2,3),flag = wx.EXPAND|wx.ALL, border = 5) 
         
        text6 = wx.StaticText(panel, label = "Age:") 
        sizer.Add(text6, pos = (3, 0), flag = wx.ALL, border = 5) 
            
        self.tc6 = wx.TextCtrl(panel) 
        sizer.Add(self.tc6, pos = (3,1), flag = wx.ALL|wx.EXPAND, border = 5) 
        #sizer.AddGrowableRow(3)

        text7 = wx.StaticText(panel,label = "Lab Reference No:") 
        sizer.Add(text7, pos = (3, 2), flag = wx.ALL, border = 5)

        self.tc7 = wx.TextCtrl(panel) 
        sizer.Add(self.tc7, pos = (3,3), flag = wx.EXPAND|wx.ALL, border = 5)

        text8 = wx.StaticText(panel,label = "Gender:")
        sizer.Add(text8, pos = (4, 0), flag = wx.ALL, border = 5) 
            
        sampleList = ['Male', 'Female']
        self.gender = wx.RadioBox(panel, -1, "", wx.DefaultPosition, wx.DefaultSize, sampleList, 2, wx.RA_SPECIFY_COLS) 
        sizer.Add(self.gender, pos = (4,1), flag = wx.ALL, border = 5) 

        text9 = wx.StaticText(panel,label = "Report Generated Date:") 
        sizer.Add(text9, pos = (4, 2), flag = wx.ALL, border = 5)

        self.tc9 = wx.TextCtrl(panel) 
        sizer.Add(self.tc9, pos = (4,3),flag = wx.ALL|wx.EXPAND, border = 5)

        text10 = wx.StaticText(panel,label = "Ward Name/Collection Centre:") 
        sizer.Add(text10, pos = (5, 0), flag = wx.ALL, border = 5) 
            
        self.tc10 = wx.TextCtrl(panel) 
        sizer.Add(self.tc10, pos = (5,1), flag = wx.ALL|wx.EXPAND, border = 5) 

        text11 = wx.StaticText(panel,label = "Lab Name:") 
        sizer.Add(text11, pos = (5, 2), flag = wx.ALL, border = 5)

        self.tc11 = wx.TextCtrl(panel) 
        sizer.Add(self.tc11, pos = (5,3),flag = wx.EXPAND|wx.ALL, border = 5) 

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
         
        saveBtn = wx.Button(panel, label = "Save", size=(90, 28)) 
        cancelBtn = wx.Button(panel, wx.ID_CLOSE, label = "Cancel", size=(90, 28)) 
            
        sizer.Add(cancelBtn, pos = (8, 2), flag = wx.LEFT, border = 50) 
        sizer.Add(saveBtn, pos = (8, 3), flag = wx.RIGHT|wx.BOTTOM, border = 10)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        saveBtn.Bind(wx.EVT_BUTTON, self.OnScreen3)

        #sizer.AddGrowableRow()
        panel.SetSizerAndFit(sizer)

    def OnScreen3(self, evt):
        dic = {}
        dic['UHID'] = self.tc.GetValue()
        dic['Referring Hospital'] = self.tc1.GetValue()
        dic['MRD No'] = self.tc2.GetValue()
        dic['Referring Dept'] = self.tc3.GetValue()
        dic['Patient Name'] = self.tc4.GetValue()
        dic['Sample Collection Date'] = self.tc5.GetValue()
        dic['Age'] = self.tc6.GetValue()
        dic['Lab Reference No'] = self.tc7.GetValue()
        dic['Gender'] = 'Female' if self.gender.GetSelection() else 'Male'
        dic['Report Generated Date'] = self.tc9.GetValue()
        dic['Ward Name/Collection Centre'] = self.tc10.GetValue()
        dic['Lab Name'] = self.tc11.GetValue()
        print(dic)
        Screen3(None, -1, 'listbox')

    def onClose(self, event):
        """"""
        self.Close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------


class Screen3(wx.Frame):
    def __init__(self, parent, id, title):
        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (650, 450))
        super(Screen3, self).__init__(parent, id, title, wx.DefaultPosition, (650, 450))
        self.second_zones = []
        zone_list = ['CET', 'GMT', 'MSK', 'EST', 'PST', 'EDT']


        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0,0)
        
        text = wx.StaticText(panel, label = "Tests")
        self.time_zones = wx.ListBox(panel, -1, size=(170, 130), choices=zone_list, style=wx.LB_SINGLE)
        #self.time_zones.SetSelection(0)
        text2 = wx.StaticText(panel, label = "Choosen Tests")
        self.time_zones2 = wx.ListBox(panel, -1, size=(170, 130), choices=[], style=wx.LB_SINGLE)



        #self.Bind(wx.EVT_LISTBOX, self.OnSelectFirst, self.time_zones)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectFirst, self.time_zones)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectSecond, self.time_zones2)
        #self.Bind(wx.EVT_LISTBOX, self.OnSelectSecond, self.time_zones2)

        sizer.Add(text, pos = (1, 0), flag = wx.LEFT|wx.TOP, border = 100)
        sizer.Add(text2, pos = (1, 3), flag = wx.LEFT|wx.RIGHT|wx.TOP, border = 100)
        sizer.Add(self.time_zones, pos = (2, 0), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)
        sizer.Add(self.time_zones2, pos = (2, 3), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)

        saveBtn = wx.Button(panel, wx.ID_CLOSE, label = "Save", size=(90, 28)) 
        cancelBtn = wx.Button(panel, label = "Cancel", size=(90, 28)) 
            
        sizer.Add(cancelBtn, pos = (4, 2), flag = wx.RIGHT, border = 50) 
        sizer.Add(saveBtn, pos = (4, 3), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
        #sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(4)
        panel.SetSizerAndFit(sizer)
        self.Centre() 
        self.Show(True)

    def onClose(self, event):
        """"""
        self.Close()

    def OnSelectFirst(self, event):
        index = event.GetSelection()
        time_zone = str(self.time_zones.GetString(index))
        if time_zone not in self.second_zones:
            self.second_zones.append(time_zone)
            self.time_zones2.Set(self.second_zones)
        else:
            print('Already selected')
            wx.MessageBox('Choosen Already, Try selecting other', 'Selected Already', wx.OK | wx.CANCEL | wx.ICON_WARNING)
            #self.time_zones.SetString(index, 'Already Choosen')


    def OnSelectSecond(self, event):
        index = event.GetSelection()
        #print(index)
        time_zone = str(self.time_zones2.GetString(index))
        self.second_zones.remove(time_zone)
        self.time_zones2.Set(self.second_zones) 





#---------------------------------------------------------------------------------------------------------------------------------------------------------------------



class GeneratePanel(wx.Frame):
    def __init__(self, parent, title):
        super(GeneratePanel, self).__init__(parent, title = title, size = (700, 500)) 

        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.SetSizer(sizer)
        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer()

        self.dpc1 = wx.adv.DatePickerCtrl( panel, wx.ID_ANY, wx.DefaultDateTime, size=(120,-1))
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateChanged, self.dpc1)
        sizer.Add(self.dpc1, (3,9), (2, 4), wx.RIGHT|wx.BOTTOM, 40)
        # In some cases the widget used above will be a native date
        # picker, so show the generic one too.
        self.dpc2 = wx.adv.GenericDatePickerCtrl(panel, wx.ID_ANY, wx.DefaultDateTime, size=(120,-1), style = wx.TAB_TRAVERSAL| wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnToDateChanged, self.dpc2)
        sizer.Add(self.dpc2, (3,16), (2, 4), wx.LEFT|wx.BOTTOM, 40)
        now = wx.DateTime.Now()
        print(wx.DateTime.FormatISODate(now))
        print(wx.DateTime.Format(now))
        
        
        self.searchExpectedResults = wx.SearchCtrl(panel,
                                    size=(250, -1),
                                    style=wx.TE_PROCESS_ENTER)
        #self.searchExpectedResults.style = wx.BORDER_RAISED
        sizer.Add(self.searchExpectedResults, (1, 8), (1, 14), wx.EXPAND|wx.RIGHT, 40)
        self.searchExpectedResults.Bind(wx.EVT_CHAR, self.on_char) # Bind an EVT_CHAR event to your SearchCtrl

        filterBtn = wx.Button(panel, label = "Filter", size=(90, 28))
        sizer.Add(filterBtn, pos = (5, 11), flag = wx.LEFT|wx.BOTTOM, border = 50)
        filterBtn.Bind(wx.EVT_BUTTON, self.onfilter)

        search_items = sorted(['test', 'entry'])
        self.textareaExpectedResults = wx.ListBox(panel, choices=search_items, size=(270, 250))
        sizer.Add(self.textareaExpectedResults, (6, 8), (2, 14), wx.EXPAND|wx.RIGHT, 40)

        sizer.AddGrowableCol(9)
        sizer.AddGrowableCol(16)
        sizer.AddGrowableCol(8)
         
        generateBtn = wx.Button(panel, label = "Generate", size=(90, 28)) 
        cancelBtn = wx.Button(panel, wx.ID_CLOSE, label = "Cancel", size=(90, 28)) 

        sizer.Add(cancelBtn, pos = (10, 11), flag = wx.RIGHT|wx.BOTTOM, border = 50) 
        sizer.Add(generateBtn, pos = (10, 17), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        generateBtn.Bind(wx.EVT_BUTTON, self.OnScreen)

        sizer.AddGrowableRow(6)
        panel.SetSizerAndFit(sizer)
        #sizer.Add(sizer)
        # self.SetSizer(sizer)
        # self.Sizer = sizer
        # self.Sizer.Fit(self)
        #self.SetupScrolling()

    def onfilter(self, evt):
        pass

    def OnScreen(self, event):
        ResultDetails(None, -1, 'Result Details')
        #pass

    def onClose(self, event):
        """"""
        self.Close()


    def OnFromDateChanged(self, evt):
        selected_date = evt.GetDate()
        self.dpc2.SetRange(dt1= selected_date, dt2= wx.DefaultDateTime)
        self.dpc1.SetRange(dt1= wx.DefaultDateTime, dt2= self.dpc2.GetValue())
        print (selected_date.Format("%d-%m-%Y"))

    def OnToDateChanged(self, evt):
        selected_date = evt.GetDate()
        self.dpc1.SetRange(dt1= wx.DefaultDateTime, dt2= selected_date)
        self.dpc2.SetRange(dt1= self.dpc1.GetValue(), dt2= wx.DefaultDateTime)
        print (selected_date.Format("%d-%m-%Y"))

    def onMatches(self):
        getValue = self.searchExpectedResults.GetValue() # get the entered string in TextCtrl with GetValue method
        print (getValue)
        search_items = sorted(['test', 'entry']) # Create a list of all searchable items in a list
        self.textareaExpectedResults.Clear()
        for item in search_items:
            if getValue in item:
                print (item)
                self.textareaExpectedResults.Append(item) # Clear the ListBox and append the matching strings in search_items to the ListBox

    def on_char(self, event):
        event.Skip()
        wx.CallAfter(self.onMatches)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------


class ResultDetails(wx.Frame):
    def __init__(self, parent, id, title):
        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (650, 450))
        super(ResultDetails, self).__init__(parent, id, title, wx.DefaultPosition, (1100, 900))
        TestPanel(self)
        self.Show()

class TestPanel(scrolled.ScrolledPanel):

    def __init__(self, parent):

        scrolled.ScrolledPanel.__init__(self, parent=parent, id= -1)

        listbox_elements = ['CET', 'GMT', 'MSK', 'EST', 'PST', 'EDT']

        self.tests = wx.ListBox(self, -1, size=(370, 130), choices=listbox_elements, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.Onlistbox, self.tests)
        sizer1 = wx.GridBagSizer()
        sizer1.Add(self.tests, pos = (2, 13), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)
        updateBtn = wx.Button(self, label = "Update", size=(90, 28))
        sizer1.Add(updateBtn, pos = (6, 12), flag = wx.LEFT|wx.BOTTOM, border = 50)
        updateBtn.Bind(wx.EVT_BUTTON, self.onUpdate)
        k = 7
        for i in range(10):
            antibody = wx.StaticText(self, wx.ID_ANY, 'Antibody')
            self.inputTwo = wx.Choice(self, choices=['+ve', '-ve', 'C'])
            self.inputTwo.SetSelection(0)
            comment = wx.StaticText(self, wx.ID_ANY, 'Comment')
            sizer1.Add(antibody, pos = (k,9), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)
            sizer1.Add(self.inputTwo, pos = (k,12), flag = wx.LEFT|wx.BOTTOM, border = 100)
            sizer1.Add(comment, pos = (k,13), flag = wx.LEFT|wx.BOTTOM, border = 50)
            k+=1

        saveBtn = wx.Button(self, label = "Save", size=(90, 28))
        sizer1.Add(saveBtn, pos = (k+1, 13), flag = wx.LEFT|wx.BOTTOM, border = 250)
        saveBtn.Bind(wx.EVT_BUTTON, self.onUpdate)

        sizer1.AddGrowableCol(9)
        #sizer1.AddGrowableCol(11)
        sizer1.AddGrowableCol(12)
        sizer1.AddGrowableCol(13)

        self.SetSizerAndFit(sizer1)
        self.SetupScrolling()

    def Onlistbox(self, evt):
        pass

    def onUpdate(self, evt):
        pass

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()