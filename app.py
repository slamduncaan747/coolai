# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS
import openai
import requests
import json


app = Flask(__name__)

CORS(app, resources={r"/sendStringForMp3": {"origins": "http://127.0.0.1:5500"}})
CORS(app, resources={r"/sendString": {"origins": "http://127.0.0.1:5500"}})

CHUNK = 1024
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILE = "output.wav"

# Set up your OpenAI API keys
openai_api_key = "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"
openai.api_key = openai_api_key

@app.route('/sendString', methods=['POST'])
def receive_string_from_frontend():
    data = request.get_json()
    message_from_frontend = data.get('message', '')
    print("Received message from frontend:", message_from_frontend)
    response = process_input(message_from_frontend)
    # Process the message (In this example, just sending the same message back)
    response_data = {'response': response}

    return jsonify(response_data)

@app.route('/sendStringForMp3', methods=['POST'])
def receive_string_from_frontend_for_mp3():
    data = request.get_json()
    message_from_frontend = data.get('message', '')
    print("Received message from frontend:", message_from_frontend)
    response = process_input(message_from_frontend)
    # Process the message (In this example, just sending the same message back)
    response_data = {'response': response}

    text_to_speech(response_data)

    return send_file("output.mp3", mimetype='audio/mpeg')

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')

def process_input(textin):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = openai_api_key  # Replace with your actual OpenAI API key

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are the chatbot of a website called moleculARweb, which provides educational material for chemistry using commodity augmented reality. You answer questions about the website, about chemistry, science, etc."},
            {"role": "user", "content": "What is the formula of acetic acid?"},
            {"role": "assistant", "content": "The formula of acetic acid is CH3COOH"},
            {"role": "user", "content": textin}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.ok:
        json_response = response.json()
        chatbot_response = json_response["choices"][0]["message"]["content"]
        return chatbot_response
    else:
        print("Error:", response.status_code, response.text)
        return None
    
if __name__ == '__main__':
    app.run(port=5000)
