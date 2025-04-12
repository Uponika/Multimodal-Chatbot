from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs, text_to_speech_with_gtts
import os
from dotenv import load_dotenv
load_dotenv()
import re
import gradio as gr

system_prompt="""You are a knowledgeable and friendly Canadian tourist guide. Speak in a warm and conversational tone as if you're assisting a visitor in real life. Your job is to recommend must-see places, local experiences, and helpful travel tips across Canada. Tailor your suggestions based on seasons, interests (e.g., nature, food, history, adventure), and location. Avoid using technical jargon or sounding robotic—be upbeat, engaging, and informative like a true local expert. Keep your responses clear and concise, and always invite further questions if the traveler wants to know more. Keep your responses short and within maximum of 10 complete sentences."""

def process_inputs(audio_file_path, image_filepath):
    # Step 1: Transcribe voice input
    speech_to_text_output = transcribe_with_groq(
        stt_model="whisper-large-v3",
        audio_filepath=audio_file_path,
        GROQ_API_KEY=os.environ['GROQ_API_KEY']
    )

    # Step 2: Analyze image using vision model
    if image_filepath:
        query = system_prompt + " " + speech_to_text_output
        doctor_response = analyze_image_with_query(
            query=query,
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
         
        doctor_response = re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', doctor_response)
    else:
        doctor_response = "No image provided for me to analyze."

    # Step 3: Convert doctor's response to speech
    audio_output_path = "final.mp3"
    text_to_speech_with_elevenlabs(
        input_text=doctor_response,
        output_filepath=audio_output_path
    )

    return speech_to_text_output, doctor_response, audio_output_path
# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Guide's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="Personal AI Tour Guide"
)

iface.launch(debug=True)