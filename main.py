#!/usr/bin/env python

"""
This demo attempts to override the C++ MainLoop and implement it
in Python.
"""

import time
import wx
from random import randint
from application import Form1


class MyEventLoop(wx.GUIEventLoop):
    def __init__(self):
        wx.GUIEventLoop.__init__(self)
        self.exitCode = 0
        self.shouldExit = False

    def Step(self):
        # Set this loop as the active one. It will automatically reset to the
        # original evtloop when the context manager exits.
        with wx.EventLoopActivator(self):

            # Generate and process idles events for as long as there
            # isn't anything else to do
            while not self.shouldExit and not self.Pending() and self.ProcessIdle():
                pass

            # Dispatch all the pending events
            self.ProcessEvents()

            # Currently on wxOSX Pending always returns true, so the
            # ProcessIdle above is not ever called. Call it here instead.
            if 'wxOSX' in wx.PlatformInfo:
                self.ProcessIdle()

            # Process remaining queued messages, if any
            while True:
                checkAgain = False
                if wx.GetApp() and wx.GetApp().HasPendingEvents():
                    wx.GetApp().ProcessPendingEvents()
                    checkAgain = True
                if 'wxOSX' not in wx.PlatformInfo and self.Pending():
                    self.Dispatch()
                    checkAgain = True
                if not checkAgain:
                    break

        return self.exitCode

    def Exit(self, rc=0):
        self.exitCode = rc
        self.shouldExit = True
        self.OnExit()
        self.WakeUp()

    def ProcessEvents(self):
        if wx.GetApp():
            wx.GetApp().ProcessPendingEvents()

        if self.shouldExit:
            return False

        return self.Dispatch()


class MyApp(wx.App):

    def MainLoop(self):
        self.SetExitOnFrameDelete(True)
        self.mainLoop = MyEventLoop()

        clicker = wx.UIActionSimulator()

        while True:

            start = time.time()

            # time.sleep(1)

            #print("Current Mouse Position: " + str(wx.GetMousePosition()))

            frame_width, frame_height = self.frame.GetSize()

            click_position_x, click_position_y = self.frame.ClientToScreen(
                (randint(20, frame_width-20), randint(20, frame_height-50)))

            clicker.MouseMove(click_position_x, click_position_y)
            clicker.MouseClick()

            #print("Click Position Monkey Tester: " + str((click_position_x, click_position_y)))

            if wx.GetKeyState(wx.WXK_TAB):
                break

            self.mainLoop.Step()

            print((time.time() - start) * 1000)

    def ExitMainLoop(self):
        self.mainLoop.Exit()

    def OnInit(self):
        self.frame = Form1()
        self.frame.Show(True)
        # self.frame.Maximize(True)
        self.SetTopWindow(self.frame)

        #self.keepGoing = True
        return True


app = MyApp(False)
app.MainLoop()
