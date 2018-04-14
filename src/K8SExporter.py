from kubernetes import client, config
import json
import yaml

namespace = "dev"

def getDeployment(baseString):
    v1 = client.AppsV1Api()
    print("Get Deployments with: " + baseString)
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    api_response = v1.list_namespaced_deployment(namespace, pretty='false', limit=10, timeout_seconds=10)
    items = api_response.items
    for item in items:
        deploymentName = item._metadata._name
        #print(deploymentName)
        if baseString in deploymentName:
            exportDeployment(deploymentName)
            
def exportDeployment(deploymentName):
    api_instance = client.AppsV1beta1Api()
    exact = True # bool | Should the export be exact.  Exact export maintains cluster-specific fields like 'Namespace'. (optional)
    export = True # bool | Should this value be exported.  Export strips fields that a user can not specify. (optional)
     
    api_response = api_instance.read_namespaced_deployment(deploymentName, namespace, pretty='true', exact=exact, export=export)
    convertToYAML(api_response.to_dict(), deploymentName+"-deployment")
    
def getService(baseString):
    api_instance = client.CoreV1Api()
    api_response = api_instance.list_namespaced_service(namespace, pretty='false', limit=10, timeout_seconds=10)
    items = api_response.items
    for item in items:
        serviceName = item._metadata._name
        #print(deploymentName)
        if baseString in serviceName:
            print('Found service:' + serviceName)
            exportService(serviceName)
    
    #print(api_response)
    
def exportService(serviceName):
    api_instance = client.CoreV1Api()
    api_response = api_instance.read_namespaced_service(serviceName, namespace, pretty='true', exact=True, export=True)
    convertToYAML(api_response.to_dict(), serviceName+"-service")
    
def removeNullValue(data):
    keysToRemove = []
    for key in data:
        value = data[key]
        if value is None:
            keysToRemove.append(key)
        if isinstance(value, dict):
            removeNullValue(value)
        if isinstance(value, list):
            removeNullsFromList(value)
    for aKey in keysToRemove:
        del data[aKey]
def removeNullsFromList(list):
    index = 0
    for element in list:
        if element is None:
            del list[index]
        if isinstance(element, dict):
            removeNullValue(element)
        index += 1

def convertToYAML(data, fileName):
    removeNullValue(data)
    with open(fileName+'.yml', 'w') as outfile:
        yaml.safe_dump(data, outfile, default_flow_style=False)
    

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

getDeployment("dev")
getService('dev')