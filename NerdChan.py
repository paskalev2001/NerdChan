import wolframalpha
client = wolframalpha.Client("Get your own key at wolframalpha")
import speech_recognition as sr
import wikipedia
import speech_recognition as sr

import PySimpleGUI as sg

sg.theme('DarkBlue4')
layout =[
    [sg.Text('Ask me something :)'), sg.InputText()],
    [sg.Button('Ask'), sg.Button('Close'),sg.Button('Voice')]
    ]
window = sg.Window('NerdChan', layout)

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 220)
engine.setProperty('voice', 'english+f3')

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


def wikiWolf():
    while True:
        event, values = window.read()
        if event in (None, 'Close'):
            break
        if event == 'Voice':
            values[0] = voiceRec()
        try:
            wiki_res = wikipedia.summary(values[0], sentences=3)
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
            wiki_res = wikipedia.summary(values[0], sentences=3)
            engine.say(wiki_res)
            sg.PopupNonBlocking(wiki_res)

        engine.runAndWait()

        print (values[0])

    window.close()
wikiWolf()
