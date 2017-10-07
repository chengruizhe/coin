########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

from slackclient import SlackClient

#client = SlackClient('xoxp-252836083635-252911914834-252852830323-7006c822107b7931c364b4af28c57ed4')
# slack_client.api_call("api.test")

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/x-www-form-urlencoded'
}


diction = {}
diction['token'] = 'xoxp-252836083635-252911914834-252852830323-7006c822107b7931c364b4af28c57ed4'
diction['name'] = 'study group'
params = urllib.parse.urlencode(diction)


conn = http.client.HTTPSConnection('slack.com/api/groups.create')

conn.request("POST", "?%s" % params, None, headers)


