#!/usr/bin/env python

"""
This demo attempts to override the C++ MainLoop and implement it
in Python.
"""

import time
import wx
import os
import pyautogui
from application import Form1
from monkey_tester import Monkey_Tester
from pathlib import Path
from PIL import ImageDraw


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

            self.take_screenshot(i, click_position)

            click_position_screen = self.frame.ClientToScreen(click_position)
            clicker.MouseMove(click_position_screen.x, click_position_screen.y)
            clicker.MouseClick()

            #print("Click Position Monkey Tester: " + str((click_position_x, click_position_y)))

            if wx.GetKeyState(wx.WXK_TAB):
                break

            self.mainLoop.Step()

            print((time.time() - start) * 1000)

            self.monkey_tester.reset_current_click_position()

            i += 1

    def ExitMainLoop(self):
        self.mainLoop.Exit()

    def OnInit(self):
        self.monkey_tester = Monkey_Tester()

        self.SetAppName("Demo App")

        self.frame = Form1(self.monkey_tester)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)

        return True

    def take_screenshot(self, i, click_position):
        """ Takes a screenshot of the screen at give pos & size (rect). """
        rect = self.frame.GetRect()

        # Take screenshot of the applicatin with pyautogui (taking screenshots with wxPython does not work in xvfb for some reason)
        screenshot = pyautogui.screenshot(region=rect.Get())

        # Add click position as a point to the screenshot
        draw = ImageDraw.Draw(screenshot)
        x, y = click_position
        r = 3
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 0, 0, 255))

        # Path of current script
        script_directory = Path(__file__).parent.absolute()
        screenshot_directory = os.path.join(script_directory, 'Screenshots')
        filename = 'screenshot_' + str(i) + '.png'

        # Save screenshot
        screenshot.save(os.path.join(screenshot_directory, filename))


def main():
    app = MyApp(False)
    app.MainLoop()


if __name__ == "__main__":
    main()
