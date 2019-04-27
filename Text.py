# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACb9dab907e5aca735ea665f370251adb8'
auth_token = 'a1b4a34038512fe2569f0504710bf947'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Treat dispenser on!",
                     from_='+15023736897',
                     to='+15024925427'
                 )

print(message.sid)
