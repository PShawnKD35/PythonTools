# Name: Get Different things from iDesk
# Version: 1.0.0
# Author: Shawn Peng
# Email: shawn.peng1@ikea.com / shawn-peng@outlook.com

import requests
import json
import urllib3
import threading

class iDesk:

    __username = None
    __password = None
    __jwt = None
    __separator = "======================"

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def getOwner(self,incident):
        owner = "Unknown"
        url = "https://intars4.ikea.com/api/arsys/v1/entry/HPD:Help%20Desk"
        querystring = "/?q='Incident%20Number'=\"" + incident + "\"&fields=values(Owner%20Login%20ID,Owner)"
        headers = {
            'authorization': self.__jwt,
            'cache-control': "no-cache"
            }
        response = requests.request("GET", url+querystring, headers=headers, verify=False)
        if response.encoding == None:
            response.encoding = "utf-8"
        if response.ok:
            obj = json.loads(response.text)
            entries = None
        else:
            owner = response.text

        try:
            entries = obj['entries']
            if entries.count != 0 : #会有问题
                owner = entries[0]['values']['Owner']
        except Exception:
            return
        finally:
            print("%s\t%s" % (incident, owner))

    def getFullName(self,networkId):
        name = "Unknown"
        url = "https://intars4.ikea.com/api/arsys/v1/entry/CTM:People"
        querystring = "?q='Remedy%20Login%20ID'=\"" + networkId + "\"&fields=values(Full%20Name)"
        headers = {
            'authorization': self.__jwt,
            'cache-control': "no-cache"
            }
        response = requests.request("GET", url+querystring, headers=headers, verify=False)
        if response.encoding == None:
            response.encoding = "utf-8"
        if response.ok:
            obj = json.loads(response.text)
            entries = None
        else:
            name = response.text
        
        try:
            entries = obj['entries']
            if entries.count != 0 : #会有问题
                name = entries[0]['values']['Full Name']
        except Exception:
            return
        finally:
            print(networkId + "\t" + name)


    def login(self):
        url = "https://intars4.ikea.com/api/jwt/login"
        payload = "username=%s&password=%s" % (self.__username, self.__password)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
            }
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        if response.ok:
            self.__jwt = "AR-JWT " + response.text
            print('Login succeeded.')
        else:
            print("Login failed: " + response.text)
        print(self.__separator)
        return response.ok, response.text

    def logout(self):
        url = "https://intars4.ikea.com/api/jwt/logout"
        headers = {
            'authorization': self.__jwt,
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, headers=headers, verify=False)
        print(self.__separator)
        if response.ok:
            self.__jwt = None
            print("Logged out.")
        else:
            print("Logging out failed:" + response.text)
        return response.ok, response.text

    def BulkGetInfo(self, method, inputParamName):
        # Disable Https secure warning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        inputParams = []
        print('Please input all the %s separated by lines. Ending by double carriage...' % inputParamName)
        inputline = input()

        while inputline != '':
            inputParams.append(inputline)
            inputline = input()

        #login
        result = self.login()
        if result[0]:
            threads = []
            for inputParam in inputParams:
                # Do things
                thread = threading.Thread(target=method,args=(inputParam,))
                thread.start()
                threads.append(thread)
            # Wait for completion
            for thread in threads:
                thread.join()
            #logout
            result = self.logout()
        print("Press anything to exit...")
        input()


## Do the real things by calling the class and methods
#idesk = iDesk("username","password")
#idesk.BulkGetInfo(idesk.getFullName, "Network ID")