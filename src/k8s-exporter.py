from kubernetes import client, config
import json
import yaml
from Tix import Form

namespace = "dev"

def getDeployment(baseString):
    v1 = client.AppsV1Api()
    print("Get Deployments with: " + baseString)
    api_response = v1.list_namespaced_deployment(namespace, pretty='false', limit=10, timeout_seconds=10)
    items = api_response.items
    for item in items:
        deploymentName = item._metadata._name
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
        if baseString in serviceName:
            print('Found service:' + serviceName)
            exportService(serviceName)

def exportService(serviceName):
    api_instance = client.CoreV1Api()
    api_response = api_instance.read_namespaced_service(serviceName, namespace, pretty='true', exact=True, export=True)
    convertToYAML(api_response.to_dict(), serviceName+"-service")
    
def getSecret(baseString):
    api_instance = client.CoreV1Api()
    api_response = api_instance.list_namespaced_secret(namespace, pretty='false', limit=10, timeout_seconds=10)
    items = api_response.items
    for item in items:
        secretName = item._metadata._name
        if baseString in secretName:
            print('Found secret:' + secretName)
            exportSecret(secretName)

def exportSecret(secretName):
    api_instance = client.CoreV1Api()
    api_response = api_instance.read_namespaced_secret(secretName, namespace, pretty='true', exact=True, export=True)
    convertToYAML(api_response.to_dict(), secretName+"-secret")
    
def removeNullValue(data):
    keysToRemove = []
    for key in data:
        value = data[key]
        if value is None:
            keysToRemove.append(key)
        if isinstance(value, dict):
            removeNullValue(value)
            formatKeys(value)
        if isinstance(value, list):
            removeNullsFromList(value)
    for aKey in keysToRemove:
        del data[aKey]

def replaceKey(dict, keyDict):
    for key in keyDict:
        dict[keyDict[key]] = dict[key]
        del dict[key]
        
def formatKeys(dict):
    oldToNewKey = {}
    for key in dict:
        if '_' in key:
            splitString = key.split('_')
            k8sFormattedString = splitString[0]
            for i in range(len(splitString)):
                if i == 0:
                    continue
                letter = splitString[i][0]
                letter = letter.upper()
                stringList = list(splitString[i])
                stringList[0] = letter
                splitString[i] = ''.join(stringList)
                k8sFormattedString += splitString[i]
            oldToNewKey[key] = k8sFormattedString
    replaceKey(dict, oldToNewKey)
    
def removeNullsFromList(list):
    index = 0
    for element in list:
        if element is None:
            del list[index]
        if isinstance(element, dict):
            print(element)
            removeNullValue(element)
            formatKeys(element)
        index += 1

def convertToYAML(data, fileName):
    formatKeys(data)
    removeNullValue(data)
    with open('../output/'+fileName+'.yml', 'w') as outfile:
        yaml.safe_dump(data, outfile, default_flow_style=False)
    

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

getDeployment("dev")
getService('dev')
getSecret('dev')