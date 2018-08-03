#!/usr/bin/env python

from __future__ import print_function
import sys
import yum
import datetime
import subprocess
import os
import re
import shutil
import tarfile
from distutils.dir_util import copy_tree
import argparse
import time
import pdb



DATE = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
FULL_PATH = '/tmp/gps/satellite-monitor-' + DATE + '/'
DIR = '/tmp/'
FILE_NAME = 'satellite-monitor' + DATE + '.tar.gz'
SAR = '/var/log/sa/'

class Satellite_Monitor():

    def __init__(self):
        if not os.path.exists(FULL_PATH):
            os.makedirs(FULL_PATH)
            os.chdir(FULL_PATH)

    
    def verify_pulpadmin_install(self):
        """Check if pulp-admin has been installed"""
        yumbase = yum.YumBase()
        if yumbase.rpmdb.searchNevra(name='pulp-admin-client'):
            print("pulp-admin installed!")
        else:
            print('pulp-admin not installed')
            print('Please install pulp-admin using this KCS:\n\
                    https://access.redhat.com/solutions/1295653')
            exit

    def get_PulpAdmin_Password(self):
        """Store the pulp password"""
        with open('/etc/pulp/server.conf', 'r') as pulpconfigfile:
            pulpconfiglines = pulpconfigfile.readlines()
        # Fetch only the line that starts with 'default_password:'
        ## This single line with a list comprehension is equivalent to:
        ## for l in pulpconfiglines:
        ##     if l.startswith('default_pass'):
        ##         passwordline = l.strip()
        passwordline = [ l.strip() for l in pulpconfiglines if l.startswith('default_password:') ]
        # List comprehensions return LISTS.
        # So passwordline is now a one-item LIST like this:
        #    ['default_password: SOmetHiNgCrAaAazY']
        # We want the string not the list
        passwordline = passwordline[0]
        # Split the string and get the second item
        pulp_pw = passwordline.split()[1]
        self.pulp_pw = pulp_pw

    def get_Pulp_Tasks(self):
        """Gather all Pulp Tasks"""
        print('Gather all Pulp Tasks')
        command = ['pulp-admin', '-u', 'admin', '-p', self.pulp_pw,
                     'tasks', 'list']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        pulptasks = output.stdout.read()
        self.write_to_file('pulp_tasks', pulptasks)

    def get_Pulp_Status(self):
        """Gather Pulp status"""
        print('Gather Pulp status')
        command = ['pulp-admin', '-u', 'admin', '-p', self.pulp_pw, 'status']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        pulpstatus = output.stdout.read()
        self.write_to_file('pulp_status', pulpstatus)

    def get_Celery_Active_Tasks(self):
        """Gather all active celery tasks"""
        print('Gather all active celery tasks')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'active']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        ctasks = output.stdout.read()
        self.write_to_file('celery_tasks_active', ctasks)

    def get_Celery_Scheduled_Tasks(self):
        """Gather all scheduled celery tasks"""
        print('Gather all scheduled celery tasks')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'scheduled']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cschtasks = output.stdout.read()
        self.write_to_file('celery_tasks_scheduled', cschtasks)

    def get_Celery_Reserved_Tasks(self):
        """Gather all reserved celery tasks"""
        print('Gather all reserved celery tasks')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'reserved']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        crsvptasks = output.stdout.read()
        self.write_to_file('celery_tasks_reserved', crsvptasks)

    def get_Celery_Revoked_Tasks(self):
        """Gather all revoked celery tasks"""
        print('Gather all revoked celery tasks')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'revoked']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        crevoketasks = output.stdout.read()
        self.write_to_file('celery_tasks_revoked', crevoketasks)

    def get_Celery_Registered_Tasks(self):
        """Gather all registered celery tasks"""
        print('Gather all registered celery tasks')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'registered']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cregtasks = output.stdout.read()
        self.write_to_file('celery_tasks_registered', cregtasks)

    def get_Celery_Stats(self):
        """Gather celery stats"""
        print('Gather celery stats')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'stats']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cstats = output.stdout.read()
        self.write_to_file('celery_stats', cstats)

    def get_Celery_Active_Queues(self):
        """Gather celery active queues"""
        print('Gather celery active queues')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'active_queues']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cactiveques = output.stdout.read()
        self.write_to_file('celery_active_queues', cactiveques)

    def get_Celery_Clock(self):
        """Gather celery clocks"""
        print('Gather celery clocks')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'clock']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cclocks = output.stdout.read()
        self.write_to_file('celery_clock', cclocks)
    
    def get_Celery_Conf(self):
        """Gather celery configs"""
        print('Gather celery configs')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'conf']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cconf = output.stdout.read()
        self.write_to_file('celery_conf', cconf)

    def get_Celery_Memory_Dump(self):
        """Gather celery memory dump"""
        print('Gather celery memory dump')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'memdump']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cmemdump = output.stdout.read()
        self.write_to_file('celery_memory_dump', cmemdump)

    def get_Celery_Memory_Sample(self):
        """Gather celery memory sample"""
        print('Gather celery memory sample')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'memsample']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cmemsamp = output.stdout.read()
        self.write_to_file('celery_memory_sample', cmemsamp)

    def get_Celery_Obj_Graph(self):
        """Gather celery object graph"""
        print('Gather celery object graph')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'objgraph']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cobjgraph = output.stdout.read()
        self.write_to_file('celery_objgraph', cobjgraph)

    def get_Celery_Ping(self):
        """Gather celery ping"""
        print('Gather celery ping')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 'ping']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cping = output.stdout.read()
        self.write_to_file('celery_ping', cping)

    def get_Celery_Report(self):
        """Gather celery bugreport"""
        print('Gather celery bugreport')
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'report']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cbug = output.stdout.read()
        self.write_to_file('celery_bugreport', cbug)

    def get_Qpid_General(self):
        """Gather Qpid General"""
        print('Gather Qpid General')
        command = ['qpid-stat', '-g', '--ssl-certificate=/etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidgen = output.stdout.read()
        self.write_to_file('qpid_general', qpidgen)

    def get_Qpid_Connections(self):
        """Gather Qpid Connections"""
        print('Gather Qpid Connections')
        command = ['qpid-stat', '-c', '--ssl-certificate=/etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidconn = output.stdout.read()
        self.write_to_file('qpid_connections', qpidconn)

    def get_Qpid_Exchanges(self):
        """Gather Qpid Exchanges"""
        print('Gather Qpid Exchanges')
        command = ['qpid-stat', '-e', '--ssl-certificate=/etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidexch = output.stdout.read()
        self.write_to_file('qpid_exchanges', qpidexch)

    def get_Qpid_Queues(self):
        """Gather Qpid Queues"""
        print('Gather Qpid Queues')
        command = ['qpid-stat', '-q', '--ssl-certificate=/etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidque = output.stdout.read()
        self.write_to_file('qpid_queue', qpidque)

    def get_Qpid_Subscriptions(self):
        """Gather Qpid Subscriptions"""
        print('Gather Qpid Subscriptions')
        command = ['qpid-stat', '-u', '--ssl-certificate=/etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidsub = output.stdout.read()
        self.write_to_file('qpid_subscriptions', qpidsub)

    def get_Qpid_Memory(self):
        """Gather Qpid Memory"""
        print('Gather Qpid Memory')
        command = ['qpid-stat', '-m', '--ssl-certificate=' +
                   '/etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidmem = output.stdout.read()
        self.write_to_file('qpid_memory', qpidmem)

    def get_Mongo_Tasks(self):
        """Gather Mongodb Tasks"""
        print('Gather Mongodb Tasks')
        command = ['mongoexport', '--db', 'pulp_database', '--collection',
                    'task_status']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        mongotasks = output.stdout.read()
        self.write_to_file('mongo_tasks', mongotasks)

    def get_Mongo_RSVP_Resource(self):
        """Gather Mongodb Reserved Resources"""
        print('Gather Mongodb Reserved Resources')
        command = ['mongoexport', '--db', 'pulp_database', '--collection',
                    'reserved_resources']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        mongoresources = output.stdout.read()
        self.write_to_file('mongo_resources', mongoresources)

    def get_Mongo_Workers(self):
        """Gather Mongodb Workers"""
        print('Gather Mongodb Workers')
        command = ['mongoexport', '--db', 'pulp_database', '--collection',
                    'workers']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        mongoworkers = output.stdout.read()
        self.write_to_file('mongo_workers', mongoworkers)

    def get_Passenger_Status(self):
        """Gather Passenger Statistics"""
        print('Gather Passenger Status')
        command = ['passenger-status']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        passengerstats = output.stdout.read()
        self.write_to_file('passenger-status', passengerstats)

    def get_Passenger_Memory(self):
        """Gather Passenger Memory Usage"""
        print('Gather Passenger Memory Usage')
        command = ['passenger-memory-stats']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        passengermem = output.stdout.read()
        self.write_to_file('passenger_memory', passengermem)

    def get_Process_Output1(self):
        """Gather ps_alxwww Output"""
        print('Gather ps_alxwww Output')
        command = ['ps', 'alxwww']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        ps_alxwww = output.stdout.read()
        self.write_to_file('ps_alxwww', ps_alxwww)

    def get_Process_Output2(self):
        """Gather ps_auxwww Output"""
        print('Gather ps_auxwww Output')
        command = ['ps', 'auxwww']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        ps_auxwww = output.stdout.read()
        self.write_to_file('ps_auxwww', ps_auxwww)

    def get_Process_Output3(self):
        """Gather ps_auxwwwm Output"""
        print('Gather ps_auxwwwm Output')
        command = ['ps', 'auxwwwm']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        ps_auxwwwm = output.stdout.read()
        self.write_to_file('ps_auxwwwm', ps_auxwwwm)

    def get_Netstat_TPL(self):
        """Gather netstat -tpl Output"""
        print('Gather netstat -tpl Output')
        command = ['netstat', '-tpl']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        netstattpl = output.stdout.read()
        self.write_to_file('netstat-tpl', netstattpl)

    def get_Nestat_TP(self):
        """Gather netstat -tp Output"""
        print('Gather netstat -tp Output')
        command = ['netstat', '-tp']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        netstattp = output.stdout.read()
        self.write_to_file('netstat-tp', netstattp)

    def get_Netstat_AUPL(self):
        """Gather netstat -aupl Output"""
        print('Gather netstat -aupl Output')
        command = ['netstat', '-aupl']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        netstataupl = output.stdout.read()
        self.write_to_file('netstat-aupl', netstataupl)


    def get_SAR_data(self):
        if not os.path.exists(SAR):
            os.makedirs(FULL_PATH + 'sa/')
            print('Gathering SAR Data')
            copy_tree(SAR, FULL_PATH + 'sa/')

    def write_to_file(self, name, content):
        """Write contents to a file"""
        if not os.path.exists(FULL_PATH):
            os.makedirs(FULL_PATH)
            os.chdir(FULL_PATH)
        with open(name, 'w') as file:
            file.write(content)

    def clean_up(self):
        """Archive all collected data"""
        self.get_SAR_data()
        os.chdir('/tmp')
        with tarfile.open(FILE_NAME, "w:gz") as tar:
            tar.add('/tmp/gps/', arcname='.')
        if os.path.exists(DIR + 'gps/'):
            shutil.rmtree('/tmp/gps/')

    def countdown(self,interval):
        print('Collection complete')
        # Find len of interval
        digitlen=len(str(interval))
        # Print countdown warning
        countdownstr='  Waiting {:>'+str(digitlen)+'} seconds to start again\r'
        # This ^ will look like ' Waiting {:>3} seconds 
        # to start again\r'
        # Loop through countdown interval
        for i in xrange(interval, 0, -1):
            print(countdownstr.format(i), end='')
            sys.stdout.flush()
            time.sleep(1)
        print('')
        print('------------')
        print('RESTARTING')
        print('------------')

    TASKS = [get_PulpAdmin_Password,
            get_Pulp_Status,
            get_Pulp_Tasks,
            get_Qpid_Connections,
            get_Qpid_Exchanges,
            get_Qpid_General,
            get_Qpid_Memory,
            get_Qpid_Queues,
            get_Qpid_Subscriptions,
            get_Celery_Active_Queues,
            get_Celery_Active_Tasks,
            get_Celery_Clock,
            get_Celery_Conf,
            get_Celery_Memory_Dump,
            get_Celery_Memory_Sample,
            get_Celery_Obj_Graph,
            get_Celery_Ping,
            get_Celery_Registered_Tasks,
            get_Celery_Report,
            get_Celery_Reserved_Tasks,
            get_Celery_Revoked_Tasks,
            get_Mongo_RSVP_Resource,
            get_Mongo_Tasks,
            get_Mongo_Workers,
            get_Passenger_Memory,
            get_Passenger_Status,
            get_Process_Output1,
            get_Process_Output2,
            get_Process_Output3,
            get_Netstat_AUPL,
            get_Netstat_TPL,
            get_Nestat_TP]

def main(raw_args=None):
    #pdb.set_trace()
    satmon = Satellite_Monitor()

    if os.geteuid() != 0:
        print("Please run as the root user.")
        exit
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i',
                            '--interval',
                            type=int,
                            default=600,
                            help='Interval in seconds to collect the information')

        parser.add_argument('-c',
                            '--clean_up',
                            help='tar up all collected files for export',
                            action='store_true')

        parser.add_argument('-r',
                            '--repeat',
                            help='',
                            action='store_true',
                            default=False)
        args = parser.parse_args(raw_args)

        if args.repeat:
            satmon.verify_pulpadmin_install()
            while True:
                for i in satmon.TASKS:
                    i(satmon)
                satmon.countdown(args.interval)
        elif args.clean_up:
            satmon.clean_up()
        else:
            satmon.verify_pulpadmin_install()
            for i in satmon.TASKS:
                i(satmon)
            satmon.clean_up()

if __name__ == '__main__':
    main()