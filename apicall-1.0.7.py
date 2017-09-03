#!/usr/bin/env python

import urllib3
import requests
import warnings
import tarfile
import os
import shutil
import getpass

#Suppress all warnings. COMMENT OUT FOR DEBUG 
warnings.filterwarnings("ignore")

#HOSTNAME = "http://batman.usersys.redhat.com"
#SAT_ADMIN = "admin"
#SAT_PW = "vector16"
PATH = '/tmp/gps/'

class ApiCall(object):

    def __init__(self):
        self.hostname = None
        self.sat_admin = None
        self.sat_pw = None
        self.information()

    def information(self):
        self.hostname = "http://"+raw_input("Please enter the FQDN or IP of the Satellite server: ")
        self.sat_admin = raw_input("Please enter the Satellite admin username: ")
        self.sat_pw = getpass.getpass("Please enter the password of this user: ")

    def search(self, call=None, name=None):
        ret = requests.get(self.hostname + call, auth=(self.sat_admin, self.sat_pw), verify=False)
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                if not os.path.exists(PATH):
                    os.makedirs(PATH)
                    os.chdir(PATH)
                fw = open(name+'.json', 'w')
                content = ret.content
                fw.write(content)
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

# Tar gz all files collected from GPS
    def clean_up(self):
        os.chdir('/tmp/')
        tar = tarfile.open("gps.tar.gz", "w:gz")
        tar.add(PATH, arcname='.')
        tar.close()
        if os.path.exists('/tmp/gps.tar.gz'):
            shutil.rmtree(PATH)
    
# Gather all Satellite organizations
    def organization_list(self):
        print("Gathering all Satellite Organizations")
        self.search("/katello/api/organizations", "organization_list")

# Gather all Satellite locations
    def location_list(self):
        print("Gathering all Satellite Locations")
        self.search("/api/locations", "location_list")

# Gather all Capsules
    def capsule_list(self):
        print("Gathering all Capsule servers")
        self.search("/katello/api/capsules", "capsule_list")

# Gather all reported information from the dashboard
    def dashboard_details(self):
        print("Gathering all Satellite Dashboard information")
        self.search("/api/dashboard", "dashboard")

# Gather all domains from the Satellite
    def domain_list(self):
        print("Gathering all Domains on the Satellite")
        self.search("/api/domains", "domain_list")

# Gather all errata synced from the Satellite
    def errata_list(self):
        print("Gathering all Errata synced on the Satllite")
        print("**This may take a while**")
        self.search("/katello/api/errata?per_page=20000", "errata_list")

# Gather all openscap policies on the Satellite
    def openscap_policy_list(self):
        print("Gathering all Openscap policies from the Satellite")
        self.search("/api/v2/compliance/policies", "openscap_policies_list")

# Gather a summary/count of all tasks on the Satellite by label
    def satellite_tasks_summary(self):
        print("Gathering Task summary by label")
        self.search("/foreman_tasks/api/tasks/summary", "satellite_tasks_summary")

# Gather the output of hammer ping
    def hammer_ping(self):
        print("Gathering results of \"hammer ping\"")
        self.search("/katello/api/ping", "hammer_ping")

# Gather all realms from the Satellite
    def realms_list(self):
        print("Gathering all Realms from the Satellite")
        self.search("/api/realms", "realms_list")

# Gather all user roles from the Satellite
    def user_roles_list(self):
        print("Gathering all Roles from the Satellite")
        self.search("/api/roles", "user_roles")

# Gather all the settings from the Satellite
    def settings_list(self):
        print("Gathering all Settings from the Satellite")
        self.search("/api/settings", "settings")

# Gather all subnets from the Satellite
    def subnets_list(self):
        print("Gathering all Subnets from the Satellite")
        self.search("/api/subnets", "subnet_list")

# Gather all users from the Satellite
    def user_list(self):
        print("Gathering all Users from the Satellite")
        self.search("/api/users", "user_list")

#Call all functions
a = ApiCall()
a.organization_list()
a.clean_up()
"""
a.location_list()
a.capsule_list()
a.dashboard_details()
a.domain_list()
a.errata_list()
a.openscap_policy_list()
a.satellite_tasks_summary()
a.hammer_ping()
a.realms_list()
a.user_roles_list()
a.settings_list()
a.subnets_list()
a.user_list()
"""
