from time import sleep
from kubernetes import client, config
import json

def main():
  config.load_incluster_config()
  api_instance = client.CoreV1Api()

  spotConfig = 'spot-labels.conf'
  workerConfig = 'worker-labels.conf'

  with open(spotConfig) as f:
    spot = json.loads(f.read())

  with open(workerConfig) as f:
    worker = json.loads(f.read())

  try:
    spot_node_list = api_instance.list_node(label_selector="cloud.google.com/gke-spot=true")
    for node in spot_node_list.items:
        api_response = api_instance.patch_node(node.metadata.name, body=spot)
        print("%s\t%s" % (node.metadata.name, node.metadata.labels))
  except api_response.ApiException:
    raise Exception("Unable to patch node")

  try:
    worker_node_list = api_instance.list_node()
    for node in worker_node_list.items:
        api_response = api_instance.patch_node(node.metadata.name, body=worker)
        print("%s\t%s" % (node.metadata.name, node.metadata.labels))
  except api_response.ApiException:
    raise Exception("Unable to patch node")

if __name__ == '__main__':
  while True:
    main()
    sleep(60)