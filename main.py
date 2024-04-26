from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


import random
import json
import pickle
import numpy as np


import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]

    return sentence_words


# Convert a sentence into a bag of words. Check if a word exists in a sentence or not
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)

    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    error_threshold = 0.25

    result = [[i,r] for i,r in enumerate(res) if r > error_threshold]

    result.sort(key = lambda x: x[1], reverse=True)
    return_list = []

    for r in result:
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})

    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break

    return result


print('AI chatbot is running')


app = Flask(__name__)

app.config['SECRET_KEY'] = 'MYSECRETKEY'

input_data = 'Hi what is your name?'

class ChatbotInput(FlaskForm):
    message = StringField('Chat', render_kw={"placeholder":"Type a message", "class":"user-input", "id":"user-input"})
    submit = SubmitField('Submit', render_kw={"class":"send-btn", "onclick":"sendMessage()"})


@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    response = ''
    form = ChatbotInput()
    input_data = 'Hello There'

    if form.validate_on_submit:
        if form.message.data is None:
            return render_template("chatbot.html", form=form)
        
        input_data = form.message.data
        ints = predict_class(input_data)
        res = get_response(ints, intents)
        response = res
    

    
   

    return render_template('chatbot.html', form=form, response=response, input_data=input_data)

if __name__ == '__main__':
    app.run(debug=True)