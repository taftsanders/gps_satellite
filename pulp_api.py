from requests import Session
import subprocess
import os
import pdb


class Pulp_api():

    def __init__(self, hostname=None, path=None):
        self.session = Session()
        selection = raw_input("Are you executing gps-satellite on the Satellite server?[Y/N]")
        selection.upper()
        if selection == 'Y':
            command1 = ['grep', '^default_login', '/etc/pulp/server.conf']
            command2 = ['cut', '-d', ' ', '-f2']
            command3 = ['grep', '^default_password', '/etc/pulp/server.conf']
            self.line1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
            self.line2 = subprocess.Popen(command3, stdout=subprocess.PIPE)
            self.line3 = subprocess.Popen(command2, stdin=self.line1.stdout, stdout=subprocess.PIPE)
            self.line4 = subprocess.Popen(command2, stdin=self.line2.stdout, stdout=subprocess.PIPE)
            self.user = self.line3.stdout.read().strip()
            self.pw = self.line4.stdout.read().strip()
        else:
            self.user = raw_input("Enter the pulp username (Found on the Satellite /etc/pulp/server.conf: ")
            self.pw = raw_input("Enter the pulp password (Found on the Satellite /etc/pulp/server.conf: ")
        self.hostname = hostname
        self.session.auth = (self.user, self.pw)
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