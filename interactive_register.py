#!/usr/bin/env python

import subprocess
import os

class Interactive_Register():

    def menu(self):
        print('Welcome to Registration Assistant')
        print('Where would you like to register?')
        dest = raw_input('1. Customer Portal' +
                         '2. Satellite' + 
                         '3. Exit')
        if str(dest) == '1':
            print('Registering to the Customer Portal...')
        elif str(dest) == '2':
            print('Registering to a Satellite...')
        elif str(dest) == '3':
            exit
        else:
            print('Invalid option')
            exit

    def register(self):
        command = ['subscription-manager', 'register']
        output = subprocess.Popen(command, shell=True)
        output.wait()

    def get_subscriptions(self):
        command = ['subscription-manager', 'list', '--available']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        subscriptions = output.stdout.read()
        

if __name__ == '__main__':
    main()