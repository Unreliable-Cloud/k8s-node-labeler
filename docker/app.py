from time import sleep
from kubernetes import client, config
import json
import yaml
import os

def main():
  config.load_incluster_config()
  api_instance = client.CoreV1Api()

  spotConfig   = 'spot-labels.yaml'
  workerConfig = 'worker-labels.yaml'
  spotLabels   = os.environ.get('SPOTS')
  workerLabels = os.environ.get('WORKERS')

  with open(spotConfig) as f:
    spot = yaml.load(f.read(), Loader=yaml.FullLoader)

  with open(workerConfig) as f:
    worker = yaml.load(f.read(), Loader=yaml.FullLoader)

  while True:
    try:
      spot_node_list = api_instance.list_node(label_selector=spotLabels)
      for node in spot_node_list.items:
          api_response = api_instance.patch_node(node.metadata.name, body=spot)
          print("%s\t%s" % (node.metadata.name, node.metadata.labels))
    except api_response.ApiException:
      raise Exception("Unable to patch node")

    try:
      worker_node_list = api_instance.list_node(label_selector=workerLabels)
      for node in worker_node_list.items:
          api_response = api_instance.patch_node(node.metadata.name, body=worker)
          print("%s\t%s" % (node.metadata.name, node.metadata.labels))
    except api_response.ApiException:
      raise Exception("Unable to patch node")

    sleep(60)

if __name__ == '__main__':
  main()
