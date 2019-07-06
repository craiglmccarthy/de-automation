#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pyautogui


def check(match):
    """Exits program if no match is found."""
    if match == None:
        pyautogui.alert(text="Unknown data - try copying it again.",
                        title='DE-Automation', button='OK', root=None,
                        timeout=None)
        sys.exit()


def click_here(png_image, window_region):
    """
    Locate png image on screen and click it in center if available, 
    otherwise exit program with alert message. Uses grayscale=True to increase
    speed.
    """
    loc = pyautogui.locateOnScreen(
        png_image, grayscale=True, region=(window_region))
    if loc:
        loc_cent = pyautogui.center(loc)
        pyautogui.click(loc_cent)
    else:
        pyautogui.alert(text="Could not locate action to perform.",
                        title='DE-Automation', button='OK', root=None,
                        timeout=None)
        sys.exit()
    return loc
