# https://27d5da82.ngrok.io/DNAgod

from flask import Flask
from flask_ask import Ask, request, statement, question, session
import json
import requests
import time
import unidecode

import os
import os.path
from multiprocessing import Value

import logging

logging.getLogger('flask_ask').setLevel(logging.DEBUG)

mmURL = "http://localhost:8080"
mmResp =  {}
mmResp['remove'] = 'removed from'
mmResp['add'] = 'added to'

app = Flask(__name__)
ask = Ask(app, "/MMalexa")

def get_reddit_news():
        sess = requests.Session()
        sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
        user_pass_dict = {'user': '',
                          'passwd': '',
                          'api_type': 'json'}
        sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
        time.sleep(1)
        html = sess.get('https://reddit.com/r/worldnews/.json?limit=10')
        data = json.loads(html.content.decode('utf-8'))
        titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
        titles = '... '.join([i for i in titles])
        return titles

def     parse_status(data):
        status = data['status'].lower()
        if (status == "success"):
                return data['status']
        else:
                return data['error'].lower()

def	build_url(action,title,item):
	if not title:
		url	 = "{u}/{a}Memo?item={i}".format(u=mmURL,a=action,i=item)
	elif not item:
		url	 = "{u}/{a}Memo?memoTitle={t}".format(u=mmURL,a=action,t=title)
	else:
		url	 = "{u}/{a}Memo?memoTitle={t}&item={i}".format(u=mmURL,a=action,t=title,i=item)
	return url

def	get_memo_id(title,item):
	SITE_ROOT =	os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "/home/pi/MagicMirror/modules/MMM-Memo",	"MMM-Memo.json")
	data = json.load(open(json_url))
	counter	= Value('i', 1)
	for	x in data['memos']:
		if (x["memoTitle"] == title)and	(x["item"] == item):
			return counter.value
		counter.value += 1
	return -1

def update_memo(action,title,item):
	thing = item
	if (action == "remove" and item != "all"):
		thing = get_memo_id(title,item)
		if (thing < 0): return "Unable to complete your request. {t} does not contain {i}".format(i=item,t=title)
	url = build_url(action,title,thing)
	sess = requests.Session()
	sess.headers.update({'User-Agent': 'I am testing Alexa: MagicMirror'})
	html = sess.get(url)
	data = json.loads(html.content.decode('utf-8'))
	msg = parse_status(data)
	if(msg == "success"):
		if (not item) and (action == "clear"):
                        return "{t} cleared".format(t=title)
		else:
                        return "{i} {a} {t}".format(a=mmResp[action],i=item, t=title)
	else:
		return "{m}".format(m=msg,u=url)

@app.route('/')
def homepage():
	return "hi there, how ya doin?"

@ask.launch
def start_skill():
	welcome_message = 'Hello there, what do you want to do?'
	return question(welcome_message)

@ask.intent('NewsIntent')
def news_intent():
	headlines = get_reddit_news()
	headline_msg = 'The current reddit headlines is {content}'.format(content=headlines)
	return statement(headline_msg)

@ask.intent('mmMemoIntent')
def mmMemo_intent(action,thing,memo):
	if (not action and not memo):
            memStat = update_memo("add","reminders",thing.lower())
    elif action == "clear":
            memStat = update_memo("remove",memo.lower(),"all")
 	elif not thing:
	        memStat = "Can't process request: missing item"
	else:
		memStat	= update_memo(action.lower(),memo.lower(),thing.lower())
	return statement(memStat)

@ask.intent("NoIntent")
def no_intent():
	bye_text = 'I am not sure why you asked me to run then, but okay... bye'
	return statement(bye_text)

if __name__ == '__main__':
	app.run(debug=True)


