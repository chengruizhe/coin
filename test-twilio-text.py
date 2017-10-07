from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC988731522e19cb52edb53ae06bd285f2"
# Your Auth Token from twilio.com/console
auth_token  = "aa37a11d869eee40c5ede1bd638215b4"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+14159069366",
    from_="+12068861058 ",
    body="Hello from Python!")

print(message.sid)
