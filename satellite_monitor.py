#!/usr/bin/env python

import yum
import datetime
import subprocess
import os
import re
import shutil
import tarfile
from distutils.dir_util import copy_tree


DATE = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
FULL_PATH = '/tmp/gps/satellite-monitor' + DATE + '/'
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
        file = open('/etc/pulp/server.conf', "r")
        for line_file in file:
            if re.findall("^default_password", line_file):
                fields_line = re.split(":", line_file)
                pulp_pw = fields_line[1].strip()
#        command1 = ['grep', '^default_login', '/etc/pulp/server.conf']
#        command2 = ['cut', '-d', ' ', '-f2']
#        command3 = ['grep', '^default_password', '/etc/pulp/server.conf']
#        self.line1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
#        self.line2 = subprocess.Popen(command3, stdout=subprocess.PIPE)
#        self.line3 = subprocess.Popen(command2, stdin=self.line1.stdout, stdout=subprocess.PIPE)
#        self.line4 = subprocess.Popen(command2, stdin=self.line2.stdout, stdout=subprocess.PIPE)
#        self.user = self.line3.stdout.read().strip()
#        self.pw = self.line4.stdout.read().strip()

    def get_Pulp_Tasks(self):
        """Gather all Pulp Tasks"""
        pulptasks = subprocess.Popen('pulp admin -u admin -p ' + self.pw +
                                    'tasks list')
        self.write_to_file('pulp_tasks', pulptasks)

    def get_Pulp_Status(self):
        """Gather Pulp status"""
        pulpstatus = subprocess.Popen('pulp admin -u admin -p ' + self.pw +
                                        'status')
        self.write_to_file('pulp_status', pulpstatus)

    def get_Celery_Active_Tasks(self):
        """Gather all active celery tasks"""
        ctasks = subprocess.Popen('celery -A pulp.server.async.app \
                                    inspect active')
        self.write_to_file('celery_tasks_active', ctasks)

    def get_Celery_Scheduled_Tasks(self):
        """Gather all scheduled celery tasks"""
        cschtasks = subprocess.Popen('celery -A pulp.server.async.app \
                                        inspect scheduled')
        self.write_to_file('celery_tasks_scheduled', cschtasks)

    def get_Celery_Reserved_Tasks(self):
        """Gather all reserved celery tasks"""
        crsvptasks = subprocess.Popen('celery -A pulp.server.async.app \
                                        inspect reserved')
        self.write_to_file('celery_tasks_reserved', crsvptasks)

    def get_Celery_Revoked_Tasks(self):
        """Gather all revoked celery tasks"""
        crevoketasks = subprocess.Popen('celery -A pulp.server.async.app \
                                        inspect reserved')
        self.write_to_file('celery_tasks_revoked', crevoketasks)

    def get_Celery_Registered_Tasks(self):
        """Gather all registered celery tasks"""
        cregtasks = subprocess.Popen('celery -A pulp.server.async.app \
                                    inspect registered')
        self.write_to_file('celery_tasks_registered', cregtasks)

    def get_Celery_Stats(self):
        """Gather celery stats"""
        cstats = subprocess.Popen('celery -A pulp.server.async.app inspect \
                                    stats')
        self.write_to_file('celery_stats', cstats)

    def get_Celery_Active_Queues(self):
        """Gather celery active queues"""
        cactiveques = subprocess.Popen('celery -A pulp.server.async.app \
                                        inspect active_queues')
        self.write_to_file('celery_active_queues', cactiveques)

    def get_Celery_Clock(self):
        """Gather celery clocks"""
        cclocks = subprocess.Popen('celery -A pulp.server.async.app \
                                    inspect clock')
        self.write_to_file('celery_clock', cclocks)
    
    def get_Celery_Conf(self):
        """Gather celery configs"""
        cconf = subprocess.Popen('celery -A pulp.server.async.app inspect conf')
        self.write_to_file('celery_conf', cconf)

    def get_Celery_Memory_Dump(self):
        """Gather celery memory dump"""
        cmemdump = subprocess.Popen('celery -A pulp.server.async.app \
                                    inspect memdump')
        self.write_to_file('celery_memory_dump', cmemdump)

    def get_Celery_Memory_Sample(self):
        """Gather celery memory sample"""
        cmemsamp = subprocess.Popen('celery -A pulp.server.async.app \
                                    inspect memsample')
        self.write_to_file('celery_memory_sample', cmemsamp)

    def get_Celery_Obj_Graph(self):
        """Gather celery object graph"""
        cobjgraph = subprocess.Popen('celery -A pulp.server.async.app \
                                        inspect objgraph')
        self.write_to_file('celery_objgraph', cobjgraph)

    def get_Celery_Ping(self):
        """Gather celery ping"""
        cping = subprocess.Popen('celery -A pulp.server.async.app inspect ping')
        self.write_to_file('celery_ping', cping)

    def get_Celery_Report(self):
        """Gather celery bugreport"""
        cbug = subprocess.Popen('celery -A pulp.server.async.app \
                                inspect report')
        self.write_to_file('celery_bugreport', cbug)

    def get_Qpid_General(self):
        qpidgen = subprocess.Popen('qpid-stat -g --ssl-certificate=/etc/pki/\
                                    katello/qpid_client_striped.crt \
                                    -b amqps://localhost:5671')
        self.write_to_file('qpid_general', qpidgen)

    def get_Qpid_Connections(self):
        qpidconn = subprocess.Popen('qpid-stat -c --ssl-certificate=/etc/pki/\
                                    katello/qpid_client_striped.crt \
                                    -b amqps://localhost:5671')
        self.write_to_file('qpid_connections', qpidconn)

    def get_Qpid_Exchanges(self):
        qpidex = subprocess.Popen('qpid-stat -e --ssl-certificate=/etc/pki/\
                                    katello/qpid_client_striped.crt \
                                    -b amqps://localhost:5671')
        self.write_to_file('qpid_exchanges', qpidex)

    def get_Qpid_Queues(self):
        qpidque = subprocess.Popen('qpid-stat -q --ssl-certificate=/etc/pki/\
                                    katello/qpid_client_striped.crt \
                                    -b amqps://localhost:5671')
        self.write_to_file('qpid_queue', qpidque)

    def get_Qpid_Subscriptions(self):
        qpidsub = subprocess.Popen('qpid-stat -u --ssl-certificate=/etc/pki/\
                                    katello/qpid_client_striped.crt \
                                    -b amqps://localhost:5671')
        self.write_to_file('qpid_subscriptions', qpidsub)

    def get_Qpid_Memory(self):
        qpidmem = subprocess.Popen('qpid-stat -m --ssl-certificate=/etc/pki/\
                                    katello/qpid_client_striped.crt \
                                    -b amqps://localhost:5671')
        self.write_to_file('qpid_memory', qpidmem)

    def get_Mongo_Tasks(self):
        mongotasks = subprocess.Popen('mongoexport --db pulp_database \
                                        --collection task_status')
        self.write_to_file('mongo_tasks', mongotasks)

    def get_Mongo_RSVP_Resource(self):
        mongoresources = subprocess.Popen('mongoexport --db pulp_database \
                                            --collection reserved_resources')
        self.write_to_file('mongo_resources', mongoresources)

    def get_Mongo_Workers(self):
        mongoworkers = subprocess.Popen('mongoexport --db pulp_database \
                                            --collection workers')
        self.write_to_file('mongo_workers', mongoworkers)

    def get_SAR_data(self):
        fromdir = '/var/log/sa/'
        os.makedirs(FULL_PATH + 'sa/')
        copy_tree(fromdir, FULL_PATH + 'sa/')

    def write_to_file(self, name, content):
        """Write contents to a file"""
        with open(name, 'w') as file:
            file.write(content)

    def clean_up(self):
        """Archive all collected data"""
        with tarfile.open(FILE_NAME, "w:gz") as tar:
            tar.add('/tmp/gps/', arcname='.')
        if os.path.exists(DIR + FILE_NAME):
            shutil.rmtree('/tmp/gps/')

def main():
    if os.geteuid() == 0:
        satmon = Satellite_Monitor()
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
    else:
        print("Please run as the root user.")