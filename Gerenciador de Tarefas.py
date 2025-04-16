#___________________________ TAREFAS __________________________________l
from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Gerenciador de Tarefas.html')

# Reconhecimento de voz pelo microfone
@app.route('/audio', methods=['POST'])
def reconhecer_audio_microfone():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        time.sleep(0.5)
        print("Diga o que deseja acrescentar na lista...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            texto = recognizer.recognize_google(audio, language="pt-BR")
            return jsonify({'tarefa': texto})
        except sr.UnknownValueError:
            return jsonify({'tarefa': "Não foi possível entender o áudio."})
        except Exception as e:
            return jsonify({'tarefa': f"Erro ao processar o áudio: {str(e)}"})

# (Opcional) Reconhecimento por arquivo (ex: áudio enviado do frontend)
@app.route('/audio-file', methods=['POST'])
def reconhecer_audio_arquivo():
    try:
        from pydub import AudioSegment
        import tempfile
        import os

        audio_file = request.files['audio']

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            audio_path = tmp.name
            audio_file.save(audio_path)

        wav_path = audio_path + ".wav"
        audio = AudioSegment.from_file(audio_path)
        audio.export(wav_path, format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_google(audio_data, language="pt-BR")

        os.remove(audio_path)
        os.remove(wav_path)

        return jsonify({'tarefa': texto})
    except Exception as e:
        return jsonify({'tarefa': f"Erro ao processar o áudio: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
