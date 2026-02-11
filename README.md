# 🤖 AI Assisted Interview Coach

An intelligent, voice-interactive technical interview coach that helps you practice for interviews using your own resume. Powered by Groq (Llama 3), Faster Whisper, and Text-to-Speech.

## 🚀 Features

- **📄 Resume Analysis**: Parses your PDF or TXT resume to ask personalized, relevant questions based on your experience.
- **🗣️ Voice Interaction**:
  - **Speech-to-Text**: uses `faster-whisper` for fast and accurate transcription of your answers.
  - **Text-to-Speech**: The AI interviewer speaks the questions aloud using `pyttsx3`.
- **🧠 Intelligent Questioning**:
  - Uses **Groq API (Llama 3)** to generate context-aware technical questions.
  - Adaptive 3-level difficulty: **Beginner, Intermediate, Advanced**.
- **📊 Comprehensive Feedback**: Provides a detailed performance report at the end of the session, highlighting strengths and areas for improvement.
- **🎙️ Real-time Interaction**: Press 'r' to record your answer, and 'x' to end the interview anytime.

## 🛠️ Tech Stack

- **Python 3.8+**
- **Groq API** (LLM provider)
- **Faster Whisper** (STT model)
- **PyAudio & Wave** (Audio recording)
- **Pyttsx3** (TTS engine)
- **Tkinter** (File selection GUI)
- **aiohttp** (Asynchronous HTTP requests)

## 📋 Prerequisites

- Python installed on your system.
- A **Groq API Key** (Get one from [Groq Console](https://console.groq.com/)).
- A working microphone and speaker/headphones.
- On Windows, you might need [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed if `pyaudio` installation fails.

## 🔧 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/ai-assisted-interview.git
    cd ai-assisted-interview
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If `pypdf` or `faster-whisper` fail to install, ensure you have the latest `pip` version: `pip install --upgrade pip`.*

3.  **Set up API Key**
    - Set your Groq API key as an environment variable to keep it secure:
      
      **Windows (PowerShell):**
      ```powershell
      $env:GROQ_API_KEY="your_actual_api_key_here"
      ```
      
      **Mac/Linux:**
      ```bash
      export GROQ_API_KEY="your_actual_api_key_here"
      ```
    - *Alternatively, you can modify `groq_llm.py` directly, but avoid committing keys to version control!*

## ▶️ Usage

1.  **Run the Application**
    ```bash
    python main.py
    ```

2.  **Select Difficulty**
    - The console will ask for a difficulty level:
      - `1` for **Beginner** (Foundational questions)
      - `2` for **Intermediate** (Standard technical questions)
      - `3` for **Advanced** (Expert-level scenarios)

3.  **Select Resume**
    - A file dialog will pop up. Select your resume file (`.pdf` or `.txt`).

4.  **Start Interview**
    - The AI will analyze your resume and ask the first question.
    - **Press 'r'** to record your answer. Speak clearly!
    - **Press 'q'** (while recording) to stop recording.
    - **Press 'x'** to end the interview and generate feedback.

## 📂 Project Structure

```
├── main.py             # Main entry point, handles audio loop and user interaction
├── groq_llm.py         # Manages Groq API calls (Interviewer logic)
├── resume_parser.py    # Extracts text from PDF/TXT resumes
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
