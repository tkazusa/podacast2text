# !/usr/bin/env python
# coding: utf-8
import argparse
import codecs
import datetime
import io
import locale
import sys


def transcribe_gcs(gcs_uri):
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
        enable_automatic_punctuation=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    operationResult = operation.result()

    d = datetime.datetime.today()
    today = d.strftime("%Y%m%d-%H%M%S")
    fout = codecs.open('output{}.txt'.format(today), 'a', 'shift_jis')

    for result in operationResult.results:
        for alternative in result.alternatives:
            fout.write(u'{}\n'.format(alternative.transcript))
    fout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='GCS path for audio file to be recognized')
    args = parser.parse_args()
    print(args.path)
    transcribe_gcs(args.path)
