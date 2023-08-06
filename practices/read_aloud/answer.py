from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .serializers import ReadAloudAnswerCreateSerializer
from .models import ReadAloud
from ..answer.models import Answer

from django.core.files.storage import default_storage

import base64, difflib, io, math, os, re, string, wave, Levenshtein, nltk, spacy, librosa
import speech_recognition as sr
from nltk.metrics.distance import edit_distance
from pydub import AudioSegment
from transformers import pipeline
from collections import Counter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


import uuid, os

# nltk.download('punkt')

recognizer = sr.Recognizer()

# spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

def evaluate_pronunciation(reference_text, user_speech):
    reference_text_clean = re.sub(r'[^\w\s]', '', reference_text.lower())
    user_speech_clean = re.sub(r'[^\w\s]', '', user_speech.lower())

    reference_words = reference_text_clean.split()
    user_speech_words = user_speech_clean.split()

    wer = edit_distance(reference_words, user_speech_words) / len(reference_words)
    pronunciation_score = 1 - wer

    return pronunciation_score * 90

def word_similarity(word1, word2):
    doc1 = nlp(word1)
    doc2 = nlp(word2)
    return doc1.similarity(doc2)

def evaluate_content(reference_text, user_speech):
    reference_text_clean = re.sub(r'[^\w\s]', '', reference_text.lower())
    user_speech_clean = re.sub(r'[^\w\s]', '', user_speech.lower())
    reference_words = reference_text_clean.split()
    user_speech_words = user_speech_clean.split()
    word_highlight = []
    # def find_error_words(reference_text, user_speech):
    # reference_words = reference_text
    # user_speech_words = user_speech
    # Function to find the Longest Common Subsequence (LCS) of two lists
    def lcs(X, Y):
        m = len(X)
        n = len(Y)
        dp = [[0] * (n+1) for _ in range(m+1)]

        for i in range(1, m+1):
            for j in range(1, n+1):
                if X[i-1] == Y[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        lcs_length = dp[m][n]
        lcs_words = []
        i, j = m, n
        while i > 0 and j > 0:
            if X[i-1] == Y[j-1]:
                lcs_words.insert(0, X[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        return lcs_words

    # Get the Longest Common Subsequence (LCS) of the two texts
    lcs_words = lcs(reference_words, user_speech_words)

    # Find the error words by comparing LCS words with the reference words
    error_words = []
    i, j = 0, 0
    for word in reference_words:
        if i < len(lcs_words) and word == lcs_words[i]:
            i += 1
            word_highlight.append((word, "correct"))
        else:
            error_words.append(word)
            word_highlight.append((word,"error"))
    for i, (word, status) in enumerate(word_highlight):
        if status == "error":
            found_match = False
            for error_word in user_speech_words:
                similarity = calculate_word_similarity(word, error_word)
                if similarity > 0.7:
                    if reference_words.count(error_word) > 1:
                        word_highlight[i] = (word, "missing")
                    else:
                        word_highlight[i] = (word, "mispronounced")
                    found_match = True
                    break
            if not found_match:
                word_highlight[i] = (word, "missing")
    user_word_counts = Counter(user_speech_words)
    lcs_word_counts = Counter(reference_words)
    # extra_words = [word for word, count in user_word_counts.items() if count > lcs_word_counts[word]]
    extra_words = []

    # Find extra words based on the conditions
    for word, count in user_word_counts.items():
        if count > lcs_word_counts[word]:
            has_similar_mispronounced_word = any(calculate_word_similarity(word, mis_word) > 0.7 for mis_word, status in word_highlight if status == "mispronounced")
            if not has_similar_mispronounced_word:
                extra_words.extend([word] * (count - lcs_word_counts[word]))


    score = 90

    # Calculate the total number of words in the reference text
    total_reference_words = len(reference_text_clean)
    # Calculate the total number of words in the user speech
    total_user_words = len(user_speech_clean)

    # Calculate the penalty for each missing/extra word based on the total number of words
    penalty_per_word = 90 / total_reference_words

    # Deduct marks for each missing word
    for word, status in word_highlight:
        if status == "missing":
            # Deduct marks based on the total number of words
            word_penalty = penalty_per_word * len(word)
            score -= word_penalty

    # Deduct marks for extra words
    for word in extra_words:
        # Deduct marks based on the total number of words
        word_penalty = penalty_per_word * len(word)
        score -= word_penalty
    return score
def calculate_word_similarity(word1, word2):
    return difflib.SequenceMatcher(None, word1, word2).ratio()

def count_repetitions(user_speech):
    words = user_speech.split()
    repetitions = 0

    for i in range(len(words) - 1):
        if words[i] == words[i + 1]:
            repetitions += 1

    return repetitions
def count_false_starts(user_speech):
    false_starts = 0
    sentences = user_speech.split('.')

    for sentence in sentences:
        words = sentence.strip().split()
        if len(words) > 1 and words[0] == words[1]:
            false_starts += 1

    return false_starts
def count_long_pauses(user_speech, pause_threshold=2.0):
    long_pauses = 0
    words = user_speech.split()
    time_between_words = [len(word) / 3.5 for word in words]  # Assuming an average reading speed of 3.5 characters per second

    for i in range(len(words) - 1):
        if time_between_words[i + 1] - time_between_words[i] > pause_threshold:
            long_pauses += 1

    return long_pauses
def get_audio_duration(audio_path):
    with wave.open(audio_path, "rb") as audio_file:
        frame_rate = audio_file.getframerate()
        num_frames = audio_file.getnframes()
        duration = num_frames / float(frame_rate)
    return duration


def calculate_speech_rate(audio_path):
    # Load the audio file
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    # Perform speech recognition to transcribe the audio
    transcription = r.recognize_google(audio)

    # Count the number of words
    words = transcription.split()
    num_words = len(words)

    # Calculate the speech duration in seconds
    speech_duration = get_audio_duration(audio_path)

    # Calculate the speech rate in words per minute
    if speech_duration > 0:
        speech_rate = (num_words / speech_duration) 
    else:
        speech_rate = 0.0

    return speech_rate


def calculate_speech_rate_score(speech_rate):
    ideal_wps_min = 2.24
    ideal_wps_max = 2.26

    if speech_rate > ideal_wps_min and speech_rate < ideal_wps_max:
        score = 1.0
    elif speech_rate < ideal_wps_min:
        score = max(1.0 - ((ideal_wps_min - speech_rate) / ideal_wps_min) + .15 , 0.0)
    else:
        score = max(1.0 - ((speech_rate - ideal_wps_max) / (ideal_wps_max * 0.5)) + .15, 0.0)

    return score

def evaluate_fluency(audio_path, speech):
    # Measure fluency using various metrics
    repetitions_score = 1.0 - (count_repetitions(speech) * 0.5)  # Adjust fluency based on repetitions
    false_starts_score = 1.0 - (count_false_starts(speech) * 0.5)  # Adjust fluency based on false starts
    long_pauses_score = 1.0 - (count_long_pauses(speech) * 0.5)  # Adjust fluency based on long pauses

    # Calculate the number of disfluencies (hesitations and pauses)
    hesitations = speech.count("uh") + speech.count("um")
    disfluencies_score = 1.0 - ((hesitations) * 0.5)  # Adjust fluency based on disfluencies

    # Calculate the speech rate score
    speech_rate = calculate_speech_rate(audio_path)
    fluency_score = calculate_speech_rate_score(speech_rate)
    print(repetitions_score)
    print(false_starts_score)
    print(long_pauses_score)
    print(disfluencies_score)
    print(fluency_score)
    # Adjust fluency score based on all the metrics
    final_fluency_score = (
        repetitions_score
        + false_starts_score
        + long_pauses_score
        + disfluencies_score
        + 4 * fluency_score
    ) / 8

    # Normalize the score to a scale of 0 to 90
    fluency_score_normalized = round(final_fluency_score * 90, 2)

    return fluency_score_normalized

def get_sampling_rate(audio_path):
    audio, sr = librosa.load(audio_path, sr=None)
    return sr

def read_aloud_and_evaluate(reference_text, audio_file_path):
    # Convert audio file to WAV format
    wav_file_path = "converted_audio.wav"
    audio = AudioSegment.from_file(audio_file_path)
    audio.export(wav_file_path, format="wav")
    print(audio_file_path)

    # imran ------->
    # model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    # tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    # pipe = pipeline("automatic-speech-recognition", model=model, tokenizer=tokenizer)

    pipe = pipeline("automatic-speech-recognition", model="Wav2Vec2")
    # Transcribe the audio
    transcription = pipe(audio_file_path)
    user_speech= transcription['text']
    #user_speech="the bill calls for the establishment of the national landslide hazard seduction program within one year of becoming law the program serves numerous functions including to identify and understand landslide hazards and risk reduced losses from landslides protect communities at risk of landslide hazards and improve communication and emergency preparedness"
    user_speech = user_speech.lower()
    print("User's speech:", user_speech)
    # Perform language processing to identify incorrect words
    # Amar
    reference_text_clean = re.sub(r'[^\w\s]', '', reference_text.lower())
    user_speech_clean = re.sub(r'[^\w\s]', '', user_speech.lower())

    reference_words = reference_text_clean.split()
    user_words = user_speech_clean.split()

    word_highlight = []
    def find_error_words(reference_text, user_speech):
        reference_text_clean = re.sub(r'[^\w\s]', '', reference_text.lower())
        user_speech_clean = re.sub(r'[^\w\s]', '', user_speech.lower())

        reference_words = reference_text_clean.split()
        user_speech_words = user_speech_clean.split()

        # Function to find the Longest Common Subsequence (LCS) of two lists
        def lcs(X, Y):
            m = len(X)
            n = len(Y)
            dp = [[0] * (n+1) for _ in range(m+1)]

            for i in range(1, m+1):
                for j in range(1, n+1):
                    if X[i-1] == Y[j-1]:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = max(dp[i-1][j], dp[i][j-1])

            lcs_length = dp[m][n]
            lcs_words = []
            i, j = m, n
            while i > 0 and j > 0:
                if X[i-1] == Y[j-1]:
                    lcs_words.insert(0, X[i-1])
                    i -= 1
                    j -= 1
                elif dp[i-1][j] > dp[i][j-1]:
                    i -= 1
                else:
                    j -= 1

            return lcs_words

        # Get the Longest Common Subsequence (LCS) of the two texts
        lcs_words = lcs(reference_words, user_speech_words)

        # Find the error words by comparing LCS words with the reference words
        error_words = []
        i, j = 0, 0
        for word in reference_words:
            if i < len(lcs_words) and word == lcs_words[i]:
                i += 1
                word_highlight.append((word, "correct"))
            else:
                error_words.append(word)
                word_highlight.append((word,"error"))
        for i, (word, status) in enumerate(word_highlight):
            if status == "error":
                found_match = False
                for error_word in user_speech_words:
                    similarity = calculate_word_similarity(word, error_word)
                    if similarity > 0.7:
                        if reference_words.count(error_word) > 1:
                            word_highlight[i] = (word, "missing")
                        else:
                            word_highlight[i] = (word, "mispronounced")
                        found_match = True
                        break
                if not found_match:
                    word_highlight[i] = (word, "missing")
        return word_highlight

    def calculate_word_similarity(word1, word2):
        return difflib.SequenceMatcher(None, word1, word2).ratio()

    highlights = find_error_words(reference_text, user_speech)   
    # audio_path = "converted_audio.wav"
    speech = user_speech
    score = evaluate_pronunciation(reference_text, user_speech)
    score = round(score, 2)
    content_score = evaluate_content(reference_text, user_speech)
    content_score = round(content_score, 2)
    fluency_score = evaluate_fluency(wav_file_path, speech)
    total_score= (score+content_score+fluency_score) / 3 
    total_score = round(total_score, 2)
    print("Pronunciation score:", score)
    print("Content score:", content_score)
    print("Fluency score:", fluency_score)
    return score, content_score, user_speech, highlights, fluency_score, total_score

score = False
content_score = False
total_score=False
fluency_score = False
user_speech = False
reference_text = False
word_highlight = []

class ReadAloudAnswerCreate(APIView):

    def post(self, request):
        global score, content_score, user_speech, reference_text, word_highlight, fluency_score, total_score
        serializer = ReadAloudAnswerCreateSerializer(data=request.data)
        if serializer.is_valid():

            data = serializer.validated_data

            audio = request.data.get('audio')
            audio_folder = os.path.join(settings.BASE_DIR , 'audio')
            if not os.path.exists(audio_folder):
                os.makedirs(audio_folder)
            unique_name = str(uuid.uuid4())+'.wav'
            audio_path = os.path.join(audio_folder, unique_name)
            with open(audio_path, 'wb') as file:
                file.write(audio.read())

            get_read_aloud = ReadAloud.objects.get(id = data['read_aloud'].id)
            reference_text = get_read_aloud.content
            score, content_score, user_speech, word_highlight, fluency_score,total_score = read_aloud_and_evaluate(reference_text, audio_path)
            final_score = {
                'score': score,
                'content_score': content_score,
                'user_speech': user_speech,
                'reference_text': reference_text,
                'word_highlight': word_highlight,
                'fluency_score': fluency_score,
                'total_score': total_score
            }
            serializer.save(user=self.request.user, score=final_score)
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return Response(final_score, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# import numpy as np
# from scipy.io import wavfile
# import uuid, os

# class ReadAloudAnswerCreate(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ReadAloudAnswerCreateSerializer
#     def perform_create(self, serializer):
#         data = serializer.validated_data
#         # serialize = serializer.save(user=self.request.user)
#         get_readaloud = ReadAloud.objects.get(id = data['read_aloud'].id)
#         # get_answer = Answer.objects.get(id=serialize.id)
#         reference_text = get_readaloud.content

#         # Save the uploaded file to a temporary file on disk
#         # (Alternatively, you can read the file directly without saving it to disk if needed.)
#         temp_file_path = os.path.join() '/path/to/temporary/file.wav'
#         with open(temp_file_path, 'wb') as temp_file:
#             for chunk in data['audio'].chunks():
#                 temp_file.write(chunk)

#         # Read the WAV file and convert it into a NumPy ndarray
#         sample_rate, audio_data = wavfile.read(temp_file_path)

#         # At this point, you have the audio data in the 'audio_data' variable as a NumPy ndarray,
#         # and 'sample_rate' contains the sample rate of the audio.


#         score, content_score, user_speech, word_highlight, fluency_score, total_score = read_aloud_and_evaluate(reference_text, data['audio'])
#         final_score = {
#             'score': score,
#             'content_score': content_score,
#             'user_speech': user_speech,
#             'reference_text': reference_text,
#             'word_highlight': word_highlight,
#             'fluency_score': fluency_score,
#             'total_score': total_score
#         }
#         serialize = serializer.save(user=self.request.user, score=final_score)
#         # get_answer.final_score = final_score
#         # get_answer.save()