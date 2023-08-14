import nltk
import spacy
from nltk.tokenize import word_tokenize
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..answer.models import Answer
from ..summarize.models import Summarize
from .serializers import SummarizeAnswerSerializer

# Load necessary models and resources
# spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
# nltk.download('punkt')

def score_summary(summary, reference):
    # Split the summary into sentences
    sentences = nltk.tokenize.sent_tokenize(summary)

    if len(sentences) > 1:
        # If there are multiple sentences, calculate only the Content score
        content_score = calculate_content_score(summary, reference)

        # Return individual scores and overall score
        scores = {
            'Content': round(content_score, 2),
            'Form': 0,
            'Grammar': 0,
            'Vocabulary': 0,
            'Overall': round(content_score, 2)
        }
    else:
        # If there is only one sentence, calculate scores for all factors
        content_score = calculate_content_score(summary, reference)
        form_score = calculate_form_score(summary)
        grammar_score = calculate_grammar_score(summary)
        vocabulary_score = calculate_vocabulary_score(summary)

        # Calculate overall score
        if form_score > 0:

            overall_score = (content_score + form_score + grammar_score + vocabulary_score)
        else:
            grammar_score=0
            vocabulary_score=0
            overall_score = (content_score + form_score + grammar_score + vocabulary_score)

        # Return individual scores and overall score
        scores = {
            'Content': round(content_score, 2),
            'Form': round(form_score, 2),
            'Grammar': round(grammar_score, 2),
            'Vocabulary': round(vocabulary_score, 2),
            'Overall': round(overall_score, 2)
        }

    return scores

# Example scoring functions

def calculate_content_score(summary, reference):
    # Compare the summary and reference for content relevance
    # Measure the similarity of the summary and reference using spaCy
    doc_summary = nlp(summary)
    doc_reference = nlp(reference)
    content_score = doc_summary.similarity(doc_reference) * 2  # Scaling the similarity score to range 0-2
    return content_score

def calculate_form_score(summary):
    # Check if the summary is in all uppercase
    if summary.isupper():
        return 0

    # Evaluate the form and structure of the summary
    # Score based on the length of the summary
    summary_length = len(word_tokenize(summary))
    if summary_length >= 5 and summary_length <= 74:
        form_score = 1
    # elif summary_length < 50 and summary_length > 5:
    #     # Calculate partial marks based on proximity to 50
    #     form_score = summary_length / 50
    else:
        form_score = 0

    return form_score


def calculate_grammar_score(summary):
    # Check the grammar and language quality of the summary
    # Score based on the number of grammatical errors (using NLTK's Punkt tokenizer as a simple example)
    num_errors = len(nltk.tokenize.sent_tokenize(summary)) - 1
    grammar_score = 2 - num_errors  # Mapping the number of errors to range 0-2
    grammar_score = max(0, grammar_score)  # Ensure the score is not negative
    return grammar_score

def calculate_vocabulary_score(summary):
    # Evaluate the vocabulary usage and richness of the summary
    # Score based on the number of unique words in the summary
    unique_words = set(word_tokenize(summary))
    vocabulary_score = len(unique_words) / 5  # Scaling the unique word count to range 0-2
    vocabulary_score = min(2, vocabulary_score)  # Cap the score at 2
    return vocabulary_score

class SummarizeAnswerCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SummarizeAnswerSerializer(data=request.data)
        if serializer.is_valid():
            # get_summarize = Summarize.objects.filter(id = serializer.validated_data['summarize'].id).first()
            score = score_summary(serializer.validated_data['summarize'].content, self.request.data.get("summarize_text"))
            serializer.save(user=self.request.user, score=score)
            return Response(score)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
