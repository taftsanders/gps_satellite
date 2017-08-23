#!/usr/bin/env python

import urllib3
import requests
import warnings

#Suppress all warnings. COMMENT OUT FOR DEBUG 
warnings.filterwarnings("ignore")

HOSTNAME = "http://batman.usersys.redhat.com"
SAT_ADMIN = "admin"
SAT_PW = 8144392

class ApiCall(object):

    def __init__(self, username=SAT_ADMIN, password=SAT_PW, url=HOSTNAME, ssl_warnings=False, ssl_verify=False):
#        import pdb; pdb.set_trace()

        # disable SSL warnings by default
        if not ssl_warnings:
            urllib3.disable_warnings()

        # create requests token to be used across the program
        self.client = requests.Session()
        self.client.auth = (username, password)
        self.client.verify = ssl_verify

    def search(self, call=None, name=None):
        
        ret = self.client.get(HOSTNAME + call)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('/tmp/'+name+'.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))


# Gather all Satellite organizations
    def organization_list(self):
        self.search("/katello/api/organizations", "organization_list")

# Gather all Satellite locations
    def location_list(self):
        self.search("/api/locations", "location_list")

# Gather all Capsules
    def capsule_list(self):
        self.search("/katello/api/capsules", "capsule_list")

# Gather all reported information from the dashboard
    def dashboard_details(self):
        self.search("/api/dashboard", "dashboard")

# Gather all domains from the Satellite
    def domain_list(self):
        self.search("/api/domains", "domain_list")

# Gather all errata synced from the Satellite
    def errata_list(self):
        self.search("/katello/api/errata", "errata_list")

# Gather all openscap policies on the Satellite
    def openscap_policy_list(self):
        self.search("/api/v2/compliance/policies", "openscap_policies_list")

# Gather a summary/count of all tasks on the Satellite by label
    def satellite_tasks_summary(self):
        self.search("/foreman_tasks/api/tasks/summary", "satellite_tasks_summary")

# Gather the output of hammer ping
    def hammer_ping(self):
        self.search("/katello/api/ping", "hammer_ping")

# Gather all realms from the Satellite
    def realms_list(self):
        self.search("/api/realms", "realms_list")

# Gather all user roles from the Satellite
    def user_roles_list(self):
        self.search("/api/roles", "user_roles")

# Gather all the settings from the Satellite
    def settings_list(self):
        self.search("/api/settings", "settings")

# Gather all subnets from the Satellite
    def subnets_list(self):
        self.search("/api/subnets", "subnet_list")

# Gather all users from the Satellite
    def user_list(self):
        self.search("/api/users", "user_list")


#Call all functions
a = ApiCall()
a.organization_list()
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
