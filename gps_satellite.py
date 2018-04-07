#!/usr/bin/env python
import pulp_api as pulp
from requests import Session
from requests.exceptions import ConnectionError
import warnings
import datetime
import tarfile
import os
import shutil
import getpass
import argparse
import subprocess
import yum
import json

# Suppress all warnings. COMMENT OUT FOR WARNINGS
warnings.filterwarnings("ignore")

DATE = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
FULL_PATH = '/tmp/gps/gps-satellite-' + DATE + '/'
DIR = '/tmp/'
FILE_NAME = 'gps-satellite-' + DATE + '.tar.gz'


class ApiCall(object):

    def __init__(self, hostname=None, username=None, password=None):
        """Initializing needed variables and lists for all api calls

        hostname = FQDN or ip address of the Satellite server
        sat_admin = admin user of the Satellite
        sat_pw = password for the admin user
        information = function to gather hostname, admin user, and password from user
        organization_id_list = initial collection of organization ids
        capsule_id_list = initial collection of capsule ids
        lce_id_list = initial collection of lifecycle environment ids
        compute_resource_id_list = initial collection of compute resources ids
        contentview_id_list = initial collection of content view ids
        hosts_id_list = initial collection of of hosts ids
        smart_variable_id_list = initial collection of smart variable ids
        """
        # get hostname
        if hostname:
            self.hostname = "https://" + hostname
        else:
            self.hostname = "http://" + raw_input("Please enter the FQDN or IP of the Satellite server" + "[" +
                                                  self.getsatellitefqdn() + "]" + ": ")

        # get username
        if username:
            self.sat_admin = username
        else:
            self.sat_admin = raw_input("Please enter the Satellite admin username: ")

        # get password
        if password:
            self.sat_pw = password
        else:
            self.sat_pw = getpass.getpass("Please enter the password of this user: ")

        self.session = Session()
        self.session.auth = (self.sat_admin, self.sat_pw)
        self.session.verify = False
        self.__connection_test()
        self.capsule_id_list()
        self.lce_id_list()
        self.compute_resource_id_list()
        self.contentview_id_list()
        self.hosts_id_list()
        self.smart_variable_id_list()

    def getsatellitefqdn(self):
        with open('/var/lib/rhsm/facts/facts.json', 'r') as f:
            content = json.loads(f.read())
            fqdn = content['network.fqdn']
            return str(fqdn)

    # Fallback for Satellite information
    def information(self):
        self.hostname = "http://" + raw_input("Please enter the FQDN or IP of the Satellite server: ")
        self.sat_admin = raw_input("Please enter the Satellite admin username: ")
        self.sat_pw = getpass.getpass("Please enter the password of this user: ")

    # Test Satellite connectivity with user and password
    def __connection_test(self):
            try:
                self.organization_id_list()
            except KeyError:
                print("Incorrect Username or Password given, please try again")
                self.information()
            except (ConnectionError, ValueError):
                print("Incorrect URL given, please try again")
                self.information()

    # Organization id loop to gather all org id's for additional api calls
    def organization_id_list(self):
        """Collect organization ids."""
        self.org_id_list = []
        print("Initializing Organization list")
        org_list = self.session.get(self.hostname + '/katello/api/organizations').json()
        for x in org_list['results']:
            self.org_id_list.append(x['id'])

    # Capsule id loop to gather all capsule id's for additional api calls
    def capsule_id_list(self):
        """Collection of capsule ids."""
        self.cap_id_list =[]
        print("Initializing Capsule list")
        capsule_list = self.session.get(self.hostname + '/katello/api/capsules').json()
        for x in capsule_list['results']:
            self.cap_id_list.append(x['id'])

    # Lifecycle env. id loop to gather all lce id's for additional information
    def lce_id_list(self):
        """Collection of lifecycle environment ids"""
        self.lifecycle_id_list = []
        print("Initializing Lifecycle Environment list")
        for x in self.org_id_list:
            lce_list = self.session.get(self.hostname + '/katello/api/organizations/' + str(x) + '/environments').json()
            for i in lce_list['results']:
                self.lifecycle_id_list.append(i['id'])

    # Compute resource id loop to gather all compute resource id's for additional information
    def compute_resource_id_list(self):
        """Collection of compute resource ids"""
        self.compute_res_id_list = []
        print("Initializing Compute Resource list")
        compute_res_list = self.session.get(self.hostname + '/api/compute_resources').json()
        for x in compute_res_list['results']:
            self.compute_res_id_list.append(x['id'])

    # Content view id loop to gather all content view id's for additional information
    def contentview_id_list(self):
        """Collection of content view ids"""
        self.contentview_id = []
        print("Initializing Content view list list")
        for x in self.org_id_list:
            cv_list = self.session.get(self.hostname + '/katello/api/organizations/' + str(x) + '/content_views').json()
            for i in cv_list['results']:
                self.contentview_id.append(i['id'])

    # Host id loop to gather all host id's for additional information
    def hosts_id_list(self):
        """Collection of host ids"""
        self.hosts_id = []
        print("Initializing Host list")
        for x in self.org_id_list:
            host_list = self.session.get(self.hostname + '/api/organizations/' + str(x) + '/hosts').json()
            for i in host_list['results']:
                self.hosts_id.append(i['id'])

    # Smart variable id loop to gather all smart variable id's for additional information
    def smart_variable_id_list(self):
        """Collection of smart variable ids"""
        self.smart_variable_id = []
        print("Initializing Puppet Smart Variable list")
        smart_variable_list = self.session.get(self.hostname + '/api/smart_variables').json()
        for x in smart_variable_list['results']:
            self.smart_variable_id.append(x['id'])

    # API query, check for file path, create filepath(if needed), writes results to file.
    def search(self, call=None, name=None):
        """Request API queried information"""
        ret = self.session.get(self.hostname + call + '?per_page=2000000')
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                if not os.path.exists(FULL_PATH):
                    os.makedirs(FULL_PATH)
                    os.chdir(FULL_PATH)
                with open(name + '.json', 'w') as fw:
                    content = ret.content
                    fw.write(content)
            else:
                return ret.text
        else:
            print("Return {}, content not available".format(ret.status_code))

    # Tar gz all files collected from GPS
    def clean_up(self):
        """Archive all collected data"""
        os.chdir(DIR)
        with tarfile.open(FILE_NAME, "w:gz") as tar:
            tar.add('/tmp/gps/', arcname='.')
        if os.path.exists(DIR + FILE_NAME):
            shutil.rmtree('/tmp/gps/')

    # Upload the tar'ed Satellite mapping to the case using the RHST
    # Use case 01979320 for testing
    def rhst_upload(self):
        """Upload mapping to case with RHST"""
        option = raw_input("Would you like to upload this file to your case? [Y/N]:\n(Please note this will require "
                           "installing the redhat-support-tool if you do not already have it installed)\n")
        while True:
            if option.upper() == 'Y':
                yb = yum.YumBase()
                if yb.rpmdb.searchNevra(name='redhat-support-tool'):
                    print "redhat-support-tool installed!"
                else:
                    print "redhat-support-tool not installed"
                    print "installing redhat-support-tool..."
                    a = subprocess.Popen("yum install redhat-support-tool -y", shell=True)
                    a.wait()
                case_num = raw_input("Please enter the case number you wish to upload this mapping to: ")
                command = "redhat-support-tool addattachment -c " + case_num + " " + DIR + FILE_NAME
                p = subprocess.Popen(command, shell=True)
                p.wait()
                if p.returncode == 0:
                    os.remove(DIR + FILE_NAME)
                    break
                else:
                    print("There appears to be an issue with uploading the Satellite mapping to the case. Please "
                          "upload the file manually to the case through the customer portal.")
            elif option.upper() == 'N':
                print("Please upload " + DIR + FILE_NAME + " to your case.")
                break
            else:
                print("ERROR: INCORRECT VALUE ENTERED")
                option = raw_input("Please enter a valid selection: 'Y' for yes or 'N' for no: ")
                option.upper()

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

    #Gather all Smart Proxies information
    def smart_proxies_list(self):
        print("Gathering all Smart Proxies")
        self.search("/api/smart_proxies", "smart_proxies")

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
        print("Gathering all Errata synced on the Satellite")
        print("**This may take a while**")
        self.search("/katello/api/errata", "errata_list")

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
        print("Gathering all REX history")
        self.search("/api/job_invocations", "rex_history")

    # Gather all Operating systems
    def os_list(self):
        print("Gathering all OS's")
        self.search("/api/operatingsystems", "os_list")

    # Gather all OStree branches
    def ostree_branches_list(self):
        print("Gathering all OStree branches")
        self.search("/katello/api/ostree_branches", "ostree_branches")

    # Gather all permissions
    def permissions_list(self):
        print("Gathering all permissions")
        self.search("/api/permissions", "permissions_list")

    # Gather all recurring logics
    def recurring_logics(self):
        print("Gathering all recurring logics")
        self.search("/foreman_tasks/api/recurring_logics", "recurring_logics")

    # Gather all docker registries
    def docker_registries(self):
        print("Gathering all docker registries")
        self.search("/docker/api/v2/registries", "docker_registries")

    # Gather all REX features
    def rex_features_list(self):
        print("Gathering all REX features")
        self.search("/api/remote_execution_features", "rex_features")

    # Gather all reports for Capsules?
    def reports_list(self):
        print("Gathering all reports")
        self.search("/api/reports", "reports")

    # Gather all smart proxies
    def smart_proxy_list(self):
        print("Gathering all smart proxies")
        self.search("/api/smart_variables", "smart_proxies_list")

    # Gather all smart variables
    def smart_variables_list(self):
        print("Gathering all smart variables")
        self.search("/api/smart_variables", "smart_variables_list")

    # Gather Statistics
    def statistics(self):
        print("Gathering statistics")
        self.search("/api/statistics", "statistics")

    # Gather Template kinds
    def template_kind_list(self):
        print("Gathering Template kinds")
        self.search("/api/template_kinds", "template_kinds")

    # Gather Usergroups
    def usergroup_list(self):
        print("Gathering usergroup list")
        self.search("/api/usergroups", "usergroups")

    # Gather content view filters
    def contentview_filters(self):
        print("Gathering content view filters")
        self.search("/katello/api/content_view_filters", "contentviewfilters")

    # Gather content view versions
    def contentview_versions(self):
        print("Gathering all content view versions")
        self.search("/katello/api/content_view_versions", "contentviewversions")

    # Gather all Docker manifests
    def docker_manifests(self):
        print("Gathering all docker manifests")
        self.search("/katello/api/docker_manifests", "dockermanifests")

    # Gather all Docker tags
    def docker_tags(self):
        print("Gathering all docker tags")
        self.search("/katello/api/docker_tags", "dockertags")

    # Gather all sub-man fact values
    def fact_values(self):
        print("Gathering all fact values")
        self.search("/api/fact_values", "sub-man_fact_values")

    ###########################################################################
    ###################START OF DEPENDANT API CALLS############################
    ###########################################################################

    # Gather all activation keys
    def activation_key_list(self):
        for i in self.org_id_list:
            print("Gathering activation keys for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/activation_keys", "activationkey_org" + str(i))

    # Gather all auth source ldaps
    def auth_source_ldap_list(self):
        for i in self.org_id_list:
            print("Gathering ldap auth sources for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/auth_source_ldaps", "auth_source_ldaps_org" + str(i))

    # Gather all content views
    def content_views_list(self):
        for i in self.org_id_list:
            print("Gathering content views for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/content_views", "content_views_org" + str(i))

    # Gather all puppet environments
    def puppet_environments_list(self):
        for i in self.org_id_list:
            print("Gathering puppet environments for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/environments", "puppet_environments_org" + str(i))

    # Gather all host collections
    def host_collection_list(self):
        for i in self.org_id_list:
            print("Gathering host collections for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/host_collections", "host_collections_org" + str(i))

    # Gather all hostgroups
    def hostgroups_list(self):
        for i in self.org_id_list:
            print("Gathering all hostgroups for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/hostgroups", "hostgroups_org" + str(i))

    # Gather all hosts
    def hosts_lists(self):
        for i in self.org_id_list:
            print("Gathering all hosts for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/hosts", "hosts_org" + str(i))

    # Gather all REX templates
    def rex_templates_list(self):
        for i in self.org_id_list:
            print("Gathering all REX templates for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/job_templates", "rex_templates_org" + str(i))

    # Gather all Lifecycle Environments (LCE)
    def lce_list(self):
        for i in self.org_id_list:
            print("Gathering all Lifecycle Environments for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/environments", "lce_org" + str(i))

    # Gather all Media
    def media_list(self):
        for i in self.org_id_list:
            print("Gathering all Media for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/media", "media_org" + str(i))

    # Gather all Products
    def products_list(self):
        for i in self.org_id_list:
            print("Gathering all Products for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/products", "products_org" + str(i))

    # Gather all provisioning templates
    def provisioning_templates_list(self):
        for i in self.org_id_list:
            print("Gathering all Provisioning templates for Org id: " + str(i))
            self.search("/api/organizations/" + str(i) + "/provisioning_templates",
                        "provisioning_templates_org" + str(i))

    # Gather all partition tables
    def partition_tables_list(self):
        for i in self.org_id_list:
            print("Gathering all Partition tables for Org id: " + str(i))
            self.search("/api/organizations/:organization_id/ptables" + str(i) + "/ptables",
                        "partition_tables_org" + str(i))

    # Gather all subscriptions
    def subscription_list(self):
        for i in self.org_id_list:
            print("Gathering all Subscriptions for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/subscriptions", "subscriptions_org" + str(i))

    # Gather manifest history
    def manifest_history(self):
        for i in self.org_id_list:
            print("Gathering Manifest history for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/subscriptions/manifest_history",
                        "manifest_history_org" + str(i))

    # Gather sync plans
    def sync_plan_list(self):
        for i in self.org_id_list:
            print("Gathering Sync plan for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/sync_plans", "sync_plan_org" + str(i))

    # Gather Uebercerts
    def uebercert_list(self):
        for i in self.org_id_list:
            print("Gathering Ubercert for Org id: " + str(i))
            self.search("/katello/api/organizations/" + str(i) + "/uebercert", "uebercert_org" + str(i))

    # Gather Capsule assigned lifecycle environments
    def capsule_lce_assigned_list(self):
        for i in self.cap_id_list:
            if i == 1:
                print("No lifecycle environments for internal Satellite's Capsule, SKIPPING")
            else:
                print("Gathering Capsule's assigned Lifecycle environments for Capsule id: " + str(i))
                self.search("/katello/api/capsules/" + str(i) + "/content/lifecycle_environments",
                            "capsule_lce_assigned_cap" + str(i))

    # Gather Capsule available lifecycle environments
    def capsule_lce_available_list(self):
        for i in self.cap_id_list:
            if i == 1:
                print("No lifecycle environments for internal Satellite's Capsule, SKIPPING")
            else:
                print("Gathering Capsule's available Lifecycle environments for Capsule id: " + str(i))
                self.search("/katello/api/capsules/" + str(i) + "/content/available_lifecycle_environments",
                            "capsule_lce_available_cap" + str(i))

    # Gather Capsule sync status
    def capsule_sync_status_list(self):
        for i in self.cap_id_list:
            if i == 1:
                print("No sync status for Satellite's internal Capsule, SKIPPING")
            else:
                print("Gathering Capsule's sync status for Capsule id: " + str(i))
                self.search("/katello/api/capsules/" + str(i) + "/content/sync", "capsule_lce_assigned_cap" + str(i))

    # Gather Capsule sync status
    def cr_avail_img_list(self):
        for i in self.compute_res_id_list:
            print("Gathering available images for Compute resource id: " + str(i))
            self.search("/api/compute_resource/" + str(i) + "/available_images", "cr_available_img_cr" + str(i))

    # Gather Content view filters
    def cv_filter_list(self):
        for i in self.contentview_id:
            print("Gathering Content view filters for Content view id: " + str(i))
            self.search("/katello/api/content_view/" + str(i) + "/filters", "cv_filter_cv" + str(i))

    # Gather Content view history
    def cv_history_list(self):
        for i in self.contentview_id:
            print("Gathering Content view history for Content view id: " + str(i))
            self.search("/katello/api/content_views/" + str(i) + "/history", "cv_history_cv" + str(i))

    # Gather Content view puppet modules
    def cv_puppet_modules_list(self):
        for i in self.contentview_id:
            print("Gathering Content view puppet modules for Content view id: " + str(i))
            self.search("/katello/api/content_views/" + str(i) + "/content_view_puppet_modules",
                        "cv_puppet_modules_cv" + str(i))

    # Gather all subscriptions assigned to each host
    def host_sub_list(self):
        for i in self.hosts_id:
            print("Gathering Host's subscriptions for Host id: " + str(i))
            self.search("/api/hosts/" + str(i) + "/subscriptions", "host_subscriptions_host" + str(i))

    # Gather all override values for smart variables
    def override_values_list(self):
        for i in self.smart_variable_id:
            print("Gathering override values for smart variable id: " + str(i))
            self.search("/api/smart_variables/" + str(i) + "/override_values", "override_values_sv" + str(i))


def main():
    if os.geteuid() == 0:
        parser = argparse.ArgumentParser()
        parser.add_argument("-a",
                            "--all",
                            help="Run all API calls from Satellite (This includes all options and will take a while)",
                            action="store_true")
        parser.add_argument("-e",
                            "--errata",
                            help="Collect errata only, this could take a while based on the repos you have enabled",
                            action="store_true")
        parser.add_argument("-u",
                            "--username",
                            dest="username",
                            help="Enter your username")
        parser.add_argument("-d",
                            "--destination",
                            dest="hostname",
                            help="Set the hostname for the Satellite server")
        parser.add_argument("-p",
                            "--password",
                            dest="password",
                            help="Set the password for the Satellite server")
        parser.add_argument("--content-view",
                            help="Collect API calls relevant to content view information",
                            action="store_true")
        parser.add_argument("--provision",
                            help="Collect API calls relevant to provisioning information",
                            action="store_true")
        parser.add_argument("-t",
                            "--test",
                            help="Test API call to the Satellite (organization call)",
                            action="store_true")
        args = parser.parse_args()

        a = ApiCall(args.hostname, args.username, args.password)
        b = pulp.Pulp_api(a.hostname, path=FULL_PATH)

        if args.all:
            ###########################
            #####INDEPENDENT CALLS#####
            ###########################
            a.organization_list()
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
            a.arch_list()
            a.audit_list()
            a.autosign_list()
            a.bookmark_list()
            a.common_parameters_list()
            a.compute_profiles()
            a.compute_resources()
            a.config_groups()
            a.config_reports()
            a.config_templates()
            a.containers_list()
            a.discovered_hosts()
            a.discovery_rules()
            a.user_role_filters()
            a.arf_reports()
            a.openscap_contents()
            a.gpgkey_list()
            a.rex_history_list()
            a.os_list()
            a.ostree_branches_list()
            a.permissions_list()
            a.recurring_logics()
            a.docker_registries()
            a.rex_features_list()
            a.reports_list()
            a.smart_proxy_list()
            a.smart_variables_list()
            a.statistics()
            a.template_kind_list()
            a.usergroup_list()
            a.contentview_filters()
            a.contentview_versions()
            a.docker_manifests()
            a.docker_tags()
            a.fact_values()
            a.smart_proxies_list()
            #############################
            #####DEPENDENT CALLS#########
            #############################
            a.activation_key_list()
            a.auth_source_ldap_list()
            a.content_views_list()
            a.puppet_environments_list()
            a.host_collection_list()
            a.hostgroups_list()
            a.hosts_lists()
            a.rex_templates_list()
            a.lce_list()
            a.media_list()
            a.products_list()
            a.provisioning_templates_list()
            a.partition_tables_list()
            a.subscription_list()
            a.manifest_history()
            a.sync_plan_list()
            a.uebercert_list()
            a.capsule_lce_assigned_list()
            a.capsule_lce_available_list()
            a.capsule_sync_status_list()
            a.cr_avail_img_list()
            a.cv_filter_list()
            a.cv_history_list()
            a.cv_puppet_modules_list()
            a.override_values_list()
            a.clean_up()
            a.rhst_upload()
        elif args.errata:
            a.errata_list()
            a.clean_up()
            a.rhst_upload()
        elif args.content_view:
            a.organization_list()
            a.location_list()
            a.capsule_list()
            a.errata_list()
            a.hammer_ping()
            a.user_roles_list()
            a.user_list()
            a.docker_registries()
            a.contentview_filters()
            a.contentview_versions()
            a.activation_key_list()
            a.content_views_list()
            a.hosts_lists()
            a.products_list()
            a.subscription_list()
            a.capsule_lce_assigned_list()
            a.capsule_sync_status_list()
            a.cv_filter_list()
            a.cv_history_list()
            a.cv_puppet_modules_list()
            a.clean_up()
            a.rhst_upload()
        elif args.provision:
            a.organization_list()
            a.location_list()
            a.capsule_list()
            a.domain_list()
            a.satellite_tasks_summary()
            a.hammer_ping()
            a.realms_list()
            a.settings_list()
            a.subnets_list()
            a.arch_list()
            a.compute_profiles()
            a.compute_resources()
            a.config_groups()
            a.config_reports()
            a.config_templates()
            a.discovered_hosts()
            a.discovery_rules()
            a.os_list()
            a.smart_proxy_list()
            a.template_kind_list()
            a.hostgroups_list()
            a.media_list()
            a.provisioning_templates_list()
            a.partition_tables_list()
            a.clean_up()
            a.rhst_upload()
        elif args.test:
            a.organization_list()
            b.get_task(FULL_PATH)
            b.get_consumers(FULL_PATH)
            b.get_orphaned_repos(FULL_PATH)
            b.get_repositories(FULL_PATH)
            a.clean_up()
            a.rhst_upload()

        else:
            ###########################
            #####INDEPENDENT CALLS#####
            ###########################
            a.organization_list()
            a.location_list()
            a.capsule_list()
            a.dashboard_details()
            a.domain_list()
            a.openscap_policy_list()
            a.satellite_tasks_summary()
            a.hammer_ping()
            a.realms_list()
            a.user_roles_list()
            a.settings_list()
            a.subnets_list()
            a.user_list()
            a.arch_list()
            a.audit_list()
            a.autosign_list()
            a.bookmark_list()
            a.common_parameters_list()
            a.compute_profiles()
            a.compute_resources()
            a.config_groups()
            a.config_templates()
            a.containers_list()
            a.discovered_hosts()
            a.discovery_rules()
            a.user_role_filters()
            a.arf_reports()
            a.openscap_contents()
            a.gpgkey_list()
            a.rex_history_list()
            a.os_list()
            a.ostree_branches_list()
            a.permissions_list()
            a.recurring_logics()
            a.docker_registries()
            a.rex_features_list()
            a.reports_list()
            a.smart_proxy_list()
            a.smart_variables_list()
            a.statistics()
            a.template_kind_list()
            a.usergroup_list()
            a.contentview_filters()
            a.contentview_versions()
            a.docker_manifests()
            a.docker_tags()
            a.fact_values()
            #############################
            #####DEPENDENT CALLS#########
            #############################
            a.activation_key_list()
            a.auth_source_ldap_list()
            a.content_views_list()
            a.puppet_environments_list()
            a.host_collection_list()
            a.hostgroups_list()
            a.hosts_lists()
            a.rex_templates_list()
            a.lce_list()
            a.media_list()
            a.products_list()
            a.provisioning_templates_list()
            a.partition_tables_list()
            a.subscription_list()
            a.manifest_history()
            a.sync_plan_list()
            a.uebercert_list()
            a.capsule_lce_assigned_list()
            a.capsule_lce_available_list()
            a.capsule_sync_status_list()
            a.cr_avail_img_list()
            a.cv_filter_list()
            a.cv_history_list()
            a.cv_puppet_modules_list()
            a.override_values_list()
            a.clean_up()
            a.rhst_upload()
    else:
        print("Please run as the root user.")



main()
