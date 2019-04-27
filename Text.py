# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Treat dispenser on!",
                     from_='',
                     to=''
                 )

print(message.sid)
