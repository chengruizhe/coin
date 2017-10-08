import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
#from slackclient import SlackClient

def createnewgp(nam, userids):

	headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/x-www-form-urlencoded'
	}


	tok = 'xoxp-252836083635-252911914834-253218659397-9766ea294cc2252ba732834addf07a9d'
	conn = http.client.HTTPSConnection('slack.com')

	diction = {}
	diction['token'] = tok
	diction['name'] = nam
	params = urllib.parse.urlencode(diction)

	conn.request("POST", "/api/groups.create?%s" % params, None, headers)
	response = conn.getresponse()
	data = response.read()

	dataDic = json.loads(data.decode('utf8'))
	# print (dataDic)
	gp_id = dataDic["group"]["id"]
	nam2 = gp_id

	for u in userids:

		dict2 = {}
		dict2['token'] = tok
		dict2['channel'] = nam2
		dict2['user'] = u
		params2 = urllib.parse.urlencode(dict2)

		conn.request("POST", "/api/groups.invite?%s" % params2, None, headers)
		response = conn.getresponse()
		data = response.read()
		# print(data)

	dict3 = {}
	dict3['token'] = tok
	dict3['channel'] = nam2
	params3 = urllib.parse.urlencode(dict3)

	conn.request("POST", "/api/groups.info?%s" % params3, None, headers)
	response = conn.getresponse()

	group_data = response.read()
	print(group_data)



	return "https://teamcoin4.slack.com/messages/" + nam2