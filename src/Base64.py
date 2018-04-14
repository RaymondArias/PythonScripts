'''
Script that base64 encodes and decodes strings 
Useful for creating k8s secrets
'''

import argparse 
import base64

#Encode input String
def encodeString(inputStr):
    return base64.b64encode(inputStr)

#Decode input string
def decodeString(inputStr):
    return base64.b64decode(inputStr)

#Turn input list of args into a string    
def convertToString(inputList):
    retStr = ''
    if len(inputList) == 1:
        return inputList[0]
    for string in inputList:
        retStr = retStr + string + ' '
    retStr = retStr.rstrip()
    return retStr    


parser = argparse.ArgumentParser(description='Base64')
parser.add_argument('input', action='store', nargs='+',
                   help='input value')
parser.add_argument('--decode','-d', action="store_true", help='decode value')

args = parser.parse_args()

inputList= args.input
inputStr = convertToString(inputList)

if not args.decode:
    print(encodeString(inputStr))
else:
    print(decodeString(inputStr))
    
