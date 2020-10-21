import wx
import wx.richtext
from wx.richtext import RichTextBuffer
from io import BytesIO
from io import StringIO
import xml.dom.minidom

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Richtext Test')
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour("white")
        
        self.rt = wx.richtext.RichTextCtrl(self, -1, value="")
        self.boldFlag = False
        self.italicFlag = False
        self.caps = False
        # self.rich.BeginFontSize(40)
        # for c, colour in rainbow_text:
        #     self.rich.BeginTextColour(colour)
        #     self.rich.WriteText(c)
        #     self.rich.EndTextColour()

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
            # font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, False)
            # style = self.rt.GetDefaultStyleEx()
            # style.SetFont(font)
            # (begin, end) = self.rt.GetSelectionRange()
            # print(begin, end)
            # self.rt.SetStyle(begin, end, style)
            # self.rt.SetFocus()
            # self.rt.SetInsertionPointEnd()
            # if self.boldFlag:
            #     self.rt.EndBold()
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
        # self.italicFlag = not self.italicFlag
        # self.SetFontStyle(fontItalic = self.italiclag)
    def on_save(self, event):
        out = BytesIO()
        handler = wx.richtext.RichTextXMLHandler()
        rt_buffer = self.rt.GetBuffer()
        handler.SaveFile(rt_buffer, out)
        self.xml_content = out.getvalue()
        print(self.xml_content)
        with open("output.xml", "w") as f:
            f.write(self.xml_content.decode('utf-8'))
        # parser = etree.XMLParser(recover=True)
        # xmlObject = etree.fromstring(str(self.xml_content), parser = parser)
        # e = xmlObject.xpath('//article[contains(text(), "stuff")]')
        # for article in e:
        #     print(etree.tostring(article, pretty_print=True))
        # pretty_xml_as_string = etree.tostring(xmlObject).decode()
        # print(pretty_xml_as_string)
    def onClick(self,evt):
        # initialize a string stream with XML data
        stream = StringIO( myXmlString )
        # create an XML handler
        handler = wx.richtext.RichTextXMLHandler()
        # load the stream into the control's buffer
        handler.LoadStream( self.GetBuffer(), stream )
        # refresh the control
        myRichTextCtrl.Refresh()

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
            _stringIO = StringIO(open('output.xml').read())
            _handler = wx.richtext.RichTextXMLHandler()
            _handler.LoadFile(self.rt.GetBuffer(), 'output.xml')
            self.rt.Refresh()
        except Exception as ex:
            print(ex)



# rainbow = ['red', 'coral', 'yellow', 'green', 'blue']
# text = """
#  Welcome to fabulous
#         Las Vegas"""
# # create a list of (char, colour) tuples
# rainbow_text = []
# ix = 0
# for c in text:
#     if c.isalpha():
#         colour = rainbow[ix]
#         if ix < len(rainbow)-1:
#             ix += 1
#         else:
#             ix = 0
#     else:
#         colour = 'white'
#     rainbow_text.append((c, colour))
# app = wx.App(0)
# title = 'Rainbow Text'
# MyFrame(None, title, rainbow_text).Show()
# app.MainLoop()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
