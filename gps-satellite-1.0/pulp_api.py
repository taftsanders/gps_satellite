from requests import Session
import subprocess
import os
import pdb


class Pulp_api():

    def __init__(self, hostname=None, path=None):
        self.session = Session()
        selection = raw_input("Are you executing gps-satellite on the Satellite server?[Y/N]")
        if selection.upper() == 'Y':
            with open('/etc/pulp/server.conf', 'r') as pulpconfigfile:
                pulpconfiglines = pulpconfigfile.readlines()
            passwordline = [ l.strip() for l in pulpconfiglines if l.startswith('default_password:') ]
            passwordline = passwordline[0]
            pulp_pw = passwordline.split()[1]
            self.pulp_pw = pulp_pw
            self.pulp_user = 'admin'

        else:
            self.pulp_user = raw_input("Enter the pulp username (Found on the Satellite /etc/pulp/server.conf: ")
            self.pulp_pw = raw_input("Enter the pulp password (Found on the Satellite /etc/pulp/server.conf: ")
        self.hostname = hostname
        self.session.auth = (self.pulp_user, self.pulp_pw)
        self.session.verify = False
        self.path = path

    def search(self, call=None, name=None):
        """Request API queried information"""
        ret = self.session.get(self.hostname + call + '?per_page=2000000')
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                    os.chdir(self.path)
                with open(name + '.json', 'w') as fw:
                    content = ret.content
                    fw.write(content)
            else:
                return ret.text
        else:
            print("Return {}, content not available".format(ret.status_code))

    def get_task(self, path):
        print("Gathering all Pulp tasks")
        self.search("/pulp/api/v2/tasks/", "pulp_tasks")

    def get_consumers(self, path):
        print("Gathering all Pulp consumers")
        self.search("/pulp/api/v2/consumers/", "pulp_consumers")

    def get_repositories(self, path):
        print("Gathering all Pulp repositories")
        self.search("/pulp/api/v2/repositories/", "pulp_repositories")

    def get_orphaned_repos(self, path):
        print("Gathering all Orphaned Pulp repositories")
        self.search("/pulp/api/v2/content/orphans/", "orphaned_repositories")