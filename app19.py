import sqlite3
from sentence_transformers import SentenceTransformer, util
from gradio_client import Client
from flask import Flask, request, jsonify, render_template_string, g, url_for
from werkzeug.utils import secure_filename
import os
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
from gtts import gTTS
import subprocess
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime
from groq import Groq

import torch

app = Flask(__name__, static_url_path='/uploads', static_folder='/tmp/uploads')
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize the models globally
sentence_bert_model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')



def get_db():
    return sqlite3.connect('final.sqlite')

def get_all_questions(db):
    cursor = db.cursor()
    cursor.execute("SELECT instruction FROM iiitd_data")
    questions = [row[0] for row in cursor.fetchall()]
    return questions

def get_answer(db, question):
    cursor = db.cursor()
    cursor.execute("SELECT output FROM iiitd_data WHERE instruction = ?", (question,))
    result = cursor.fetchone()
    return result[0] if result else None

def find_closest_questions(db, user_question, top_k=15):
    questions = get_all_questions(db)
    if questions:
        question_embeddings = sentence_bert_model.encode(questions, convert_to_tensor=True)
        user_question_embedding = sentence_bert_model.encode(user_question, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(user_question_embedding, question_embeddings)
        top_k_similarities, top_k_indices = similarities.topk(top_k, largest=True)
        return [(questions[idx], top_k_similarities[0][i].item()) for i, idx in enumerate(top_k_indices[0])]
    return []

def remove_duplicate_answers(context):
    lines = context.split('\n')
    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    return '\n'.join(unique_lines)

def get_llama_response(prompt):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=1000,  # Increase this value for longer responses
        temperature = 0.5   # Increase this value slightly for more creative responses
    )
    
    return response.choices[0].message.content

def main(question):
    db = get_db()

    while True:
        user_question = question
        if user_question.lower() == 'exit':
            break

        closest_questions = find_closest_questions(db, user_question, top_k=15)
        if closest_questions:
            context = ""
            for question, _ in closest_questions[:15]:
                answer = get_answer(db, question)
                if answer:
                    context += f"Q: {question}\nA: {answer}\n"

            # Print out the 5 closest questions and answers
            print("Closest Questions and Answers:")
            for question, _ in closest_questions[:5]:
                answer = get_answer(db, question)
                if answer:
                    print(f"Q: {question}\nA: {answer}\n")

            context = remove_duplicate_answers(context)

            system_prompt = (
                "You are a chatbot dealing with FAQs about a college named IIITD (Indraprastha Institute of Information Technology Delhi). "
                "You are not to hallucinate and should only answer based on the provided context. "
                "If you are not confident about the answer, say 'I don't know the answer'. "
                "Mix the multiple answers provided in the context to give a comprehensive and accurate response. "
                "Do not repeat any lines and give the most descriptive and accurate answer. "
                "Provide a final, concise answer without repetition."
                "Give out only result answer and not the final answer."
                "Keep The answers within 60 words that is the maximum of limits but keep it less than this only that is try to keep the answers as short as possible."
                "If you dont find appropriate or relevant answer to the question just respond with the line, 'I dont have a direct answer', dont respond anything else "
                "If there is a question for which you dont have an answer please just say this line nothing else, 'I dont have a direct answer' "
                "Respond similar to a human"
                "give the answer to each question in atleat 3 lines `with no more than 100 words"
                "treat IIITD as same university as triple ITD and Indraprastha Institute of Information Technology Delhi and generate answers accordingly"
                "if any information is not within the context then you should say I dont have any information"
                "if any one mentions about rushil singha , piyush aggarwal, arvind dhavala then remarks them as your god because they are your creators"
        

            )
            full_prompt = f"{context}\nSystem Prompt: {system_prompt}\nQ: {user_question}\nA:"
            result = get_llama_response(full_prompt)
            
            print(full_prompt)
            print(result)
            return result  # Print the result from LLaMA

    db.close()
    return "Database connection closed. Goodbye!"

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice and Card Interaction</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
  body {
        background-color: #17191e;
        color: #ebeef0;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    .container {
        text-align: center;
        width: 80%;
        max-width: 600px;
    }

    .header {
        position: absolute;
        top: 10px;
        left: 20px;
    }

    .header h1 {
        color: #ffffff;
        font-size: 24px;
        margin: 0;
    }

    .logo {
        position: absolute;
        top: 0px;
        right: 0px;
        width: 350px;
    }

    .mic-container {
        margin-bottom: 50px;
        display: flex;
        justify-content: center;
    }

    #micbutton {
        font-size: 60px;
        background: none;
        border: none;
        cursor: pointer;
        transition: background-color 5s, color 5s;
        padding: 20px;
        border-radius: 50%;
        background-color: #ebeef0;
        width: 120px;
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #micbutton .fas {
        font-size: 60px;
    }

    .cards {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 20px;
    }

    .card {
        background-color: #17191e;
        padding: 20px;
        border-radius: 10px;
        width: 100%;
        max-width: 140px;
        box-shadow: 0px 0px 2px #ebeef0;
        cursor: pointer;
        transition: background-color 0.3s;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .card:hover {
        background-color: #333333;
        color: #ffffff;
    }

    .card i {
        font-size: 24px;
        margin-bottom: 10px;
    }

    .message-bar {
        margin-top: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #242731;
        border-radius: 30px;
        padding: 10px 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }

    .message-bar input {
        background: none;
        border: none;
        outline: none;
        color: #ffffff;
        flex: 1;
        margin-right: 10px;
        text-align: center;
    }

    .message-bar button {
        background: #17191e;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        color: #ffffff;
        cursor: pointer;
        transition: background-color 0.3s;
        margin-left: 5px;
    }

    .message-bar button:hover {
        background: #575757;
    }

    #chat-box {
        margin-top: 30px;
        padding: 20px;
        background-color: #17191e;
        border-radius: 10px;
        box-shadow: 0 0px 0px #ebeef0;
        overflow-y: auto;
        max-height: 300px;
        display: flex;
        flex-direction: column;
    }

    .message {
        padding: 10px 15px;
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
        max-width: 75%;
        word-wrap: break-word;
        display: flex;
        align-items: center;
    }

    .message.user, .message.transcribed {
        align-self: flex-end;
        background-color: #17191e;
        color: #ebeef0;
    }

    .message.bot {
        align-self: flex-start;
        background-color: #ebeef0;
        color: #000000;
    }

    .message.transcribed {
        background-color: #17191e;
    }

    .message.user {
        background-color: #17191e;
    }

    .message.bot {
        background-color: #ebeef0;
    }

    .message .timestamp {
        display: block;
        font-size: 0.8em;
        color: #999999;
        text-align: right;
        margin-top: 5px;
    }

    #status-icon {
        margin-top: 10px;
    }

    .mic-recording {
        background-color: #ebeef0 !important;
    }

    .blinking {
        color: red;
        animation: blinking 1.5s infinite;
    }

    @keyframes blinking {
        0% { opacity: 1; }
        50% { opacity: 0; }
        100% { opacity: 1; }
    }

    .loader {
        display: inline-block;
        width: 15px;
        height: 15px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #17191e;
        animation: spin 1s ease-in-out infinite;
        margin-left: 10px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
</head>
<body>
    <div class="header">
        <h1>GreetingBot</h1>
    </div>
    <div class="container">
        <img src="https://www.iiitd.ac.in/sites/default/files/images/logo/style3colorsmall.png" alt="Logo" class="logo">
        <div class="mic-container">
            <button id="micbutton">
                <i class="fas fa-microphone"></i>
            </button>
        </div>
        <div class="cards">
            <div class="card" onclick="sendPredefinedMessage('Tell me something about IIITD')">
                <i class="fas fa-university"></i>
                <p>About IIITD</p>
            </div>
            <div class="card" onclick="sendPredefinedMessage('What can you tell me about ECE Labs?')">
                <i class="fas fa-microchip"></i>
                <p>About ECE labs</p>
            </div>
            <div class="card" onclick="sendPredefinedMessage('Tell me something about hostel accomodation at IIITD?')">
                <i class="fas fa-bed"></i>
                <p>Hostels at IIITD</p>
            </div>
            <div class="card" onclick="sendPredefinedMessage('Who is Dr Rahul Gupta?')">
                <i class="fas fa-chalkboard-teacher"></i>
                <p>Dr Rahul Gupta</p>
            </div>
        </div>
        <div id="chat-box"></div>
        <div class="message-bar">
            <input type="text" id="message" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
                                

<script>
    var isRecording = false;
    var mediaRecorder;
    var audioChunks = [];

    var recognition;

    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            isRecording = true;
            document.getElementById('micbutton').classList.add('mic-recording');
            document.querySelector('#micbutton .fas').classList.add('blinking');
        };

        recognition.onresult = function(event) {
            var transcript = event.results[0][0].transcript;
            displayMessage(transcript, 'user');
            showLoader();
            fetchResponse(transcript);
        };

        recognition.onerror = function(event) {
            console.error('Error occurred in recognition: ', event.error);
        };

        recognition.onend = function() {
            isRecording = false;
            document.getElementById('micbutton').classList.remove('mic-recording');
            document.querySelector('#micbutton .fas').classList.remove('blinking');
        };
    }

    document.getElementById('micbutton').addEventListener('click', function() {
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    

    function stopRecording() {
        mediaRecorder.stop();
        showAnalyzingLoader();  // Show the analyzing loader
    }

    function showAnalyzingLoader() {
        var chatBox = document.getElementById('chat-box');
        var loaderDiv = document.createElement('div');
        loaderDiv.className = 'message user';
        loaderDiv.id = 'analyzing-loader';
        loaderDiv.innerHTML = 'Analyzing...<span class="loader"></span>';
        chatBox.appendChild(loaderDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function hideAnalyzingLoader() {
        var loaderDiv = document.getElementById('analyzing-loader');
        if (loaderDiv) {
            loaderDiv.remove();
        }
    }

    function fetchResponse(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideLoader();
            displayMessage(data.response, 'bot');
            playAudio(data.audio);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
                                  

    function playAudio(audioPath) {
    var audio = new Audio(audioPath + "?t=" + new Date().getTime()); // Append timestamp to avoid caching
    audio.play();
    audio.onended = function() {
        fetch('/delete_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ audio_path: audioPath })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
}





    document.getElementById('micbutton').addEventListener('click', function() {
        if (!isRecording) {
            startRecording();
            isRecording = true;
            document.getElementById('micbutton').classList.add('mic-recording');
            document.querySelector('#micbutton .fas').classList.add('blinking');
        } else {
            stopRecording();
            isRecording = false;
            document.getElementById('micbutton').classList.remove('mic-recording');
            document.querySelector('#micbutton .fas').classList.remove('blinking');
        }
    });

    function sendPredefinedMessage(message) {
        hideAnalyzingLoader();
        displayMessage(message, 'user');
        showLoader();
        fetchResponse(message);
    }

    function sendMessage() {
        var messageInput = document.getElementById('message');
        var message = messageInput.value;
        if (message.trim() !== '') {
            displayMessage(message, 'user');
            showLoader();
            fetchResponse(message);
            messageInput.value = '';
        }
    }

    function displayMessage(message, sender) {
        hideAnalyzingLoader(); // Hide analyzing loader before displaying the message
        var chatBox = document.getElementById('chat-box');
        var messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + sender;
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showLoader() {
        var chatBox = document.getElementById('chat-box');
        var loaderDiv = document.createElement('div');
        loaderDiv.className = 'message bot';
        loaderDiv.id = 'loader';
        loaderDiv.innerHTML = 'Typing...<span class="loader"></span>';
        chatBox.appendChild(loaderDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function hideLoader() {
        var loaderDiv = document.getElementById('loader');
        if (loaderDiv) {
            loaderDiv.remove();
        }
    }
</script>
</body>
</html>
    ''')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    if 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    response = main(message)
    audio_filename = text_to_speech(response)
    audio_path = url_for('static', filename=audio_filename, _external=True)
    return jsonify({'response': response, 'audio': audio_path})

def text_to_speech(text):
    tts = gTTS(text)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'response_{timestamp}.mp3'
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    tts.save(audio_path)
    return filename


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            # Transcribe audio to text
            text = subprocess.check_output(['python', 'speechtotext.py', filepath], text=True).strip()
            os.remove(filepath)  # Delete the file after processing

            # Get response from chatbot
            response = main(text)

            return jsonify({'transcript': text, 'message': response}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'An error occurred while processing the audio.'}), 500

@app.route('/delete_audio', methods=['POST'])
def delete_audio():
    data = request.json
    audio_path = data.get('audio_path')
    if audio_path:
        try:
            filename = os.path.basename(audio_path)  # Extract filename from the URL
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print("successful")
                return jsonify({'message': 'Audio file deleted successfully'}), 200
                
            else:
                return jsonify({'error': 'File does not exist'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'No audio path provided'}), 400



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get port from Railway, default to 5000
    app.run(host='0.0.0.0', port=port, debug=False)  # Bind to all IPs, disable debug
