#!/usr/bin/env python

import gps_satellite as gps
import satellite_monitor as monitor

class Menu(object):
    print('Welcome to GPS Satellite. What would you like to do today?')
    option=raw_input('1. Gather Satellite Facts\n' +
                     '2. Monitor Satellite Performance\n' +
                     '3. Exit\n')
    if option == '1':
        gps.main()
    elif option == '2':
        print('How would you like run Satellite Monitor?')
        option=raw_input('1. One Shot\n' +
                         '2. On a interval\n')
        if option == '1':
            monitor.main()
        elif option == '2':
            interval = raw_input('Please set your interval in seconds: ')
            monitor.main(['-i', str(interval), '-r'])
        else:
            print('Not a valid option!')
            exit
    elif option == '3':
        exit
    else:
        print('Option not valid, goodbye')
        exit