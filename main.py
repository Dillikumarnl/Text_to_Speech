import os
import time
from dotenv import load_dotenv
import PyPDF2
from google.cloud import texttospeech

load_dotenv()

pdf_path = os.getenv('pdf')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('CONFIDENTIAL')

client = texttospeech.TextToSpeechClient()

def extract_text_from_pdf(path):
    """Extract text from a PDF file."""
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


text_for_speech = extract_text_from_pdf(pdf_path)
time.sleep(1)
synthesis_input = texttospeech.SynthesisInput(text=text_for_speech)

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name='en-US-Studio-O',
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    effects_profile_id=['small-bluetooth-speaker-class-device'],
    speaking_rate=1,
    pitch=1
)

response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

with open(f"{pdf_path}.mp3", "wb") as output:
    output.write(response.audio_content)
    print(f'Audio content written to file "{pdf_path.replace(".pdf", "")}.mp3"')
