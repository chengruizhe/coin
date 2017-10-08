import http.client, urllib.request, urllib.parse, urllib.error, base64, json

class FaceAPI():

    def __init__(self):
        self.KEY = 'e9fed229e33c4950ba28d8630d7bc282'

    #takes groupID, groupName, groupData
    def createPersonGroup(self, groupID, groupName, groupData):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.KEY,
        }

        body = {
           "name":groupName,
            "userData":groupData
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("PUT", "/face/v1.0/persongroups/" + str(groupID) + "?%s" % params, json.dumps(body), headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    #takes name, personData, groupId, returns peronsID
    def addPersonToGroup(self, name, personData, groupID):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.KEY,
        }

        body = {
           "name": name,
            "userData": personData
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/persongroups/" + str(groupID) + "/persons?%s" % params, json.dumps(body), headers)
            response = conn.getresponse()
            data = response.read()
            dataDic = json.loads(data.decode('utf8'))
            personID = dataDic["personId"]
            print(data)
            conn.close()
            return personID
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    #returns persisted face Id
    def addFaceToPerson(self, groupID, personID, url):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.KEY,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'userData': '{string}',
            'targetFace': '',
        })

        body = {"url": url}

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST",
                         "/face/v1.0/persongroups/"+str(groupID)+"/persons/"+personID+"/persistedFaces?%s" % params,
                         json.dumps(body), headers)
            response = conn.getresponse()
            data = response.read()
            dataDic = json.loads(data.decode('utf8'))
            persistedFaceId = dataDic["persistedFaceId"]
            print(data)
            conn.close()
            return persistedFaceId
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def identifyFace(self, faceIds, groupID):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.KEY,
        }

        params = urllib.parse.urlencode({
        })

        body = {
            "personGroupId": groupID,
            "faceIds": faceIds,
            "maxNumOfCandidatesReturned": 1,
            "confidenceThreshold": 0.5
        }

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/identify?%s" % params, json.dumps(body), headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def detectFace(self, binaryImage):
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.KEY,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': '',
        })

        body = binaryImage

        try:
            conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/detect?%s" % params, binaryImage, headers)
            response = conn.getresponse()
            data = response.read()
            dataList = json.loads(data.decode('utf8'))
            faceIds = []
            faceRectangles = {}
            print ("hahahahahahahahahahahahahahahahahah")
            print(dataList)
            for image in dataList:
                faceIds.append(image['faceId'])
                faceRectangles[image['faceId']] = image["faceRectangle"]
            print(data)
            conn.close()
            return faceIds, faceRectangles
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

#service = FaceAPI()
#service.createPersonGroup(1,"Group1", "Class1")
#personID = service.addPersonToGroup("Henry Ang", "lol", 1)
#henryImage = "https://s3.amazonaws.com/coin4/1.jpeg"
#service.addFaceToPerson(1, personID, henryImage)
# detected = service.detectFace("https://s3.amazonaws.com/coin4/realHenry.JPG")
# service.identifyFace(detected, 1)
# detected = service.detectFace("https://s3.amazonaws.com/coin4/rnb.jpeg")
# service.identifyFace(detected, 1)
