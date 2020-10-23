import wx
import wx.richtext
from wx.richtext import RichTextBuffer
from io import BytesIO
from io import StringIO
from xml.dom import minidom
import xml.etree.ElementTree as ET

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Richtext Test')
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour("white")
        
        self.rt = wx.richtext.RichTextCtrl(self, -1, value="")
        self.boldFlag = False   
        self.italicFlag = False
        self.caps = False

        save_button = wx.Button(self, label="Save")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)

        sizer.Add(self.rt, 1, wx.EXPAND|wx.ALL, 6)
        sizer.Add(save_button, 0, wx.EXPAND|wx.ALL, 6)
        self.Bold = wx.Button(self, label="Bold")
        self.Italic = wx.Button(self, label="Italic")

        sizer.Add(self.Bold, 0, wx.EXPAND|wx.ALL, 6)
        sizer.Add(self.Italic, 0, wx.EXPAND|wx.ALL, 6)

        self.Bold.Bind(wx.EVT_BUTTON, self.on_Bold)
        self.Italic.Bind(wx.EVT_BUTTON, self.on_italic)

        self.loadText()

        self.SetSizer(sizer)
        self.Show()

    def on_Bold(self,evt):
        _selection = self.rt.GetStringSelection()
        if _selection:
            if self.rt.IsSelectionBold():
                self.boldFlag = False
                self.Bold.SetBackgroundColour(wx.Colour(240, 240, 240))
            elif not self.rt.IsSelectionBold():
                self.boldFlag = True
                self.Bold.SetBackgroundColour((255, 230, 200, 255))
            self.rt.ApplyBoldToSelection()
            self.rt.SetFocus()
            pos = self.rt.GetSelectionRange()[1]
            print(pos)
            self.rt.SetInsertionPoint(pos)
            return

        if not self.boldFlag:
            # self.Bold.SetFocus()
            self.Bold.SetBackgroundColour((255, 230, 200, 255))
            self.rt.SetFocus()
            pos1 = self.rt.GetCaretPosition()
            self.rt.SetInsertionPoint(pos1)
            self.rt.BeginBold()
            self.boldFlag = True
            self.caps = True
        elif self.boldFlag:
            self.Bold.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.rt.SetFocus()
            pos1 = self.rt.GetCaretPosition()
            self.rt.SetInsertionPoint(pos1)
            if self.caps:
                self.rt.EndBold()
            else:
                self.rt.SetFont(wx.Font(10, family = wx.DEFAULT, style = wx.NORMAL, weight = wx.NORMAL))
            self.boldFlag = False
            self.caps = False

    def on_italic(self, evt):
        self.rt.ApplyItalicToSelection()
        if not self.italicFlag:
            self.Italic.SetBackgroundColour((255, 230, 200, 255))
            self.rt.SetFocus()
            pos1 = self.rt.GetCaretPosition()
            self.rt.SetInsertionPointEnd(pos1)
            self.rt.BeginItalic()
            self.italicFlag = True
        elif self.italicFlag:
            self.Italic.SetBackgroundColour(wx.Colour(240, 240, 240))
            self.rt.SetFocus()
            pos1 = self.rt.GetCaretPosition()
            self.rt.SetInsertionPointEnd(pos1)
            self.rt.EndItalic()
            self.italicFlag = False

    def on_save(self, event):
        out = BytesIO()
        handler = wx.richtext.RichTextXMLHandler()
        rt_buffer = self.rt.GetBuffer()
        handler.SaveFile(rt_buffer, out)
        self.xml_content = out.getvalue()
        print(self.xml_content)
        with open("output.xml", "w") as f:
            f.write(self.xml_content.decode('utf-8'))


    def loadTextStream(self):
        '''
        '''
        try:
            _file = open('output.xml', 'r')
            _rtf = _file.read()
            _file.close()
            print(_rtf)
            self.rt.Freeze()
            _handler = wx.richtext.RichTextXMLHandler()
            _handler.SetFlags(wx.richtext.RICHTEXT_HANDLER_INCLUDE_STYLESHEET)
            rt_buffer = self.rt.GetBuffer()
            output = StringIO(_rtf)
            _handler.LoadStream(rt_buffer,  output)
            self.rt.refresh()
            self.rt.Thaw()
            #self.rt.LoadFile('output.xml',  wx.richtext.RICHTEXT_TYPE_XML)
        except Exception as ex:
            print(ex)
    
    def loadText(self):
        '''
        '''
        try:
            _bytesIO = BytesIO(open('output.xml', 'rb').read())
            _handler = wx.richtext.RichTextXMLHandler()
            _handler.LoadFile(self.rt.GetBuffer(), _bytesIO)
            #_handler.LoadFile(self.rt.GetBuffer(), 'output.xml')
            self.rt.Refresh()
            # self.loadXML()
        except Exception as ex:
            print(ex)

    def loadXML(self):
        try:
            _xml = ET.parse('output.xml')
            _root =  _xml.getroot()
            print(_root)
            print(_root[0][0].attribute)
        except Exception as ex:
            print(ex)

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
