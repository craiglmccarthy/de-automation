#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DE-Automation -
Automates data entry into a background check database.
An API would make more sense, but it wouldn't be as fun.
Uses a mix of pyautogui.locateOnScreen functions and relative positioning.
Based on a 1920 x 1200 screen resolution with database running in Chrome.
"""

import datetime
import re
import sys
import time

import pyautogui
import pyperclip

from de_demonyms import demonyms
from de_pyautogui import check, click_here
from de_regex import re_dict, re_match, re_match_dob

# Speed of pyautogui.
pyautogui.PAUSE = 0.25

# Copy user submitted form from a CRM system via pyperclip.
user_form = pyperclip.paste()

# Determine the entry type.
name_screen = re_match(user_form, re_dict['name_screen'])
if name_screen == 'Person':
    entry_type = 'Person'
    first_name = re_match(user_form, re_dict['first_name'])
    middle_name = re_match(user_form, re_dict['middle_name'])
    surname = re_match(user_form, re_dict['surname'])
    dob = re_match_dob(user_form, re_dict['dob'])

    # Unpack the dob tuple.
    try:
        day, month, year = dob
        if day.isdecimal():
            day = int(day)
    except:
        day, month, year = ('', '', '',)

    # Converts date entries.
    if month.isdecimal():
        month = int(month)
    elif month.lower() in 'january':
        month = 1
    elif month.lower() in 'february':
        month = 2
    elif month.lower() in 'march':
        month = 3
    elif month.lower() in 'april':
        month = 4
    elif month.lower() in 'may':
        month = 5
    elif month.lower() in 'june':
        month = 6
    elif month.lower() in 'july':
        month = 7
    elif month.lower() in 'august':
        month = 8
    elif month.lower() in 'september':
        month = 9
    elif month.lower() in 'october':
        month = 10
    elif month.lower() in 'november':
        month = 11
    elif month.lower() in 'december':
        month = 12

    # Converts yy into yyyy, uses the following to 'guess' the century.
    if year.isdecimal():
        if len(year) == 2:
            if int(year) > int(datetime.datetime.now().strftime('%y')):
                year = int('19' + year)
            else:
                year = int('20' + year)
    citizenship = re_match(user_form, re_dict['citizenship'])

    # Checks against synonym dictionary.
    if citizenship.lower() in demonyms:
        citizenship = demonyms[citizenship.lower()]

elif name_screen == 'Entity':
    entry_type = 'Entity'
    entity_name = re_match(user_form, re_dict['entity_name'])
    entity_aff = re_match(user_form, re_dict['entity_aff'])

    # Checks against synonym dictionary.
    if entity_aff.lower() in demonyms:
        entity_aff = demonyms[entity_aff.lower()]
else:
    pyautogui.alert(text="Unknown data - try copying it again.",
                    title='DE-Automation', button='OK', root=None,
                    timeout=None)
    sys.exit()

# Assign search type.
search_type = re_match(user_form, re_dict['search_type'])

# =============================================================================
# Start pyautogui actions.
ans = pyautogui.confirm(text="I need to see the 'Clear' button to begin.\
\n\nAre you ready?", title='DE-Automation', buttons=['Yes', 'No'])
if ans == 'No':
    sys.exit()

# Click clear button and reset the screen.
clear = pyautogui.locateOnScreen('1920_1200/clear.png', grayscale=True)
check(clear)
pyautogui.click(clear)
time.sleep(1)

# Get screen window right coordinate.
screen_window_right, _, _, _ = clear

# Attempts to locates two Search by Name Type and assigns variable to the first
# to load. Added count to quit program after 20 loops.
w_b = False
count = 0
while w_b is False:
    if pyautogui.locateOnScreen('1920_1200/search_by_name_type_b.png',
                                grayscale=True) != None:
        loc_sbnt = pyautogui.locateOnScreen(
            '1920_1200/search_by_name_type_b.png', grayscale=True)
        w_b = True
    elif pyautogui.locateOnScreen('1920_1200/search_by_name_type_w.png',
                                  grayscale=True) != None:
        loc_sbnt = pyautogui.locateOnScreen(
            '1920_1200/search_by_name_type_w.png', grayscale=True)
        w_b = True
    elif count == 20:
        sys.exit()
    else:
        count += 1

# Click on Search by Name Type button.
pyautogui.click(pyautogui.center(loc_sbnt))

# Get screen window left and top coordinates.
screen_window_left_unadjusted, screen_window_top, _, _ = loc_sbnt

# Adjust screen window left coordinate.
screen_window_left = screen_window_left_unadjusted - 300
if screen_window_left < 0:
    screen_window_left = 0

# Create windown search region.
window_region = [screen_window_left, screen_window_top,
                 screen_window_right - screen_window_left,
                 1200 - screen_window_top]

# Locate First Name / Entity text field.
loc_first = pyautogui.locateOnScreen(
    '1920_1200/first_name.png', grayscale=True, region=(window_region))
check(loc_first)
x_fir_name, y_fir_name = pyautogui.center(loc_first)

# Determine pyautogui actions by entry type.
# Person entry type.
if entry_type == 'Person':
    pyautogui.click(x_fir_name, y_fir_name)  # First Name text field
    pyautogui.typewrite(first_name)
    if len(middle_name) > 0:  # Middle Name text field
        pyautogui.press('tab')
        pyautogui.typewrite(middle_name)
        pyautogui.press('tab')
    else:
        pyautogui.press('tab')
        pyautogui.press('tab')

    pyautogui.typewrite(surname)  # Surname text field
    if search_type == 'Precise':
        click_here('1920_1200/precise.png', window_region)  # Precise
    else:
        click_here('1920_1200/near.png', window_region)  # Near

    # Date of birth.
    if day != None:
        pyautogui.click(x_fir_name, y_fir_name + 125)  # Day
        pyautogui.typewrite(str(day))
    if month != None:
        pyautogui.click(x_fir_name + 120, y_fir_name + 125)  # Month
        if month == 1:
            pyautogui.click(x_fir_name + 120, y_fir_name + 185)  # Jan
        elif month == 2:
            pyautogui.click(x_fir_name + 120, y_fir_name + 217)  # Feb
        elif month == 3:
            pyautogui.click(x_fir_name + 120, y_fir_name + 249)  # Mar
        elif month == 4:
            pyautogui.click(x_fir_name + 120, y_fir_name + 282)  # Apr
        elif month == 5:
            pyautogui.click(x_fir_name + 120, y_fir_name + 312)  # May
        elif month == 6:
            pyautogui.click(x_fir_name + 120, y_fir_name + 345)  # Jun
        elif month == 7:
            pyautogui.click(x_fir_name + 120, y_fir_name + 377)  # Jul
        elif month == 8:
            pyautogui.click(x_fir_name + 120, y_fir_name + 410)  # Aug
        elif month == 9:
            pyautogui.click(x_fir_name + 120, y_fir_name + 440)  # Sept
        elif month == 10:
            pyautogui.click(x_fir_name + 120, y_fir_name + 472)  # Oct
        elif month == 11:
            pyautogui.click(x_fir_name + 120, y_fir_name + 505)  # Nov
        elif month == 12:
            pyautogui.click(x_fir_name + 120, y_fir_name + 535)  # Dec
        if year != None:
            pyautogui.click(x_fir_name + 240, y_fir_name + 125)  # Year
            pyautogui.typewrite(str(year))

    if dob != None:
        if dob != ('Day', 'Month', 'Year'):
            pyautogui.click(x_fir_name + 384, y_fir_name + 127)  # Strict

    if citizenship != '':  # Citizenship
        click_here('1920_1200/region.png', window_region)
        time.sleep(0.25)

        # Find a region
        click_here('1920_1200/find_a_region.png', window_region)
        pyautogui.typewrite(citizenship)
        pyautogui.press('enter')
        pyautogui.press('enter')
        click_here('1920_1200/region.png', window_region)

    # Copy to clipboard
    current_date = datetime.datetime.now().strftime('%d%m%y')
    pyperclip.copy(current_date + '_' + surname + first_name[0])

# Entity entry type.
else:
    pyautogui.click(x_fir_name + 75, y_fir_name - 45)  # Entity tab
    pyautogui.click(x_fir_name, y_fir_name)  # First Name text field
    pyautogui.typewrite(entity_name)
    if search_type == 'Precise':
        click_here('1920_1200/precise.png',
                   window_region)  # Precise
    else:
        click_here('1920_1200/near.png', window_region)  # Near

    if entity_aff != '':  # Entity affiliation
        click_here('1920_1200/region.png', window_region)
        time.sleep(0.25)

        # Find a region
        click_here('1920_1200/find_a_region.png', window_region)
        pyautogui.typewrite(entity_aff)
        pyautogui.press('enter')
        pyautogui.press('enter')
        click_here('1920_1200/region.png', window_region)

    # Copy to clipboard
    current_date = datetime.datetime.now().strftime('%d%m%y')
    pyperclip.copy(current_date + '_' + entity_name)
