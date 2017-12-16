import gps_satellite as gps
from requests import Session


class Pulp_api(object):

    def __init__(self):
        self.session = Session()
        self.user = gps.subprocess.Popen("grep ^default_login /etc/pulp/server.conf | cut -d' ' -f2", shell=True)
        self.pw = gps.subprocess.Popen("grep ^default_password /etc/pulp/server.conf | cut -d' ' -f2", shell=True)
        self.session.auth = (self.user, self.pw)
        self.session.verify = False
        self.gps = gps.ApiCall()

    def search(self, call=None, name=None):
        """Request API queried information"""
        ret = self.session.get(self.gps.hostname + call)
        if ret.ok and ret.status_code == 200:
            if 'json' in ret.headers.get('Content-Type'):
                if not gps.os.path.exists(gps.FULL_PATH):
                    gps.os.makedirs(gps.FULL_PATH)
                    gps.os.chdir(gps.FULL_PATH)
                fw = open(name + '.json', 'w')
                content = ret.content
                fw.write(content)
                fw.close()
            else:
                return ret.text
        else:
            print("Return {}, content not available".format(ret.status_code))

    def get_task(self):
        print("Gathering all Pulp tasks")
        self.search("/pulp/api/v2/tasks/", "Pulp tasks")
