# Motion Detection AI Agent

An ambient AI agent that wakes up when it detects a human, holds a conversation, and uses its camera to observe the room when ignored. Built entirely in Python, it chains together real-time computer vision, large language models, speech recognition, and neural text-to-speech into a single autonomous loop.

---

## How It Works

1. **Face detection** runs continuously on a webcam feed. The moment a face appears, the agent wakes up.
2. **GPT-4o-mini** generates a response in-character and sends it to the TTS pipeline.
3. **OpenAI TTS** (`gpt-4o-mini-tts`) reads the response aloud, with emotional tone extracted from stage directions embedded in the LLM output (e.g. `*frustrated* "Why are you here again?"`).
4. **Google Speech Recognition** listens for a reply. If the user responds, the conversation continues.
5. **If the user goes quiet** for two cycles, the agent captures a photo, sends it to **GPT-4.1-mini vision**, gets a description of the scene, and uses that to craft a contextually-aware response — commenting on what it can see.
6. After a configurable lifetime (default 5 minutes), the agent shuts itself down and returns to watching for motion.

```
Webcam → Face Detected → LLM Prompt → TTS Response
           ↑                               ↓
     Motion Loop ←── STT Listens ←── User Speaks
           ↑
     (if silent) → Photo → Vision API → LLM re-prompts
```

---

## Key Features

- **Real-time face detection** using OpenCV Haar cascades with histogram equalisation for low-light robustness
- **Multi-modal AI pipeline** — text generation, vision analysis, and speech synthesis all coordinated in a single loop
- **Contextual awareness** — the agent takes and analyses a photo of the room if the user stops responding, then references what it sees
- **Emotional speech synthesis** — stage directions in LLM output (`*whisper*`, `*angry*`) are parsed and forwarded as tone instructions to the TTS model
- **Threaded architecture** — a background `threading` timer counts down the agent's lifetime alongside the main conversation loop, and speech recognition runs in a worker thread that hands its result back through a `Queue`
- **Configurable** via `config.json` — LLM lifetime, camera selection (including multi-camera random selection), and talk speed

---

## Tech Stack

| Area | Technology |
|---|---|
| Computer Vision | OpenCV (`cv2`), Haar Cascade Classifier |
| LLM | OpenAI GPT-4o-mini |
| Vision / Scene Analysis | OpenAI GPT-4.1-mini (vision) via Files API |
| Text-to-Speech | OpenAI `gpt-4o-mini-tts` (neural TTS with emotional instructions) |
| Speech-to-Text | Google Speech Recognition (`speech_recognition`) |
| Concurrency | Python `threading`, `Queue` |
| Audio Playback | `python-vlc` |
| Config & Secrets | JSON config file, `python-dotenv` |
| Logging | Colour-coded structured logs via `colorama` |

---

## Skills Demonstrated

- **Real-time computer vision** — live webcam processing, frame conversion, Haar cascade face detection
- **LLM prompt engineering** — multi-personality system prompts, conversation history management, structured output parsing
- **Multi-modal AI integration** — coordinating text, vision, and audio models in a single coherent pipeline
- **Concurrent Python** — managing multiple threads safely with queues and shared state
- **OpenAI API** — chat completions, vision (Files API), streaming TTS audio
- **Audio I/O** — microphone capture with ambient noise adjustment, audio file streaming and playback
- **System design** — event-driven architecture where each component hands off cleanly to the next

---

## Project Structure

```
src/
├── main.py            # Orchestration — main loop, threading, conversation history
├── detectFace.py      # OpenCV face detection, blocks until a face is found
├── newllm.py          # GPT-4o-mini chat completions, persona/system prompts
├── describeSetting.py # GPT-4.1-mini vision — describes the room from a photo
├── textToSpeech.py    # OpenAI TTS, stage direction parsing, audio playback
├── speechToText.py    # Google STT, microphone capture, threaded queue interface
└── config.json        # Runtime configuration (lifetime, camera index, etc.)
```

---

## Setup

**Requirements:** Python 3.10+, an OpenAI API key, and a webcam.

```bash
pip install openai opencv-python speechrecognition colorama python-vlc python-dotenv
```

Add your API key to a `.env` file:

```
OPENAI_API_KEY=your_key_here
```

Run:

```bash
cd src
python main.py
```

The agent will wait silently until it detects a face, then introduce itself.

---

## Configuration

Edit `src/config.json` to adjust behaviour:

| Key | Description | Default |
|---|---|---|
| `LLM_LIFETIME` | Seconds before the agent shuts down | `300` |
| `MULTIPLE_CAMERAS` | Randomly pick from a list of camera indices | `false` |
| `CAMERA_DIGITS` | Camera index or list of indices | `[0, 1]` |
