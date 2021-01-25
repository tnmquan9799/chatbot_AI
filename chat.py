import random
import json
import torch
import speech_recognition
import pyttsx3
import time
import webbrowser

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents2.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

ear = speech_recognition.Recognizer()
mouth = pyttsx3.init()
voices = mouth.getProperty('voices')
mouth.setProperty("voice", voices[1].id)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


bot_name = "Sam"
print(f"Bot: This is {bot_name}. How can I help you")
mouth.say(f"This is {bot_name}. How can I help you")
mouth.runAndWait()
while True:
    # sentence = "do you use credit cards?"
    with speech_recognition.Microphone() as mic:
        audio = ear.listen(mic)

    sentence = ear.recognize_google(audio)
    print("You: " + sentence)
    if sentence == "exit":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice((intent['responses']))
                message = response.split(": ")
                print(f"{bot_name}: " + response)
                mouth.say(message[0])
                mouth.runAndWait()
                webbrowser.open_new(message[1])
    else:
        print(f"{bot_name}: I do not understand...")
        mouth.say("I do not understand...")
        mouth.runAndWait()
