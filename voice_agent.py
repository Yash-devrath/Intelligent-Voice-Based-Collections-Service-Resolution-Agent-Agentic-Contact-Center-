# Voice Agent: Microphone → Whisper STT → Groq AI → gTTS Speaker
import os
import tempfile
import pyaudio
import wave
import whisper
import pygame
from gtts import gTTS
from dotenv import load_dotenv
from agent import run_agent
from actions import send_payment_link, offer_emi, schedule_callback

load_dotenv()

CUSTOMER_ID = "CUST_001"

# Load Whisper model once (base = fast + accurate)
print("⏳ Loading Whisper model... (first time takes 1 minute)")
whisper_model = whisper.load_model("base")
print("✅ Whisper ready!\n")

# ──────────────────────────────────────
# RECORD voice from microphone
# ──────────────────────────────────────
def record_audio(filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    print("🎙️  Listening... speak now!")

    stream = p.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("✅ Recording done.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# ──────────────────────────────────────
# SPEECH TO TEXT using Whisper (offline)
# ──────────────────────────────────────
def speech_to_text(filename):
    print("🔄 Converting speech to text...")
    result = whisper_model.transcribe(filename, language="en")
    return result["text"].strip()

# ──────────────────────────────────────
# TEXT TO SPEECH using gTTS
# ──────────────────────────────────────
def text_to_speech(text):
    print("🔊 Speaking reply...")
    
    # Save to a fixed file in project folder (avoids Windows temp file locking)
    audio_path = "agent_reply.mp3"
    
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(audio_path)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

# ──────────────────────────────────────
# MAIN VOICE LOOP
# ──────────────────────────────────────
def run_voice_agent():
    print("=" * 50)
    print("🤖 Voice Agent Ready — Accenture Demo")
    print("=" * 50)
    print("Press Ctrl+C anytime to stop.\n")

    while True:
        input("\n⏎  Press ENTER to start speaking...")

        # Save audio to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_file = tmp.name
        tmp.close()

        # Record 5 seconds
        record_audio(audio_file, duration=5)

        # Transcribe
        user_text = speech_to_text(audio_file)
        os.remove(audio_file)

        if not user_text:
            print("⚠️  Nothing detected. Try again.\n")
            continue

        print(f"\n📝 You said: {user_text}")

        # Run AI agent
        reply = run_agent(CUSTOMER_ID, user_text)
        print(f"🤖 Agent: {reply}\n")

        # Trigger actions
        if "payment" in user_text.lower():
            print(send_payment_link(CUSTOMER_ID, 2500))
        elif "emi" in user_text.lower():
            print(offer_emi(CUSTOMER_ID, 6000))
        elif "callback" in user_text.lower():
            print(schedule_callback(CUSTOMER_ID, "Tomorrow 10 AM"))

        # Speak the reply
        text_to_speech(reply)

if __name__ == "__main__":
    run_voice_agent()

