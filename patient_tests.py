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
from wx.lib.wordwrap import wordwrap


filename="regis1.jpeg"
class MyApp(wx.App):
    def __init__(self):
        super().__init__()

        frame = MyFrame(parent=None, title="Register")
        frame.SetIcon(wx.Icon("./SoftLogo2.ico"))
        frame.Show()


class MyFrame(wx.Frame):         
    def __init__(self, parent, title, style= wx.DEFAULT_FRAME_STYLE): 
        super(MyFrame, self).__init__(parent, title = title, size = (1300, 800)) 
        path = os.path.abspath("./SoftLogo2.png")
        self.icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)
        self.InitUI()
        # wx.Frame.__init__(self, None, wx.ID_ANY, "Choose Dot in Picture", size=(700,500))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.img = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        jpeg = self.img.ConvertToBitmap()
        self.image=wx.StaticBitmap(self.panel, wx.ID_ANY, jpeg, wx.DefaultPosition, wx.DefaultSize, 0)
        #print(image.GetScaleMode())
        hbox.Add(self.image, 0, wx.CENTER)
        vbox.Add((0,0), 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.CENTER)
        vbox.Add((0,0), 1, wx.EXPAND)
        
        self.image.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
        self.Bind(wx.EVT_SIZE, self.onResize)
        self.panel.SetSizer(vbox)
        self.SetBackgroundColour(wx.LIGHT_GREY)
        
        self.Layout()
        # self.Centre()
        self.Show(True)
        
    # def MakeModal(self, modal=True):
    #     if modal and not hasattr(self, '_disabler'):
    #         self._disabler = wx.WindowDisabler(self)
    #     if not modal and hasattr(self, '_disabler'):
    #         del self._disabler

    def onResize(self, event):
        # self.Layout()
        frame_size = self.GetSize()
        frame_h = (frame_size[0]-10) / 2
        frame_w = (frame_size[1]-10) / 2
        img1 = self.img.Scale(frame_h,frame_w)
        self.image.SetBitmap(img1.ConvertToBitmap())
        self.Refresh()
        self.Layout()

    def on_clic(self, evt):
        PatientDetails(self, title = 'ENTER PATIENT DETAILS').ShowModal() 
        x, y=evt.GetPosition()
        #print("clicked at", x, y)


    def InitUI(self):   
        #self.text = wx.TextCtrl(parent=self, id=wx.ID_ANY, style = wx.EXPAND|wx.TE_MULTILINE) 
        menuBar = wx.MenuBar() 

        reportsMenu = ReportsMenu(parentFrame=self)
        menuBar.Append(reportsMenu, '&Reports') 

        masterMenu = MasterMenu(parentFrame=self)
        menuBar.Append(masterMenu, '&Master')

        aboutMenu = AboutMenu(parentFrame=self)
        menuBar.Append(aboutMenu, '&About')
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.SetFont(self.font)

        self.SetMenuBar(menuBar)

        self.toolbar = self.CreateToolBar()
        self.toolbar.Realize()
        self.toolbar.SetBackgroundColour(wx.Colour(255, 255, 0))
        self.statusBar = self.CreateStatusBar() 
        # self.SetIcon(self.icon)
        # self.Bind(wx.EVT_MENU, self.ToggleStatusBar)
        # self.Bind(wx.EVT_MENU, self.ToggleToolBar)
        # self.Bind(wx.EVT_PAINT, self.OnPaint, self.toolbar)
        self.Centre() 
        self.Show(True)

    def OnPaint(self, e):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush('#c56c00'))
        dc.DrawRectangle(10, 15, 90, 60)

    def ToggleStatusBar(self, event):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, event):
        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class AboutMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        # self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        # self.SetFont(self.font)
        self.OnInit()
        self.parentFrame = parentFrame
    def OnInit(self):
        aboutItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&About', helpString = "Opens the About Box", kind=wx.ITEM_NORMAL)
        self.Append(aboutItem)
        self.Bind(wx.EVT_MENU, handler=self.onAboutDlg, source=aboutItem)

    def onAboutDlg(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName("CPC DIAGNOSTICS")
        # info.SetVersion("0.0.1 Beta")
        info.SetCopyright("(C) 2008 Python Geeks Everywhere")
        info.SetDescription(wordwrap(
            "Developed by CPC Diagnostics for Nimhans ",
            350, wx.ClientDC(self.parentFrame.panel)))
        info.SetWebSite("https://www.cpcdiagnostics.in/", "CPC Diagnostics Page")
        info.SetDevelopers(["Mir kaleem Mohideen", "Vivek"])
        info.SetLicence(wordwrap("Completely and totally open source!", 500,
                                wx.ClientDC(self.parentFrame.panel)))
        info.SetIcon(wx.Icon("./cpc.ico"))
        # Show the wx.AboutBox
        wx.adv.AboutBox(info)

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
        frame = GeneratePanel(None, 'PENDING REPORTS').ShowModal()
        # frame.SetSize((1000, 880))
        # frame.Show()
        app.MainLoop()

    def onView(self, event):
        app = wx.App(redirect=False)
        frame = ViewPanel(None, 'VIEW REPORTS').ShowModal()
        # frame.SetSize((1000, 880))
        # frame.Show()
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
        frame = TestMasterPanel(None, 'Test Master').ShowModal()
        # frame.SetSize((900, 700))
        # frame.Show()
        app.MainLoop()
        #pass
    def onHospitalMaster(self, event):
        app = wx.App(redirect=False)
        frame = HospitalMasterPanel(None, 'Hospital Master').ShowModal()
        # frame.SetSize((900, 700))
        # frame.Show()
        app.MainLoop()

    def onLabMaster(self, event):
        app = wx.App(redirect=False)
        frame = LabMasterPanel(None, 'Lab Master').ShowModal()
        # frame.SetSize((900, 700))
        # frame.Show()
        app.MainLoop()

    def onDepartmentMaster(self, event):
        app = wx.App(redirect=False)
        frame = DepartmentMasterPanel(None, 'Department Master').ShowModal()
        # frame.SetSize((900, 700))
        # frame.Show()
        app.MainLoop()
#---------------------------------------------------------------------------------------------------------------------------------------------

class TestMasterPanel(wx.Dialog):
    def __init__(self, parent, title):
        super(TestMasterPanel, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
        self.sizer = wx.GridBagSizer(0,0)
        self.test_itemsid = {dict_value['Name'] : dict_key  for lst_items in db.getAssayList() for dict_key, dict_value in lst_items.items()}
        if len(self.test_itemsid)==1 and list(self.test_itemsid.keys())[0] == None and list(self.test_itemsid.values())[0] == None:
            self.test_items = []
            self.test_itemsid = {}
        else:
            self.test_items = [i for i in self.test_itemsid]
        print(self.test_itemsid)
        self.testsList = wx.ListBox(self.panel, choices=self.test_items, size=(270, 250), style=wx.LB_MULTIPLE)
        #self.testsList.SetSelection(0)
        self.sizer.Add(self.testsList, pos = (0,0), flag = wx.ALL|wx.EXPAND, border = 5)
        self.Bind(wx.EVT_LISTBOX, self.onListboxSelection, self.testsList)

        self.antibodiesBtn = wx.Button(self.panel, label = "Antibody", size=(90, 28)) 

        bitmap1 = wx.Bitmap("delete.png", wx.BITMAP_TYPE_PNG)
        pic1 = self.scale_bitmap(bitmap1, 35, 30)
        self.discardBtn = wx.BitmapButton(self.panel, id = wx.ID_ANY, bitmap = pic1)
        self.discardBtn.SetToolTip("Remove")
        # self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))

        bitmap = wx.Bitmap("plus1.png", wx.BITMAP_TYPE_PNG)
        pic = self.scale_bitmap(bitmap, 35, 30)
        addBtn = wx.BitmapButton(self.panel, id = wx.ID_ANY, bitmap = pic)
        addBtn.SetToolTip("Add")
        # addBtn = wx.Button(self.panel, label = "Add", size=(90, 28))



        self.sizer.Add(self.antibodiesBtn, pos = (2,0), flag = wx.LEFT, border = 50)
        self.sizer.Add(self.discardBtn, pos = (1,3), flag = wx.RIGHT, border = 50)
        self.sizer.Add(addBtn, pos = (8,0), flag = wx.LEFT, border = 50)

        self.antibodiesBtn.Bind(wx.EVT_BUTTON, self.onAntibodiesClick)
        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)
        addBtn.Bind(wx.EVT_BUTTON, self.onAdd)

        # if not self.test_items:
        #     self.discardBtn.Disable()
        #     self.antibodiesBtn.Disable()
        # else:
        self.discardBtn.Hide()
        self.antibodiesBtn.Disable()

        self.sizer.AddGrowableCol(0)
        self.panel.SetSizerAndFit(self.sizer)
        self.Centre()
        self.sizer.Layout()
        self.Layout() 

    def scale_bitmap(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        # result = wx.BitmapFromImage(image)
        return result

    def onListboxSelection(self, evt):
        #pass
        self.index = evt.GetSelection()
        self.discardBtn.Show()
        self.antibodiesBtn.Enable()
        # self.panel.SetSizerAndFit(self.sizer)
        self.sizer.Layout()

    def onDiscard(self, evt):
        if self.index != None:
            self.selectedString = str(self.testsList.GetString(self.index))
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} test?'.format(self.selectedString), 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                #print(self.selectedString)
                print(self.test_itemsid[self.selectedString])
                if db.disableAssay(self.test_itemsid[self.selectedString]):
                    del self.test_itemsid[self.selectedString] 
                    self.test_items.remove(self.selectedString)
                    # if not self.test_items:
                    self.antibodiesBtn.Disable()
                    self.discardBtn.Hide()
                    self.testsList.Deselect(self.index)
                    self.index = None
                    self.testsList.Set(self.test_items)
                    print(self.test_itemsid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Chosen, Try Choosing Test that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.testsList.Deselect(self.index)
            self.index = None
            self.discardBtn.Hide()
            self.antibodiesBtn.Disable()
        dlg = MyDialog(self).ShowModal()
        print(self.test_itemsid)
        dlg.Destroy()

    def onAntibodiesClick(self, evt):
        if self.index != None:
            selectedString = str(self.testsList.GetString(self.index))
            # app = wx.App(redirect=False)
            Antibdy_Frame = AntibodyMasterPanel(None, 'Antibody Master', selectedString, self.test_itemsid).ShowModal()
            self.testsList.Deselect(self.index)
            self.index = None
            # Antibdy_Frame.SetSize((900, 700))
            # Antibdy_Frame.Show()
            # app.MainLoop()

        else:
            wx.MessageBox('None of them Chosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.addPanel.SetFont(self.font)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the test that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        testInput = None
        if self.addtext.GetValue(): testInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 


        if testInput is not None and testInput not in self.parent.test_items:
            addedAssayId = db.addAssay(testInput)
            if addedAssayId != -1:
                self.parent.test_itemsid[testInput] = addedAssayId
                self.parent.test_items.append(testInput)
                self.parent.testsList.Set(self.parent.test_items)
                self.parent.discardBtn.Hide()
                self.parent.antibodiesBtn.Disable()
                self.Close()
            else:
                wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        elif testInput is not None:
            msgBox = wx.MessageBox('The {0} had already exists, Try Adding New Test'.format(testInput), 'Existing Error', wx.OK| wx.ICON_WARNING)
            # print(msgBox)
            # print(wx.OK)
            if msgBox == wx.OK:
                self.addtext.SetValue('')
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the test name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class AntibodyMasterPanel(wx.Dialog):
    def __init__(self, parent, title, selectedString, assayIdDict):
        super(AntibodyMasterPanel, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parentFrame = parent
        self.testName = selectedString
        self.assayId = assayIdDict[self.testName]
        self.Antibdy_index = None 
        self.Result_index = None  
        self.choices = []
        self.flag = 1
        h = self.InitUI()
        # self.Centre() 
        # self.Show()      

    def InitUI(self): 
        self.finalSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer5 = wx.BoxSizer(wx.VERTICAL)
        self.sizer6 = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
        dc = wx.ScreenDC()
        dc.SetFont(font)
        testName = "   "+self.testName + ':'
        self.panel = wx.Panel(self, size = dc.GetTextExtent(testName))
        self.panel1 = wx.Panel(self)
        self.panel2 = wx.Panel(self)
        self.panel3 = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
        self.panel1.SetFont(self.font)
        self.panel2.SetFont(self.font)
        self.panel3.SetFont(self.font)

        # self.sizer = wx.GridBagSizer(0,0)

        self.test_name = wx.StaticText(self.panel, label = testName) 
        self.test_name.SetFont(font)

        self.antibodyTitle = wx.StaticText(self.panel1, label = "Antibodies", style=wx.ALIGN_CENTER) 
        self.font1 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
        self.antibodyTitle.SetFont(self.font1)

        self.antibdy_itemsid = {antibody['Name'] : anti_id  for anti_id, antibody in db.getAntiBodies(self.assayId).items()}
        #print(self.antibdy_itemsid)
        if len(self.antibdy_itemsid)==1 and list(self.antibdy_itemsid.keys())[0] == None and list(self.antibdy_itemsid.values())[0] == None:
            self.Antibdy_items = []
            self.antibdy_itemsid = {}
        else:
            self.Antibdy_items = [antibodyNames for antibodyNames in self.antibdy_itemsid if antibodyNames]
        self.AntibdyList = wx.ListBox(self.panel1, choices=self.Antibdy_items, size=(270, 250), style=wx.LB_MULTIPLE)
        print(self.antibdy_itemsid)
        # # self.AntibdyList.SetSelection(0)
        # self.sizer.Add(self.AntibdyList, pos = (2,0), flag = wx.LEFT|wx.RIGHT|wx.EXPAND, border = 40)
        self.AntibdyList.Bind(wx.EVT_LISTBOX, self.onListboxSelection)

        bitmap1 = wx.Bitmap("delete.png", wx.BITMAP_TYPE_PNG)
        pic1 = self.scale_bitmap(bitmap1, 35, 40)
        self.discardBtn = wx.BitmapButton(self.panel1, id = wx.ID_ANY, bitmap = pic1)
        self.discardBtn.SetToolTip("Remove")
        bitmap = wx.Bitmap("plus1.png", wx.BITMAP_TYPE_PNG)
        pic = self.scale_bitmap(bitmap, 35, 40)
        self.addBtn = wx.BitmapButton(self.panel1, id = wx.ID_ANY, bitmap = pic)
        self.addBtn.SetToolTip("Add")

        self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
        self.discardBtn.Bind(wx.EVT_BUTTON, self.onMsg)
        self.sizer1.Add(self.antibodyTitle, 0, wx.ALL|wx.CENTER, 5)
        self.sizer1.Add(self.AntibdyList, 0, wx.ALL|wx.CENTER, 5)
        self.sizer2.Add(self.addBtn, 0, wx.ALL|wx.CENTER, 5)
        self.sizer2.Add(self.discardBtn, 0, wx.ALL|wx.CENTER, 5)
        self.sizer1.Add(self.sizer2, 0, wx.ALL|wx.CENTER, 5)

        self.antibdytitleComment = wx.StaticText(self.panel2, label = "", size = (270, 23), style=wx.ALIGN_CENTER) #self.antibdy_selectedText + '{0}'.format(' Comment')
        self.antibdytitleComment.SetFont(self.font1)
        self.commentRichTxtctrl = rt.RichTextCtrl(self.panel2, value=" ", size=(270, 250))
        self.Bold = wx.Button(self.panel2, label="B", size=(25, 18))
        self.Italic = wx.Button(self.panel2, label="I", size=(25, 18))
        self.saveBtnComment = wx.Button(self.panel2, label = "Save", size=(90, 28))

        self.sizer3.Add(self.antibdytitleComment, 0, wx.ALL|wx.CENTER, 5)
        self.sizer3.Add(self.commentRichTxtctrl, 0, wx.ALL|wx.CENTER, 5)
        self.sizer4.Add(self.Bold, 0, wx.ALL|wx.CENTER, 5)
        self.sizer4.Add(self.Italic, 0, wx.ALL|wx.CENTER, 5)
        self.sizer4.Add(self.saveBtnComment, 0, wx.ALL|wx.CENTER, 5)
        self.sizer3.Add(self.sizer4, 0, wx.ALL|wx.CENTER, 5)


        self.antibdytitleResult = wx.StaticText(self.panel3, size = (270, 23), label = "", style=wx.ALIGN_CENTER) #self.antibdy_selectedText + '{0}'.format(' Options')
        self.antibdytitleResult.SetFont(self.font1)
        self.listResult = wx.ListCtrl(self.panel3, -1, size=(270, 250), style=wx.LB_SINGLE)
        # self.listResult = wx.ListBox(self.panel3, size=(270, 250), style=wx.LB_SINGLE)  # choices= self.choices,
        bitmap1 = wx.Bitmap("delete.png", wx.BITMAP_TYPE_PNG)
        pic1 = self.scale_bitmap(bitmap1, 35, 40)
        self.discardBtnResult = wx.BitmapButton(self.panel3, id = wx.ID_ANY, bitmap = pic1)
        self.discardBtnResult.SetToolTip("Remove")
        # self.discardBtn = wx.Button(self.panel, label = "Discard", size=(90, 28))
        bitmap = wx.Bitmap("plus1.png", wx.BITMAP_TYPE_PNG)
        pic = self.scale_bitmap(bitmap, 35, 40)
        self.addBtnResult = wx.BitmapButton(self.panel3, id = wx.ID_ANY, bitmap = pic)
        self.addBtnResult.SetToolTip("Add")

        self.sizer5.Add(self.antibdytitleResult, 0, wx.ALL|wx.CENTER, 5)
        self.sizer5.Add(self.listResult, 0, wx.ALL|wx.CENTER, 5)
        self.sizer6.Add(self.addBtnResult, 0, wx.ALL|wx.CENTER, 5)
        self.sizer6.Add(self.discardBtnResult, 0, wx.ALL|wx.CENTER, 5)
        self.sizer5.Add(self.sizer6, 0, wx.ALL|wx.CENTER, 5)

        self.panel1.SetSizer(self.sizer1)
        self.panel2.SetSizer(self.sizer3)
        self.panel3.SetSizer(self.sizer5)

        self.sizer.Add(self.panel1, 1, wx.EXPAND, 0)
        self.sizer.Add(self.panel2, 1, wx.EXPAND, 0)
        self.sizer.Add(self.panel3, 1, wx.EXPAND, 0)

        # self.panel.SetBackgroundColour(wx.Colour(0, 255, 0))
        self.finalSizer.Add(self.test_name, 0, wx.EXPAND, 0)
        self.finalSizer.Add(self.sizer, 1, wx.EXPAND, 0)

        self.antibdytitleComment.Hide()
        self.commentRichTxtctrl.Hide()
        self.Bold.Hide()
        self.Italic.Hide()
        self.saveBtnComment.Hide()
        self.antibdytitleResult.Hide()
        self.listResult.Hide()
        self.discardBtnResult.Hide()
        self.addBtnResult.Hide()
        self.discardBtn.Hide()

        self.SetSizer(self.finalSizer)
        # self.finalSizer.Fit(self)
        self.Layout()


    def scale_bitmap(self, bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        # result = wx.BitmapFromImage(image)
        return result

    def onMsg(self, evt):
        if self.Antibdy_index == None :  
            wx.MessageBox('None of them Chosen, Try Choosing any Antibody that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onListboxSelection(self, evt):
        # dc = wx.ScreenDC()
        # dc.SetFont(self.font1)
        self.listResult.ClearAll()
        self.previousDefaultIndex = -1
        self.Antibdy_index = evt.GetSelection()
        self.discardBtn.Bind(wx.EVT_BUTTON, self.onDiscard)

        self.antibdy_selectedText = str(self.AntibdyList.GetString(self.Antibdy_index))
        self.antiId = self.antibdy_itemsid[self.antibdy_selectedText]
        getAntibdyDict = db.getAntiBodies(self.assayId)
        self.choicesid ={choice: choiceId for choiceId, choice in getAntibdyDict[self.antiId]['Options'].items()}
        defaultOptionId = getAntibdyDict[self.antiId].get('Default', -1)
        if defaultOptionId > -1:  
            self.defaultOption = list(self.choicesid.keys())[list(self.choicesid.values()).index(defaultOptionId)]
        else:
            self.defaultOption = ''
        print(self.choicesid)
        comment = getAntibdyDict[self.antiId]['Comment']

        if len(self.choicesid)==1 and list(self.choicesid.keys())[0] == None and list(self.choicesid.values())[0] == None:
            self.choices = []
            self.choicesid = {}
            self.flag = 0
        else:
            self.choices= [choice for choice in self.choicesid if choice]
        self.antibdytitleResult.SetLabel('Options')
        self.antibdytitleResult.SetForegroundColour(wx.RED)
        self.antibdytitleComment.SetLabel('Comment')
        self.antibdytitleComment.SetForegroundColour(wx.RED)
        # size1 = dc.GetTextExtent(self.antibdy_selectedText+ '{0}'.format(' Options'))
        # size2 = dc.GetTextExtent(self.antibdy_selectedText+ '{0}'.format(' Comment'))
        self.antibdytitleComment.Show()
        self.commentRichTxtctrl.Show()
        self.Bold.Show()
        self.Italic.Show()
        self.saveBtnComment.Show()
        self.antibdytitleResult.Show()
        self.listResult.Show()
        self.discardBtnResult.Hide()
        self.addBtnResult.Show()
        self.discardBtn.Show()
        # self.listResult.Set(self.choices)
        self.listResult.InsertColumn(0, "Choices", width = self.panel1.GetSize()[0])
        if self.choices:
            for row, item in enumerate(self.choices):
                self.listResult.InsertItem(row, item)
        if self.defaultOption:
            defaultIndex = self.listResult.FindItem(-1, self.defaultOption)
            # print(defaultIndex)
            self.previousDefaultIndex = defaultIndex
            font = self.listResult.Parent.GetFont()
            font.SetStyle(wx.FONTSTYLE_ITALIC)
            self.listResult.SetItemFont(defaultIndex,font)
            self.listResult.SetItemBackgroundColour(defaultIndex, wx.Colour(223, 223, 223))
            self.listResult.SetItemTextColour(defaultIndex, wx.RED)

        self.Bold.Bind(wx.EVT_BUTTON, self.on_Bold)
        self.Italic.Bind(wx.EVT_BUTTON, self.on_italic)
        # self.commentRichTxtctrl.SetValue(self.comment)
        try:
            _bytesIO = BytesIO(bytes(comment, 'utf-8'))
            _handler = wx.richtext.RichTextXMLHandler()
            _handler.LoadFile(self.commentRichTxtctrl.GetBuffer(), _bytesIO)
            self.commentRichTxtctrl.Refresh()
            # self.loadXML()
        except Exception as ex:
            print(ex)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListbox1Selection, self.listResult)

        self.listResult.Bind(wx.EVT_MOTION, self.onMouseOver)

        self.Bind(wx.EVT_CONTEXT_MENU, self.showPopupMenu, self.listResult)
        self.addBtnResult.Bind(wx.EVT_BUTTON, self.onAddResult)
        self.discardBtnResult.Bind(wx.EVT_BUTTON, self.onMsg1)
        self.saveBtnComment.Bind(wx.EVT_BUTTON, self.onSaveComment)

        # self.antibdytitleComment.Wrap(dc.GetTextExtent(self.antibdytitleComment.Label)[1])
        # self.antibdytitleResult.Wrap(220)
        # self.panel2.SetSizer(self.sizer3)
        # self.panel3.SetSizer(self.sizer5)
        self.createMenu()
        self.SetSizer(self.finalSizer)
        self.Layout()

        #self.panel.SetSize(wx.Size(1000,1400))

    def createMenu(self):
        self.menu = wx.Menu()
        item1 = self.menu.Append(-1,'set as Default')
        self.Bind(wx.EVT_MENU, handler=self.Show, source=item1)
        # item2 = self.menu.Append(-1,'Item 2')

    def Show(self, evt):
        self.listResult.Show()
        font = self.listResult.Parent.GetFont()
        font.SetStyle(wx.FONTSTYLE_ITALIC)
        if self.previousDefaultIndex > -1:
            font1 = self.listResult.Parent.GetFont()
            self.listCtrlColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
            # self.listResult.SetBackgroundColour(wx.RED)
            self.listResult.SetItemFont(self.previousDefaultIndex,font1)
            self.listResult.SetItemBackgroundColour(self.previousDefaultIndex, self.listCtrlColor)
            self.listResult.SetItemTextColour(self.previousDefaultIndex, wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOXTEXT))
        self.listResult.SetItemFont(self.SelectIndex,font)
        self.listResult.SetItemBackgroundColour(self.SelectIndex, wx.Colour(223, 223, 223))
        self.listResult.SetItemTextColour(self.SelectIndex, wx.RED)
        optionId = self.choicesid[self.setDefaultFor]
        db.setDefaultOption(self.assayId, self.antiId, optionId)  
        self.previousDefaultIndex = self.SelectIndex
        
    def showPopupMenu(self,evt):
        # position = evt.GetPosition()
        # print(evt.GetSelection())
        ListBox = evt.GetEventObject()
        self.SelectIndex = ListBox.GetFirstSelected()
        self.setDefaultFor = ListBox.GetItemText(self.SelectIndex)
        print(self.setDefaultFor)
        self.PopupMenu(self.menu)
        

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
            self.Italic.SetBackgroundonDiscardResultColour(wx.Colour(240, 240, 240))
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
            wx.MessageBox('None of them Chosen, Try Choosing any Option that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)


    def onDiscard(self, evt):
        if self.Antibdy_index != None:
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard Antibody->{0} for {1} Test?'.format(self.antibdy_selectedText, self.testName), 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            dia = dialog.ShowModal() 
            if dia == wx.ID_YES:
                print(self.antibdy_itemsid[self.antibdy_selectedText])
                if db.disableAntiBody(self.assayId, self.antibdy_itemsid[self.antibdy_selectedText]):
                    del self.antibdy_itemsid[self.antibdy_selectedText]
                    self.Antibdy_items.remove(self.antibdy_selectedText)
                    self.AntibdyList.Deselect(self.Antibdy_index)
                    self.Antibdy_index = None
                    # if not self.Antibdy_items:
                    #     self.discardBtn.Hide()
                    self.AntibdyList.Set(self.Antibdy_items)
                    self.listResult.Hide()
                    self.commentRichTxtctrl.Hide()
                    self.saveBtnComment.Hide()
                    self.Bold.Hide()
                    self.Italic.Hide()
                    self.antibdytitleComment.Hide()
                    self.antibdytitleResult.Hide()
                    self.addBtnResult.Hide()
                    self.discardBtnResult.Hide()
                    self.discardBtn.Hide()
                    print(self.antibdy_itemsid)
                else:
                    wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Chosen, Try Choosing any Antibody that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.Antibdy_index != None:
            self.AntibdyList.Deselect(self.Antibdy_index)
            self.Antibdy_index = None
            self.listResult.Hide()
            self.antibdytitleResult.Hide()
            self.commentRichTxtctrl.Hide()
            self.Bold.Hide()
            self.Italic.Hide()
            self.saveBtnComment.Hide()
            self.antibdytitleComment.Hide()
            self.addBtnResult.Hide()
            self.discardBtnResult.Hide()
            self.discardBtn.Hide()
        dlg1 = MyDialog1(self).ShowModal()
        print(self.antibdy_itemsid)
        dlg1.Destroy()

    def onListbox1Selection(self, evt):
        ListBox = evt.GetEventObject()
        self.Result_index = ListBox.GetFirstSelected()
        # self.Result_index = evt.GetSelection()
        self.discardBtnResult.Show()

        # if self.Antibdy_index != None:
        #     self.AntibdyList.Deselect(self.Antibdy_index)
        #     self.Antibdy_index = None

        self.discardBtnResult.Bind(wx.EVT_BUTTON, self.onDiscardResult)

        self.Layout()
        # self.panel.SetSizerAndFit(self.sizer)
    def onMouseOver(self, event):
        #Loop through all items and set bgcolor to default, then:
        item_index, flag = self.listResult.HitTest(event.GetPosition())
        # print("previous-{}".format(self.previousDefaultIndex))
        # print(item_index)
        tip = self.listResult.GetToolTip()
        if item_index != -1 and item_index == self.previousDefaultIndex:
            if flag == wx.LIST_HITTEST_ONITEMLABEL:
                self.listResult.SetToolTipString("DEFAULT " + self.listResult.GetItemText(item_index))
        else:
            self.listResult.SetToolTip(None)
        # event.Skip()
    def add_tooltip(self, widget, text):
        """Add a tooltip to widget with the specified text."""
        tooltip = wx.ToolTip(text)
        widget.SetToolTip(tooltip)
        tooltip.SetAutoPop(0.0000000) 

    def onMouseLeave(self, event):
        #Loop through all items and set bgcolor to default, then:
        self.RefreshItems()
        event.Skip()

    def onDiscardResult(self, evt):
        if self.Result_index != None:
            if self.Result_index != self.previousDefaultIndex:
                self.selected_String1 = str(self.listResult.GetItemText(self.Result_index))#.GetString(self.Result_index))
                dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard Option->{0} for {1} Antibody?'.format(self.selected_String1, self.antibdy_selectedText), 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
                dia = dialog.ShowModal() 
                if dia == wx.ID_YES:
                    optionId = self.choicesid[self.selected_String1]
                    print(optionId)
                    ret_value = db.disableOption(self.assayId, self.antiId, optionId)
                    if ret_value != -1:
                        del self.choicesid[self.selected_String1]
                        self.choices.remove(self.selected_String1)
                        self.discardBtnResult.Hide()
                        if not self.choices:
                            self.flag = 0
                            # self.discardBtnResult.Hide()
                        self.listResult.DeleteItem(self.Result_index)
                        # self.listResult.Deselect(self.Result_index)
                        self.listResult.Select(-1)
                        self.Result_index = None
                        # self.listResult.Set(self.choices)
                        print(self.choicesid)
                    else:
                        wx.MessageBox('--------------', 'Error', wx.OK| wx.ICON_WARNING)
            else:
                wx.MessageBox('SET ANY OTHER OPTION AS DEFAULT TO DISCARD THIS OPTION', 'DEFAULT CHOSEN', wx.OK| wx.ICON_WARNING)

        else:
            wx.MessageBox('None of them Chosen, Try Choosing any Option that you want to Disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAddResult(self, evt):
        if self.Result_index != None:
            # self.listResult.Deselect(self.Result_index)
            self.listResult.Select(-1)
            self.Result_index = None
            self.discardBtnResult.Hide()
        dlg2 = MyDialog2(self).ShowModal()
        print(self.choicesid)
        # dlg2.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog1(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.addPanel.SetFont(self.font)
        self.text = wx.StaticText(self.addPanel, -1, 'Enter the Antibody that you want to Add in Test->{0}:'.format(self.parent.testName), pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        antibdyInput = None
        if self.addtext.GetValue(): antibdyInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour('#848484') 
        if antibdyInput is not None and antibdyInput not in self.parent.Antibdy_items:
            addedAntibdyId = db.addAntiBody(self.parent.assayId, antibdyInput)
            if addedAntibdyId != -1 and type(addedAntibdyId) == int:
                self.parent.antibdy_itemsid[antibdyInput] = addedAntibdyId
                self.parent.Antibdy_items.append(antibdyInput)
                self.parent.AntibdyList.Set(self.parent.Antibdy_items)
                self.parent.discardBtn.Hide()
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
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Antibody name")  # This text is grey, and disappears when you type

#---------------------------------------------------------------------------------------------------------------------------------------------

class MyDialog2(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.addPanel.SetFont(self.font)
        self.text1 = wx.StaticText(self.addPanel, -1,'Enter the Option that you want to Add in Antibody->{0}:'.format(self.parent.antibdy_selectedText), pos=(10, 12))
        self.addtext1 = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn1 = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour(wx.BLACK)

    def onAdd1(self, evt):
        optionInput = None
        if self.addtext1.GetValue(): optionInput =self.addtext1.GetValue()
        if self.addtext1.GetValue() and self.addtext1.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
            self.addtext1.SetFont(font)
            self.addtext1.SetForegroundColour('#848484') 
        if optionInput is not None and optionInput not in self.parent.choices:
            addedChoiceId = db.addOption(self.parent.assayId, self.parent.antiId, optionInput)
            if addedChoiceId and type(addedChoiceId) == int:
                self.parent.choicesid[optionInput] = addedChoiceId
                self.parent.choices.append(optionInput)
                self.parent.listResult.Append([optionInput])
                # self.parent.listResult.Set(self.parent.choices)
                self.parent.discardBtnResult.Hide()
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
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
                self.addtext1.SetFont(font)
                self.addtext1.SetForegroundColour('#848484')
                self.addtext1.SetHint("Enter the Option name")  # This text is grey, and disappears when you type

#---------------------------------------------------------------------------------------------------------------------------------------------
class HospitalMasterPanel(wx.Dialog):
    def __init__(self, parent, title):
        super(HospitalMasterPanel, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
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
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} Hospital?'.format(self.selectedString), 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
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
            wx.MessageBox('None of them Chosen, Try Choosing Hospital that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.hspList.Deselect(self.index)
            self.index = None
        dlg = MyDialog3(self).ShowModal()
        print(self.hsp_items)
        dlg.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------

class MyDialog3(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.addPanel.SetFont(self.font)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the Hospital that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        hspInput = None
        if self.addtext.GetValue(): hspInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Hospital name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class LabMasterPanel(wx.Dialog):
    def __init__(self, parent, title):
        super(LabMasterPanel, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
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
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} Lab?'.format(self.selectedString), 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
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
            wx.MessageBox('None of them Chosen, Try Choosing Lab that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.labList.Deselect(self.index)
            self.index = None
        dlg = MyDialog4(self).ShowModal()
        print(self.lab_items)
        dlg.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog4(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.addPanel.SetFont(self.font)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the Lab that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        labInput = None
        if self.addtext.GetValue(): labInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
                self.addtext.SetFont(font)
                self.addtext.SetForegroundColour('#848484')
                self.addtext.SetHint("Enter the Lab name")  # This text is grey, and disappears when you type
#---------------------------------------------------------------------------------------------------------------------------------------------
class DepartmentMasterPanel(wx.Dialog):
    def __init__(self, parent, title):
        super(DepartmentMasterPanel, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parentFrame = parent
        self.InitUI()
        self.Centre() 
        self.Show()     
        self.index = None

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
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
            dialog = wx.MessageDialog(self, 'Are you sure, Do you want to Discard {0} Department?'.format(self.selectedString), 'Confirm', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
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
            wx.MessageBox('None of them Chosen, Try Choosing Department that you want to disable', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onAdd(self, evt):
        if self.index != None:
            self.dptList.Deselect(self.index)
            self.index = None
        dlg = MyDialog5(self).ShowModal()
        print(self.dpt_items)
        dlg.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------
class MyDialog5(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Add", size=(800,135))
        self.parent = parent
        self.addPanel = wx.Panel(self)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.addPanel.SetFont(self.font)
        self.text = wx.StaticText(self.addPanel, -1, "Enter the Department that you want to Add:", pos=(10, 12))
        self.addtext = wx.TextCtrl(self.addPanel, size = (35,35), style = wx.TE_PROCESS_ENTER)
        self.addBtn = wx.Button(self.addPanel, label = "Add", size=(75, 28))
        font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)

    def onAdd(self, evt):
        dptInput = None
        if self.addtext.GetValue(): dptInput =self.addtext.GetValue()
        if self.addtext.GetValue() and self.addtext.GetForegroundColour() == '#848484':
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
            self.addtext.SetFont(font)
            self.addtext.SetForegroundColour(wx.BLACK)
        else:
            font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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
                font = wx.Font(10, wx.DEFAULT, wx.FONTSTYLE_ITALIC, wx.NORMAL, False, "Arial")
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

class PatientDetails(wx.Dialog): 
    def __init__(self, parent, title):
        super(PatientDetails, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER) 
        self.parentFrame = parent  
        #HIGHLIGHT_COLOR = (255, 0, 0)
        #self.highligt_color = wx.Colour(HIGHLIGHT_COLOR)
        self.windowFrameColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME)
        self.SetBackgroundColour(wx.LIGHT_GREY)
        self.InitUI(self.parentFrame) 
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
        rtc.SetBackgroundColour(wx.LIGHT_GREY)

    def InitUI(self, parent): 
        
        self.panel = wx.Panel(self) 
        sizer = wx.GridBagSizer(0,0)
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
        # self.panel.SetBackgroundColour(wx.Colour(35, 35, 142))
        #text = wx.StaticText(self.panel, label = "UHID:") 
        text = rt.RichTextCtrl(self.panel,size=(130,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self)) 
        self.Assign(text, "UHID:")
        text.SetForegroundColour(wx.BLACK)
        sizer.Add(text, pos = (0, 0), flag = wx.ALL, border = 5)
        text.SetForegroundColour(wx.BLACK)
        # text.SetEditable(False)
        
        self.tc = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc, pos = (0, 1), flag = wx.ALL|wx.EXPAND, border = 5)
        self.tc.SetToolTip("Enter UHID No.")
        self.tc.SetForegroundColour(wx.BLACK)

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
        text2.SetForegroundColour(wx.BLACK)
            
        self.tc2 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc2, pos = (1,1), flag = wx.ALL|wx.EXPAND, border = 5) 
        self.tc2.SetForegroundColour(wx.BLACK)

        text3 = wx.StaticText(self.panel,label = " Referring Dept:") 
        sizer.Add(text3, pos = (1, 2), flag = wx.ALL, border = 5)
        text3.SetForegroundColour(wx.BLACK)

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
        self.tc4.SetForegroundColour(wx.BLACK)
            
        text5 = wx.StaticText(self.panel,label = " Sample Collection Date:") 
        sizer.Add(text5, pos = (2, 2), flag = wx.ALL, border = 5)
        text5.SetForegroundColour(wx.BLACK)

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
        text7.SetForegroundColour(wx.BLACK)

        self.tc7 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc7, pos = (3,3), flag = wx.EXPAND|wx.ALL, border = 5)
        self.tc7.SetForegroundColour(wx.BLACK)

        #text8 = wx.StaticText(self.panel,label = "Gender:")
        text8 = rt.RichTextCtrl(self.panel,size=(130,30),style=wx.richtext.RE_READONLY|wx.NO_BORDER|wx.FONTFAMILY_DEFAULT|wx.TEXT_ATTR_FONT_FACE, validator = MouseNavigate(self))
        self.Assign(text8, "Gender:")
        sizer.Add(text8, pos = (4, 0), flag = wx.ALL, border = 5) 
            
        sampleList = ['Male', 'Female']
        self.gender = wx.RadioBox(self.panel, -1, "", wx.DefaultPosition, wx.DefaultSize, sampleList, 2, wx.RA_SPECIFY_COLS) 
        sizer.Add(self.gender, pos = (4,1), flag = wx.ALL, border = 5) 

        text9 = wx.StaticText(self.panel,label = " Lab Name:") 
        sizer.Add(text9, pos = (4, 2), flag = wx.ALL, border = 5)
        text9.SetForegroundColour(wx.BLACK)

        self.lab_items = db.getLabs()
        self.lab_items.insert(0, "-- Select --")
        self.tc8 = wx.Choice(self.panel, choices= self.lab_items)
        self.tc8.SetSelection(0)
        sizer.Add(self.tc8, pos = (4,3),flag = wx.EXPAND|wx.ALL, border = 5) 

        text10 = wx.StaticText(self.panel,label = " Ward Name/Collection Centre:") 
        sizer.Add(text10, pos = (5, 0), flag = wx.ALL, border = 5) 
        text10.SetForegroundColour(wx.BLACK)
            
        self.tc9 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc9, pos = (5,1), flag = wx.ALL|wx.EXPAND, border = 5)
        self.tc9.SetForegroundColour(wx.BLACK) 

        text11 = wx.StaticText(self.panel,label = "Email:") 
        sizer.Add(text11, pos = (5, 2), flag = wx.ALL, border = 5)
        text11.SetForegroundColour(wx.BLACK)

        self.tc10 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc10, pos = (5,3),flag = wx.ALL|wx.EXPAND, border = 5)
        self.tc10.SetForegroundColour(wx.BLACK)

        text12 = wx.StaticText(self.panel,label = "Phone No:") 
        sizer.Add(text12, pos = (6, 0), flag = wx.ALL, border = 5)
        text12.SetForegroundColour(wx.BLACK)

        self.tc11 = wx.TextCtrl(self.panel) 
        sizer.Add(self.tc11, pos = (6,1),flag = wx.ALL|wx.EXPAND, border = 5)
        self.tc11.SetForegroundColour(wx.BLACK)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
         
        saveBtn = wx.Button(self.panel, label = "Save", size=(90, 28)) 
        cancelBtn = wx.Button(self.panel, wx.ID_CLOSE, label = "Cancel", size=(90, 28))
        saveBtn.SetToolTip("Register")
        saveBtn.SetBackgroundColour(wx.Colour(47, 47, 47))
        saveBtn.SetForegroundColour(wx.Colour(255, 255, 255))
        cancelBtn.SetBackgroundColour(wx.Colour(47, 47, 47))
        cancelBtn.SetForegroundColour(wx.Colour(255, 255, 255))
            
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
                            TestRegisterScreen(self, -1, 'Register Tests', _requestId, dic['Patient Name']).ShowModal()
                            self.Close()
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


class TestRegisterScreen(wx.Dialog):
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
        # text2 = wx.StaticText(panel, label = "Chosen Tests")
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
        super(TestRegisterScreen, self).__init__(parent, id, title, wx.DefaultPosition, (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.testsUpdateList_items = []
        self.test_itemsChosenid = []
        self.parent = parent
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

        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        panel.SetFont(self.font)

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
        # font1 = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        # font1.SetPointSize(12)
        
        text = wx.StaticText(panel, label = "Tests", size = (170,80))
        self.testsListbox = wx.ListBox(panel, -1, size=(270, 230), choices=self.test_items, style=wx.LB_SINGLE)
        text.SetFont(font)
        #self.testsListbox.SetSelection(0)
        text2 = wx.StaticText(panel, label = "Chosen Tests", size = (170,80))
        self.testsChosenListbox = wx.ListBox(panel, -1, size=(270, 230), choices=[], style=wx.LB_SINGLE)
        text2.SetFont(font)
        name = wx.StaticText(self, label= "Name: " +patientName, size = (220, 120))
        name.SetFont(font)
        # age = wx.StaticText(self, label= "Age     : {0}".format(self.parent.age))
        # age.SetFont(font1)
        # gender = wx.StaticText(self, label= "Gender: {0}".format(self.parent.gender))
        # gender.SetFont(font1)  

        #self.Bind(wx.EVT_LISTBOX, self.OnSelectFirst, self.testsListbox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectFirst, self.testsListbox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelectSecond, self.testsChosenListbox)
        #self.Bind(wx.EVT_LISTBOX, self.OnSelectSecond, self.testsChosenListbox)
        vbox.Add(name, flag=wx.LEFT|wx.TOP, border=50)
        #sizer.Add(name, pos = (0, 0), flag = wx.CENTER|wx.TOP|wx.BOTTOM, border = 20)
        sizer.Add(text, pos = (1, 0), flag = wx.ALIGN_CENTER)
            # flag = wx.LEFT, border = 100)
        sizer.Add(text2, pos = (1, 3), flag = wx.ALIGN_CENTER) 
         # flag = wx.LEFT|wx.RIGHT, border = 100)
        sizer.Add(self.testsListbox, pos = (2, 0), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, border = 50)
        sizer.Add(self.testsChosenListbox, pos = (2, 3), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, border = 50)

        saveBtn = wx.Button(panel, wx.ID_CLOSE, label = "Save", size=(90, 28)) 
        cancelBtn = wx.Button(panel, label = "Cancel", size=(90, 28)) 
        cancelBtn.SetBackgroundColour(wx.Colour(47, 47, 47))
        cancelBtn.SetForegroundColour(wx.Colour(255, 255, 255))
        saveBtn.SetBackgroundColour(wx.Colour(47, 47, 47))
        saveBtn.SetForegroundColour(wx.Colour(255, 255, 255))
            
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
                # self.parent.Close()
        else:
            if self.test_itemsChosenid:
                wx.MessageBox('Test not Registered', 'Error', wx.OK | wx.ICON_WARNING)
            else:
                wx.MessageBox('None of them Chosen, Try Choosing Test', 'Selection Error', wx.OK| wx.ICON_WARNING)

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
            wx.MessageBox('Chosen Already, Try selecting other', 'Selected Already', wx.OK | wx.CANCEL | wx.ICON_WARNING)
            #self.testsListbox.SetString(index, 'Already Chosen')


    def OnSelectSecond(self, event):
        index = event.GetSelection()
        #print(index)
        selected_String1 = str(self.testsChosenListbox.GetString(index))
        self.testsUpdateList_items.remove(selected_String1)
        self.test_itemsChosenid.remove(self.test_itemsid[selected_String1])
        self.testsChosenListbox.Set(self.testsUpdateList_items)
        print(self.testsUpdateList_items)






#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

class GeneratePanel(wx.Dialog):
    def __init__(self, parent, title):
        super(GeneratePanel, self).__init__(parent, title = title, size = (1300, 800), style = wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER) 
        self.index = 0
        self.selectedIndex = None
        self.myRowDict = {}
        self.searchNameDict = {}
        self.myRequestIdDict = {}
        self.details = {}

        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer()

        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        panel.SetFont(self.font)

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
            ResultDetails(self, -1, 'Result Details', rqstId).ShowModal()
        else:
            wx.MessageBox('None of them Chosen, Try Choosing Patient that you want to generate Report for', 'Selection Error', wx.OK| wx.ICON_WARNING)
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
class ResultDetails(wx.Dialog):
    def __init__(self, parent, id, title, RqstId):
        #wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (650, 450))
        super(ResultDetails, self).__init__(parent, id, title, wx.DefaultPosition, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
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
        self.Centre()
        self.Show()

class TestPanel(scrolled.ScrolledPanel):

    def __init__(self, parent):

        scrolled.ScrolledPanel.__init__(self, parent=parent, id= -1)
        self.parent = parent
        self.index = None
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.parent.SetFont(self.font)
        if self.parent.pendingRequest != None:
            for i in self.parent.pendingRequest:
                self.parent.pendingTestAssays.append(i['assayName'])
        else:
            self.parent.pendingTestAssays = []

        self.tests = wx.ListBox(self, -1, size=(370, 130), choices=self.parent.pendingTestAssays, style=wx.LB_MULTIPLE)
        self.Bind(wx.EVT_LISTBOX, self.Onlistbox, self.tests)
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
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
            # flag = 0
            self.antibdyIdDict = {}
            self.optionIdDict = {}
            self.antiBodyDict = {}
            self.commentDict = {}
            self.checklistSelect = []
            self.addMany = []
            self.antiBodyOptionCheck = {}
            self.isdefault = {}
            # self.boldFlag = False
            # self.italicFlag = False
            self.caps = False
            font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
            for i in self.parent.pendingRequest:
                if i['assayName'] == self.selectedString:
                    self.assayId = i['assayId']
                    antibodiesOptionsComments = i['antiBodies']
                    print(antibodiesOptionsComments)
            # self.sizer2 = wx.GridBagSizer()
            ids = 1
            antibodyCount= len(antibodiesOptionsComments)
            if antibodyCount%3 != 0:
                rows = antibodyCount//3 +1
            elif antibodyCount%3 == 0:
                rows = antibodyCount//3
            cols = 3
            self.gs = wx.GridSizer(rows, cols, 25, 65)
            for dic in antibodiesOptionsComments:
                # if flag%3 == 0 or flag == 0:
                #     vbox1 = wx.BoxSizer(wx.VERTICAL)
                #     antibodyText = wx.StaticText(self, -1, 'Antibodies')
                #     optionsText = wx.StaticText(self, -1, 'Options')
                #     commentText = wx.StaticText(self, -1, 'Comments')
                #     antibodyText.SetFont(font)
                #     optionsText.SetFont(font)
                #     commentText.SetFont(font)
                #     vbox1.Add(antibodyText, flag = wx.EXPAND)
                #     vbox1.Add(optionsText, flag = wx.EXPAND|wx.BOTTOM, border = 10)
                #     vbox1.Add(commentText, flag = wx.EXPAND)
                #     self.addMany.append((vbox1, 0, wx.EXPAND))
                # flag+=1

                choices=[i for i in dic['options'].values() if i != None]
                if not choices:
                    continue
                vbox = wx.BoxSizer(wx.VERTICAL)
                dc = wx.ScreenDC()
                # dc.SetFont(font)

                antibody = wx.StaticText(self, ids, dic['antiBody'], size= dc.GetTextExtent(dic['antiBody'] + "          "))
                antibody.SetFont(font)
                self.antibdyIdDict[dic['antiBody']] = dic['antiBodyId']
                self.optionIdDict[dic['antiBodyId']] = {option: Id for Id, option in dic['options'].items()}

                defaultOptionId = dic.get('default', -1)
                if defaultOptionId > -1:
                    self.defaultOption = list(self.optionIdDict[dic['antiBodyId']].keys())[list(self.optionIdDict[dic['antiBodyId']].values()).index(defaultOptionId)]
                    choices.insert(0,choices.pop(choices.index(self.defaultOption)))
                    self.antiBodyDict[dic['antiBodyId']] = defaultOptionId
                    self.antiBodyOptionCheck[dic['antiBody']] = {'default' : self.defaultOption}
                    self.isdefault[dic['antiBody']]= {'default' : self.defaultOption}
                else:
                    choices.insert(0, '-- Select --')
                    self.checklistSelect.append(ids)
                print(choices)            
                self.inputTwo = wx.Choice(self,id =ids, choices = choices)
                self.inputTwo.SetSelection(0)
                # self.sizer2.Add(antibody, pos = (k,9), flag = wx.RIGHT|wx.BOTTOM, border = 100)
                # self.sizer2.Add(self.inputTwo, pos = (k,12), flag = wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 100)

                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer1 = wx.BoxSizer(wx.HORIZONTAL)
                #save_button = wx.Button(self, label="Save")
                self.rt = rt.RichTextCtrl(self, ids, value="", size=(250, 100))
                self.Bold = wx.Button(self, id =ids, label="B", size=(25, 18))
                self.Bold.myname = "Bold"
                Italic = wx.Button(self, id =ids, label="I", size=(25, 18))
                Italic.myname = "Italic"

                # if dic['comment']:
                #     self.rt = rt.RichTextCtrl(self, ids, value= dic['comment'], size=(250, 100))
                #     # comment = wx.TextCtrl(self, ids, dic['comment'], size=(300, -1))
                # else:
                    # comment = wx.TextCtrl(self, ids, '', size=(300, -1))

                try:
                    _bytesIO = BytesIO(bytes(dic['comment'], 'utf-8'))
                    _handler = wx.richtext.RichTextXMLHandler()
                    _handler.LoadFile(self.rt.GetBuffer(), _bytesIO)
                    self.rt.Refresh()
                    # self.loadXML()
                except Exception as ex:
                    print(ex)

                sizer.Add(self.rt, 1, wx.EXPAND|wx.ALL, 6)
                sizer1.Add(self.Bold, 0, wx.EXPAND|wx.ALL, 6)
                sizer1.Add(Italic, 0, wx.EXPAND|wx.ALL, 6)
                sizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 6)

                # self.sizer2.Add(sizer, pos = (k,13), flag = wx.LEFT|wx.BOTTOM, border = 100)
                vbox.Add(antibody, flag = wx.EXPAND|wx.BOTTOM, border = 5)
                vbox.Add(self.inputTwo, flag = wx.EXPAND)
                vbox.Add(sizer, flag = wx.EXPAND)
                self.addMany.append((vbox, 0, wx.EXPAND))

                self.SomeNewEvent, self.EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
                # then bind the events in the constructor or somewhere
                self.inputTwo.Bind(wx.EVT_CHOICE, self.OnChoiceSelect)
                self.rt.Bind(wx.EVT_CHAR, self.onKeyDownHandler, id = self.rt.GetId())
                self.rt.Bind(wx.EVT_LEFT_DOWN, self.onKeyDownHandler, id = self.rt.GetId())
                self.rt.Bind(wx.EVT_RIGHT_UP, self.onKeyDownHandler, id = self.rt.GetId())
                # bind also new event handler but 
                self.rt.Bind(self.EVT_SOME_NEW_EVENT , self.onKeyDownAction, id = self.rt.GetId())
                self.rt.Bind(wx.EVT_TEXT, self.onCommentModified, id = self.rt.GetId())
                self.Bold.Bind(wx.EVT_BUTTON, self.on_Bold, id = self.Bold.GetId())
                Italic.Bind(wx.EVT_BUTTON, self.on_italic, id = Italic.GetId())

                out = BytesIO()
                handler = wx.richtext.RichTextXMLHandler()
                rt_buffer = self.rt.GetBuffer()
                handler.SaveFile(rt_buffer, out)
                xml_content = out.getvalue()

                self.commentDict[dic['antiBodyId']] =  utilsDb.getRichTextFormat(xml_content.decode('utf-8')) #xml_content.decode('utf-8')#self.rt.GetValue()
                ids+=1

                # id2 = comment.GetEventObject().GetId()
                # antibdyId = self.antibdyIdDict[wx.FindWindowById(id2).GetValue()]
                # self.antiBodyDict[antibdyId] = optId
            self.gs.AddMany(self.addMany)
            self.saveBtn = wx.Button(self, label = "Save", size=(90, 28))
            # self.sizer2.Add(self.saveBtn, pos = (k+1, 13), flag = wx.LEFT|wx.BOTTOM, border = 250)
            self.saveBtn.Bind(wx.EVT_BUTTON, self.onMsgbox)#onUpdateReport)
            self.controlSizer.Add(self.gs, 0, wx.ALL, 5)
            self.controlSizer.Add(self.saveBtn, 0, wx.ALL|wx.ALIGN_CENTER, 10)
            # self.controlSizer.Add(self.sizer2, 0, wx.ALL, 5)
            self.SetSizer(self.mainSizer)
            self.SetupScrolling()
            #self.Centre()
            self.Layout()
        else:
            wx.MessageBox('None of them Chosen, Try Choosing Test that you want to generate Report for', 'Selection Error', wx.OK| wx.ICON_WARNING)

    def onMsgbox(self,event):
        dia = Confirmation(self, "Confirmation").ShowModal() 
        # if dia == wx.ID_YES:



    def OnChoiceSelect(self, event):
        id1 = event.GetEventObject().GetId()
        # print(id1)
        # print(wx.FindWindowById(id1).GetLabel())
        antibody = wx.FindWindowById(id1).GetLabel()
        antibdyId = self.antibdyIdDict[antibody]
        option = event.GetString()
        if id1 in self.checklistSelect:
            if event.GetSelection()>0:
                optId = self.optionIdDict[antibdyId][option]
                self.antiBodyDict[antibdyId] = optId
                # if antibody in self.isdefault:
                #     if option == self.isdefault[antibody]['default']:
                #         self.antiBodyOptionCheck[antibody] = self.isdefault[antibody]
                #     else:
                self.antiBodyOptionCheck[antibody] = option
            elif event.GetSelection()==0:
                wx.MessageBox("Choose the result for Update", 'Error', wx.OK | wx.ICON_WARNING)
                self.antiBodyDict.pop(antibdyId, None)
                self.antiBodyOptionCheck.pop(antibody, None)
        elif event.GetSelection()>=0:
            optId = self.optionIdDict[antibdyId][option]
            self.antiBodyDict[antibdyId] = optId
            if antibody in self.isdefault:
                if option == self.isdefault[antibody]['default']:
                    self.antiBodyOptionCheck[antibody] = self.isdefault[antibody]
                else:
                    self.antiBodyOptionCheck[antibody] = option
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

            self.commentDict[antibdyId] = utilsDb.getRichTextFormat(xml_content.decode('utf-8')) #xml_content.decode('utf-8') #rtc.GetValue()
            event.Skip()

    def on_Bold(self, event):
        boldBtnWidget = event.GetEventObject()
        id1 = boldBtnWidget.GetId()
        widgetCtrl = [rtcCtrl for rtcCtrl in [widgetCtrl for widgetCtrl in self.GetChildren() if isinstance(widgetCtrl, wx.richtext.RichTextCtrl)] if rtcCtrl.GetId() == id1][0]
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
        # print(self.commentDict)
        try:
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
                    OpenReport(self, "Open Report", self.parent.email, self.parent.name, jsonHead['reportFile']).ShowModal()
                else:
                    self.controlSizer.Clear(True)
                    dialog = wx.MessageBox('Results is Updated for {0} test'.format(self.selectedString), 'Successfully Updated', wx.OK)
                # self.ScrollChildIntoView(self.tests)
                self.SetupScrolling(rate_y=5, scrollToTop=True, scrollIntoView=True)
                self.tests.Deselect(self.index)
                self.index = None
                self.tests.Clear()
                self.tests.Set(self.parent.pendingTestAssays)
                self.tests.Update()
                # for i in db.getPendingRequest(self.parent.RqstId):
                #     print(i['assayName'])
            else:
                wx.MessageBox('Test Report not updated', 'Error', wx.OK | wx.ICON_WARNING)
        except Exception as err:
            wx.MessageBox(str(err), 'Error', wx.OK | wx.ICON_WARNING)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Confirmation(wx.Dialog):
    def __init__(self, parent, title):
        super(Confirmation, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parent = parent
        pnl = wx.Panel(self)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        checkString = [not(isinstance(val, dict)) for val in self.parent.antiBodyOptionCheck.values()]
        isNoDefaultAll = any(checkString)
        string = """The choosed option are:"""
        if isNoDefaultAll:
            self.msgcontrol= wx.ListCtrl(pnl, -1, size=(400, 600), style=wx.LB_SINGLE) #style = wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
            self.msgcontrol.InsertColumn(0, 'Antibodies', width = 250) 
            self.msgcontrol.InsertColumn(1, 'Choosed Options', wx.LIST_FORMAT_RIGHT, 150)
            for antibody, value in self.parent.antiBodyOptionCheck.items():
                if not isinstance(value, dict):
                    # string += """\n{} -> {}""".format(antibody, value)
                    self.index = self.msgcontrol.InsertItem(0, antibody) 
                    self.msgcontrol.SetItem(self.index, 1, value)
            # wx.MessageBox(string, "Confirm" ,wx.OK | wx.ICON_INFORMATION)
        else:
            # wx.MessageBox("ALL are choosed as default","Confirm",wx.OK | wx.ICON_INFORMATION)
            self.msgcontrol = wx.StaticText(pnl, label = "ALL are choosed as default")
            font = wx.Font(18, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
            self.msgcontrol.SetFont(font)

        self.confirmBtn = wx.Button(pnl, label = "Confirm", size=(90, 28))
        self.confirmBtn.Bind(wx.EVT_BUTTON, self.onConfirm)
        self.cancelBtn = wx.Button(pnl, label = "Cancel", size=(90, 28))
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)

        h_sizer.Add(self.msgcontrol, 0, wx.CENTER)
        h_sizer1.Add(self.cancelBtn, 0, wx.ALL, 10)
        h_sizer1.Add(self.confirmBtn, 0, wx.ALL, 10)
        
        main_sizer.Add((0,0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add(h_sizer1, 0, wx.CENTER)
        # main_sizer.Add(self.confirmBtn, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        # main_sizer.Add(self.cancelBtn, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        main_sizer.Add((0,0), 1, wx.EXPAND)
        
        pnl.SetSizer(main_sizer)
    def onConfirm(self, evt):
        self.Close()
        self.parent.onUpdateReport(evt)
    #     TestPanel().onUpdateReport
    #     # pass
    def onCancel(self, evt):
        self.Close()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ViewPanel(wx.Dialog):
    def __init__(self, parent, title):
        super(ViewPanel, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER) 
        self.index = 0
        self.selectedIndex = None
        self.myRowDict = {}
        self.searchNameDict = {}
        self.myRequestIdDict = {}
        self.details = {}

        panel = wx.Panel(self, -1)
        sizer = wx.GridBagSizer()

        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        panel.SetFont(self.font)

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
            OpenReport(self, "Open Report", self.details[rqstId]["Email"], self.details[rqstId]["Name"], jsonHead['reportFile']).ShowModal()
        else:
            wx.MessageBox('None of them Chosen, Try Choosing Patient that you want to generate Report for', 'Selection Error', wx.OK| wx.ICON_WARNING)
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
class OpenReport(wx.Dialog):
    def __init__(self, parent, title, email, name, reportname):
        super(OpenReport, self).__init__(parent, title = title, size = (1300, 800), style =  wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.parentFrame = parent
        self.email = email
        self.name = name
        self.reportPath = reportname
        self.InitUI()
        self.Centre() 
        self.Show()     
    def InitUI(self):
        self.panel = wx.Panel(self)        
        self.font=wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")
        self.panel.SetFont(self.font)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")

        if self.email:
            self.text = wx.TextCtrl(self.panel,-1, self.email, size=(300, -1))

        else:
            self.text = wx.TextCtrl(self.panel,-1, size=(300, -1))

        st1 = wx.StaticText(self.panel, label='Name:', size = (100, 100))
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        name = wx.StaticText(self.panel, label= self.name, size = (350, 100))
        name.SetFont(font)
        hbox1.Add(name, proportion=0)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        # vbox.Add((-1, 50))

        st2 = wx.StaticText(self.panel, label='Email:', size = (100, 50))
        st2.SetFont(font)
        vbox.Add(st2, flag=wx.LEFT | wx.TOP, border=10)
        # vbox.Add((-1, 10))

        vbox.Add(self.text, flag=wx.LEFT|wx.RIGHT,border=10)
        # vbox.Add((-1, 25))

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
        print(self.reportPath)
        utilsDb.sendEmail({ self.name :
                {
                    'to': [self.text.GetValue()],
                    'body': "Hey, get your Report",
                    'subject': "Report from Nimhans",
                    'attachments' : [self.reportPath]
                }
              })
        # pass

#---------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
