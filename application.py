import wx

# Set up a panel within a frame with a load of widgets
# Set up events on each of the widgets
# display the results in a scrolling text frame


class journey:
    def __init__(self):
        self.starts = ""
        self.ends = ""

    def setstart(self, place):
        self.starts = place

    def setend(self, place):
        self.ends = place

    def __str__(self):
        return "from "+self.starts + " to "+self.ends


class Form1(wx.Frame):
    def __init__(self):
        wx.Panel.__init__(
            self, None, title="My Journey Planner", size=(550, 425))

        # Set up some basic element. Placement is a bit crude as this
        # is really an event handling demo! It would also be a good idea
        # to define constants for the IDs!

        self.quote = wx.StaticText(self, -1, "My Journey :",
                                   wx.Point(20, 30))
        self.logger = wx.TextCtrl(self, 5, "",
                                  wx.Point(330, 20), wx.Size(200, 300),
                                  wx.TE_MULTILINE | wx.TE_READONLY)
        self.button = wx.Button(self, 10, "Submit", wx.Point(200, 325))
        self.leaver = wx.Button(self, 11, "Quit", wx.Point(200, 355))

        self.lblhear = wx.StaticText(self, -1, "From", wx.Point(10, 90))
        self.lblhear2 = wx.StaticText(self, -1, "To", wx.Point(150, 90))

        self.sampleList = ['Manchester', 'Dublin', 'Melksham', 'Bristol']
        self.edithear = wx.ComboBox(self, 30, "",
                                    wx.Point(40, 90), wx.Size(95, -1),
                                    self.sampleList, wx.CB_DROPDOWN)
        self.sampleList2 = ['London', 'New York', 'Salisbury', 'Bath']
        self.edithear2 = wx.ComboBox(self, 31, "",
                                     wx.Point(180, 90), wx.Size(95, -1),
                                     self.sampleList2, wx.CB_DROPDOWN)

        # Add event handlers as appropriate

        wx.EVT_BUTTON(self, 10, self.OnClick)
        wx.EVT_BUTTON(self, 11, self.OnClick)

        for box in range(30, 32, 1):
            wx.EVT_COMBOBOX(self, box, self.EvtComboBox)
            wx.EVT_TEXT(self, box, self.EvtText)

        # Absolute placement as we've done above is NOT a good idea, but it
        # does mean that this demo lets you see the events more easily.

        self.going = journey()

    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())

    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
        if event.GetId() == 30:
            self.going.setstart(event.GetString())
        else:
            self.going.setend(event.GetString())

    def OnClick(self, event):
        self.logger.AppendText(" Click on object with Id %d\n" %
                               event.GetId())
        print(self.going)

    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())

    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
