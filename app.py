import os
from flask import Flask, request
from fbmessenger import BaseMessenger
from fbmessenger import quick_replies, elements, templates
from fbmessenger.elements import Text
from fbmessenger.thread_settings import GreetingText, GetStartedButton, MessengerProfile

tickets = ['Movie Tickets', 'Event Tickets']

scrap = None


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
    	from scrap import index
    	self.movies = index()
    	self.page_access_token = 'EAAEhKs1vgJcBAEscpN8JE7qBdjiIdA8FkxOOQZBjat2lJNWTddnQ3b51gZBwCykS422uGs3ZBVJOZCrMZBD1MyYjfJKUsQiy3MFjhnYDcbIdVAsEmdxUp4qaWsSQEkpg0gwMZAylf0PaBtoa6i4HWdePVpPTUdgjILySlZB5o2tCXT5U5wxdSls'
    	self.j = 0
    	self.saved_response = []
    	self.movie_responses = {
    	'Cinema': ['Genesis Deluxe', 'Film House'],
    	'Location': [['Psalm', 'Leisure Mall', 'Maryland'], ['Ikeja', 'Ojota']],
    	'Movie Type': ['New Releases', 'Movies Showing Today', 'Movies Showing In 7 Days', 'Coming Soon'],
    	'Movies': [title for title in self.movies[2]]
    	}
    	self.questions = ['Select Cinema', 'Select Location', 'Select Movie Type', 'Select Movie']
    	self.questions_check = {'Select Cinema': 'quick', 'Select Location':'quick', 'Select Movie Type': 'quick', 'Select Movie': 'carousel'}
    	super(Messenger, self).__init__(self.page_access_token)


    def message(self, message):
        print('message')
        print(message)                
        get_sender = Text(text= str(message['sender']['id']))
        get_text = Text(text= str(message['message']['text']))
        try:
        	chck_payload = Text(text= str(message['message']['quick_reply']['payload']))
        except KeyError:
        	chck_payload = 'text'
        text = get_text.to_dict()
        text = text['text']
        check = self.read(text, chck_payload)
        print(check)
        # problem hereeeee
        if check != 2:
        	print('check')
        	response = self.movie_route()
        	if self.questions_check[response[0]] == 'quick':
        		print(response)
        		quick_reply = [quick_replies.QuickReply(title=i, payload='quick') for i in response[1]]
        		quick_reply += [quick_replies.QuickReply(title='Go back', payload='quick')]
        		quick_replies_set = quick_replies.QuickReplies(quick_replies=quick_reply)
        		text = { 'text': response[0]}
        		text['quick_replies'] = quick_replies_set.to_dict()
        		self.send(text, 'RESPONSE')
        	else:
        		text = {'text': response[0]}
        		self.send(text, 'RESPONSE')
        		print('carousel')
        		print(self.movies)
        		elems  = []
        		i = 0
        		while i < len(self.movies[0]):
        			btn = elements.Button(title='Read More', payload=movies[2][i], button_type='postback')
        			elem = elements.Element(
        				title=self.movies[2][i],
        				image_url=self.movies[0][i],
        				subtitle=self.movies[1][i],
        				buttons=[
        					btn
        				]
        				)
        			elems.append(elem)
        			i+=1
        		res = templates.GenericTemplate(elements=elems)        		
        		messenger.send(res.to_dict(), 'RESPONSE')
	        	quick_reply = [quick_replies.QuickReply(title='Go back', payload='quick')]
	        	quick_replies_set = quick_replies.QuickReplies(quick_replies=quick_reply)
	        	default = {'quick_replies': quick_replies_set.to_dict()}
	        	self.send(default, 'RESPONSE')
        		print(self.movie_responses['Movies'])


    def movie_route(self):
    	to_reply = ''
    	to_ask = self.questions[self.j]
    	for msg, reply in self.movie_responses.items():
    		if msg in to_ask:
    			to_reply = reply
    			break
    	try:
    		if 'Genesis' in self.saved_response[-1]:
    			to_reply = to_reply[0]
    		elif 'Film' in self.saved_response[-1]:
    			to_reply = to_reply[1]
    	except IndexError:
    		pass
    	return to_ask, to_reply


    def delivery(self, message):
        pass


    def go_back(self, message):
    	if self.j == 0 or len(self.saved_response) == 0:
    		self.postback(message.title())
    		return
    	print(self.j, len(self.saved_response))
    	try:
    		self.j -= 1
    		self.saved_response.pop()
    	except IndexError:
    		print('')


    def read(self, message, payload):    	
    	valid = False
    	text = message.title()
    	chck_payload = payload
    	if text not in tickets and len(self.saved_response) == 0:
    		self.send({'text': 'Please follow the thread '}, 'RESPONSE')
    		self.postback(text)
    		valid = 2
    		return valid
    	elif text in tickets:
    		print('in')
    		self.saved_response.append(text)
    	elif text == 'Go Back':    		
    		self.go_back(text)
    		valid = True if len(self.saved_response) > 1 else 'no'
    		print(valid)
    		return valid
    	else:
    		for i in self.movie_responses:        	        	
    			if text in self.movie_responses[i]:
    				valid = True
    				break        	
    			b = any(isinstance(el, list) for el in self.movie_responses[i])
    			if b is True:
    				flat_list = [item for sublist in self.movie_responses[i] for item in sublist]
    				if text in flat_list:
    					valid = True
    					break
    			else:    			
    				valid = False    		
    		if valid is False:
    			self.send({'text': 'i didnt get that please follow the thread'}, 'RESPONSE')
    		print('not in')
    		print(valid)
    	if valid is True:
    		self.j += 1
    		self.saved_response.append(text)    	    		
    	return valid

    def account_linking(self, message):
        pass

    def postback(self, message):
    	print('postback')
    	try:
    		payload = message['postback']['payload']
    	except Exception as e:
    		payload = message
    	if 'start' in payload:
    		text = { 'text': 'Welcome to InstaTickets'}
    		self.send(text, 'RESPONSE')
    		quick_reply_1 = quick_replies.QuickReply(title='Movie Tickets', payload='first')
    		quick_reply_2 = quick_replies.QuickReply(title='Event Tickets', payload='first')
    		quick_reply_3 = quick_replies.QuickReply(title='Quit', payload='quit')
    		quick_replies_set = quick_replies.QuickReplies(quick_replies=[
    			quick_reply_1,
    			quick_reply_2,
    			quick_reply_3
    			])
    		text = { 'text': 'What ticket do you want to buy?'}
    		text['quick_replies'] = quick_replies_set.to_dict()
    		self.send(text, 'RESPONSE')
    	else:
    		quick_reply_1 = quick_replies.QuickReply(title='Movie Tickets', payload='movie')
    		quick_reply_2 = quick_replies.QuickReply(title='Event Tickets', payload='event')
    		quick_reply_3 = quick_replies.QuickReply(title='Quit', payload='quit')
    		quick_replies_set = quick_replies.QuickReplies(quick_replies=[
    			quick_reply_1,
    			quick_reply_2,
    			quick_reply_3
    			])
    		text = { 'text': 'What ticket do you want to buy?'}
    		text['quick_replies'] = quick_replies_set.to_dict()
    		self.send(text, 'RESPONSE')    		


    def optin(self, message):
        pass

    def init_bot(self):
    	greeting_text = GreetingText('Welcome to InstaTickets')
    	messenger_profile = MessengerProfile(greetings=[greeting_text])
    	messenger.set_messenger_profile(messenger_profile.to_dict())        
    	get_started = GetStartedButton(payload='start')
    	messenger_profile = MessengerProfile(get_started=get_started)
    	messenger.set_messenger_profile(messenger_profile.to_dict())


# def load_scrap():
# 	try:
# 		r = requests.get('http://127.0.0.1:5000/')
# 		if r.status_code == 200:
# 			print('Server started, quiting start_loop')
# 			not_started = False
# 			print(r.status_code)
# 		except:
# 			print('Server not yet started')


app = Flask(__name__)
app.debug = True
messenger = Messenger('EAAEhKs1vgJcBAEscpN8JE7qBdjiIdA8FkxOOQZBjat2lJNWTddnQ3b51gZBwCykS422uGs3ZBVJOZCrMZBD1MyYjfJKUsQiy3MFjhnYDcbIdVAsEmdxUp4qaWsSQEkpg0gwMZAylf0PaBtoa6i4HWdePVpPTUdgjILySlZB5o2tCXT5U5wxdSls')



@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        print('port')
        if request.args.get('hub.verify_token') == 'hello':
            print('ss')
            messenger.init_bot()
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':    	
        messenger.handle(request.get_json(force=True))
    return ''


if __name__ == '__main__':
    app.run()
