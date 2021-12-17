#!/usr/bin/env python

"""
This demo attempts to override the C++ MainLoop and implement it
in Python.
"""

import time
import wx
import os
from application import Form1
from monkey_tester import Monkey_Tester
from pathlib import Path


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
        i = 0

        while True:

            start = time.time()

            # time.sleep(1)

            #print("Current Mouse Position: " + str(wx.GetMousePosition()))

            frame_width, frame_height = self.frame.GetSize()
            click_position = self.monkey_tester.generate_click(
                frame_width, frame_height, 20)

            click_position_screen = self.frame.ClientToScreen(click_position)
            clicker.MouseMove(click_position_screen.x, click_position_screen.y)
            clicker.MouseClick()

            #print("Click Position Monkey Tester: " + str((click_position_x, click_position_y)))

            if wx.GetKeyState(wx.WXK_TAB):
                break

            self.mainLoop.Step()

            print((time.time() - start) * 1000)

            self.monkey_tester.reset_current_click_position()

            self.take_screenshot(i)
            i += 1

    def ExitMainLoop(self):
        self.mainLoop.Exit()

    def OnInit(self):
        self.monkey_tester = Monkey_Tester()

        self.frame = Form1(self.monkey_tester)
        self.frame.Show(True)

        self.SetTopWindow(self.frame)

        return True

    def take_screenshot(self, i):
        """ Takes a screenshot of the screen at give pos & size (rect). """
        rect = self.frame.GetRect()

        # Create a DC for the whole screen area
        screen = wx.ScreenDC()

        # Create a Bitmap that will hold the screenshot image later on
        # Note that the Bitmap must have a size big enough to hold the screenshot
        bmp = wx.Bitmap(rect.width, rect.height)

        # Create a memory DC that will be used for actually taking the screenshot
        mem = wx.MemoryDC()

        # Tell the memory DC to use our Bitmap
        # all drawing action on the memory DC will go to the Bitmap now
        mem.SelectObject(bmp)

        # Blit (in this case copy) the actual screen on the memory DC
        # and thus the Bitmap
        mem.Blit(0,  # Copy to this X coordinate
                 0,  # Copy to this Y coordinate
                 rect.width,  # Copy this width
                 rect.height,  # Copy this height
                 screen,  # From where do we copy?
                 rect.x,  # What's the X offset in the original DC?
                 rect.y  # What's the Y offset in the original DC?
                 )

        del mem  # Release bitmap

        # Path of current script
        script_directory = Path(__file__).parent.absolute()
        screenshot_directory = os.path.join(script_directory, 'Screenshots')
        filename = 'screenshot_' + str(i) + '.png'

        bmp.SaveFile(os.path.join(screenshot_directory,
                     filename), wx.BITMAP_TYPE_PNG)


app = MyApp(False)
app.MainLoop()
