import speech_recognition
import pyttsx3

ear = speech_recognition.Recognizer()
mouth = pyttsx3.init()
# with speech_recognition.Microphone() as mic:
#     mouth.say("I'm listening")
#     mouth.runAndWait()
#     audio = ear.listen(mic)
#
# message = ear.recognize_google(audio)
# mouth.say("Did you just say " + message)
# mouth.runAndWait()

voices = mouth.getProperty('voices')
for voice in voices:
    print("Voice: %s" % voice.name)
    print(" - ID: %s" % voice.id)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    print("\n")
