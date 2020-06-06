import wx
# import wx.richtext as rt
# import images
# http://www.ccp4.ac.uk/dist/checkout/wxPython-src-3.0.2.0/wxPython/demo/RichTextCtrl.py
# https://stackoverflow.com/questions/40257359/how-to-dynamically-update-multiple-wxpython-static-text

def GetRoundBitmap( w, h, r ):
    maskColor = wx.Colour(0,0,0)
    shownColor = wx.Colour(5,5,5)
    b = wx.EmptyBitmap(w,h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColor))
    dc.DrawRectangle(0,0,w,h)
    dc.SetBrush(wx.Brush(shownColor))
    dc.SetPen(wx.Pen(shownColor))
    dc.DrawRoundedRectangle(0,0,w,h,r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColor)
    return b

def GetRoundShape( w, h, r ):
    return wx.Region( GetRoundBitmap(w,h,r) )

class PanelOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        wx.StaticText(self, label = "'^⌘G - Select All    (Ctrl-Cmd-G)        ^⌘G - Select All    (Ctrl-Cmd-G)\n^⌘G - Select All    (Ctrl-Cmd-G)        ^⌘G - Select All    (Ctrl-Cmd-G)")
        self.SetTransparent( 220 )

    def OnKeyDown(self, event):
        self.Destroy()

class FancyFrame(wx.Frame):
    def __init__(self):
        sizer = wx.GridBagSizer()
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED  )
        wx.Frame.__init__(self, None, title='Fancy', style = style)

        # self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.TE_READONLY|wx.HSCROLL|wx.NO_BORDER);
        # self.rtc.Disable()
        boldstatic = wx.Font(pointSize = 24, family = wx.DEFAULT,
               style = wx.BOLD, weight = wx.BOLD,
               faceName = 'Consolas')
        normalstatic = wx.Font(pointSize = 10, family = wx.DEFAULT,
               style = wx.NORMAL, weight = wx.NORMAL,
               faceName = 'Consolas')
        # font = wx.Font(pointSize = 18, family = wx.DEFAULT,
        #        style = wx.NORMAL, weight = wx.NORMAL,
        #        faceName = 'Consolas')
        self.SetFont(boldstatic)
        self.SetBackgroundColour((211,211,211))
        self.label = wx.StaticText(self, label = "^⌘G", pos = (100,50))
        self.SetFont(normalstatic)
        self.label2 = wx.StaticText(self, label = " - Select All    (Ctrl-Cmd-G)", pos = (200,50))
        # sizer.Add(self.label, (4, 0), (1, 5), wx.EXPAND)
        # sizer.Add(self.label2, (5, 0), (1, 5), wx.EXPAND)
        # wx.StaticText(self, label = "^⌘G - Select All    (Ctrl-Cmd-G)  ||  ^⌘G - Select All    (Ctrl-Cmd-G)\n^⌘G - Select All    (Ctrl-Cmd-G)        ^⌘G - Select All    (Ctrl-Cmd-G)")
        # self.rtc.Bind(wx.EVT_SET_FOCUS,self.OnInput)
        # self.rtc.Bind(wx.EVT_KILL_FOCUS,self.OnInput)
        # self.rtc.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        # self.rtc.BeginFontSize(14)
        # self.rtc.BeginBold()
        # self.rtc.WriteText("^⌘G")
        # self.rtc.EndBold()
        # self.rtc.BeginFontSize(10)
        # self.rtc.WriteText(" - Select All    (Ctrl-Cmd-G)\n")
        # self.rtc.BeginFontSize(14)
        # self.rtc.WriteText("Different font sizes on the same line is allowed, too.")
        # self.rtc.EndFontSize()

        # self.rtc.WriteText(" Next we'll show an indented paragraph.")

        # self.rtc.BeginLeftIndent(60)
        # self.rtc.Newline()

        # self.rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. An attractive woman came into the cafe, which is nothing remarkable.")
        # self.rtc.EndLeftIndent()
        # self.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD))
        # font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        # wx.text.SetFont(font)
        # self.panelOne = PanelOne(self)
        # self.SetFocus()
        w, h = wx.GetDisplaySize()
        self.SetSize((w/2, h/2))
        self.SetPosition( ((w-w/2)/2,(h-h/2)/2) )
        self.SetTransparent( 220 )

        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.Bind(wx.EVT_MOTION, self.OnMouse)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.SetSizer(sizer)
        self.Show(True)

    
    def OnInput(self, e):
        self.Destroy()
        # e.Skip()

    def SetRoundShape(self, event=None):
        w, h = self.GetSizeTuple()
        self.SetShape(GetRoundShape( w,h, 10 ) )

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc = wx.GCDC(dc)
        w, h = self.GetSizeTuple()
        r = 10
        dc.SetPen( wx.Pen("#D3D3D3dth = 2"))
        dc.SetBrush( wx.Brush("#D3D3D3"))
        dc.DrawRoundedRectangle( 0,0,w,h,r )

    def OnKeyDown(self, event):
        # self.Close(force=True)
        self.Destroy()

    def OnMouse(self, event):
        """implement dragging"""
        if not event.Dragging():
            self._dragPos = None
            return
        self.CaptureMouse()
        if not self._dragPos:
            self._dragPos = event.GetPosition()
        else:
            pos = event.GetPosition()
            displacement = self._dragPos - pos
            self.SetPosition( self.GetPosition() - displacement )

app = wx.App()
f = FancyFrame()
app.MainLoop()