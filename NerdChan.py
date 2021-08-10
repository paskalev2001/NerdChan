import wolframalpha
import speech_recognition as sr
import wikipedia
import speech_recognition as sr
import pyttsx3
import PySimpleGUI as sg

def readConfig(name):
    configFile = open("./config/"+name,'r')
    configLines = configFile.readlines()
    config = {}
    for line in configLines:
        line = line.replace('\n','')
        kvp = line.split('=')
        config[kvp[0]] = kvp[1]
    if(config['apiKey']==''):
        sg.PopupNonBlocking("Warning: Wolfram api key is not set therefore NerdChan will only return results from wikipedia. \n Visit https://developer.wolframalpha.com/portal/myapps/ to get one and write it in the config file.")
    return config

def voiceRec():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Sphinx
    try:
        voice_out = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + voice_out)
        return voice_out
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

def wikiWolf(currentConfig):
    while True:
        event, values = window.read()
        if event in (None, 'Close'):
            break
        if event == 'Voice':
            values[0] = voiceRec()
        try:
            wiki_res = wikipedia.summary(values[0], sentences=currentConfig["wikiLenght"])
            wolfram_res = next(client.query(values[0]).results).text
            engine.say(wolfram_res)
            sg.PopupNonBlocking("Wolfram Result: "+wolfram_res,"Wikipedia Result: "+wiki_res)
        except wikipedia.exceptions.DisambiguationError:
            wolfram_res = next(client.query(values[0]).results).text
            engine.say(wolfram_res)
            sg.PopupNonBlocking(wolfram_res)
        except wikipedia.exceptions.PageError:
            wolfram_res = next(client.query(values[0]).results).text
            engine.say(wolfram_res)
            sg.PopupNonBlocking(wolfram_res)
        except:
            wiki_res = wikipedia.summary(values[0], sentences=currentConfig["wikiLenght"])
            engine.say(wiki_res)
            sg.PopupNonBlocking(wiki_res)

        engine.runAndWait()

        #print (values[0])

    window.close()


currentConfig = readConfig("Default.config")

client = wolframalpha.Client(currentConfig["apiKey"])
sg.theme(currentConfig["theme"])
layout =[
    [sg.Text('Ask me something :)'), sg.InputText()],
    [sg.Button('Ask'), sg.Button('Close'),sg.Button('Voice')]
    ]
window = sg.Window('NerdChan', layout)

engine = pyttsx3.init()
engine.setProperty('rate', currentConfig["rate"])
engine.setProperty('voice', currentConfig["voice"])

wikiWolf(currentConfig)
