#!/usr/bin/env python

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


DATE = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
FULL_PATH = '/tmp/gps/satellite-monitor-' + DATE + '/'
DIR = '/tmp/'
FILE_NAME = 'satellite-monitor' + DATE + '.tar.gz'

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
        command = ['pulp-admin', '-u', 'admin', '-p', self.pulp_pw,
                     'tasks', 'list']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        pulptasks = output.stdout.read()
        self.write_to_file('pulp_tasks', pulptasks)

    def get_Pulp_Status(self):
        """Gather Pulp status"""
        command = ['pulp-admin', '-u', 'admin', '-p', self.pulp_pw, 'status']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        pulpstatus = output.stdout.read()
        self.write_to_file('pulp_status', pulpstatus)

    def get_Celery_Active_Tasks(self):
        """Gather all active celery tasks"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'active']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        ctasks = output.stdout.read()
        self.write_to_file('celery_tasks_active', ctasks)

    def get_Celery_Scheduled_Tasks(self):
        """Gather all scheduled celery tasks"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'scheduled']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cschtasks = output.stdout.read()
        self.write_to_file('celery_tasks_scheduled', cschtasks)

    def get_Celery_Reserved_Tasks(self):
        """Gather all reserved celery tasks"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'reserved']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        crsvptasks = output.stdout.read()
        self.write_to_file('celery_tasks_reserved', crsvptasks)

    def get_Celery_Revoked_Tasks(self):
        """Gather all revoked celery tasks"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'revoked']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        crevoketasks = output.stdout.read()
        self.write_to_file('celery_tasks_revoked', crevoketasks)

    def get_Celery_Registered_Tasks(self):
        """Gather all registered celery tasks"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'registered']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cregtasks = output.stdout.read()
        self.write_to_file('celery_tasks_registered', cregtasks)

    def get_Celery_Stats(self):
        """Gather celery stats"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'stats']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cstats = output.stdout.read()
        self.write_to_file('celery_stats', cstats)

    def get_Celery_Active_Queues(self):
        """Gather celery active queues"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'active_queues']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cactiveques = output.stdout.read()
        self.write_to_file('celery_active_queues', cactiveques)

    def get_Celery_Clock(self):
        """Gather celery clocks"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'clock']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cclocks = output.stdout.read()
        self.write_to_file('celery_clock', cclocks)
    
    def get_Celery_Conf(self):
        """Gather celery configs"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'conf']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cconf = output.stdout.read()
        self.write_to_file('celery_conf', cconf)

    def get_Celery_Memory_Dump(self):
        """Gather celery memory dump"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'memdump']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cmemdump = output.stdout.read()
        self.write_to_file('celery_memory_dump', cmemdump)

    def get_Celery_Memory_Sample(self):
        """Gather celery memory sample"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'memsample']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cmemsamp = output.stdout.read()
        self.write_to_file('celery_memory_sample', cmemsamp)

    def get_Celery_Obj_Graph(self):
        """Gather celery object graph"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'objgraph']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cobjgraph = output.stdout.read()
        self.write_to_file('celery_objgraph', cobjgraph)

    def get_Celery_Ping(self):
        """Gather celery ping"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 'ping']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cping = output.stdout.read()
        self.write_to_file('celery_ping', cping)

    def get_Celery_Report(self):
        """Gather celery bugreport"""
        command = ['celery', '-A', 'pulp.server.async.app', 'inspect', 
                    'report']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        cbug = output.stdout.read()
        self.write_to_file('celery_bugreport', cbug)

    def get_Qpid_General(self):
        command = ['qpid-stat', '-g', '--ssl-certificate=\
                    /etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidgen = output.stdout.read()
        self.write_to_file('qpid_general', qpidgen)

    def get_Qpid_Connections(self):
        command = ['qpid-stat', '-c', '--ssl-certificate=\
                    /etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidconn = output.stdout.read()
        self.write_to_file('qpid_connections', qpidconn)

    def get_Qpid_Exchanges(self):
        command = ['qpid-stat', '-e', '--ssl-certificate=\
                    /etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidexch = output.stdout.read()
        self.write_to_file('qpid_exchanges', qpidexch)

    def get_Qpid_Queues(self):
        command = ['qpid-stat', '-q', '--ssl-certificate=\
                    /etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidque = output.stdout.read()
        self.write_to_file('qpid_queue', qpidque)

    def get_Qpid_Subscriptions(self):
        command = ['qpid-stat', '-u', '--ssl-certificate=\
                    /etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidsub = output.stdout.read()
        self.write_to_file('qpid_subscriptions', qpidsub)

    def get_Qpid_Memory(self):
        command = ['qpid-stat', '-m', '--ssl-certificate=\
                    /etc/pki/katello/qpid_client_striped.crt', 
                    '-b', 'amqps://localhost:5671']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        qpidmem = output.stdout.read()
        self.write_to_file('qpid_memory', qpidmem)

    def get_Mongo_Tasks(self):
        command = ['mongoexport', '--db', 'pulp_database', '--collection',
                    'task_status']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        mongotasks = output.stdout.read()
        self.write_to_file('mongo_tasks', mongotasks)

    def get_Mongo_RSVP_Resource(self):
        command = ['mongoexport', '--db', 'pulp_database', '--collection',
                    'reserved_resources']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        mongoresources = output.stdout.read()
        self.write_to_file('mongo_resources', mongoresources)

    def get_Mongo_Workers(self):
        command = ['mongoexport', '--db', 'pulp_database', '--collection',
                    'workers']
        output = subprocess.Popen(command, stdout=subprocess.PIPE)
        mongoworkers = output.stdout.read()
        self.write_to_file('mongo_workers', mongoworkers)

    def get_SAR_data(self):
        fromdir = '/var/log/sa/'
        os.makedirs(FULL_PATH + 'sa/')
        copy_tree(fromdir, FULL_PATH + 'sa/')

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

def main():
    if os.geteuid() == 0:
        parser = argparse.ArgumentParser()
        parser.add_argument("-i",
                            "--interval",
                            help="Interval in which to collect the information",
                            action="store_true")
        parser.add_argument('-c',
                            '--clean_up',
                            help='tar up all collected files for export',
                            action='store_true')

        args = parser.parse_args()
        satmon = Satellite_Monitor()

        if args.interval:
            while True:
                satmon.get_PulpAdmin_Password()
                satmon.get_Pulp_Status()
                satmon.get_Pulp_Tasks()
                satmon.get_Qpid_Connections()
                satmon.get_Qpid_Exchanges()
                satmon.get_Qpid_General()
                satmon.get_Qpid_Memory()
                satmon.get_Qpid_Queues()
                satmon.get_Qpid_Subscriptions()
                satmon.get_Celery_Active_Queues()
                satmon.get_Celery_Active_Tasks()
                satmon.get_Celery_Clock()
                satmon.get_Celery_Conf()
                satmon.get_Celery_Memory_Dump()
                satmon.get_Celery_Memory_Sample()
                satmon.get_Celery_Obj_Graph()
                satmon.get_Celery_Ping()
                satmon.get_Celery_Registered_Tasks()
                satmon.get_Celery_Report()
                satmon.get_Celery_Reserved_Tasks()
                satmon.get_Celery_Revoked_Tasks()
                satmon.get_Mongo_RSVP_Resource()
                satmon.get_Mongo_Tasks()
                satmon.get_Mongo_Workers()
#                time.sleep(INTERVAL)
        elif args.clean_up:
            satmon.clean_up()
        else:
            satmon.get_PulpAdmin_Password()
            satmon.get_Pulp_Status()
            satmon.get_Pulp_Tasks()
            satmon.get_Qpid_Connections()
            satmon.get_Qpid_Exchanges()
            satmon.get_Qpid_General()
            satmon.get_Qpid_Memory()
            satmon.get_Qpid_Queues()
            satmon.get_Qpid_Subscriptions()
            satmon.get_Celery_Active_Queues()
            satmon.get_Celery_Active_Tasks()
            satmon.get_Celery_Clock()
            satmon.get_Celery_Conf()
            satmon.get_Celery_Memory_Dump()
            satmon.get_Celery_Memory_Sample()
            satmon.get_Celery_Obj_Graph()
            satmon.get_Celery_Ping()
            satmon.get_Celery_Registered_Tasks()
            satmon.get_Celery_Report()
            satmon.get_Celery_Reserved_Tasks()
            satmon.get_Celery_Revoked_Tasks()
            satmon.get_Mongo_RSVP_Resource()
            satmon.get_Mongo_Tasks()
            satmon.get_Mongo_Workers()
            satmon.clean_up()
    else:
        print("Please run as the root user.")

main()