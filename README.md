Yandex TTS API

Overview

This project provides a simplified API for interacting with the Yandex TTS (Text-to-Speech) service, part of Yandex Cloud's Speech Kit. The API allows users to synthesize speech from text input and offers options to customize the voice, speech rate, language, and output file name.

Features

Text Synthesis: Accepts text input for speech synthesis.
Voice Options: Allows selection of the voice of the speaker.
Speech Rate: Provides control over the speed of speech.
Language Support: Enables selection of the language for synthesis.
Audio Output: Returns a download link for the synthesized audio file in WAV format (8 kHz, 128-bit PCM, Mono).
DynDNS Access: The API is accessible via DynDNS or similar services.
Requirements

Docker
Installation

Clone the repository:
git clone <repository-url>
cd <repository-directory>
Build the Docker image:
sudo docker build -t yandex_tts_api .
Run the Docker container:
sudo docker run -p 80:5000 --rm --name yandex_tts_api yandex_tts_api
API Usage

Endpoint: /synthesize
Method: POST
Request Body:{
    "text": "Hello, world!",
    "voice": "oksana",
    "speech_rate": "1.0",
    "language": "ru-RU",
    "output_file_name": "output.wav"
}
Response:
{
    "download_link": "http://example.com/path/to/output.wav"
}
License

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments

Yandex Cloud Documentation for TTS service details.
