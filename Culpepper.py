from gtts import gTTS
import speech_recognition as spchrec
import os
import webbrowser
import smtplib
import requests
import spotipy


sp = spotipy.Spotify()

def voice_command(sound):
    print(sound)
    voice = gTTS(text=sound, lang='en')
    voice.save('sound.mp3')
    os.system('mpg123 sound.mp3')


# Function to hear command
def give_command():

    with spchrec.Microphone() as source:
        print('I am ready for your next command')
        rec = spchrec.Recognizer()
        rec.pause_threshold = 1
        rec.adjust_for_ambient_noise(source, duration=.5)
        sound = rec.listen(source)

    try:
        cmnd = rec.recognize_google(sound)
        print("The command given was: " + cmnd + '\n')

    # listen again for command in case of exception
    except spchrec.UnknoewnValueError:
        helper(give_command())
    return cmnd


# Condition control for giving voice command
def helper(cmnd):

        if 'open Bing' in cmnd:
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            url1 = 'https://www.bing.com'
            webbrowser.get(chrome_path).open(url1)

        if 'what\'s up' in cmnd:
            voice_command('Not much, chilling')

        if 'email' in cmnd:
            voice_command('Who do you want to send an email to')
            email_to = give_command()

            if 'Kevin' in email_to:
                voice_command('What do you want the message to say')
                message = give_command()

                #init Email
                email_whole = smtplib.SMTP('smtp.gmail.com', 587)

                #identify server
                email_whole.ehlo()

                #encrypt message
                email_whole.starttls()

                #login to email
                email_whole.login('', '')

                #send email
                email_whole.sendmail('', '', message)

                #close connection
                email_whole.close()

                #confirmation of sent
                voice_command('Email Sent')

        if 'weather' in cmnd:
            weather_response = requests.get("http://api.openweathermap.org/data/2.5/{api-key}")
            json_data = weather_response.json()
            for item in json_data['weather']:
                day_main = item.get('main')
                voice_command(day_main)
                day_desc = item.get('description')
                voice_command(day_desc)


while True:
        voice_command('how can i help you?')
        helper(give_command())






