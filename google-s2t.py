import argparse

from google.cloud import speech
from pydub import AudioSegment


def main(speech_file):
    """Transcribe the given audio file synchronously with
        the selected model."""

    client = speech.SpeechClient()

    sound = AudioSegment.from_wav(speech_file)
    sound = sound.set_channels(1)
    sound.export("temp", format="wav")

    with open("temp.wav", 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        # encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code='ro-RO',
        model='command_and_search')

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'speech_file', help='Full path of audio file to be recognized')
    args = parser.parse_args()
    main(args.speech_file)
