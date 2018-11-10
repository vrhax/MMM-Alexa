# MMM-Alexa
**NB: This is a work in progress !!!**

This is an example Alexa skills Flask_Ask program that interacts with the MagicMirror MMM-Memo module to add/remove items from memos. In order to use this, you need the following:

Create an "Alexa" directory `/home/pi/Alexa` <= this is (obviously) where your MMalexa.py & ngrok files will go

Install flask and flask_ask:

```
pip install flask
pip install flask-ask
```

Install ngrok:

```
cd Alexa
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo chmod +x ngrok
./ngrok authtoken <ngrok token>
sudo cp ./ngrok/ngrok.yml /opt/ngrok/ngrok.yml
sudo cp ngrok /opt/ngrok/
```
Your ngrok token can be found in your ngrok dashboard, under auth.

Install MMM-Memo: see https://github.com/schnibel/MMM-Memo

Add the MMM-Memo module to your `/home/pi/MagicMirror/config/config.js` file

Modify the `MMalexa.py` AND `MMalexaSkill.json` files accordingly. I added some very generic lists for testing.

See https://pythonprogramming.net/testing-deploying-alexa-skill-flask-ask-python-tutorial/?completed=/headlines-function-alexa-skill-flask-ask-python-tutorial/ for creating an Alexa skill.

Cut/paste or upload the `MMalexaSkill.json`

Choose your invocation, so that Alexa knows to ask your server, as oppsed to her generic skill set. For example, if your invocation is `MyPi` you would then say: `Alexa, ask MyPi to add eggs to groceries` or `Alexa, ask MyPi for reddit news`

Set your enpoint url. Your ngrok endpoint can be found in your ngrok dashboard, under status. Copy the https link, and paste it in the default region under the endpoint section, followed by /MMalexa for example:

```
https://<assigned hex number>.ngrok.io/MMalexa
```

You can change MMalexa to anything you want but if you do so, you must also change it in the MMalexa.py script.

```
ask = Ask(app,"/<whatever you want>"
```
and modify the endpoint accordingly

```
https://<assigned hex number>.ngrok.io/<whatever you want>
```

Also, please be aware, anytime you restart ngrok, the <assigned hex number> will change, and you'll need to modify your Alexa skill, save the endpoint, save your model, and build your model.
  
Once everything is copacetic you'll probably want to set up services to run `MMalexa.py` and `ngrok` on boot

```
sudo cp <name>.service to /etc/systemd/system/
sudo chmod 755 /etc/systemd/system/<name>.service
```

Do this for both `alexa.service` and `ngrok.service`

see https://pythonprogramming.net/intro-alexa-skill-flask-ask-python-tutorial/ for an overview of how alexa works with flask ask.



