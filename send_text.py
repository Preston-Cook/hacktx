from twilio.rest import Client

account_SID = 'AC42cc81cdd317e5435f173da1cae30bd3'
auth_token = '443c7e49f126abdcbbda288c06ef9eb1'
my_phone = '+12678438063'

client = Client(account_SID, auth_token)

def send_message():
    message = client.messages.create(
        to='+19728377554',
        from_=my_phone,
        body='Hello from Python!'
    )