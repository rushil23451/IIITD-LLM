# IIITD GreetingBot 🤖

<div align="center">
  <img src="https://www.iiitd.ac.in/sites/default/files/images/logo/style3colorsmall.png" alt="IIITD Logo" width="400"/>
  <br><br>
  <p>
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
    <img src="https://img.shields.io/badge/LLaMA_3.3-FF6F00?style=for-the-badge&logo=meta&logoColor=white" alt="LLaMA 3.3"/>
    <img src="https://img.shields.io/badge/Sentence_BERT-4285F4?style=for-the-badge&logo=bert&logoColor=white" alt="Sentence BERT"/>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  </p>
  <h3>A conversational AI assistant for Indraprastha Institute of Information Technology Delhi (IIITD) that answers frequently asked questions through both text and voice interactions.</h3>
</div>

## 📌 Overview

IIITD GreetingBot is an interactive web application designed to provide instant answers to questions about IIITD. The bot leverages advanced NLP techniques to understand user queries and responds with accurate information about the institution, its facilities, faculty, and more.

### ✨ Key Features

<table>
  <tr>
    <td>
      <h4>🎤 Voice & Text Interaction</h4>
      <p>Speak or type your questions naturally</p>
    </td>
    <td>
      <h4>🧠 Natural Language Understanding</h4>
      <p>Accurately interprets user queries using sentence embeddings</p>
    </td>
  </tr>
  <tr>
    <td>
      <h4>📚 Context-Aware Responses</h4>
      <p>Comprehensive answers based on semantically similar FAQs</p>
    </td>
    <td>
      <h4>🔊 Text-to-Speech</h4>
      <p>Converts responses to spoken audio for accessibility</p>
    </td>
  </tr>
  <tr>
    <td>
      <h4>🔍 Pre-defined Question Cards</h4>
      <p>Quick access to common queries</p>
    </td>
    <td>
      <h4>🌃 Modern Sleek UI</h4>
      <p>Dark-themed, responsive interface</p>
    </td>
  </tr>
</table>

## 🛠️ Technology Stack

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/Backend-darkblue?style=for-the-badge" alt="Backend"/></td>
      <td>Flask, SQLite</td>
    </tr>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/NLP-darkgreen?style=for-the-badge" alt="NLP"/></td>
      <td>
        <ul>
          <li>Sentence-BERT for semantic similarity matching</li>
          <li>LLaMA 3.3 for response generation (via Groq API)</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/Speech-purple?style=for-the-badge" alt="Speech"/></td>
      <td>
        <ul>
          <li>Web Speech API for speech recognition</li>
          <li>gTTS for text-to-speech conversion</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/Frontend-darkorange?style=for-the-badge" alt="Frontend"/></td>
      <td>HTML, CSS, JavaScript</td>
    </tr>
  </table>
</div>

## 🚀 Installation & Setup

<details>
<summary>Click to expand installation instructions</summary>

### Prerequisites
- Python 3.8+
- pip
- Groq API Key

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/iiitd-greetingbot.git
cd iiitd-greetingbot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key
Set your Groq API key as an environment variable:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### Step 4: Run the Application
```bash
python app.py
```

The server will start at http://localhost:5000
</details>

## 📊 How It Works

<div align="center">
  <img src="https://img.shields.io/badge/1-Query_Processing-blue?style=for-the-badge" alt="Step 1"/>
  <p>The system takes user input via text or speech</p>
  ⬇️
  <img src="https://img.shields.io/badge/2-Semantic_Search-green?style=for-the-badge" alt="Step 2"/>
  <p>Finds semantically similar questions in the SQLite database using sentence embeddings</p>
  ⬇️
  <img src="https://img.shields.io/badge/3-Context_Building-yellow?style=for-the-badge" alt="Step 3"/>
  <p>Collects relevant Q&A pairs from the knowledge base</p>
  ⬇️
  <img src="https://img.shields.io/badge/4-Response_Generation-red?style=for-the-badge" alt="Step 4"/>
  <p>Uses LLaMA 3.3 to generate concise, accurate responses</p>
  ⬇️
  <img src="https://img.shields.io/badge/5-Text_to_Speech-purple?style=for-the-badge" alt="Step 5"/>
  <p>Converts text responses to audio for accessibility</p>
</div>

## 🔧 Project Structure

```
iiitd-greetingbot/
├── app.py              # Main Flask application
├── final.sqlite        # SQLite database with IIITD FAQ data
├── requirements.txt    # Python dependencies
└── static/             # Static assets and generated audio files
```

## 👥 Usage

<div align="center">
  <table>
    <tr>
      <td align="center"><h3>💬 Ask Questions</h3></td>
      <td>
        <ul>
          <li><b>🎤 Voice</b>: Click the microphone button and speak</li>
          <li><b>⌨️ Text</b>: Type in the message bar</li>
          <li><b>🔍 Quick Cards</b>: Click pre-defined question cards</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center"><h3>👀 View Responses</h3></td>
      <td>Read text responses in the chat interface</td>
    </tr>
    <tr>
      <td align="center"><h3>🔊 Listen</h3></td>
      <td>Audio responses play automatically</td>
    </tr>
  </table>
</div>


## 🧠 Knowledge Base

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/IIITD-General-blue?style=for-the-badge" alt="General Info"/></td>
      <td align="center"><img src="https://img.shields.io/badge/Faculty-Profiles-green?style=for-the-badge" alt="Faculty"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/Department-Details-yellow?style=for-the-badge" alt="Departments"/></td>
      <td align="center"><img src="https://img.shields.io/badge/Course-Information-red?style=for-the-badge" alt="Courses"/></td>
    </tr>
    <tr>
      <td align="center"><img src="https://img.shields.io/badge/Campus-Facilities-purple?style=for-the-badge" alt="Facilities"/></td>
      <td align="center"><img src="https://img.shields.io/badge/Hostel-Accommodations-brown?style=for-the-badge" alt="Hostels"/></td>
    </tr>
    <tr>
      <td colspan="2" align="center"><img src="https://img.shields.io/badge/Admission-Procedures-teal?style=for-the-badge" alt="Admissions"/></td>
    </tr>
  </table>
</div>

## 📝 Customization

To update or expand the knowledge base:
1. Add new Q&A pairs to the SQLite database
2. Ensure questions are phrased naturally for better semantic matching
3. Keep answers concise and accurate (recommended 3-4 lines, under 100 words)

---

<div align="center">
  <p>⭐ Star this repo if you found it useful! ⭐</p>
  <p>Made with ❤️ for IIITD</p>
</div>
