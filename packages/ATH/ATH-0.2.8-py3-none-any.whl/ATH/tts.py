import speech_recognition as sr
import pyttsx3

voice = pyttsx3.init()
r = sr.Recognizer()

def tts(thing):
    voice.say(thing)
    voice.runAndWait()
    return thing

def stt():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            return MyText
    except:
        pass