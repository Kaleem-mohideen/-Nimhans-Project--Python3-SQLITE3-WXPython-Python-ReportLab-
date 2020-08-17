import os
import wx  
import wx.lib.agw.thumbnailctrl as TC
from PIL import Image
import datetime
import wx.adv
import wx.lib.scrolledpanel as scrolled

filename="regis.jpeg"
class MyApp(wx.App):
    def __init__(self):
        super().__init__()

        frame = MyFrame(parent=None, title="Menu Bar App")
        frame.Show()


class ReportsMenu(wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame
    
    def OnInit(self):
        generateItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Generate\tCtrl+N', kind=wx.ITEM_NORMAL)
        self.Append(generateItem)
        self.Bind(wx.EVT_MENU, handler=self.onGenerate, source=generateItem)

        viewItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text="&View\tCtrl+O", helpString="Save your file", kind=wx.ITEM_NORMAL)
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


class MasterMenu(wx.Menu):
    def __init__(self):
        super().__init__()
        self.OnInit()

    def OnInit(self):
        pass
        # copyItem = wx.MenuItem(self, 100,text = "Copy",kind = wx.ITEM_NORMAL)
        # self.Append(copyItem) 
        # cutItem = wx.MenuItem(self, 101,text = "Cut",kind = wx.ITEM_NORMAL) 
        # self.Append(cutItem) 
        # pasteItem = wx.MenuItem(self, 102,text = "Paste",kind = wx.ITEM_NORMAL) 
        # self.Append(pasteItem)
    

class MyFrame(wx.Frame):         
    def __init__(self, parent, title): 
        super().__init__(parent, title = title, size = (500, 400))  
        self.InitUI()
        # wx.Frame.__init__(self, None, wx.ID_ANY, "Choose Dot in Picture", size=(700,500))
        self.panel = wx.Panel(self, wx.ID_ANY)
        jpeg = wx.Image(filename, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        image=wx.StaticBitmap(self.panel, -1, jpeg, (150, 80), (jpeg.GetWidth(), jpeg.GetHeight()))
        print(image.GetScaleMode())
        image.Bind(wx.EVT_LEFT_DOWN, self.on_clic)
        self.Show(True)

    def on_clic(self, evt):
        PatientDetails(self, title = 'ENTER PATIENT DETAILS')
        x, y=evt.GetPosition()
        print("clicked at", x, y)


    def InitUI(self):   
        #self.text = wx.TextCtrl(parent=self, id=wx.ID_ANY, style = wx.EXPAND|wx.TE_MULTILINE) 
        menuBar = wx.MenuBar() 

        reportsMenu = ReportsMenu(parentFrame=self)
        menuBar.Append(reportsMenu, '&Reports') 

        masterMenu = MasterMenu()
        menuBar.Append(masterMenu, '&Master')

        self.SetMenuBar(menuBar) 

        #self.Bind(wx.EVT_MENU, self.MenuHandler)
        self.Centre() 
        self.Show(True)


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
            
        tc = wx.TextCtrl(panel) 
        sizer.Add(tc, pos = (0, 1), flag = wx.ALL|wx.EXPAND, border = 5)

        text1 = wx.StaticText(panel, label = "Referring Hospital:")
        sizer.Add(text1, pos = (0, 2), flag = wx.ALL, border = 5)

        tc1 = wx.TextCtrl(panel) 
        sizer.Add(tc1, pos = (0,3),flag = wx.EXPAND|wx.ALL, border = 5)
         
        text2 = wx.StaticText(panel, label = "MRD No:") 
        sizer.Add(text2, pos = (1, 0), flag = wx.ALL, border = 5)
            
        tc2 = wx.TextCtrl(panel) 
        sizer.Add(tc2, pos = (1,1), flag = wx.ALL|wx.EXPAND, border = 5) 

        text3 = wx.StaticText(panel,label = "Referring Dept:") 
        sizer.Add(text3, pos = (1, 2), flag = wx.ALL, border = 5)

        tc3 = wx.TextCtrl(panel) 
        sizer.Add(tc3, pos = (1,3),flag = wx.EXPAND|wx.ALL, border = 5)
         
        text4 = wx.StaticText(panel,label = "Patient Name:") 
        sizer.Add(text4, pos = (2, 0), flag = wx.ALL, border = 5) 
            
        tc4 = wx.TextCtrl(panel) 
        sizer.Add(tc4, pos = (2,1), flag = wx.ALL|wx.EXPAND, border = 5) 
            
        text5 = wx.StaticText(panel,label = "Sample Collection Date:") 
        sizer.Add(text5, pos = (2, 2), flag = wx.ALL, border = 5)
            
        tc5 = wx.TextCtrl(panel) 
        sizer.Add(tc5, pos = (2,3),flag = wx.EXPAND|wx.ALL, border = 5) 
         
        text6 = wx.StaticText(panel, label = "Age:") 
        sizer.Add(text6, pos = (3, 0), flag = wx.ALL, border = 5) 
            
        tc6 = wx.TextCtrl(panel) 
        sizer.Add(tc6, pos = (3,1), flag = wx.ALL|wx.EXPAND, border = 5) 
        #sizer.AddGrowableRow(3)

        text7 = wx.StaticText(panel,label = "Lab Reference No:") 
        sizer.Add(text7, pos = (3, 2), flag = wx.ALL, border = 5)

        tc7 = wx.TextCtrl(panel) 
        sizer.Add(tc7, pos = (3,3), flag = wx.EXPAND|wx.ALL, border = 5)

        text8 = wx.StaticText(panel,label = "Gender:")
        sizer.Add(text8, pos = (4, 0), flag = wx.ALL, border = 5) 
            
        sampleList = ['Male', 'Female']
        gender = wx.RadioBox(panel, -1, "", wx.DefaultPosition, wx.DefaultSize, sampleList, 2, wx.RA_SPECIFY_COLS) 
        sizer.Add(gender, pos = (4,1), flag = wx.ALL, border = 5) 

        text9 = wx.StaticText(panel,label = "Report Generated Date:") 
        sizer.Add(text9, pos = (4, 2), flag = wx.ALL, border = 5)

        tc9 = wx.TextCtrl(panel) 
        sizer.Add(tc9, pos = (4,3),flag = wx.ALL|wx.EXPAND, border = 5)

        text10 = wx.StaticText(panel,label = "Ward Name/Collection Centre:") 
        sizer.Add(text10, pos = (5, 0), flag = wx.ALL, border = 5) 
            
        tc10 = wx.TextCtrl(panel) 
        sizer.Add(tc10, pos = (5,1), flag = wx.ALL|wx.EXPAND, border = 5) 

        text11 = wx.StaticText(panel,label = "Lab Name:") 
        sizer.Add(text11, pos = (5, 2), flag = wx.ALL, border = 5)

        tc11 = wx.TextCtrl(panel) 
        sizer.Add(tc11, pos = (5,3),flag = wx.EXPAND|wx.ALL, border = 5) 

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
        Screen3(None, -1, 'listbox')

    def onClose(self, event):
        """"""
        self.Close()


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





#----------------------------------------------------------------------



class GeneratePanel(wx.Frame):
    def __init__(self, parent, title):
        super(GeneratePanel, self).__init__(parent, title = title, size = (700, 500)) 

        # sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.SetSizer(sizer)
        sizer = wx.GridBagSizer()

        self.dpc1 = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, size=(120,-1))
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnFromDateChanged, self.dpc1)
        sizer.Add(self.dpc1, (3,9), (2, 4), wx.RIGHT|wx.BOTTOM, 40)
        # In some cases the widget used above will be a native date
        # picker, so show the generic one too.
        self.dpc2 = wx.adv.GenericDatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, size=(120,-1), style = wx.TAB_TRAVERSAL| wx.adv.DP_DROPDOWN| wx.adv.DP_SHOWCENTURY| wx.adv.DP_ALLOWNONE )
        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnToDateChanged, self.dpc2)
        sizer.Add(self.dpc2, (3,16), (2, 4), wx.LEFT|wx.BOTTOM, 40)
        now = wx.DateTime.Now()
        print(wx.DateTime.FormatISODate(now))
        print(wx.DateTime.Format(now))
        
        
        self.searchExpectedResults = wx.SearchCtrl(self,
                                    size=(250, -1),
                                    style=wx.TE_PROCESS_ENTER)
        #self.searchExpectedResults.style = wx.BORDER_RAISED
        sizer.Add(self.searchExpectedResults, (1, 8), (1, 14), wx.EXPAND|wx.RIGHT, 40)
        self.searchExpectedResults.Bind(wx.EVT_CHAR, self.on_char) # Bind an EVT_CHAR event to your SearchCtrl

        filterBtn = wx.Button(self, label = "Filter", size=(90, 28))
        sizer.Add(filterBtn, pos = (5, 11), flag = wx.LEFT|wx.BOTTOM, border = 50)
        filterBtn.Bind(wx.EVT_BUTTON, self.onfilter)

        search_items = sorted(['test', 'entry'])
        self.textareaExpectedResults = wx.ListBox(self, choices=search_items, size=(270, 250))
        sizer.Add(self.textareaExpectedResults, (6, 8), (2, 14), wx.EXPAND|wx.RIGHT, 40)

        sizer.AddGrowableCol(9)
        sizer.AddGrowableCol(16)
        sizer.AddGrowableCol(8)
         
        generateBtn = wx.Button(self, label = "Generate", size=(90, 28)) 
        cancelBtn = wx.Button(self, wx.ID_CLOSE, label = "Cancel", size=(90, 28)) 

        sizer.Add(cancelBtn, pos = (10, 11), flag = wx.RIGHT|wx.BOTTOM, border = 50) 
        sizer.Add(generateBtn, pos = (10, 17), flag = wx.RIGHT|wx.LEFT|wx.BOTTOM, border = 5)

        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        generateBtn.Bind(wx.EVT_BUTTON, self.OnScreen)

        sizer.AddGrowableRow(6)
        self.SetSizerAndFit(sizer)
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