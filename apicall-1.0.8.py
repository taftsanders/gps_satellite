#!/usr/bin/env python

#from redhat-support-tool import RHHelp
#from optparse import Option
import requests
import warnings
import tarfile
import os
import shutil
import getpass
import pdb

# Suppress all warnings. COMMENT OUT FOR DEBUG
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

        #Gather Satellite FQDN, admin username, and satellite password
    def information(self):
        self.hostname = "http://"+raw_input("Please enter the FQDN or IP of the Satellite server: ")
        self.sat_admin = raw_input("Please enter the Satellite admin username: ")
        self.sat_pw = getpass.getpass("Please enter the password of this user: ")

    def organization_id_list(self):
        org_id_list = []
        org_list_ret = requests.get(self.hostname + '/katello/api/organizations',
                auth=(self.sat_admin, self.sat_pw), verify=False)
        org_list = org_list_ret.json()
        for x in org_list['results']:
            org_id_list.append(x['id'])

    def lce_id_list(self):
        lce_id_list = []
        for x in org_id_list:
            lce_list_ret = requests.get(self.hostname + \
                    '/katello/api/organizations/' + str(x) + '/environments',
                    auth=(self.sat_admin, self.sat_pw), verify=False)
            lce_list = lce_list_ret.json()
            for i in lce_list['results']:
                lce_id_list.append(i['id'])

        #Using redhat-support-tool, upload gps-satellite tarball to case provided by user. If tarball
        #cannot be uploaded, tarball will remain on filesystem and error will be displayed.
#    def rh_support_tool(self):


        #API query, check for file path, create filepath(if needed), writes results to file.
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
a.organization_id_list()
a.lce_id_list()
print()
# print(lce_id_list)
"""
a.organization_list()
a.clean_up()
def get_options(cls):
    return [Option('-p', '--product', dest='product',
                        help=_('The product the case will be opened against. '
                                '(required)'), default=None),
                Option('-v', '--version', dest='version',
                        help=_('The version of the product the case '
                                'will be opened against. (required)'),
                       default=None),
                Option('-s', '--summary', dest='summary',
                        help=_('A summary for the case (required)'),
                        default=None),
                Option('-d', '--description', dest='description',
                        help=_('A description for the case. (required)'),
                        default=None),
                Option('-S', '--severity', dest='severity',
                        help=_('The severity of the case. (optional)'),
                        default=None)]

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

