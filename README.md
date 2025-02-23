## What is VoiceOS?

VoiceOS is an innovative AI-powered voice assistant designed to redefine computer interaction. By leveraging state-of-the-art speech recognition, natural language processing, and text-to-speech technologies, VoiceOS lets you control your computer completely hands-free. In just a few months, we transformed a simple idea into a comprehensive system that manages applications, documents, web content, and emails—all via voice commands.

### Key Achievements

- **Real-Time Voice Control:** Integrated cutting-edge speech-to-text (Whisper) and natural language understanding (GPT-4) to execute complex commands.
- **Seamless Automation:** Developed a suite of automated functions for document processing, email management, and application control.
- **Web Integration:** Enabled intelligent web scraping and summarization, allowing users to quickly extract key information from any webpage.
- **Natural TTS Output:** Implemented OpenAI’s TTS API to provide natural-sounding voice responses, making the interaction more human-like.
- **Robust Command Mapping:** Built a dynamic command interpreter that uses both predefined mappings and GPT-4 insights to translate natural language into system actions.

### Links

- **Demo Video:** [VoiceOS Demo Video](https://www.youtube.com/watch?v=3Cpx_2eMyJ0)

## Files and Descriptions

### `DocumentSummarizer_test.py`
**Description:**  
This script extracts text from web pages or documents and summarizes it using GPT-4. The summary is then read aloud using OpenAI’s TTS API.

### `DocumentTranslator_test.py`
**Description:**  
This script detects the language of selected text and translates it to English using AI, then optionally reads out the translated text.

### `Document_test.py`
**Description:**  
Automates document creation and formatting. It can open new documents, set titles, type sample text, and apply formatting such as bold, underline, and italics.

### `email_test.py`
**Description:**  
Handles email automation by opening Gmail, composing emails, inserting recipients, subjects, and bodies, and finally sending emails—all via voice commands.

### `shortcuts_test.py`
**Description:**  
Provides various keyboard shortcuts to control window management and system functions, enhancing productivity through voice-triggered commands.

### `updatedvoice_test.py`
**Description:**  
Implements full voice control by integrating OpenAI’s Whisper, GPT-4, and TTS APIs. This module listens for voice commands, processes them, and executes corresponding system actions.

### `vscode_testing.py`
**Description:**  
Automates operations in Visual Studio Code, such as opening the editor, creating new files, and running scripts, all triggered via voice commands.

### `test.py`
**Description:**  
A general testing file used to debug and validate the functionalities of various components of VoiceOS.

## Installation Instructions

To run VoiceOS, you'll need to install several Python packages. Use the following pip install commands to set up your environment:

```bash
pip install opencv-python
pip install mediapipe
pip install pyttsx3
pip install speechrecognition
pip install pyautogui
pip install numpy
pip install pyaudio
pip install pyobjc-framework-Quartz  # MacOS only
pip install pygetwindow              # Windows only
pip install openai
pip install pydub
pip install keyboard
pip install requests
pip install beautifulsoup4
pip install selenium
pip install webdriver-manager
pip install transformers
pip install nltk
```
After installing, download the NLTK data by running:

```bash
import nltk
nltk.download('punkt')
```

Also, create a file named config.py and add your OpenAI API key:
```bash
openai_api_key = "your-api-key-here"
```
## Usage

### Run VoiceOS

To start VoiceOS, simply run:

```bash
python VoiceOS.py
```

The program listens for voice commands and executes corresponding actions based on predefined mappings.

## Summarize Web Content
- Open a webpage.
- Press **SPACE** (this copies the URL).
- VoiceOS will fetch the page content, summarize it with GPT-4, and read it out loud using OpenAI TTS.

## Translate Text
- Highlight any text.
- Say **"Translate this"**.
- The assistant will translate the text to English and speak the translation.

## Automate Emails
- Say **"Compose an email to [Name]"**.
- Follow prompts for subject and body.
- Say **"Send email"** to dispatch the email automatically.

## Control Windows
Use commands like:
- **"Close window"**
- **"Switch tab"**
- **"Open VS Code"**

## Future Plans
- **Custom Voice Models:** Train personalized TTS models for unique voice outputs.
- **Offline Speech Processing:** Develop offline capabilities for faster response and enhanced privacy.
- **Expanded Integration:** Extend voice command functionalities to smart home devices and third-party applications.
- **Enhanced Personalization:** Allow users to customize command mappings and responses.

## Contributing
Pull requests are welcome! Please fork the repository, make your changes, and submit a pull request with detailed information.

## Contact
For questions or contributions, contact **Dhanvinkumar Ganeshkumar** at **2027dganeshk@tjhsst.edu**.
