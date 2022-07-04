from time import sleep
from kubernetes import client, config
from threading import Thread
from leaderelection import Elect
import json
import yaml
import os

def main():
  if os.path.isdir("/var/run/secrets/kubernetes.io"):
    config.load_incluster_config()
  else:
    config.load_config()
  api_instance   = client.CoreV1Api()
  leaderelection = Elect(configmap='node-labeler-leader-election')
  le             = Thread(target=leaderelection.run)
  
  le.setDaemon(True)
  le.start()

  spotConfig   = 'spot-labels.yaml'
  workerConfig = 'worker-labels.yaml'
  spotLabels   = os.environ.get('SPOTS')
  workerLabels = os.environ.get('WORKERS')
  logObject    = {}

  with open(spotConfig) as f:
    spot = yaml.load(f.read(), Loader=yaml.FullLoader)

  with open(workerConfig) as f:
    worker = yaml.load(f.read(), Loader=yaml.FullLoader)

  while True:
    leader = leaderelection.check_leader()
    if leader:
      logObject['message'] = "I am the leader with the lock"
      print(json.dumps(logObject))
      try:
        spot_node_list = api_instance.list_node(label_selector=spotLabels)
        for node in spot_node_list.items:
            api_response               = api_instance.patch_node(node.metadata.name, body=spot)
            node                       = node.metadata.name
            logObject['nodeName']      = node
            logObject['labelSelector'] = spotLabels
            logObject['message']       = "Set spot-worker label for " + node
            logOut                     = json.dumps(logObject)
            print(logOut)
      except api_response.ApiException:
        raise Exception("Unable to patch node")

      try:
        worker_node_list = api_instance.list_node(label_selector=workerLabels)
        for node in worker_node_list.items:
            api_response               = api_instance.patch_node(node.metadata.name, body=worker)
            node                       = node.metadata.name
            logObject['nodeName']      = node
            logObject['labelSelector'] = workerLabels
            logObject['message']       = "Set worker label for " + node
            logOut                     = json.dumps(logObject)
            print(logOut)
      except api_response.ApiException:
        raise Exception("Unable to patch node")
    else:
      sleepTime = 10
      logObject['message'] = "I am not the leader with the lock. Trying again in " + sleepTime + " seconds"
      print(json.dumps(logObject))
      sleep(sleepTime)

    sleep(60)

if __name__ == '__main__':
  main()
