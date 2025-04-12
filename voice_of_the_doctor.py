import os
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="Hi this is Ai Uponika!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Will",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

#Step2: Use Model for Text output to Voice

import os
import platform
import subprocess
from pydub import AudioSegment
from elevenlabs import save
from elevenlabs.client import ElevenLabs
import sys
import re
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.Popen([sys.executable, "-c", f"from playsound import playsound; playsound(r'{output_filepath}')"])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text="Hi this is Uponika Roy, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def convert_mp3_to_wav(mp3_file, wav_file):
    sound = AudioSegment.from_mp3(mp3_file)
    sound.export(wav_file, format="wav")

def clean_and_shorten_text(text):
    # Remove markdown like **bold** and *italic*
    clean_text = re.sub(r'\*+', '', text)   

    
    # Add an enthusiastic intro if missing
    if not clean_text.startswith("Wow") and not clean_text.startswith("You're"):
        clean_text = "You're going to love this! " + clean_text
    
    return clean_text

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    final_text = clean_and_shorten_text(input_text)
    audio = client.generate(
        text=final_text,
        voice="Domi",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    save(audio, output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Windows":
            wav_filepath = output_filepath.replace(".mp3", ".wav")
            subprocess.Popen([sys.executable, "-c", f"from playsound import playsound; playsound(r'{output_filepath}')"])
        elif os_name == "Darwin":
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath])  # Or replace with ffplay if needed
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Call the function
input_text = "Hi, this is Uponika Roy from ElevenLabs autoplay test!"
# text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")