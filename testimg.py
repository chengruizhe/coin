


########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import time
import matplotlib.pyplot as plt

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'f490e3d2d928423d9bec87f85b15809a',
}

params = urllib.parse.urlencode({
})

# Replace the example URL below with the URL of the image you want to analyze.
body = "{ 'url': 'https://tupian.baidu.com/search/down?tn=download&word=download&ie=utf8&fr=detail&url=https%3A%2F%2Ftimgsa.baidu.com%2Ftimg%3Fimage%26quality%3D80%26size%3Db9999_10000%26sec%3D1507391073325%26di%3D92c482dcc025f69b7b2e22015dcf8fd2%26imgtype%3D0%26src%3Dhttp%253A%252F%252Fimgsrc.baidu.com%252Fimage%252Fc0%25253Dshijue1%25252C0%25252C0%25252C294%25252C40%252Fsign%253Df9058992de3f8794c7f2406dba726481%252Fa5c27d1ed21b0ef47095f274d7c451da81cb3e9e.jpg&thumburl=https%3A%2F%2Fss0.bdstatic.com%2F70cFvHSh_Q1YnxGkpoWK1HF6hhy%2Fit%2Fu%3D2220107433%2C3991199515%26fm%3D200%26gp%3D0.jpg' }"

try:
    # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
    #   URL below with "westcentralus".
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    result = json.loads(data.decode("utf8"))

    t0 = time.time()
    taxis = []
    anger, contempt, disgust, fear, happiness, neutral, sadness, surprise = [[] for i in range(8)]
    taxis.append(time.time() - t0)
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
    anger.append(angert)
    contempt.append(contemptt)
    disgust.append(disgustt)
    fear.append(feart)
    happiness.append(happinesst)
    neutral.append(neutralt)
    sadness.append(sadnesst)
    surprise.append(surpriset)

    plt.plot(anger, taxis)
    plt.plot(contempt, taxis)
    plt.plot(disgust, taxis)
    plt.plot(fear, taxis)
    plt.plot(happiness, taxis)
    plt.plot(neutral, taxis)
    plt.plot(sadness, taxis)
    plt.plot(surprise, taxis)
    plt.legend(['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise'], loc='upper left')
    plt.savefig('emotions.png')

    conn.close()
except Exception as e:
    print(e.args)
####################################
