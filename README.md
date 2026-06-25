<h1 align="center">Motion-Detecting LLM Assistant</h1>
<p align="center">An ambient AI agent that wakes when it sees a face, talks to you, and comments on the room when ignored.</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Vision-OpenCV-5C3EE8?logo=opencv&logoColor=white">
  <img src="https://img.shields.io/badge/LLM-GPT--4o--mini-412991?logo=openai&logoColor=white">
  <img src="https://img.shields.io/badge/TTS-OpenAI%20neural-412991?logo=openai&logoColor=white">
</p>

A single autonomous Python loop that chains real-time computer vision, an LLM, speech recognition,
and neural text-to-speech. It sits idle watching a webcam; the moment a face appears it wakes up,
introduces itself, and holds a spoken conversation. If you stop replying, it takes a photo, asks a
vision model what it can see, and works that into its next line, before shutting itself down after a
set lifetime and going back to watching.

## ✨ Features
- **Face-triggered wake** — OpenCV Haar cascades with histogram equalisation (low-light robust) block until a face appears.
- **Spoken conversation** — GPT-4o-mini replies in-character, read aloud with OpenAI neural TTS; Google Speech Recognition listens for your answer.
- **Emotional speech** — stage directions in the LLM output (`*frustrated*`, `*whisper*`) are parsed and passed to the TTS model as tone instructions.
- **Contextual awareness** — if you go quiet for two cycles it captures a photo, sends it to GPT-4.1-mini vision, and references what it sees.
- **Threaded architecture** — a background timer counts down the agent's lifetime while speech recognition runs in a worker thread that hands results back through a `Queue`.

## 🛠 Stack
| Area | Tech |
|---|---|
| Computer vision | OpenCV (`cv2`), Haar cascade |
| LLM | OpenAI GPT-4o-mini |
| Vision / scene | OpenAI GPT-4.1-mini (Files API) |
| Text-to-speech | OpenAI `gpt-4o-mini-tts` |
| Speech-to-text | Google Speech Recognition |
| Concurrency | `threading`, `Queue` |
| Audio / logs | `python-vlc`, `colorama` |

## 🚀 Run
Requirements: Python 3.10+, an OpenAI API key, and a webcam.
```bash
pip install openai opencv-python speechrecognition colorama python-vlc python-dotenv
echo "OPENAI_API_KEY=your_key_here" > .env
cd src && python main.py
```
The agent waits silently until it detects a face, then introduces itself. Tune behaviour in `src/config.json`:

| Key | Description | Default |
|---|---|---|
| `LLM_LIFETIME` | seconds before the agent shuts down | `300` |
| `MULTIPLE_CAMERAS` | randomly pick from a list of camera indices | `false` |
| `CAMERA_DIGITS` | camera index or list of indices | `[0, 1]` |

## 🧠 How it works
```
Webcam → Face Detected → LLM Prompt → TTS Response
           ↑                               ↓
     Motion Loop ←── STT Listens ←── User Speaks
           ↑
     (if silent) → Photo → Vision API → LLM re-prompts
```
`src/` splits cleanly by responsibility: `detectFace.py` (blocks until a face is found),
`newllm.py` (chat completions + persona prompts), `describeSetting.py` (vision scene description),
`textToSpeech.py` (TTS + stage-direction parsing), `speechToText.py` (threaded STT), all
orchestrated by `main.py`.

## 🗺 Roadmap
Runs locally; a personal computer-vision + LLM experiment.
- [ ] Swap Google STT for a local recogniser to cut latency and the network dependency
- Known limitation: needs an OpenAI API key and internet; conversation quality depends on the mic and ambient noise.
