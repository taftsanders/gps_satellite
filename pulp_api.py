from requests import Session
import subprocess
import os
import pdb



class Pulp_api():

    def __init__(self,hostname=None, path=None):
        self.session = Session()
        command1 = ['grep', '^default_login', '/etc/pulp/server.conf']
        command2 = ['cut', '-d', ' ', '-f2']
        command3 = ['grep', '^default_password', '/etc/pulp/server.conf']
        self.line1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
        self.line2 = subprocess.Popen(command3, stdout=subprocess.PIPE)
        self.line3 = subprocess.Popen(command2, stdin=self.line1.stdout, stdout=subprocess.PIPE)
        self.line4 = subprocess.Popen(command2, stdin=self.line2.stdout, stdout=subprocess.PIPE)
        self.user = self.line3.stdout.read().strip()
        self.pw = self.line4.stdout.read().strip()
        self.hostname = hostname
        self.session.auth = (self.user, self.pw)
        self.session.verify = False
        self.path = path

    def search(self, call=None, name=None):
        """Request API queried information"""
        #pdb.set_trace()
        ret = self.session.get(self.hostname + call + '?per_page=2000000')
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                    os.chdir(self.path)
                fw = open(name + '.json', 'w')
                content = ret.content
                fw.write(content)
                fw.close()
            else:
                return ret.text
        else:
            print("Return {}, content not available".format(ret.status_code))

    def get_task(self, path):
        print("Gathering all Pulp tasks")
        self.search("/pulp/api/v2/tasks/", "Pulp tasks")
