from time import sleep
import uuid
from threading import Thread
import json
import yaml
import os
from kubernetes import client, config
from kubernetes.leaderelection import leaderelection, electionconfig
from kubernetes.leaderelection.resourcelock.configmaplock import ConfigMapLock

if os.path.isdir("/var/run/secrets/kubernetes.io"):
  config.load_incluster_config()
  lock_namespace = os.environ.get('NAMESPACE')
else:
  config.load_config()
  lock_namespace = "kube-system"

api_instance   = client.CoreV1Api()
spotConfig     = 'spot-labels.yaml'
workerConfig   = 'worker-labels.yaml'
spotLabels     = os.environ.get('SPOTS')
workerLabels   = os.environ.get('WORKERS')
candidate_id   = uuid.uuid4()
lock_name      = "node-labeler-leader-election"
logObject      = {}

def main():
  leaseConfig    = electionconfig.Config(ConfigMapLock(lock_name, lock_namespace, candidate_id), lease_duration=15,
                                         renew_deadline=10, retry_period=5, onstarted_leading=startLeader,
                                         onstopped_leading=endLeader)

  startElection = leaderelection.LeaderElection(leaseConfig)
  th            = Thread(target=startElection.run())
  th.setDaemon(True)
  th.start()

def endLeader():
    logObject['info'] = "I not am the leader with the lock"
    logOut            = json.dumps(logObject)
    print(logOut)

def startLeader():
  logObject['info'] = "I am the leader with the lock"
  logOut            = json.dumps(logObject)

  with open(spotConfig) as f:
    spot = yaml.load(f.read(), Loader=yaml.FullLoader)

  with open(workerConfig) as f:
    worker = yaml.load(f.read(), Loader=yaml.FullLoader)

  print(logOut)

  while True:
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
    sleep(60)

if __name__ == '__main__':
  main()
