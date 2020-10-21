import os
import wx  
import wx.lib.agw.thumbnailctrl as TC
from PIL import Image
import datetime as dt
import wx.adv
import wx.lib.scrolledpanel as scrolled
import dbManager as db
import pdf1 as pdf
import utils as utilsDb
import string
import wx.richtext as rt
from collections import OrderedDict
import subprocess, os, platform
import wx.lib.newevent
from io import BytesIO

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
        frame = GeneratePanel(None, 'PENDING REPORTS')
        frame.SetSize((1000, 880))
        frame.Show()
        app.MainLoop()

    def onView(self, event):
        app = wx.App(redirect=False)
        frame = ViewPanel(None, 'VIEW REPORTS')
        frame.SetSize((1000, 880))
        frame.Show()
        app.MainLoop()     

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
        HospitalMasterItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Hospital Master', kind=wx.ITEM_NORMAL)
        self.Append(HospitalMasterItem)
        self.Bind(wx.EVT_MENU, handler=self.onHospitalMaster, source=HospitalMasterItem)
        LabMasterItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Lab Master', kind=wx.ITEM_NORMAL)
        self.Append(LabMasterItem)
        self.Bind(wx.EVT_MENU, handler=self.onLabMaster, source=LabMasterItem)
        DepartmentMasterItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Department Master', kind=wx.ITEM_NORMAL)
        self.Append(DepartmentMasterItem)
        self.Bind(wx.EVT_MENU, handler=self.onDepartmentMaster, source=DepartmentMasterItem)

    def onTestMaster(self, event):
        app = wx.App(redirect=False)
        frame = TestMasterPanel(None, 'Test Master')
        frame.SetSize((800, 580))
        frame.Show()
        app.MainLoop()
        #pass
    def onHospitalMaster(self, event):
        app = wx.App(redirect=False)
        frame = HospitalMasterPanel(None, 'Hospital Master')
        frame.SetSize((800, 580))
        frame.Show()
        app.MainLoop()

    def onLabMaster(self, event):
        app = wx.App(redirect=False)
        frame = LabMasterPanel(None, 'Lab Master')
        frame.SetSize((800, 580))
        frame.Show()
        app.MainLoop()

    def onDepartmentMaster(self, event):
        app = wx.App(redirect=False)
        frame = DepartmentMasterPanel(None, 'Department Master')
        frame.SetSize((800, 580))
        frame.Show()
        app.MainLoop()
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
        self.Centre()
        self.Layout() 

    def onListboxSelection(self, evt):
        #pass
        self.index = evt.GetSelection()
        

    def onDiscard(self, evt):
        if self.index != None:
            self.selectedString = str(self.testsList.GetString(self.index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} test?'.format(self.selectedString), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
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
            wx.MessageBox('None of them Choosen, Try Choosing Test that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

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
            Antibdy_Frame.SetSize((1500, 580))
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
        self.text = wx.StaticText(self.addPanel, -1, "Enter the test that you want to Add:", pos=(10, 12))
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
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Test'.format(testInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
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
        self.sizer.Add(self.AntibdyList, pos = (1,0), flag = wx.BOTTOM|wx.LEFT|wx.EXPAND, border = 10)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.AntibdyList)

        self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        self.addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))

        self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.discardBtn.Bind(wx.EVT_BUTTON, self.onMsg)

        self.sizer.Add(self.discardBtn, pos = (5,1), flag = wx.RIGHT, border = 50)
        self.sizer.Add(self.addBtn, pos = (5,0), flag = wx.LEFT|wx.BOTTOM, border = 10)

        if not self.Antibdy_items:
            self.discardBtn.Disable()
        else:
            self.discardBtn.Enable()

        self.sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(self.sizer)

    def onMsg(self, evt):
        if self.Antibdy_index == None :  
            wx.MessageBox('None of them Choosen, Try Choosing any Antibody that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

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
        comment = getAntibdyDict[self.antiId]['Comment']

        try:
            _stringIO = StringIO(open('output.xml').read())
            _handler = wx.richtext.RichTextXMLHandler()
            _handler.LoadFile(self.rt.GetBuffer(), 'output.xml')
            self.rt.Refresh()
        except Exception as ex:
            print(ex)

        self.comment = comment if comment else ''

        if not self.choices and self.flag:
            if len(self.choicesid)==1 and list(self.choicesid.keys())[0] == None and list(self.choicesid.values())[0] == None:
                self.choices = []
                self.flag = 0
            else:
                self.choices= [choice for choice in self.choicesid if choice]
            self.listResult = wx.ListBox(self.panel, choices= self.choices, size=(270, 100), style=wx.LB_MULTIPLE)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            #save_button = wx.Button(self, label="Save")
            self.Bold = wx.Button(self, label="B", size=(25, 18))
            self.Italic = wx.Button(self, label="I", size=(25, 18))

            self.Bold.Bind(wx.EVT_BUTTON, self.on_Bold)
            self.Italic.Bind(wx.EVT_BUTTON, self.on_italic)

            if self.comment:
                self.commentRichTxtctrl = rt.RichTextCtrl(self, value= self.comment, size=(250, 100))
            else:
                self.commentRichTxtctrl = rt.RichTextCtrl(self, value="", size=(250, 100))

            sizer.Add(self.commentRichTxtctrl, 1, wx.EXPAND|wx.ALL, 6)
            sizer1.Add(self.Bold, 0, wx.EXPAND|wx.ALL, 6)
            sizer1.Add(self.Italic, 0, wx.EXPAND|wx.ALL, 6)
            sizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 6)

            # self.commentRichTxtctrl = wx.TextCtrl(self, id=-1, value='', pos=wx.DefaultPosition,size=(270,100), style= wx.TE_MULTILINE | wx.SUNKEN_BORDER)
            # self.commentRichTxtctrl.SetValue(self.comment)
            self.addBtnResult = wx.Button(self.panel, label = "Add", size=(90, 28))
            self.discardBtnResult = wx.Button(self.panel, label = "Discard", size=(90, 28))
            self.saveBtnComment = wx.Button(self.panel, label = "Save", size=(90, 28))
            font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            self.antibdytitletResult = wx.StaticText(self.panel, label = self.antibdy_selectedText + '{0}'.format(' Options'))
            self.antibdytitletResult.SetFont(font)
            self.antibdytitletComment = wx.StaticText(self.panel, label = self.antibdy_selectedText + '{0}'.format(' Comment'))
            self.antibdytitletComment.SetFont(font)
            #self.listResult.SetSelection(0)
            self.sizer.Add(self.antibdytitletResult, pos = (0,5), flag = wx.TOP|wx.RIGHT|wx.EXPAND, border = 40)
            self.sizer.Add(self.listResult, pos = (1,5), flag = wx.BOTTOM|wx.RIGHT|wx.EXPAND, border = 10)
            self.sizer.Add(self.antibdytitletComment, pos = (0,7), flag = wx.TOP|wx.RIGHT|wx.EXPAND, border = 40)
            self.sizer.Add(sizer, pos = (1,7), flag = wx.BOTTOM|wx.RIGHT|wx.EXPAND, border = 10)
            self.sizer.Add(self.addBtnResult, pos = (5,5), flag = wx.BOTTOM|wx.RIGHT, border = 10)
            self.sizer.Add(self.discardBtnResult, pos = (5,6), flag = wx.RIGHT, border = 50)
            self.sizer.Add(self.saveBtnComment, pos = (5,8), flag = wx.RIGHT, border = 50)
            self.sizer.AddGrowableCol(5)
            self.sizer.AddGrowableCol(4)

        else:
            if len(self.choicesid)==1 and list(self.choicesid.keys())[0] == None and list(self.choicesid.values())[0] == None:
                self.choices = []
                self.choicesid = {}
                self.flag = 0
            else:
                self.choices= [choice for choice in self.choicesid if choice]
            self.antibdytitletResult.SetLabel(self.antibdy_selectedText+ '{0}'.format(' Options'))
            self.antibdytitletComment.SetLabel(self.antibdy_selectedText+ '{0}'.format(' Comment'))
            self.listResult.Set(self.choices)
            self.commentRichTxtctrl.Show()
            self.commentRichTxtctrl.SetValue(self.comment)
            self.saveBtnComment.Show()
            self.addBtnResult.Enable()
            self.discardBtnResult.Enable()
        self.Bind(wx.EVT_LISTBOX, self.onListbox1Selection, self.listResult)
        self.addBtnResult.Bind(wx.EVT_BUTTON, self.onAddResult)
        self.discardBtnResult.Bind(wx.EVT_BUTTON, self.onMsg1)
        self.saveBtnComment.Bind(wx.EVT_BUTTON, self.onSaveComment)
        self.panel.SetSizerAndFit(self.sizer)
        self.Centre()
        self.Layout()
        #self.panel.SetSize(wx.Size(1000,1400))

    def on_Bold(self,evt):
        _selection = self.commentRichTxtctrl.GetStringSelection()
        if _selection:
            print(_selection)
            if self.commentRichTxtctrl.IsSelectionBold():
                self.Bold.SetBackgroundColour(wx.Colour(240, 240, 240))
            elif not self.commentRichTxtctrl.IsSelectionBold():
                self.Bold.SetBackgroundColour(wx.LIGHT_GREY)
            self.commentRichTxtctrl.ApplyBoldToSelection()
            self.commentRichTxtctrl.SetFocus()
            return
        self.color_Match = self.Bold.GetBackgroundColour() == wx.LIGHT_GREY
        print(self.color_Match)
        if not self.color_Match:
            print('Bold',True)
            # self.Bold.SetFocus()
            self.Bold.SetBackgroundColour(wx.LIGHT_GREY)
            self.commentRichTxtctrl.SetFocus()
            pos1 = self.commentRichTxtctrl.GetCaretPosition()
            self.commentRichTxtctrl.SetInsertionPoint(pos1+1)
            self.commentRichTxtctrl.BeginBold()

        elif self.color_Match:
            self.commentRichTxtctrl.SetFocus()
            pos1 = self.commentRichTxtctrl.GetCaretPosition()
            self.commentRichTxtctrl.SetInsertionPoint(pos1+1)
            self.commentRichTxtctrl.EndBold()
            self.Bold.SetBackgroundColour(wx.Colour(240, 240, 240))
            print('Bold',False)


    def on_italic(self, evt):
        _selection = self.commentRichTxtctrl.GetStringSelection()
        if _selection:
            print(_selection)
            if self.commentRichTxtctrl.IsSelectionItalics():
                self.Italic.SetBackgroundColour(wx.Colour(240, 240, 240))
            elif not self.commentRichTxtctrl.IsSelectionItalics():
                self.Italic.SetBackgroundColour(wx.LIGHT_GREY)
            self.commentRichTxtctrl.ApplyItalicToSelection()
            self.commentRichTxtctrl.SetFocus()
            return
        self.color_Match1 = self.Italic.GetBackgroundColour() == wx.LIGHT_GREY
        if not self.color_Match1:
            print('Italic',True)
            self.Italic.SetBackgroundColour(wx.LIGHT_GREY)
            self.commentRichTxtctrl.SetFocus()
            pos1 = self.commentRichTxtctrl.GetCaretPosition()
            self.commentRichTxtctrl.SetInsertionPoint(pos1+1)
            self.commentRichTxtctrl.BeginItalic()

        elif self.color_Match1:
            self.commentRichTxtctrl.SetFocus()
            pos1 = self.commentRichTxtctrl.GetCaretPosition()
            self.commentRichTxtctrl.SetInsertionPoint(pos1+1)
            self.Italic.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.commentRichTxtctrl.EndItalic()
            print('Italic', False)

    def onSaveComment(self, evt):
        out = BytesIO()
        handler = wx.richtext.RichTextXMLHandler()
        rt_buffer = self.commentRichTxtctrl.GetBuffer()
        handler.SaveFile(rt_buffer, out)
        xml_content = out.getvalue()

        _comment = xml_content.decode('utf-8') #self.commentRichTxtctrl.GetValue()
        if db.updateAntiBodyComment(self.assayId, self.antibdy_itemsid[self.antibdy_selectedText], _comment):
            if _comment:
                dialog = wx.MessageBox('Comment is Updated for {0} test'.format(self.antibdy_selectedText), 'Successfully Updated', wx.OK)
            # if dialog == wx.OK:
            #     self.Close()
        
    def onMsg1(self, evt):
        if self.Result_index == None :  
            wx.MessageBox('None of them Choosen, Try Choosing any Option that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)


    def onDiscard(self, evt):
        if self.Antibdy_index != None:
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard Antibody->{0} for {1} Test?'.format(self.antibdy_selectedText, self.testName), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
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
                    self.commentRichTxtctrl.Hide()
                    self.saveBtnComment.Hide()
                    self.antibdytitletComment.Hide()
                    self.antibdytitletResult.SetLabel('')
                    self.addBtnResult.Disable()
                    self.discardBtnResult.Disable()
                    print(self.antibdy_itemsid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing any Antibody that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.Antibdy_index != None:
            self.AntibdyList.Deselect(self.Antibdy_index)
            self.Antibdy_index = None
            self.listResult.Clear()
            self.antibdytitletResult.SetLabel('')
            self.commentRichTxtctrl.Hide()
            self.saveBtnComment.Hide()
            self.antibdytitletComment.Hide()
            self.addBtnResult.Disable()
            self.discardBtnResult.Disable()
        dlg1 = MyDialog1(self)
        print(self.antibdy_itemsid)
        dlg1.Destroy()

    def onListbox1Selection(self, evt):
        self.Result_index = evt.GetSelection()

        if self.Antibdy_index != None:
            self.AntibdyList.Deselect(self.Antibdy_index)
            self.Antibdy_index = None

        self.discardBtnResult.Bind(wx.EVT_BUTTON, self.onDiscardResult)

    def onDiscardResult(self, evt):
        if self.Result_index != None:
            self.selected_String1 = str(self.listResult.GetString(self.Result_index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard Option->{0} for {1} Antibody?'.format(self.selected_String1, self.antibdy_selectedText), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
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
                        self.discardBtnResult.Disable()
                    self.listResult.Deselect(self.Result_index)
                    self.Result_index = None
                    self.listResult.Set(self.choices)
                    print(self.choicesid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing any Option that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

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
        self.text = wx.StaticText(self.addPanel, -1, 'Enter the Antibody that you want to Add in Test->{0}:'.format(self.parent.testName), pos=(10, 12))
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
        antibdyInput = None
        if self.addtext.GetValue(): antibdyInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 
        if antibdyInput is not None and antibdyInput not in self.parent.Antibdy_items:
            addedAntibdyId = db.addAntiBody(self.parent.assayId, antibdyInput)
            if addedAntibdyId != -1 and type(addedAntibdyId) == int:
                self.parent.antibdy_itemsid[antibdyInput] = addedAntibdyId
                self.parent.Antibdy_items.append(antibdyInput)
                self.parent.AntibdyList.Set(self.parent.Antibdy_items)
                self.parent.discardBtn.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif antibdyInput is not None:
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Antibody'.format(antibdyInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
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
        optionInput = None
        if self.addtext1.GetValue(): optionInput =self.addtext1.GetValue()
        if self.addtext1.GetValue() and self.addtext1.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour('#848484') 
        if optionInput is not None and optionInput not in self.parent.choices:
            addedChoiceId = db.addOption(self.parent.assayId, self.parent.antiId, optionInput)
            if addedChoiceId and type(addedChoiceId) == int:
                self.parent.choicesid[optionInput] = addedChoiceId
                self.parent.choices.append(optionInput)
                self.parent.listResult.Set(self.parent.choices)
                self.parent.discardBtnResult.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif optionInput is not None:
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Option'.format(optionInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
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
class HospitalMasterPanel(wx.Frame):
    def __init__(self, parent, title):
        super(HospitalMasterPanel, self).__init__(parent, title = title)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)
        self.hsp_items = db.getHospitals()
        print(self.hsp_items)
        self.hspList = wx.ListBox(self.panel, choices=self.hsp_items, size=(270, 250), style=wx.LB_MULTIPLE)
        sizer.Add(self.hspList, pos = (0,0), flag = wx.ALL|wx.EXPAND, border = 5)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.hspList)

        self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))


        sizer.Add(self.discardBtn, pos = (1,3), flag = wx.RIGHT, border = 50)
        sizer.Add(addBtn, pos = (8,0), flag = wx.LEFT, border = 50)

        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)
        addBtn.Bind(wx.EVT_BUTTON, self.onAdd)

        if not self.hsp_items:
            self.discardBtn.Disable()
        else:
            self.discardBtn.Enable()

        sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(sizer)
        self.Centre()
        self.Layout() 

    def onListboxSelection(self, evt):
        #pass
        self.index = evt.GetSelection()
        

    def onDiscard(self, evt):
        if self.index != None:
            self.selectedString = str(self.hspList.GetString(self.index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} Hospital?'.format(self.selectedString), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                print(self.selectedString)
                if db.disableHospital(self.selectedString):
                    self.hsp_items.remove(self.selectedString)
                    if not self.hsp_items:
                        self.discardBtn.Disable()
                    self.hspList.Deselect(self.index)
                    self.index = None
                    self.hspList.Set(self.hsp_items)
                    print(self.hsp_items)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Hospital that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.hspList.Deselect(self.index)
            self.index = None
        dlg = MyDialog3(self)
        print(self.hsp_items)
        dlg.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------

class MyDialog3(wx.Dialog, HospitalMasterPanel):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the Hospital that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.addtext.SetFont(font)
        self.addtext.SetForegroundColour('#848484') 
        self.addtext.SetHint("Enter the Hospital name")  # This text is grey, and disappears when you type
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

    def onFirstClick(self, evt):
        if self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        hspInput = None
        if self.addtext.GetValue(): hspInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 


        if hspInput is not None and hspInput not in self.parent.hsp_items:
            addedHsp = db.addHospital(hspInput)
            if addedHsp:
                self.parent.hsp_items.append(hspInput)
                self.parent.hspList.Set(self.parent.hsp_items)
                self.parent.discardBtn.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif hspInput is not None:
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Hospital'.format(hspInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
            if msgBox == wx.OK:
                self.addtext.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Hospital name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class LabMasterPanel(wx.Frame):
    def __init__(self, parent, title):
        super(LabMasterPanel, self).__init__(parent, title = title)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)
        self.lab_items = db.getLabs()
        print(self.lab_items)
        self.labList = wx.ListBox(self.panel, choices=self.lab_items, size=(270, 250), style=wx.LB_MULTIPLE)
        #self.labList.SetSelection(0)
        sizer.Add(self.labList, pos = (0,0), flag = wx.ALL|wx.EXPAND, border = 5)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.labList)

        self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))


        sizer.Add(self.discardBtn, pos = (1,3), flag = wx.RIGHT, border = 50)
        sizer.Add(addBtn, pos = (8,0), flag = wx.LEFT, border = 50)

        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)
        addBtn.Bind(wx.EVT_BUTTON, self.onAdd)

        if not self.lab_items:
            self.discardBtn.Disable()
        else:
            self.discardBtn.Enable()

        sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(sizer)
        self.Centre()
        self.Layout() 

    def onListboxSelection(self, evt):
        #pass
        self.index = evt.GetSelection()
        

    def onDiscard(self, evt):
        if self.index != None:
            self.selectedString = str(self.labList.GetString(self.index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} Lab?'.format(self.selectedString), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                print(self.selectedString)
                if db.disableLab(self.selectedString):
                    self.lab_items.remove(self.selectedString)
                    if not self.lab_items:
                        self.discardBtn.Disable()
                    self.labList.Deselect(self.index)
                    self.index = None
                    self.labList.Set(self.lab_items)
                    print(self.lab_items)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Lab that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.labList.Deselect(self.index)
            self.index = None
        dlg = MyDialog4(self)
        print(self.lab_items)
        dlg.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog4(wx.Dialog, LabMasterPanel):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the Lab that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.addtext.SetFont(font)
        self.addtext.SetForegroundColour('#848484') 
        self.addtext.SetHint("Enter the Lab name")  # This text is grey, and disappears when you type
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
        labInput = None
        if self.addtext.GetValue(): labInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 


        if labInput is not None and labInput not in self.parent.lab_items:
            addedLab = db.addLab(labInput)
            if addedLab:
                self.parent.lab_items.append(labInput)
                self.parent.labList.Set(self.parent.lab_items)
                self.parent.discardBtn.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif labInput is not None:
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Lab'.format(labInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
            if msgBox == wx.OK:
                self.addtext.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Lab name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class DepartmentMasterPanel(wx.Frame):
    def __init__(self, parent, title):
        super(DepartmentMasterPanel, self).__init__(parent, title = title)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)
        self.dpt_items = db.getDepartments()
        print(self.dpt_items)
        self.dptList = wx.ListBox(self.panel, choices=self.dpt_items, size=(270, 250), style=wx.LB_MULTIPLE)
        #self.dptList.SetSelection(0)
        sizer.Add(self.dptList, pos = (0,0), flag = wx.ALL|wx.EXPAND, border = 5)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.dptList)

        self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))


        sizer.Add(self.discardBtn, pos = (1,3), flag = wx.RIGHT, border = 50)
        sizer.Add(addBtn, pos = (8,0), flag = wx.LEFT, border = 50)

        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)
        addBtn.Bind(wx.EVT_BUTTON, self.onAdd)

        if not self.dpt_items:
            self.discardBtn.Disable()
        else:
            self.discardBtn.Enable()

        sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(sizer)
        self.Centre()
        self.Layout() 

    def onListboxSelection(self, evt):
        #pass
        self.index = evt.GetSelection()
        

    def onDiscard(self, evt):
        if self.index != None:
            self.selectedString = str(self.dptList.GetString(self.index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} Department?'.format(self.selectedString), 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                print(self.selectedString)
                if db.disableDepartment(self.selectedString):
                    self.dpt_items.remove(self.selectedString)
                    if not self.dpt_items:
                        self.discardBtn.Disable()
                    self.dptList.Deselect(self.index)
                    self.index = None
                    self.dptList.Set(self.dpt_items)
                    print(self.dpt_items)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Choosen, Try Choosing Department that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.dptList.Deselect(self.index)
            self.index = None
        dlg = MyDialog5(self)
        print(self.dpt_items)
        dlg.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog5(wx.Dialog, DepartmentMasterPanel):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the Department that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
        self.addtext.SetFont(font)
        self.addtext.SetForegroundColour('#848484') 
        self.addtext.SetHint("Enter the Department name")  # This text is grey, and disappears when you type
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
        dptInput = None
        if self.addtext.GetValue(): dptInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 


        if dptInput is not None and dptInput not in self.parent.dpt_items:
            addedDpt = db.addDepartment(dptInput)
            if addedDpt:
                self.parent.dpt_items.append(dptInput)
                self.parent.dptList.Set(self.parent.dpt_items)
                self.parent.discardBtn.Enable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif dptInput is not None:
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Department'.format(dptInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
            if msgBox == wx.OK:
                self.addtext.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL)
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Department name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class CharValidator(wx.Validator):
    ''' Validates data as it is entered into the text controls. '''

    #----------------------------------------------------------------------
    def __init__(self, flag):
        wx.Validator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    #----------------------------------------------------------------------
    def Clone(self):
        '''Required Validator method'''
        return CharValidator(self.flag)

    #----------------------------------------------------------------------
    def Validate(self, win):
        return True

    #----------------------------------------------------------------------
    def TransferToWindow(self):
        return True

    #----------------------------------------------------------------------
    def TransferFromWindow(self):
        return True

    #----------------------------------------------------------------------
    def OnChar(self, event):
        keycode = int(event.GetKeyCode())
        if keycode < 256:
            #print keycode
            key = chr(keycode)
            #print key
            if self.flag == 'only-digit' and key in string.ascii_letters or key in string.punctuation:
                return
            if self.flag == 'only-alpha' and key in string.digits or key in string.punctuation:
                return
        event.Skip()
class MouseNavigate(wx.Validator):
    ''' Validates data as it is entered into the text controls. This validator is used to ensure that the user has entered something
         into the text object editor dialog's text field.'''

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """ Standard constructor."""
        wx.Validator.__init__(self)
        self.parent = parent
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)

      #----------------------------------------------------------------------
    def Clone(self):
        '''Required Validator method. Standard cloner.
             Note that every validator must implement the Clone() method.'''
        return MouseNavigate(self.parent)

      #----------------------------------------------------------------------
    def Validate(self, win):
        return True

      #----------------------------------------------------------------------
    def TransferToWindow(self):
        """ Transfer data from validator to window.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
        return True
      #----------------------------------------------------------------------
    def TransferFromWindow(self):
        """ Transfer data from window to validator.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
        return True # Prevent wxDialog from complaining
      #----------------------------------------------------------------------
    """ Validate the contents of the given text control.
         """
    def OnMouseEvent(self, event):
        if event.Moving():
            self.parent.SetCursor(wx.STANDARD_CURSOR)

    def OnSetFocus(self, event):
        self.parent.Navigate(wx.NavigationKeyEvent.IsForward)

class PatientDetails(wx.Frame): 
    def __init__(self, parent, title):
        super(PatientDetails, self).__init__(parent, title = title, size = (700, 500)) 
        self.parentFrame = parent  
        #HIGHLIGHT_COLOR = (255, 0, 0)
        #self.highligt_color = wx.Colour(HIGHLIGHT_COLOR)
        self.windowFrameColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME)
        self.InitUI() 
        self.Centre() 
        self.Show()      

    def Assign(self, rtc, strng):
        #print(strng)
        rtc.WriteText(strng)
        rtc.BeginFontSize(12)
        rtc.BeginBold()
        rtc.BeginTextColour('red')
        rtc.WriteText ("*")
        rtc.EndTextColour()
        rtc.EndBold()
        rtc.EndFontSize()
        rtc.EnableVerticalScrollbar(False)
        rtc.GetCaret().Hide()
        rtc.SetBackgroundColour(self.windowFrameColor)

    def InitUI(self): 
       
        self.panel = wx.Panel(self) 
        sizer = wx.GridBagSizer(0,0)
            
        #text = wx.StaticText(self.panel, label = "UHID:") 
        text = rt.RichTextCtrl(self.panel,size=(130,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self))
        self.Assign(text, "UHID:")
        sizer.Add(text, pos = (0, 0), flag = wx.ALL, border = 5)
        
        self.tc = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc, pos = (0, 1), flag = wx.ALL|wx.EXPAND, border = 5)
        self.tc.SetToolTip("Enter UHID No.")

        #text1 = wx.StaticText(self.panel, label = "Referring Hospital:")
        text1 = rt.RichTextCtrl(self.panel,size=(170,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self))
        self.Assign(text1, "Referring Hospital:")
        sizer.Add(text1, pos = (0, 2), flag = wx.ALL, border = 5)

        self.hsp_items = db.getHospitals()
        self.hsp_items.insert(0, "-- Select --")
        self.tc1 = wx.Choice(self.panel, choices= self.hsp_items)
        self.tc1.SetSelection(0)
        #self._droplist.Bind(wx.EVT_CHOICE, self.choice_click) 
        sizer.Add(self.tc1, pos = (0,3),flag = wx.EXPAND|wx.ALL, border = 5)
         
        text2 = wx.StaticText(self.panel, label = " MRD No:") 
        sizer.Add(text2, pos = (1, 0), flag = wx.ALL, border = 5)
            
        self.tc2 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc2, pos = (1,1), flag = wx.ALL|wx.EXPAND, border = 5) 

        text3 = wx.StaticText(self.panel,label = " Referring Dept:") 
        sizer.Add(text3, pos = (1, 2), flag = wx.ALL, border = 5)

        self.dpt_items = db.getDepartments()
        self.dpt_items.insert(0, "-- Select --")
        self.tc3 = wx.Choice(self.panel, choices= self.dpt_items)
        self.tc3.SetSelection(0)
        sizer.Add(self.tc3, pos = (1,3),flag = wx.EXPAND|wx.ALL, border = 5)
         
        #text4 = wx.StaticText(self.panel,label = "Patient Name:")
        text4 = rt.RichTextCtrl(self.panel,size=(130,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self))
        self.Assign(text4, "Patient Name:")
        sizer.Add(text4, pos = (2, 0), flag = wx.ALL, border = 5) 
            
        self.tc4 = wx.TextCtrl(self.panel, validator=CharValidator('only-alpha')) 
        sizer.Add(self.tc4, pos = (2,1), flag = wx.ALL|wx.EXPAND, border = 5) 
            
        text5 = wx.StaticText(self.panel,label = " Sample Collection Date:") 
        sizer.Add(text5, pos = (2, 2), flag = wx.ALL, border = 5)

        self.date1 = wx.adv.DatePickerCtrl( self.panel, wx.ID_ANY, size=(120,-1), style = wx.TAB_TRAVERSAL| wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE)
        self.date1.SetValue(wx.DefaultDateTime)
        self.date1.SetToolTip("Select date of Sample Collection")
        sizer.Add(self.date1, pos = (2,3),flag = wx.EXPAND|wx.ALL, border = 5)
        #invaliddt = wx.DateTime()
        #.SetValue(invaliddt)
         
        #text6 = wx.StaticText(self.panel, label = "Date of Birth:") 
        text6 = rt.RichTextCtrl(self.panel,size=(130,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self))
        self.Assign(text6, "Date of Birth:")
        sizer.Add(text6, pos = (3, 0), flag = wx.ALL, border = 5)

        self.date2 = wx.adv.DatePickerCtrl( self.panel, wx.ID_ANY, size=(120,-1), style = wx.TAB_TRAVERSAL| wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE)
        self.date2.SetValue(wx.DefaultDateTime)
        self.date2.SetToolTip("Select Date of Birth")
        sizer.Add(self.date2, pos = (3,1), flag = wx.ALL|wx.EXPAND, border = 5)
        self.date2.SetRange(dt1= wx.DefaultDateTime, dt2= wx.DateTime.Now())
        #self.Age.SetMaxLength(3)   
        #sizer.AddGrowableRow(3)

        text7 = wx.StaticText(self.panel,label = " Lab Reference No:") 
        sizer.Add(text7, pos = (3, 2), flag = wx.ALL, border = 5)

        self.tc7 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc7, pos = (3,3), flag = wx.EXPAND|wx.ALL, border = 5)

        #text8 = wx.StaticText(self.panel,label = "Gender:")
        text8 = rt.RichTextCtrl(self.panel,size=(130,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self))
        self.Assign(text8, "Gender:")
        sizer.Add(text8, pos = (4, 0), flag = wx.ALL, border = 5) 
            
        sampleList = ['Male', 'Female']
        self.gender = wx.RadioBox(self.panel, -1, "", wx.DefaultPosition, wx.DefaultSize, sampleList, 2, wx.RA_SPECIFY_COLS) 
        sizer.Add(self.gender, pos = (4,1), flag = wx.ALL, border = 5) 

        text9 = wx.StaticText(self.panel,label = " Lab Name:") 
        sizer.Add(text9, pos = (4, 2), flag = wx.ALL, border = 5)

        self.lab_items = db.getLabs()
        self.lab_items.insert(0, "-- Select --")
        self.tc8 = wx.Choice(self.panel, choices= self.lab_items)
        self.tc8.SetSelection(0)
        sizer.Add(self.tc8, pos = (4,3),flag = wx.EXPAND|wx.ALL, border = 5) 

        text10 = wx.StaticText(self.panel,label = " Ward Name/Collection Centre:") 
        sizer.Add(text10, pos = (5, 0), flag = wx.ALL, border = 5) 
            
        self.tc9 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc9, pos = (5,1), flag = wx.ALL|wx.EXPAND, border = 5) 

        text11 = wx.StaticText(self.panel,label = "Email:") 
        sizer.Add(text11, pos = (5, 2), flag = wx.ALL, border = 5)

        self.tc10 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc10, pos = (5,3),flag = wx.ALL|wx.EXPAND, border = 5)

        text12 = wx.StaticText(self.panel,label = "Phone No:") 
        sizer.Add(text12, pos = (6, 0), flag = wx.ALL, border = 5)

        self.tc11 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc11, pos = (6,1),flag = wx.ALL|wx.EXPAND, border = 5)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
         
        saveBtn = wx.Button(self.panel, label = "Save", size=(90, 28)) 
        cancelBtn = wx.Button(self.panel, wx.ID_CLOSE, label = "Cancel", size=(90, 28))
        saveBtn.SetToolTip("Register")
            
        sizer.Add(cancelBtn, pos = (8, 2), flag = wx.LEFT, border = 50) 
        sizer.Add(saveBtn, pos = (8, 3), flag = wx.RIGHT|wx.BOTTOM, border = 10)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        saveBtn.Bind(wx.EVT_BUTTON, self.onRegisterPatient)

        self.panel.SetSizerAndFit(sizer)

    def onRegisterPatient(self, evt):
        dic = {}
        dic['UHID'] = self.tc.GetValue() if self.tc.GetValue() else None
        dic['Referring Hospital'] = self.tc1.GetStringSelection() if self.tc1.GetSelection() else None
        dic['MRD No'] = self.tc2.GetValue() if self.tc2.GetValue()  else None
        dic['Referring Dept'] = self.tc3.GetStringSelection() if self.tc3.GetSelection() else None
        dic['Patient Name'] = self.tc4.GetValue() if self.tc4.GetValue() else None
        dic['Sample Collection Date'] = dt.date(*(map(int, wx.DateTime.FormatISODate(self.date1.GetValue()).split('-')))) if self.date1.GetValue().IsValid() else None
        dic['Date of Birth'] = dt.date(*(map(int, wx.DateTime.FormatISODate(self.date2.GetValue()).split('-')))) if self.date2.GetValue().IsValid() else None
        dic['Lab Reference No'] = self.tc7.GetValue() if self.tc7.GetValue() else None
        dic['Gender'] = 'F' if self.gender.GetSelection() else 'M'
        #dic['Report Generated Date'] = self.tc9.GetValue()
        dic['Lab Name'] = self.tc8.GetStringSelection() if self.tc8.GetSelection() else None
        dic['Ward Name/Collection Centre'] = self.tc9.GetValue() if self.tc9.GetValue() else None
        dic['Email'] = self.tc10.GetValue() if self.tc10.GetValue() else None
        dic['phone'] = self.tc11.GetValue() if self.tc11.GetValue() else None
        print(dic)
        if dic['UHID']:
            if dic['Referring Hospital']:
                if dic['Patient Name']:
                    if dic['Date of Birth']:
                        if dic['Gender']:
                            _requestId = db.registerPatient(dic['UHID'], dic['Patient Name'], dic['Date of Birth'], dic['Referring Hospital'], dic['Gender'], dic['MRD No'], dic['Ward Name/Collection Centre'], dic['Sample Collection Date'], dic['Lab Reference No'], dic['Referring Dept'], dic['Lab Name'], dic['Email'], dic['phone'])
                            TestRegisterScreen(None, -1, 'Register Tests', _requestId, dic['Patient Name'])
                        else:
                            #color = self.windowFrameColor if self.textctrl.GetValue() else self.highligt_color
                            #self.gender.SetHint("Mandatory field")
                            tip = wx.adv.RichToolTip("Mandatory","Field is empty,Choose Gender\n""\n""Fill the Mandatory field.")
                            tip.SetIcon(wx.ICON_WARNING)
                            tip.ShowFor(self.gender)
                    else:
                        #self.date2.SetHint("Mandatory field")
                        tip = wx.adv.RichToolTip("Mandatory","Field is empty,Enter Date of Birth\n""\n""Fill the Mandatory field.")
                        tip.SetIcon(wx.ICON_WARNING)
                        tip.ShowFor(self.date2)
                else:
                    self.tc4.SetHint("Mandatory field")
                    tip = wx.adv.RichToolTip("Mandatory","Field is empty,Enter Patient Name\n""\n""Fill the Mandatory field.")
                    tip.SetIcon(wx.ICON_WARNING)
                    tip.ShowFor(self.tc4)

            else:
                #self.tc1.SetHint("Mandatory field")
                tip = wx.adv.RichToolTip("Mandatory","Field is empty,Enter Referring Hospital\n""\n""Fill the Mandatory field.")
                tip.SetIcon(wx.ICON_WARNING)
                tip.ShowFor(self.tc1)
        else:
            self.tc.SetHint("Mandatory field")
            tip = wx.adv.RichToolTip("Mandatory","Field is empty,Enter UHID Number\n""\n""Fill the Mandatory field.")
            tip.SetIcon(wx.ICON_WARNING)
            tip.ShowFor(self.tc)


    def onClose(self, event):
        """"""
        self.Close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------


class TestRegisterScreen(wx.Frame):
    def __init__(self, parent, id, title, _requestId, patientName):
        # #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (650, 450))
        # self.requestId = _requestId
        # super(TestRegisterScreen, self).__init__(parent, id, title, wx.DefaultPosition, (650, 450))
        # self.testsUpdateList_items = []
        # self.test_itemsChosenid = []
        # self.test_itemsid = {dict_value['Name'] : dict_key  for lst_items in db.getAssayList() for dict_key, dict_value in lst_items.items()}
        # if len(self.test_itemsid)==1 and list(self.test_itemsid.keys())[0] == None and list(self.test_itemsid.values())[0] == None:
        #     self.test_items = []
        #     self.test_itemsid = {}
        # else:
        #     self.test_items = [i for i in self.test_itemsid]
        # print(self.test_itemsid)


        # panel = wx.Panel(self, -1)
        # sizer = wx.GridBagSizer(0,0)
        
        # text = wx.StaticText(panel, label = "Tests")
        # self.testsListbox = wx.ListBox(panel, -1, size=(170, 130), choices=self.test_items, style=wx.LB_SINGLE)
        # #self.testsListbox.SetSelection(0)
        # text2 = wx.StaticText(panel, label = "Choosen Tests")
        # self.testsChosenListbox = wx.ListBox(panel, -1, size=(170, 130), choices=[], style=wx.LB_SINGLE)

        # #self.Bind(wx.EVT_LISTBOX, self.OnSelectFirst, self.testsListbox)
        # self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectFirst, self.testsListbox)
        # self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectSecond, self.testsChosenListbox)
        # #self.Bind(wx.EVT_LISTBOX, self.OnSelectSecond, self.testsChosenListbox)

        # sizer.Add(text, pos = (1, 0), flag = wx.LEFT|wx.TOP, border = 100)
        # sizer.Add(text2, pos = (1, 3), flag = wx.LEFT|wx.RIGHT|wx.TOP, border = 100)
        # sizer.Add(self.testsListbox, pos = (2, 0), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)
        # sizer.Add(self.testsChosenListbox, pos = (2, 3), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)

        # saveBtn = wx.Button(panel, wx.ID_CLOSE, label = "Save", size=(90, 28)) 
        # cancelBtn = wx.Button(panel, label = "Cancel", size=(90, 28)) 
            
        # sizer.Add(cancelBtn, pos = (4, 2), flag = wx.RIGHT, border = 50) 
        # sizer.Add(saveBtn, pos = (4, 3), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        # cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        # saveBtn.Bind(wx.EVT_BUTTON, self.onTestRegister)

        # sizer.AddGrowableCol(1)
        # sizer.AddGrowableCol(3)
        # #sizer.AddGrowableRow(0)
        # sizer.AddGrowableRow(4)
        # panel.SetSizerAndFit(sizer)
        # self.Centre() 
        # self.Show(True)

        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (950, 550))
        self.requestId = _requestId
        super(TestRegisterScreen, self).__init__(parent, id, title, wx.DefaultPosition, (950, 550))
        self.testsUpdateList_items = []
        self.test_itemsChosenid = []
        self.test_itemsid = {dict_value['Name'] : dict_key  for lst_items in db.getAssayList() for dict_key, dict_value in lst_items.items()}
        if len(self.test_itemsid)==1 and list(self.test_itemsid.keys())[0] == None and list(self.test_itemsid.values())[0] == None:
            self.test_items = []
            self.test_itemsid = {}
        else:
            self.test_items = [i for i in self.test_itemsid]
        print(self.test_itemsid)


        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer(0,0)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        text = wx.StaticText(panel, label = "Tests")
        self.testsListbox = wx.ListBox(panel, -1, size=(270, 230), choices=self.test_items, style=wx.LB_SINGLE)
        #self.testsListbox.SetSelection(0)
        text2 = wx.StaticText(panel, label = "Choosen Tests")
        self.testsChosenListbox = wx.ListBox(panel, -1, size=(270, 230), choices=[], style=wx.LB_SINGLE)

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        # font1 = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        # font1.SetPointSize(12)

        name = wx.StaticText(self, label= patientName)
        name.SetFont(font)
        # age = wx.StaticText(self, label= "Age     : {0}".format(self.parent.age))
        # age.SetFont(font1)
        # gender = wx.StaticText(self, label= "Gender: {0}".format(self.parent.gender))
        # gender.SetFont(font1)  

        #self.Bind(wx.EVT_LISTBOX, self.OnSelectFirst, self.testsListbox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectFirst, self.testsListbox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectSecond, self.testsChosenListbox)
        #self.Bind(wx.EVT_LISTBOX, self.OnSelectSecond, self.testsChosenListbox)
        vbox.Add(name, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        #sizer.Add(name, pos = (0, 0), flag = wx.CENTER|wx.TOP|wx.BOTTOM, border = 20)
        sizer.Add(text, pos = (1, 0), flag = wx.LEFT, border = 100)
        sizer.Add(text2, pos = (1, 3), flag = wx.LEFT|wx.RIGHT, border = 100)
        sizer.Add(self.testsListbox, pos = (2, 0), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, border = 50)
        sizer.Add(self.testsChosenListbox, pos = (2, 3), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, border = 50)

        saveBtn = wx.Button(panel, wx.ID_CLOSE, label = "Save", size=(90, 28)) 
        cancelBtn = wx.Button(panel, label = "Cancel", size=(90, 28)) 
            
        sizer.Add(cancelBtn, pos = (4, 2), flag = wx.RIGHT, border = 50) 
        sizer.Add(saveBtn, pos = (4, 3), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        saveBtn.Bind(wx.EVT_BUTTON, self.onTestRegister)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableCol(0)
        #sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(4)

        hbox.Add(sizer, flag= wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        vbox.Add(hbox)
        panel.SetSizerAndFit(vbox)
        self.Centre() 
        self.Show(True)
        self.Layout()

    def onClose(self, event):
        """"""
        self.Close()
    def onTestRegister(self, event):
        """"""
        if self.test_itemsChosenid and db.registerAssays(self.requestId, self.test_itemsChosenid):
            dialog = wx.MessageBox('Registered Tests are {0}'.format(self.testsUpdateList_items), 'Successfully Registered', wx.OK)
            if dialog == wx.OK:
                self.Close()
        else:
            if self.test_itemsChosenid:
                wx.MessageBox('Test not Registered', 'Error', wx.OK | wx.ICON_WARNING)
            else:
                wx.MessageBox('None of them Choosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def OnSelectFirst(self, event):
        index = event.GetSelection()
        selected_String = str(self.testsListbox.GetString(index))
        if selected_String not in self.testsUpdateList_items:
            self.testsUpdateList_items.append(selected_String)
            self.test_itemsChosenid.append(self.test_itemsid[selected_String])
            self.testsChosenListbox.Set(self.testsUpdateList_items)
            print(self.testsUpdateList_items)
        else:
            print('Already selected')
            wx.MessageBox('Choosen Already, Try selecting other', 'Selected Already', wx.OK | wx.CANCEL | wx.ICON_WARNING)
            #self.testsListbox.SetString(index, 'Already Choosen')


    def OnSelectSecond(self, event):
        index = event.GetSelection()
        #print(index)
        selected_String1 = str(self.testsChosenListbox.GetString(index))
        self.testsUpdateList_items.remove(selected_String1)
        self.test_itemsChosenid.remove(self.test_itemsid[selected_String1])
        self.testsChosenListbox.Set(self.testsUpdateList_items)
        print(self.testsUpdateList_items)






#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

class GeneratePanel(wx.Frame):
    def __init__(self, parent, title):
        super(GeneratePanel, self).__init__(parent, title = title, size = (700, 1000)) 
        self.index = 0
        self.selectedIndex = None
        self.myRowDict = {}
        self.searchNameDict = {}
        self.myRequestIdDict = {}
        self.details = {}

        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer()

        self.dpc1 = wx.adv.DatePickerCtrl( panel, wx.ID_ANY, size=(120,-1))
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateChanged, self.dpc1)
        self.dpc1.Bind(wx.EVT_SET_FOCUS, self.Onfocus)
        sizer.Add(self.dpc1, (3,9), (2, 4), wx.RIGHT|wx.BOTTOM, 40)

        self.dpc2 = wx.adv.GenericDatePickerCtrl(panel, wx.ID_ANY, wx.DefaultDateTime, size=(120,-1), style = wx.TAB_TRAVERSAL| wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnToDateChanged, self.dpc2)
        self.dpc2.Bind(wx.EVT_SET_FOCUS, self.Onfocus)
        sizer.Add(self.dpc2, (3,16), (2, 4), wx.LEFT|wx.BOTTOM, 40)

        self.dpc1.SetValue(wx.DateTime.Now().SetDay(1))

        self.searchExpectedResults = wx.SearchCtrl(panel,
                                    size=(250, -1),
                                    style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.searchExpectedResults, (1, 8), (1, 14), wx.EXPAND|wx.RIGHT, 40)
        self.searchExpectedResults.Bind(wx.EVT_CHAR, self.on_char) # Bind an EVT_CHAR event to your SearchCtrl
        self.searchExpectedResults.Bind(wx.EVT_SET_FOCUS, self.Onfocus)

        filterBtn = wx.Button(panel, label = "Filter", size=(90, 28))
        sizer.Add(filterBtn, pos = (5, 11), flag = wx.LEFT|wx.BOTTOM, border = 50)
        filterBtn.Bind(wx.EVT_BUTTON, self.onfilter)

        self.textareaExpectedResults = wx.ListCtrl(panel, -1, style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES) 
        self.textareaExpectedResults.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.textareaExpectedResults.InsertColumn(0, 'Patient Name', width = 300) 
        self.textareaExpectedResults.InsertColumn(1, 'Gender', wx.LIST_FORMAT_RIGHT, 70) 
        self.textareaExpectedResults.InsertColumn(2, 'Age', wx.LIST_FORMAT_RIGHT, 100) 
        self.textareaExpectedResults.InsertColumn(3, 'Email', wx.LIST_FORMAT_RIGHT, 100)
        self.textareaExpectedResults.InsertColumn(4, 'Date', wx.LIST_FORMAT_RIGHT, 200)

        frmDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc1.GetValue()).split('-')))) if self.dpc1.GetValue().IsValid() else None
        toDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc2.GetValue()).split('-')))) if self.dpc2.GetValue().IsValid() else None
        Reports = db.getReports(frmDate, toDate)
        self.textareaExpectedResults.DeleteAllItems()
        for i in Reports:
            self.index = self.textareaExpectedResults.InsertItem(self.index, i["patientName"]) 
            self.textareaExpectedResults.SetItem(self.index, 1, i["gender"]) 
            self.textareaExpectedResults.SetItem(self.index, 2, i["age"])
            self.textareaExpectedResults.SetItem(self.index, 3, i["email"] if i["email"] else '')            
            self.textareaExpectedResults.SetItem(self.index, 4, i["requestTime"])
            self.myRowDict[self.index] = [i["patientName"], i["gender"], i["age"], i["email"], i["requestTime"]]
            self.myRequestIdDict[self.index] = i["requestId"]
            self.details[i["requestId"]] = {"Email":i["email"] if i["email"] else ''}
            self.details[i["requestId"]]["Name"] = i["patientName"]
            self.details[i["requestId"]]["Gender"] = i["gender"]
            self.details[i["requestId"]]["Age"] = i["age"]
            self.index+=1
        print(self.myRowDict)
        self.myRequestIdDict1 = self.myRequestIdDict.copy()
        count = self.textareaExpectedResults.GetItemCount()
        for row in range(count):
            item = self.textareaExpectedResults.GetItem(row, col=0)
            self.searchNameDict[item.GetText()] = row 
        
        sizer.Add(self.textareaExpectedResults, (6, 8), (2, 14), wx.EXPAND|wx.RIGHT, 40)

        sizer.AddGrowableCol(9)
        sizer.AddGrowableCol(16)
        sizer.AddGrowableCol(8)
         
        self.generateBtn = wx.Button(panel, label = "Generate", size=(90, 28)) 
        cancelBtn = wx.Button(panel, wx.ID_CLOSE, label = "Cancel", size=(90, 28)) 

        sizer.Add(cancelBtn, pos = (10, 11), flag = wx.RIGHT|wx.BOTTOM, border = 50) 
        sizer.Add(self.generateBtn, pos = (10, 17), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        self.generateBtn.Bind(wx.EVT_BUTTON, self.OnScreen)

        if self.textareaExpectedResults.IsEmpty():
            self.generateBtn.Disable()
        else:
            self.generateBtn.Enable()

        sizer.AddGrowableRow(6)
        panel.SetSizerAndFit(sizer)

    def Onfocus(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None

    def onfilter(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None
        self.myRowDict = {}
        self.searchNameDict = {}
        self.myRequestIdDict = {}
        self.details = {}
        frmDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc1.GetValue()).split('-')))) if self.dpc1.GetValue().IsValid() else None
        toDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc2.GetValue()).split('-')))) if self.dpc2.GetValue().IsValid() else None
        dateFilteredReports = db.getReports(frmDate, toDate)
        self.textareaExpectedResults.DeleteAllItems()
        for i in dateFilteredReports:
            self.index = self.textareaExpectedResults.InsertItem(self.index, i["patientName"]) 
            self.textareaExpectedResults.SetItem(self.index, 1, i["gender"])
            self.textareaExpectedResults.SetItem(self.index, 2, i["age"])
            self.textareaExpectedResults.SetItem(self.index, 3, i["email"] if i["email"] else '')            
            self.textareaExpectedResults.SetItem(self.index, 4, i["requestTime"])
            self.myRowDict[self.index] = [i["patientName"], i["gender"], i["age"], i["email"], i["requestTime"]]
            self.myRequestIdDict[self.index] = i["requestId"]
            self.details[i["requestId"]] = {"Email":i["email"] if i["email"] else ''}
            self.details[i["requestId"]]["Name"] = i["patientName"]
            self.details[i["requestId"]]["Gender"] = i["gender"]
            self.details[i["requestId"]]["Age"] = i["age"]
            self.index+=1
        print(self.myRowDict)
        self.myRequestIdDict1 = self.myRequestIdDict.copy()
        count = self.textareaExpectedResults.GetItemCount()
        for row in range(count):
            item = self.textareaExpectedResults.GetItem(row, col=0)
            self.searchNameDict[item.GetText()] = row 
        if self.textareaExpectedResults.IsEmpty():
            self.generateBtn.Disable()
        else:
            self.generateBtn.Enable()

    def onItemSelected(self, event):
        self.selectedIndex = event.GetIndex()

    def OnScreen(self, event):
        if self.selectedIndex != None:
            print(self.selectedIndex)
            rqstId = self.myRequestIdDict[self.selectedIndex]
            print(rqstId)
            ResultDetails(self, -1, 'Result Details', rqstId)
        else:
            wx.MessageBox('None of them Choosen, Try Choosing Patient that you want to generate Report for', 'Selection Error', wx.OK| wx.ICON_WARNING)
        #pass

    def onClose(self, event):
        """"""
        self.Close()


    def OnFromDateChanged(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None
        selected_date = evt.GetDate()
        self.dpc1.SetRange(dt1= wx.DefaultDateTime, dt2= wx.DateTime.Now())
        self.dpc2.SetRange(dt1= selected_date, dt2= wx.DateTime.Now())
        print (selected_date.Format("%d-%m-%Y"))

    def OnToDateChanged(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None
        selected_date = evt.GetDate()
        #self.dpc1.SetRange(dt1= wx.DefaultDateTime, dt2= selected_date)
        self.dpc2.SetRange(dt1= self.dpc1.GetValue(), dt2= wx.DateTime.Now())
        print (selected_date.Format("%d-%m-%Y"))

    def onMatches(self):
        print(self.searchNameDict)
        self.searchNameDictSorted = OrderedDict(sorted(self.searchNameDict.items(), key=lambda t: t[0]))
        print(self.searchNameDictSorted)
        nameSearch = self.searchExpectedResults.GetValue() # get the entered string in TextCtrl with GetValue method
        print (nameSearch)
        self.textareaExpectedResults.DeleteAllItems()
        row1 = 0
        self.myRequestIdDict = {}
        for Name in self.searchNameDictSorted:
            print(Name)
            if nameSearch in Name:
                print(self.searchNameDictSorted[Name])
                index = self.searchNameDictSorted[Name]
                print(self.myRowDict[index])
                #self.textareaExpectedResults.InsertItem(self.textareaExpectedResults.GetItemCount(), "The END")
                self.textareaExpectedResults.Append(self.myRowDict[index])
                self.myRequestIdDict[row1] = self.myRequestIdDict1[index]
                row1+=1
        if self.textareaExpectedResults.IsEmpty():
            self.generateBtn.Disable()
        else:
            self.generateBtn.Enable()

    def on_char(self, event):
        event.Skip()
        wx.CallAfter(self.onMatches)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class ResultDetails(wx.Frame):
    def __init__(self, parent, id, title, RqstId):
        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (650, 450))
        super(ResultDetails, self).__init__(parent, id, title, wx.DefaultPosition, (1100, 900))
        #self.parent = parent
        self.RqstId = RqstId
        self.email = parent.details[RqstId]["Email"]
        self.name = parent.details[RqstId]["Name"]
        self.gender = parent.details[RqstId]['Gender']
        self.age = parent.details[RqstId]['Age']

        if parent.selectedIndex != None:
            parent.textareaExpectedResults.Select(parent.selectedIndex, on=0)
            parent.selectedIndex = None
        self.pendingRequest = db.getPendingRequest(self.RqstId)
        self.pendingTestAssays = []
        print(self.pendingRequest)
        TestPanel(self)
        self.Show()

class TestPanel(scrolled.ScrolledPanel):

    def __init__(self, parent):

        scrolled.ScrolledPanel.__init__(self, parent=parent, id= -1)
        self.parent = parent
        self.index = None
        if self.parent.pendingRequest != None:
            for i in self.parent.pendingRequest:
                self.parent.pendingTestAssays.append(i['assayName'])
        else:
            self.parent.pendingTestAssays = []

        self.tests = wx.ListBox(self, -1, size=(370, 130), choices=self.parent.pendingTestAssays, style=wx.LB_MULTIPLE)
        self.Bind(wx.EVT_LISTBOX, self.Onlistbox, self.tests)
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font1 = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font1.SetPointSize(12)

        name = wx.StaticText(self, label= self.parent.name)
        name.SetFont(font)
        age = wx.StaticText(self, label= "Age     : {0}".format(self.parent.age))
        age.SetFont(font1)
        gender = wx.StaticText(self, label= "Gender: {0}".format(self.parent.gender))
        gender.SetFont(font1)        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.controlSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer1 = wx.GridBagSizer()
        self.sizer1.Add(self.tests, pos = (2, 13), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 50)
        self.sizer.Add(name, 0, flag = wx.RIGHT|wx.TOP, border = 50)
        self.sizer.Add(age, 0, flag = wx.RIGHT, border = 50)
        self.sizer.Add(gender, 0, flag = wx.RIGHT, border = 50)
        updateBtn = wx.Button(self, label = "Update", size=(90, 28))
        self.sizer1.Add(updateBtn, pos = (6, 12), flag = wx.LEFT|wx.BOTTOM, border = 50)
        updateBtn.Bind(wx.EVT_BUTTON, self.onUpdate)
        

        self.sizer1.AddGrowableCol(9)
        #self.sizer1.AddGrowableCol(11)
        self.sizer1.AddGrowableCol(12)
        self.sizer1.AddGrowableCol(13)

        #self.SetupScrolling()
        self.hbox.Add(self.sizer, 0, wx.LEFT)
        self.hbox.Add(self.sizer1, 0, wx.RIGHT)
        self.mainSizer.Add(self.hbox, 0, wx.CENTER)
        self.mainSizer.Add(self.controlSizer, 0, wx.CENTER)

        self.SetSizerAndFit(self.mainSizer)
        
        

    def Onlistbox(self, evt):
        self.index = evt.GetSelection()
        self.selectedString = str(self.tests.GetString(self.index))

    def onUpdate(self, evt):
        if self.index != None:
            self.controlSizer.Clear(True)
            k = 7
            flag = 1
            self.antibdyIdDict = {}
            self.optionIdDict = {}
            self.antiBodyDict = {}
            self.commentDict = {}
            # self.boldFlag = False
            # self.italicFlag = False
            self.caps = False
            font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            for i in self.parent.pendingRequest:
                if i['assayName'] == self.selectedString:
                    self.assayId = i['assayId']
                    antibodiesOptions = i['antiBodies']
                    print(antibodiesOptions)
            self.sizer2 = wx.GridBagSizer()
            ids = 0
            for dic in antibodiesOptions:
                if flag:
                    antibodyText = wx.StaticText(self, -1, 'Antibodies')
                    optionsText = wx.StaticText(self, -1, 'Options')
                    commentText = wx.StaticText(self, -1, 'Comments')
                    antibodyText.SetFont(font)
                    optionsText.SetFont(font)
                    commentText.SetFont(font)
                    self.sizer2.Add(antibodyText, pos = (k,9), flag = wx.RIGHT|wx.BOTTOM, border = 100)
                    self.sizer2.Add(optionsText, pos = (k,12), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 100)
                    self.sizer2.Add(commentText, pos = (k,13), flag = wx.LEFT|wx.BOTTOM, border = 100)
                    flag = 0
                    k+=1

                choices=[i for i in dic['options'].values() if i != None]
                if not choices:
                    continue

                antibody = wx.StaticText(self, ids, dic['antiBody'])
                self.antibdyIdDict[dic['antiBody']] = dic['antiBodyId']
                self.optionIdDict[dic['antiBodyId']] = {option: Id for Id, option in dic['options'].items()}
                choices.insert(0, '-- Select --')
                print(choices)            
                self.inputTwo = wx.Choice(self,id =ids, choices = choices)
                self.inputTwo.SetSelection(0)
                self.sizer2.Add(antibody, pos = (k,9), flag = wx.RIGHT|wx.BOTTOM, border = 100)
                self.sizer2.Add(self.inputTwo, pos = (k,12), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 100)


                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer1 = wx.BoxSizer(wx.HORIZONTAL)
                #save_button = wx.Button(self, label="Save")
                self.Bold = wx.Button(self, id =ids, label="B", size=(25, 18))
                self.Bold.myname = "Bold"
                Italic = wx.Button(self, id =ids, label="I", size=(25, 18))
                Italic.myname = "Italic"

                self.Bold.Bind(wx.EVT_BUTTON, self.on_Bold, id = self.Bold.GetId())
                Italic.Bind(wx.EVT_BUTTON, self.on_italic, id = Italic.GetId())

                try:
                    _stringIO = StringIO(open('output.xml').read())
                    _handler = wx.richtext.RichTextXMLHandler()
                    _handler.LoadFile(self.rt.GetBuffer(), 'output.xml')
                    self.rt.Refresh()
                except Exception as ex:
                    print(ex)

                if dic['comment']:
                    self.rt = rt.RichTextCtrl(self, ids, value= dic['comment'], size=(250, 100))
                    # comment = wx.TextCtrl(self, ids, dic['comment'], size=(300, -1))
                else:
                    self.rt = rt.RichTextCtrl(self, ids, value="", size=(250, 100))
                    # comment = wx.TextCtrl(self, ids, '', size=(300, -1))

                sizer.Add(self.rt, 1, wx.EXPAND|wx.ALL, 6)
                sizer1.Add(self.Bold, 0, wx.EXPAND|wx.ALL, 6)
                sizer1.Add(Italic, 0, wx.EXPAND|wx.ALL, 6)
                sizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 6)

                self.sizer2.Add(sizer, pos = (k,13), flag = wx.LEFT|wx.BOTTOM, border = 100)
                self.inputTwo.Bind(wx.EVT_CHOICE, self.OnChoiceSelect)

                self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
                # then bind the events in the constructor or somewhere
                self.rt.Bind(wx.EVT_CHAR, self.onKeyDownHandler, id = self.rt.GetId())
                self.rt.Bind(wx.EVT_LEFT_DOWN, self.onKeyDownHandler, id = self.rt.GetId())
                self.rt.Bind(wx.EVT_RIGHT_UP, self.onKeyDownHandler, id = self.rt.GetId())
                # bind also new event handler but 
                self.rt.Bind(self.EVT_SOME_NEW_EVENT , self.onKeyDownAction, id = self.rt.GetId())

                out = BytesIO()
                handler = wx.richtext.RichTextXMLHandler()
                rt_buffer = self.rt.GetBuffer()
                handler.SaveFile(rt_buffer, out)
                xml_content = out.getvalue()

                self.commentDict[dic['antiBodyId']] = xml_content.decode('utf-8') #self.rt.GetValue()
                self.rt.Bind(wx.EVT_TEXT, self.onCommentModified, id = self.rt.GetId())
                k+=1
                ids+=1

                # id2 = comment.GetEventObject().GetId()
                # antibdyId = self.antibdyIdDict[wx.FindWindowById(id2).GetValue()]
                # self.antiBodyDict[antibdyId] = optId
            self.saveBtn = wx.Button(self, label = "Save", size=(90, 28))
            self.sizer2.Add(self.saveBtn, pos = (k+1, 13), flag = wx.LEFT|wx.BOTTOM, border = 250)
            self.saveBtn.Bind(wx.EVT_BUTTON, self.onUpdateReport)
            self.controlSizer.Add(self.sizer2, 0, wx.ALL, 5)
            #self.SetSizer(self.controlSizer)
            self.SetSizer(self.mainSizer)
            self.SetupScrolling()
            #self.Centre()
            self.Layout()
        else:
            wx.MessageBox('None of them Choosen, Try Choosing Test that you want to generate Report for', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def OnChoiceSelect(self, event):
        if event.GetSelection():
            id1 = event.GetEventObject().GetId()
            antibdyId = self.antibdyIdDict[wx.FindWindowById(id1).GetLabel()]
            optId = self.optionIdDict[antibdyId][event.GetString()]
            self.antiBodyDict[antibdyId] = optId
    def onCommentModified(self, event):
        rtc = event.GetEventObject()
        if len(rtc.GetValue()) > 0:
            id1 = rtc.GetId()
            antibdyId = self.antibdyIdDict[wx.FindWindowById(id1).GetLabel()]

            out = BytesIO()
            handler = wx.richtext.RichTextXMLHandler()
            rt_buffer = rtc.GetBuffer()
            handler.SaveFile(rt_buffer, out)
            xml_content = out.getvalue()

            self.commentDict[antibdyId] = xml_content.decode('utf-8') #rtc.GetValue()
            event.Skip()

    def on_Bold(self, event):
        boldBtnWidget = event.GetEventObject()
        id1 = boldBtnWidget.GetId()
        widgetCtrl = [rtcCtrl for rtcCtrl in [widgetCtrl for widgetCtrl in self.GetChildren() if isinstance(widgetCtrl, wx.richtext.RichTextCtrl)] if rtcCtrl.GetId() == id1][0]
        # print(widgetCtrl)
        # _selection = widgetCtrl.GetStringSelection()
        # if _selection:
        #     if widgetCtrl.IsSelectionBold():
        #         self.boldFlag = False
        #         boldBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
        #     elif not widgetCtrl.IsSelectionBold():
        #         self.boldFlag = True
        #         boldBtnWidget.SetBackgroundColour((255, 230, 200, 255))
        #     widgetCtrl.ApplyBoldToSelection()
        #     widgetCtrl.SetFocus()
        #     pos = widgetCtrl.GetSelectionRange()[1]
        #     print(pos)
        #     widgetCtrl.SetInsertionPoint(pos)
        #     return
        # if not self.boldFlag:
        #     # self.Bold.SetFocus()
        #     boldBtnWidget.SetBackgroundColour((255, 230, 200, 255))
        #     widgetCtrl.SetFocus()
        #     pos1 = widgetCtrl.GetCaretPosition()
        #     widgetCtrl.SetInsertionPoint(pos1+1)
        #     widgetCtrl.BeginBold()
        #     self.boldFlag = True
        #     self.caps = True
        # elif self.boldFlag:
        #     boldBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
        #     widgetCtrl.SetFocus()
        #     pos1 = widgetCtrl.GetCaretPosition()
        #     widgetCtrl.SetInsertionPoint(pos1+1)
        #     if self.caps:
        #         widgetCtrl.EndBold()
        #     else:
        #         widgetCtrl.SetFont(wx.Font(10, family = wx.DEFAULT, style = wx.NORMAL, weight = wx.NORMAL))
        #     self.boldFlag = False
        #     self.caps = False
        _selection = widgetCtrl.GetStringSelection()
        if _selection:
            # print(_selection)
            if widgetCtrl.IsSelectionBold():
                boldBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
            elif not widgetCtrl.IsSelectionBold():
                boldBtnWidget.SetBackgroundColour(wx.LIGHT_GREY)
            widgetCtrl.ApplyBoldToSelection()
            widgetCtrl.SetFocus()
            return
        self.color_Match = boldBtnWidget.GetBackgroundColour() == wx.LIGHT_GREY
        if not self.color_Match:
            print('Bold',True)
            # boldBtnWidget.SetFocus()
            boldBtnWidget.SetBackgroundColour(wx.LIGHT_GREY)
            widgetCtrl.SetFocus()
            pos1 = widgetCtrl.GetCaretPosition()
            widgetCtrl.SetInsertionPoint(pos1+1)
            widgetCtrl.BeginBold()
            # f = widgetCtrl.GetFont()
            # f.SetWeight(wx.FONTWEIGHT_BOLD)
            # widgetCtrl.BeginFont(f)
            
        elif self.color_Match:
            widgetCtrl.SetFocus()
            pos1 = widgetCtrl.GetCaretPosition()
            widgetCtrl.SetInsertionPoint(pos1+1)
            widgetCtrl.EndBold()
            boldBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
            print('Bold',False)
            # f = widgetCtrl.GetFont()
            # f.SetWeight(wx.FONTWEIGHT_NORMAL)
            # widgetCtrl.BeginFont(f)

    def on_italic(self, event):
        italicBtnWidget = event.GetEventObject()
        id1 = italicBtnWidget.GetId()
        widgetCtrl = [rtcCtrl for rtcCtrl in [widgetCtrl for widgetCtrl in self.GetChildren() if isinstance(widgetCtrl, wx.richtext.RichTextCtrl)] if rtcCtrl.GetId() == id1][0]
        # widgetCtrl.ApplyItalicToSelection()
        # # if not self.italicFlag:
        # #     widgetCtrl.SetFocus()
        # #     widgetCtrl.SetInsertionPointEnd()
        # #     widgetCtrl.BeginItalic()
        # #     self.italicFlag = True
        # # elif self.italicFlag:
        # #     widgetCtrl.SetFocus()
        # #     widgetCtrl.SetInsertionPointEnd()
        # #     widgetCtrl.EndItalic()
        # #     self.italicFlag = False
        # if not self.italicFlag:
        #     italicBtnWidget.SetBackgroundColour((255, 230, 200, 255))
        #     widgetCtrl.SetFocus()
        #     pos1 = widgetCtrl.GetCaretPosition()
        #     widgetCtrl.SetInsertionPointEnd(pos1+1)
        #     widgetCtrl.BeginItalic()
        #     self.italicFlag = True
        # elif self.italicFlag:
        #     italicBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
        #     widgetCtrl.SetFocus()
        #     pos1 = widgetCtrl.GetCaretPosition()
        #     widgetCtrl.SetInsertionPointEnd(pos1+1)
        #     widgetCtrl.EndItalic()
        #     self.italicFlag = False

        _selection = widgetCtrl.GetStringSelection()
        if _selection:
            # print(_selection)
            if widgetCtrl.IsSelectionItalics():
                italicBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
            elif not widgetCtrl.IsSelectionItalics():
                italicBtnWidget.SetBackgroundColour(wx.LIGHT_GREY)
            widgetCtrl.ApplyItalicToSelection()
            widgetCtrl.SetFocus()
            return
        self.color_Match1 = italicBtnWidget.GetBackgroundColour() == wx.LIGHT_GREY
        if not self.color_Match1:
            print('Italic',True)
            italicBtnWidget.SetBackgroundColour(wx.LIGHT_GREY)
            widgetCtrl.SetFocus()
            pos1 = widgetCtrl.GetCaretPosition()
            widgetCtrl.SetInsertionPoint(pos1+1)
            widgetCtrl.BeginItalic()
            # f = widgetCtrl.GetFont()
            # f.SetStyle(wx.ITALIC)
            # widgetCtrl.BeginFont(f)
        elif self.color_Match1:
            widgetCtrl.SetFocus()
            pos1 = widgetCtrl.GetCaretPosition()
            widgetCtrl.SetInsertionPoint(pos1+1)
            italicBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
            widgetCtrl.EndItalic()
            print('Italic', False)
            # f = widgetCtrl.GetFont()
            # f.SetStyle(wx.NORMAL)
            # widgetCtrl.BeginFont(f)

    # then define the handlers
    def onKeyDownAction(self, event):
        rtc = event.GetEventObject()
        id1 = rtc.GetId()
        print("Insertion point {}".format(rtc.GetInsertionPoint()))
        btnWidget = [Btn for Btn in [widgetCtrl for widgetCtrl in self.GetChildren() if isinstance(widgetCtrl, wx.Button)] if Btn.GetId() == id1]
        print(btnWidget)
        for i in btnWidget:
            if i.myname == "Bold":
                boldBtnWidget = i
            elif i.myname == "Italic":
                italicBtnWidget = i
        if rtc.IsSelectionBold():
            boldBtnWidget.SetBackgroundColour(wx.LIGHT_GREY)
        elif not rtc.IsSelectionBold():
            boldBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
        if rtc.IsSelectionItalics():
            italicBtnWidget.SetBackgroundColour(wx.LIGHT_GREY)
        elif not rtc.IsSelectionItalics():
            italicBtnWidget.SetBackgroundColour(wx.Colour(240, 240, 240))
        event.Skip()
    def onKeyDownHandler(self, event):
        rtc = event.GetEventObject()
        event.Skip()
        # post the new event so it will be handled later
        wx.PostEvent(rtc, self.SomeNewEvent())

    def onUpdateReport(self, event):
        print(self.antiBodyDict)
        print(self.commentDict)
        if db.updatePendingReport(self.parent.RqstId, self.assayId, self.antiBodyDict, self.commentDict):
            self.selectedString = str(self.tests.GetString(self.index))
            self.parent.pendingTestAssays.remove(self.selectedString)
            if not self.parent.pendingTestAssays:
                jsonHead = {}
                self.saveBtn.Disable()
                self.controlSizer.Clear(True)
                jsonHeader = db.getRequestHeader(self.parent.RqstId)
                print(jsonHeader)
                jsonHead['UHID'] = jsonHeader['uhid'] if 'uhid' in jsonHeader else ''
                jsonHead['Referring Hospital'] = jsonHeader['hospitalName'] if 'hospitalName' in jsonHeader else ''
                jsonHead['MRD No'] = jsonHeader['mrd'] if 'mrd' in jsonHeader else ''
                jsonHead['Referring Dept'] = jsonHeader['departmentName'] if 'departmentName' in jsonHeader else ''
                jsonHead['Patient Name'] = jsonHeader['patientName'] if 'patientName' in jsonHeader else ''
                jsonHead['Sample Collection Date'] = jsonHeader['collectionDate'] if 'collectionDate' in jsonHeader else ''
                jsonHead['Age'] = utilsDb.getAge(jsonHeader['patientDob']) if 'patientDob' in jsonHeader else ''
                jsonHead['Lab Reference No'] = jsonHeader['labReferenceNumber'] if 'labReferenceNumber' in jsonHeader else ''
                jsonHead['Gender'] = jsonHeader['patientGender'] if 'patientGender' in jsonHeader else ''
                jsonHead['Report Generated Date'] = jsonHeader['reportDate'] if 'reportDate' in jsonHeader else ''
                jsonHead['Ward Name/Collection Centre'] = jsonHeader['collectionPoint'] if 'collectionPoint' in jsonHeader else ''
                jsonHead['Lab Name'] = jsonHeader['labName'] if 'labName' in jsonHeader else ''  
                jsonHead['Email'] = jsonHeader['patientEmail'] if 'patientEmail' in jsonHeader else ''
                jsonHead['Ph No'] = jsonHeader['mobile'] if 'mobile' in jsonHeader else ''
                jsonHead['reportFile'] = jsonHeader['reportFile'] if 'reportFile' in jsonHeader else utilsDb.getFileName(jsonHead['Patient Name'], jsonHead['UHID'])
                jsonResults = db.getPatientReport(self.parent.RqstId)
                pdfReportFileName =pdf.Header(jsonHead, jsonResults)
                db.updateFileName(jsonHeader['requestId'], jsonHead['reportFile'])
                OpenReport(self, "Open Report", self.parent.email, self.parent.name, jsonHead['reportFile'])
            else:
                self.controlSizer.Clear(True)
                dialog = wx.MessageBox('Results is Updated for {0} test'.format(self.selectedString), 'Successfully Updated', wx.OK)
            self.tests.Deselect(self.index)
            self.index = None
            self.tests.Clear()
            self.tests.Set(self.parent.pendingTestAssays)
            self.tests.Update()
            # for i in db.getPendingRequest(self.parent.RqstId):
            #     print(i['assayName'])
        else:
            wx.MessageBox('Test Report not updated', 'Error', wx.OK | wx.ICON_WARNING)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ViewPanel(wx.Frame):
    def __init__(self, parent, title):
        super(ViewPanel, self).__init__(parent, title = title, size = (700, 500)) 
        self.index = 0
        self.selectedIndex = None
        self.myRowDict = {}
        self.searchNameDict = {}
        self.myRequestIdDict = {}
        self.details = {}

        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer()

        self.dpc1 = wx.adv.DatePickerCtrl( panel, wx.ID_ANY, size=(120,-1))
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateChanged, self.dpc1)
        self.dpc1.Bind(wx.EVT_SET_FOCUS, self.Onfocus)
        sizer.Add(self.dpc1, (3,9), (2, 4), wx.RIGHT|wx.BOTTOM, 40)

        self.dpc2 = wx.adv.GenericDatePickerCtrl(panel, wx.ID_ANY, wx.DefaultDateTime, size=(120,-1), style = wx.TAB_TRAVERSAL| wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnToDateChanged, self.dpc2)
        self.dpc2.Bind(wx.EVT_SET_FOCUS, self.Onfocus)
        sizer.Add(self.dpc2, (3,16), (2, 4), wx.LEFT|wx.BOTTOM, 40)

        self.dpc1.SetValue(wx.DateTime.Now().SetDay(1))

        self.searchExpectedResults = wx.SearchCtrl(panel,
                                    size=(250, -1),
                                    style=wx.TE_PROCESS_ENTER)
        sizer.Add(self.searchExpectedResults, (1, 8), (1, 14), wx.EXPAND|wx.RIGHT, 40)
        self.searchExpectedResults.Bind(wx.EVT_CHAR, self.on_char) # Bind an EVT_CHAR event to your SearchCtrl
        self.searchExpectedResults.Bind(wx.EVT_SET_FOCUS, self.Onfocus)

        filterBtn = wx.Button(panel, label = "Filter", size=(90, 28))
        sizer.Add(filterBtn, pos = (5, 11), flag = wx.LEFT|wx.BOTTOM, border = 50)
        filterBtn.Bind(wx.EVT_BUTTON, self.onfilter)

        self.textareaExpectedResults = wx.ListCtrl(panel, -1, style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES) 
        self.textareaExpectedResults.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.textareaExpectedResults.InsertColumn(0, 'Patient Name', width = 300) 
        self.textareaExpectedResults.InsertColumn(1, 'Gender', wx.LIST_FORMAT_RIGHT, 70) 
        self.textareaExpectedResults.InsertColumn(2, 'Age', wx.LIST_FORMAT_RIGHT, 100) 
        self.textareaExpectedResults.InsertColumn(3, 'Email', wx.LIST_FORMAT_RIGHT, 100)
        self.textareaExpectedResults.InsertColumn(4, 'Date', wx.LIST_FORMAT_RIGHT, 200)

        frmDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc1.GetValue()).split('-')))) if self.dpc1.GetValue().IsValid() else None
        toDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc2.GetValue()).split('-')))) if self.dpc2.GetValue().IsValid() else None
        Reports = db.getReports(_fromDate=frmDate, _toDate=toDate, _pending=False)
        self.textareaExpectedResults.DeleteAllItems()
        for i in Reports:
            self.index = self.textareaExpectedResults.InsertItem(self.index, i["patientName"]) 
            self.textareaExpectedResults.SetItem(self.index, 1, i["gender"]) 
            self.textareaExpectedResults.SetItem(self.index, 2, i["age"])
            self.textareaExpectedResults.SetItem(self.index, 3, i["email"] if i["email"] else '')            
            self.textareaExpectedResults.SetItem(self.index, 4, i["requestTime"])
            self.myRowDict[self.index] = [i["patientName"], i["gender"], i["age"], i["email"], i["requestTime"]]
            self.myRequestIdDict[self.index] = i["requestId"]
            self.details[i["requestId"]] = {"Email":i["email"] if i["email"] else ''}
            self.details[i["requestId"]]["Name"] = i["patientName"]            
            self.index+=1
        print(self.myRowDict)
        self.myRequestIdDict1 = self.myRequestIdDict.copy()
        count = self.textareaExpectedResults.GetItemCount()
        for row in range(count):
            item = self.textareaExpectedResults.GetItem(row, col=0)
            self.searchNameDict[item.GetText()] = row 
        
        sizer.Add(self.textareaExpectedResults, (6, 8), (2, 14), wx.EXPAND|wx.RIGHT, 40)

        sizer.AddGrowableCol(9)
        sizer.AddGrowableCol(16)
        sizer.AddGrowableCol(8)
         
        self.openBtn = wx.Button(panel, label = "Open", size=(90, 28)) 
        cancelBtn = wx.Button(panel, wx.ID_CLOSE, label = "Cancel", size=(90, 28)) 

        sizer.Add(cancelBtn, pos = (10, 11), flag = wx.RIGHT|wx.BOTTOM, border = 50) 
        sizer.Add(self.openBtn, pos = (10, 17), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        self.openBtn.Bind(wx.EVT_BUTTON, self.onOpen)

        if self.textareaExpectedResults.IsEmpty():
            self.openBtn.Disable()
        else:
            self.openBtn.Enable()

        sizer.AddGrowableRow(6)
        panel.SetSizerAndFit(sizer)

    def Onfocus(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None

    def onfilter(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None
        self.myRowDict = {}
        self.searchNameDict = {}
        self.myRequestIdDict = {}
        self.details = {}
        frmDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc1.GetValue()).split('-')))) if self.dpc1.GetValue().IsValid() else None
        toDate = dt.date(*(map(int, wx.DateTime.FormatISODate(self.dpc2.GetValue()).split('-')))) if self.dpc2.GetValue().IsValid() else None
        dateFilteredReports = db.getReports(_fromDate=frmDate, _toDate=toDate, _pending=False)
        self.textareaExpectedResults.DeleteAllItems()
        for i in dateFilteredReports:
            self.index = self.textareaExpectedResults.InsertItem(self.index, i["patientName"]) 
            self.textareaExpectedResults.SetItem(self.index, 1, i["gender"])
            self.textareaExpectedResults.SetItem(self.index, 2, i["age"])
            self.textareaExpectedResults.SetItem(self.index, 3, i["email"] if i["email"] else '')            
            self.textareaExpectedResults.SetItem(self.index, 4, i["requestTime"])
            self.myRowDict[self.index] = [i["patientName"], i["gender"], i["age"], i["email"], i["requestTime"]]
            self.myRequestIdDict[self.index] = i["requestId"]
            self.details[i["requestId"]] = {"Email":i["email"] if i["email"] else ''}
            self.details[i["requestId"]]["Name"] = i["patientName"]
            self.index+=1
        print(self.myRowDict)
        self.myRequestIdDict1 = self.myRequestIdDict.copy()
        count = self.textareaExpectedResults.GetItemCount()
        for row in range(count):
            item = self.textareaExpectedResults.GetItem(row, col=0)
            self.searchNameDict[item.GetText()] = row 
        if self.textareaExpectedResults.IsEmpty():
            self.openBtn.Disable()
        else:
            self.openBtn.Enable()

    def onItemSelected(self, event):
        self.selectedIndex = event.GetIndex()

    def onOpen(self, event):
        if self.selectedIndex != None:
            print(self.selectedIndex)
            rqstId = self.myRequestIdDict[self.selectedIndex]
            print(rqstId)
            jsonHeader = db.getRequestHeader(rqstId)
            print(jsonHeader)
            jsonHead = {}
            jsonResults = db.getPatientReport(rqstId)
            jsonHead['UHID'] = jsonHeader['uhid'] if 'uhid' in jsonHeader else ''
            jsonHead['Referring Hospital'] = jsonHeader['hospitalName'] if 'hospitalName' in jsonHeader else ''
            jsonHead['MRD No'] = jsonHeader['mrd'] if 'mrd' in jsonHeader else ''
            jsonHead['Referring Dept'] = jsonHeader['departmentName'] if 'departmentName' in jsonHeader else ''
            jsonHead['Patient Name'] = jsonHeader['patientName'] if 'patientName' in jsonHeader else ''
            jsonHead['Sample Collection Date'] = jsonHeader['collectionDate'] if 'collectionDate' in jsonHeader else ''
            jsonHead['Age'] = utilsDb.getAge(jsonHeader['patientDob']) if 'patientDob' in jsonHeader else ''
            jsonHead['Lab Reference No'] = jsonHeader['labReferenceNumber'] if 'labReferenceNumber' in jsonHeader else ''
            jsonHead['Gender'] = jsonHeader['patientGender'] if 'patientGender' in jsonHeader else ''
            jsonHead['Report Generated Date'] = jsonHeader['reportDate'] if 'reportDate' in jsonHeader else ''
            jsonHead['Ward Name/Collection Centre'] = jsonHeader['collectionPoint'] if 'collectionPoint' in jsonHeader else ''
            jsonHead['Lab Name'] = jsonHeader['labName'] if 'labName' in jsonHeader else ''  
            jsonHead['Email'] = jsonHeader['patientEmail'] if 'patientEmail' in jsonHeader else ''
            jsonHead['Ph No'] = jsonHeader['mobile'] if 'mobile' in jsonHeader else ''
            jsonHead['reportFile'] = jsonHeader['reportFile'] if 'reportFile' in jsonHeader else utilsDb.getFileName(jsonHead['Patient Name'], jsonHead['UHID'])
            pdfReportFileName =pdf.Header(jsonHead, jsonResults)
            db.updateFileName(jsonHeader['requestId'], jsonHead['reportFile'])
            OpenReport(self, "Open Report", self.details[rqstId]["Email"], self.details[rqstId]["Name"], jsonHead['reportFile'])
        else:
            wx.MessageBox('None of them Choosen, Try Choosing Patient that you want to generate Report for', 'Selection Error', wx.OK| wx.ICON_WARNING)
        #pass

    def onClose(self, event):
        """"""
        self.Close()


    def OnFromDateChanged(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None
        selected_date = evt.GetDate()
        self.dpc1.SetRange(dt1= wx.DefaultDateTime, dt2= wx.DateTime.Now())
        self.dpc2.SetRange(dt1= selected_date, dt2= wx.DateTime.Now())
        print (selected_date.Format("%d-%m-%Y"))

    def OnToDateChanged(self, evt):
        if self.selectedIndex != None:
            self.textareaExpectedResults.Select(self.selectedIndex, on=0)
            self.selectedIndex = None
        selected_date = evt.GetDate()
        #self.dpc1.SetRange(dt1= wx.DefaultDateTime, dt2= selected_date)
        self.dpc2.SetRange(dt1= self.dpc1.GetValue(), dt2= wx.DateTime.Now())
        print (selected_date.Format("%d-%m-%Y"))

    def onMatches(self):
        print(self.searchNameDict)
        self.searchNameDictSorted = OrderedDict(sorted(self.searchNameDict.items(), key=lambda t: t[0]))
        print(self.searchNameDictSorted)
        nameSearch = self.searchExpectedResults.GetValue() # get the entered string in TextCtrl with GetValue method
        print (nameSearch)
        self.textareaExpectedResults.DeleteAllItems()
        row1 = 0
        self.myRequestIdDict = {}
        for Name in self.searchNameDictSorted:
            print(Name)
            if nameSearch in Name:
                print(self.searchNameDictSorted[Name])
                index = self.searchNameDictSorted[Name]
                print(self.myRowDict[index])
                #self.textareaExpectedResults.InsertItem(self.textareaExpectedResults.GetItemCount(), "The END")
                self.textareaExpectedResults.Append(self.myRowDict[index])
                self.myRequestIdDict[row1] = self.myRequestIdDict1[index]
                row1+=1
        if self.textareaExpectedResults.IsEmpty():
            self.openBtn.Disable()
        else:
            self.openBtn.Enable()

    def on_char(self, event):
        event.Skip()
        wx.CallAfter(self.onMatches)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class OpenReport(wx.Frame):
    def __init__(self, parent, title, email, name, reportname):
        super(OpenReport, self).__init__(parent, title = title, size = (1000, 500))
        self.parentFrame = parent
        self.email = email
        self.name = name
        self.reportPath = reportname
        self.InitUI()
        self.Centre() 
        self.Show()     
    def InitUI(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        if self.email:
            text = wx.TextCtrl(self.panel,-1, self.email, size=(300, -1))

        else:
            text = wx.TextCtrl(self.panel,-1, size=(300, -1))

        st1 = wx.StaticText(self.panel, label='Name:')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        name = wx.StaticText(self.panel, label= self.name)
        name.SetFont(font)
        hbox1.Add(name, proportion=0)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        vbox.Add((-1, 50))

        st2 = wx.StaticText(self.panel, label='Email:')
        st2.SetFont(font)
        vbox.Add(st2, flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add((-1, 10))

        vbox.Add(text, flag=wx.LEFT|wx.RIGHT,border=10)
        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.openBtn = wx.Button(self.panel, label='Open', size=(90, 30))
        hbox5.Add(self.openBtn)
        sendBtn = wx.Button(self.panel, label='Send', size=(90, 30))
        hbox5.Add(sendBtn, flag=wx.LEFT, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM, border=10)

        self.openBtn.Bind(wx.EVT_BUTTON, self.onView)
        sendBtn.Bind(wx.EVT_BUTTON, self.onSend)
        # text.Bind(wx.EVT_KEY_UP, self.ontext)

        self.panel.SetSizer(vbox)
        self.Layout()


    def onView(self, evt):
        filepath = self.reportPath
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
        


    def onSend(self, evt):
        pass

#---------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()