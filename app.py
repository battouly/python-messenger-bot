#Python libraries that we need to import for our bot
import os, random, json
from flask import Flask, request, session
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN', default=None)
#ACCESS_TOKEN= 'EAADzRRZAmHuUBAEGDCTIC8wwZAPmZAaSk1GTrMFy27CbX42vv9GD6dxpjpCfo98ZCe37AWYUaMNyvTmhVWFqZC7vBilufuIC7gxpWZAwZBncJSx91A7MjvlE9fF6HjgWLU382o7mWCvMScejbFV38bLDPtQd6EP2gFIjANlZA9AQMDP71NjXkAlx'
VERIFY_TOKEN = 'hello'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       data = request.get_json()
       for event in data['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning! <3 ", "Keep on being you! (y)", "We're greatful to know you :)", "Aww I'm proud of you. <3 <3 <3"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run(port=8080 , host='0.0.0.0', debug=True)
    
    
# http://wiki.nginx.org/Pitfalls
# http://wiki.nginx.org/QuickStart
# http://wiki.nginx.org/Configuration