# Питоновские библиотеки
from speechkit import Session, ShortAudioRecognition
from speech_recognition import Recognizer, AudioFile
from subprocess import run

# Cвои библиотеки
from config import oauth_token, catalog_id

def oga_to_wav(src, dest):
    process = run(['ffmpeg', '-i', src, dest])
    if process.returncode != 0:
        raise Exception("Something went wrong")

def voice_to_text_yandex(path):
    session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)

    with open(path, 'rb') as f:
        data = f.read()

    recognizeShortAudio = ShortAudioRecognition(session)

    text = recognizeShortAudio.recognize(
        data, format='lpcm', sampleRateHertz='48000')
    return text

def voice_to_text_google(path):
    r = Recognizer()
    harvard = AudioFile(path)
    with harvard as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, None, "ru-RU", False)
    except:
        text = ''
    return text