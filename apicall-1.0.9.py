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
        return org_id_list 

    def lce_id_list(self):
        lce_id_list = []
        org_list = self.organization_id_list()
        for x in org_list:
            lce_list_ret = requests.get(self.hostname + \
                    '/katello/api/organizations/' + str(x) + '/environments',
                    auth=(self.sat_admin, self.sat_pw), verify=False)
            lce_list = lce_list_ret.json()
            for i in lce_list['results']:
                lce_id_list.append(i['id'])
        return lce_id_list

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

# Gather all architectures from Satellite
    def arch_list(self):
        print("Gathering all architectures from the Satellite")
        self.search("/api/architectures", "arch_list")

# Gather all audits from Satellite
    def audit_list(self):
        print("Gathering all audits from the Satellite")
        self.search("/api/audits", "audit_list")

# Gather all autosigns from Satellite
    def autosign_list(self):
        print("Gathering all autosigns from the Satellite")
        self.search("/api/smart_proxies/smart_proxy_id/autosign", "autosign_list")

# Gather all boomarks from Satellite
    def bookmark_list(self):
        print("Gathering all bookmarks from the Satellite")
        self.search("/api/bookmarks", "bookmark_list")

# Gather all global (common) parameters
    def common_parameters_list(self):
        print("Gathering all global parameters from the Satellite")
        self.search("/api/common_parameters", "global_paramters")

# Gather all compute profiles
    def compute_profiles(self):
        print("Gathering all compute profiles from the Satellite")
        self.search("/api/compute_profiles", "compute_profiles")

# Gather all compute resources
    def compute_resources(self):
        print("Gathering all compute resources from the Satellite")
        self.search("/api/compute_resources", "compute_resources")

# Gather all config groups
    def config_groups(self):
        print("Gathering all config groups from the Satellite")
        self.search("/api/config_groups", "config_groups")

# Gather all config reports
    def config_reports(self):
        print("Gathering all config reports from the Satelite")
        self.search("/api/config_reports", "config_reports")

# Gather all config templates
    def config_templates(self):
        print("Gathering all config templates from the Satellite")
        self.search("/api/config_templates", "config_templates")

# Gather all docker containers
    def containers_list(self):
        print("Gathering all docker containers from the Satellite")
        self.search("/docker/api/v2/containers", "docker_containers")

# Gather all discovered hosts
    def discovered_hosts(self):
        print("Gathering all discovered hosts from the Satellite")
        self.search("/api/v2/discovered_hosts", "discovered_hosts")

# Gather all discovery rules
    def discovery_rules(self):
        print("Gathering all discovery rules from the Satellite")
        self.search("/api/v2/discovery_rules", "discovery_rules")

# Gather all user role filters
    def user_role_filters(self):
        print("Gathering all user role filters from the Satellite")
        self.search("/api/filters", "user_role_filters")

# Gather all openscap arf reports
    def arf_reports(self):
        print("Gathering all openscap arf reports from the Satellite")
        self.search("/api/v2/compliance/arf_reports", "openscap_arf_reports")

# Gather all openscap contents
    def openscap_contents(self):
        print("Gathering all openscap contents from the Satellite")
        self.search("/api/v2/compliance/scap_contents", "openscap_contents")

# Gather all GPG keys
    def gpgkey_list(self):
        print("Gathering all GPG keys from the Satellite")
        self.search("/katello/api/gpg_keys", "gpgkey_list")

# Gather all REX job history
    def rex_history_list(self):
        print("Gathering all REX hisotry")
        self.search("/api/job_invocations", "rex_history")

# Gather all Operating systems
    def os_list(self):
        print("Gathering all OS's")
        self.search("/api/operatingsystems", "os_list")

# Gather all OStree branches
    def ostree_branches_list(self):
        print("Gathering all OStree branches")
        self.search("/katello/api/ostree_branches", "ostree_branches")


###########################################################################
###################START OF DEPENDANT API CALLS############################
###########################################################################

# Gather all activation keys
    def activation_key_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering activation keys for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/activation_keys", "activationkey_org" + str(i))

# Gather all auth source ldaps
    def auth_source_ldap_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering ldap auth sources for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/auth_source_ldaps", "auth_source_ldaps_org" + str(i))

# Gather all content views
    def content_views_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering content views for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/content_views", "content_views_org" + str(i))

# Gather all puppet environments
    def puppet_environments_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering puppet environments for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/environments", "puppet_environments_org" + str(i))

# Gather all host collections
    def host_collection_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering host collections for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/host_collections", "host_collections_org" + str(i))

# Gather all host collections
    def host_collection_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gatering all host collections for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/host_collections", "host_collections_org" + str(i))

# Gather all hostgroups
    def hostgroups_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering all hostgroups for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/hostgroups", "hostgroups_org" + str(i))

# Gather all hosts
    def hosts_lists(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering all hosts for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/hosts", "hosts_org" + str(i))

# Gather all REX templates
    def rex_templates_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering all REX templates for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/job_templates", "rex_templates_org" + str(i))

# Gather all Lifecycle Environments (LCE)
    def lce_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering all Lifecycle Environments for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/environments", "lce_org" + str(i))

# Gather all Media
    def media_list(self):
        x = self.organization_id_list()
        for i in x:
            print("Gathering all Media for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/media", "media_org" + str(i))


#Call all functions
a = ApiCall()
a.content_views()
"""
a.auth_source_ldap()
a.activation_key_list()
a.organization_list()
a.clean_up()
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

