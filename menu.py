#!/usr/bin/env python

import gps_satellite as gps
import satellite_monitor as monitor

class Menu(object):
    print('Welcome to GPS Satellite. What would you like to do today?')
    option=raw_input('1. Gather Satellite Facts\n\
                      2. Gather System Facts\n\
                      3. Exit')
    if option == '1':
        gps.main()
    elif option == '2':
        monitor.main()
    elif option == '3':
        exit
    else:
        print('Option not valid, goodbye')
        exit