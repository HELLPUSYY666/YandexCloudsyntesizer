import os
import subprocess
import time
import requests
from flask import Flask, request, jsonify

token = 't1.9euelZqey57PmZrIm4mbnZWPy5ySm-3rnpWalcaKiouUlcnPmoqXjJiTkcbl9PczD0tH-e8rfzm73fT3cz1IR_nvK385u83n9euelZqZmJKUjJWPx4mbx87JkMyane_8xeuelZqZmJKUjJWPx4mbx87JkMyanQ.3dgm_FfYUF8NxdmDmazKVKgY_MIDR_jwqbsC3CTyLWd1-B5eilSNXJW7E1ykrg8Jl-QwfhP5tnFsSJ4huGz2Dg'
folder_id = 'b1gljv4klrpj79nu4s95'

root_path = os.path.dirname(__file__)
target_path = '/tmp/speechkit/'

os.makedirs(target_path, exist_ok=True)


def synthesize(text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {'Authorization': 'Bearer ' + token}

    data = {
        'folderId': folder_id,
        'text': text,
        'lang': 'ru-RU',
        'voice': 'jane',
        'emotion': 'evil',
        'speed': '1.1',
        'format': 'lpcm',
        'sampleRateHertz': 48000,
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError(f"Invalid response received: code: {resp.status_code}, message: {resp.text}")

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def write_file(text):
    filename = str(int(time.time()))
    with open(os.path.join(target_path, f"{filename}.raw"), "wb") as f:
        for audio_content in synthesize(text):
            f.write(audio_content)

    time.sleep(2)
    return filename


def convert(filename):
    cmd = [
        "/opt/homebrew/bin/sox",
        "-r", "48000", "-b", "16", "-e", "signed-integer", "-c", "1",
        os.path.join(target_path, f"{filename}.raw"),
        os.path.join(target_path, f"{filename}.wav"),
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Conversion failed: {result.stderr}")


def read_text():
    with open("text.txt", "r", encoding="UTF-8") as f:
        text = f.read()
    return text


convert(write_file(read_text()))

app = Flask(__name__)


@app.route('/synthesize', methods=['POST'])
def api_synthesize():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "Text is required"}), 400

    filename = write_file(text)
    convert(filename)

    return jsonify({"message": "Synthesis completed", "filename": filename + ".wav"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
