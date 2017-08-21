#!/usr/bin/env python

import requests

HOSTNAME = "https://batman.usersys.redhat.com"
SAT_ADMIN = "admin"
SAT_PW = 8144392

class apicall(object):

# I need a better understanding of the following function. Not entirely sure what it does.
    def __init__(self):
        pass

# Gather all Satellite organizations in a file
    def organization_list(self):
        ret = requests.get(HOSTNAME + "/katello/api/organizations", auth=(SAT_ADMIN, SAT_PW), verify=False)

# Check if request returns ok and status code of 200, then write contents to file
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('organization.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def location_list(self):
        ret = requests.get(HOSTNAME + "/api/locations", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('locations.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def capsule_list(self):
        ret = requests.get(HOSTNAME + "/katello/api/capsules", auth=(SAT_ADMIN, SAT_PW), verify=False)
        
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('capsules.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def dashboard_details(self):
        ret = requests.get(HOSTNAME + "/api/dashboard", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('dashboard.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def domain_list(self):
        ret = requests.get(HOSTNAME + "/api/domains", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('domains.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def errata_list(self):
        ret = requests.get(HOSTNAME + "/katello/api/errata", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('errata.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def openscap_policy_list(self):
        ret = requests.get(HOSTNAME + "/api/v2/compliance/policies", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('openscap_policies.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def satellite_tasks_summary(self):
        ret = requests.get(HOSTNAME + "/foreman_tasks/api/tasks/summary", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('satellite_tasks_summary.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code)) 

    def hammer_ping(self):
        ret = requests.get(HOSTNAME + "/katello/api/ping", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('hammer_ping.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def realms_list(self):
        ret = requests.get(HOSTNAME + "/api/realms", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('realms_list.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def user_roles_list(self):
        ret = requests.get(HOSTNAME + "/api/roles", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('user_roles.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def settings_list(self):
        ret = requests.get(HOSTNAME + "/api/settings", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('settings.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def subnets_list(self):
        ret = requests.get(HOSTNAME + "/api/subnets", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('subnets_list.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))

    def user_list(self):
        ret = requests.get(HOSTNAME + "/api/users", auth=(SAT_ADMIN, SAT_PW), verify=False)

        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                fw = open('user_list.json', 'w')
                fw.write(str(ret.json()))
                fw.close()
            else:
                return ret.text
        else:
            print("oops {}".format(ret.status_code))


#Call all functions
a = apicall()
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
