import wx
import wx.richtext
from io import BytesIO
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lxml import etree

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

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rt, 1, wx.EXPAND|wx.ALL, 6)
        sizer.Add(save_button, 0, wx.EXPAND|wx.ALL, 6)
        self.Bold = wx.Button(self, label="Bold")
        Italic = wx.Button(self, label="Italic")

        sizer.Add(self.Bold, 0, wx.EXPAND|wx.ALL, 6)
        sizer.Add(Italic, 0, wx.EXPAND|wx.ALL, 6)

        self.Bold.Bind(wx.EVT_BUTTON, self.on_Bold)
        Italic.Bind(wx.EVT_BUTTON, self.on_italic)

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
            print('f', self.boldFlag)
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
            self.rt.SetFocus()
            self.rt.SetInsertionPointEnd()
            self.rt.BeginItalic()
            self.italicFlag = True
        elif self.italicFlag:
            self.rt.SetFocus()
            self.rt.SetInsertionPointEnd()
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
        with open("output.xml", "a") as f:
            f.write(str(self.xml_content))
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
        handler.LoadStream( myRichTextCtrl.GetBuffer(), stream )
        # refresh the control
        myRichTextCtrl.Refresh()

class MyFrame(wx.Frame):
    def __init__(self): 


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
