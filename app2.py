import random
from flask import Flask, request
from pymessenger.bot import Bot
from pprint import pprint

app = Flask(__name__)
ACCESS_TOKEN = 'EAAEhKs1vgJcBAEscpN8JE7qBdjiIdA8FkxOOQZBjat2lJNWTddnQ3b51gZBwCykS422uGs3ZBVJOZCrMZBD1MyYjfJKUsQiy3MFjhnYDcbIdVAsEmdxUp4qaWsSQEkpg0gwMZAylf0PaBtoa6i4HWdePVpPTUdgjILySlZB5o2tCXT5U5wxdSls'
VERIFY_TOKEN = 'hello'
bot = Bot(ACCESS_TOKEN)

# We will receive messages that Facebook sends our bot at this endpoint

recipients = set()
welcome_message = ['Welcome to InstaTickets', 'What ticket do you want to buy']


@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        pprint(output)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                print(message)
                if message.get('message'):
                    message_text = message['message'].get('text')
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message_text:
                        if recipient_id not in recipients:
                            recipients.add(recipient_id)
                            for msg in welcome_message:
                                send_message(recipient_id, msg, 'text')
                        else:
                            print(message_text)
                            response_sent_text = get_message(message_text)
                            send_message(recipient_id, response_sent_text, 'template')
                    # if user sends us a GIF, photo,video, or any other non-text item
                    # if message['message'].get('attachments'):
                    #     response_sent_nontext = get_message()
                    #     bot.send_generic_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# chooses a random message to send to the user
def get_message(message_text):
    element = [{'title': 'What tickets do you want',
    'buttons': [{
    'type': 'postback',
    'title': 'buy tickeet',
    'text': 'Buy Ticket'
    }]
    }]
    sample_responses = ["Welcome to Gcl!", "Gcl is proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    # return random.choice(sample_responses)
    return sample_responses


# uses PyMessenger to send response to user
def send_message(recipient_id, response, formats):
    # sends user the text message provided via input response parameter
    if formats == 'text':
        bot.send_text_message(recipient_id, response)
    else:
        bot.send_quick_replies_message(recipient_id='recipient_id', text='choose', quick_replies=response)
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
