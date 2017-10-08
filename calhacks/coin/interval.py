import os, base64
def getResult(img):
    ########### Python 3.2 #############
    import http.client, urllib.request, urllib.parse, urllib.error, sys

    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f490e3d2d928423d9bec87f85b15809a',
    }

    params = urllib.parse.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    # body = "{ 'url': '" + imgURL + "' }"
    body = img   # Takes binary

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print(e.args)
    ####################################

# Six lines that follows need implementation
def uploadImage():  # Uploads the current keyframe
    return
def getImage():     # Gets the current keyframe from webcam
    PATH = '/Users/ryancheng/Desktop/calhacks/coin/media/monitor/status.png'
    # from PIL import Image
    # img = Image.open(PATH)
    with open(PATH, 'rb') as file:
        img = file.read()
    return img
def getFlag():      # Gets the boolean flag whether the current session has terminated: True if terminated
    PATH = '/Users/ryancheng/Desktop/calhacks/coin/media/monitor/status.txt'
    if os.path.isfile(PATH):
        return True
    else:
        return False

import time, json
import matplotlib.pyplot as plt

delay = 3

def run():
    flag = True
    t0 = time.time()

    taxis = []
    anger, contempt, disgust, fear, happiness, neutral, sadness, surprise = [[] for i in range(8)]

    while flag:
        if getFlag():
            flag = False
            continue

        img = getImage()
        if not img:
            continue

        """
        imgURL = uploadImage(img)
        if not imgURL:
            continue
        """

        # result = json.loads(img).decode("utf8")
        result = json.loads(getResult(img).decode("utf8"))
        taxis.append(time.time() - t0)
        print("result")
        print(result)
        angert,contemptt, disgustt, feart, happinesst, neutralt, sadnesst, surpriset = [0 for i in range(8)]
        for i in range(len(result)):
            angert += result[i]['scores']['anger']
            contemptt += result[i]['scores']['contempt']
            disgustt += result[i]['scores']['disgust']
            feart += result[i]['scores']['fear']
            happinesst += result[i]['scores']['happiness']
            neutralt += result[i]['scores']['neutral']
            sadnesst += result[i]['scores']['sadness']
            surpriset += result[i]['scores']['surprise']
        anger.append(angert / len(result))
        contempt.append(contemptt / len(result))
        disgust.append(disgustt / len(result))
        fear.append(feart / len(result))
        happiness.append(happinesst / len(result))
        neutral.append(neutralt / len(result))
        sadness.append(sadnesst / len(result))
        surprise.append(surpriset / len(result))

        plt.plot(anger, taxis)
        plt.plot(contempt, taxis)
        plt.plot(disgust, taxis)
        plt.plot(fear, taxis)
        plt.plot(happiness, taxis)
        plt.plot(neutral, taxis)
        plt.plot(sadness, taxis)
        plt.plot(surprise, taxis)
        plt.legend(['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise'], loc='upper left')
        plt.savefig('/Users/ryancheng/Desktop/calhacks/coin/media/emotion/emotions.png')

        time.sleep(delay)

    return True