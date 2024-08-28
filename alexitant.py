import speech_recognition as sr  # pip install SpeechRecognition
import pyttsx3 # pip install pyytsx3
import pywhatkit # pip install pywhatkit
import wikipedia # pip install wikipedia - for information
import pyjokes # pip install pyjokes - for jokes
import webbrowser as wb
import pyautogui  # pip install pyautogui - for screenshot & camera function
import requests
from pywinauto.application import Application
from bs4 import BeautifulSoup
import datetime
import winsound

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
'''engine.setProperty('voice', voices[1].id)    ---------- if you want to change the voice of assistant
'''

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'assistant' in command:
                '''command = command.replace('assistant', '') '''
                print(command)
    except:
        pass
    return command

def alarm(Timing):
    altime = str(datetime.datetime.now().strptime(Timing,"%I:%M %p"))
    altime = altime[11:-3]
    Horeal = altime[:2]
    Horeal = int(Horeal)
    Mireal = altime[3:5]
    Mireal = int(Mireal)
    print(f"Done, alarm is set for {Timing} ")
    while True:
        if Horeal==datetime.datetime.now().hour:
            if Mireal==datetime.datetime.now().minute:
                print("alarm is running")
                winsound.PlaySound('abc',winsound.SND_LOOP)

            elif Mireal<datetime.datetime.now().minute:
                break

def run_assistant():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M %p')
        talk(f"Current time is: " + time)
    elif 'weather' in command:
        print("enter city")
        city = take_command()

        # create url
        url = "https://www.google.com/search?q=" + "weather" + city

        # requests instance
        html = requests.get(url).content

        # getting raw data
        soup = BeautifulSoup(html, 'html.parser')

        # get the temperature
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

        # this contains time and sky description
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        # format data
        data = str.split('\n')
        time = data[0]
        sky = data[1]
        # list having all div tags having particular class name
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

        # particular list with required data
        strd = listdiv[5].text

        # formatting the string
        pos = strd.find('Wind')
        other_data = strd[pos:]
        # printing all the data
        print("Temperature is", temp)
        print("Time: ", time)
        print("Sky Description: ", sky)
        print(other_data)
    elif 'screenshot' in command:
        im = pyautogui.screenshot()
        im.save("ss.jpg") 
    elif 'alarm' in command:
        talk("Tell Time to set alarm")
        tt = take_command()
        tt = tt.replace("set alarm to ", "")
        tt = tt.replace(".","")
        tt = tt.upper()
        import alarm
        alarm.alarm(tt)
    elif 'click photo' in command:
        pyautogui.press("super")
        pyautogui.typewrite("camera")
        pyautogui.press("enter")
        pyautogui.sleep(2)
        talk("SMILE")
        pyautogui.press("enter")
    elif 'browser' in command:
        wb.open('https://www.google.com')
    elif 'stock' in command:
        wb.open('https://www.cnbc.com/markets/')
    elif 'india news' in command:
        wb.open('https://timesofindia.indiatimes.com/india')
    elif 'world news' in command:
        wb.open('https://www.hindustantimes.com/world-news')
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk("According to Wikipedia...")
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke(language="en", category="neutral"))
    elif 'volume up' in command:
        pyautogui.press("volumeup")
    elif 'volume down' in command:
        pyautogui.press("volumedown")
    elif 'mute ' in command:
        pyautogui.press("volumemute")
    elif 'open notepad' in command:
        app = Application().start("notepad.exe")
    elif "exit" in command:
        talk("Shutting Down...")
        exit()
    else:
        talk('Please say the command again.')

while True:
    run_assistant()