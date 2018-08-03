#!/usr/bin/env python

import subprocess
import os
import gps_satellite as gps

class Interactive_Register():

    def menu(self):
        print('Welcome to Registration Assistant')
        print('Where would you like to register?')
        dest = raw_input('1. Customer Portal\n' +
                         '2. Satellite\n' + 
                         '3. Exit\n')
        if str(dest) == '1':
            print('Registering to the Customer Portal...')
            self.register()
            self.get_subscriptions()
        elif str(dest) == '2':
            print('Registering to a Satellite...')
            self.get_latest_ca_consumer_rpm()
            self.register()
        elif str(dest) == '3':
            exit
        else:
            print('Invalid option')
            exit

    def register(self):
        command = 'sudo subscription-manager register'
        reg = subprocess.Popen(command, shell=True)
        reg.wait()

    def get_latest_ca_consumer_rpm(self):
        get_fqdn = raw_input('What is the fully qaulified domain name of your Satellite server?\n' +
                             'Example: satellite.example.redhat.com ')
        command = 'rpm -Uvh http://' + get_fqdn + '/pub/katello-ca-consumer-latest.noarch.rpm'
        reg = subprocess.Popen(command, shell=True)
        reg.wait()
    
    def get_Sat_Org(self):
        

    def get_subscriptions(self):
        command = ['subscription-manager', 'list', '--available']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        subscriptions = output.stdout.read()
        sub1 = subscriptions.strip()
        #print(sub1)
        sub2 = sub1.split('\n')
        print(sub2)
        
def main():
    register = Interactive_Register()
    register.menu()



if __name__ == '__main__':
    main()