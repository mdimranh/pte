import eng_to_ipa as ipa
import nltk
from django.http import JsonResponse
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.security.permission import IsStudentPermission
from rest_framework.views import APIView
from django.db.models import Q

from .models import ReadAloud
from .serializers import ReadAloudSerializer, ReadAloudAnswerListSerializer
from ..answer.models import Answer

# nltk.download("wordnet")
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')



class ReadAloudView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = ReadAloudSerializer
    queryset = ReadAloud.objects.all()

class ReadAloudCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    permission_classes = [IsAdminUser]
    queryset = ReadAloud.objects.all()
    serializer_class = ReadAloudSerializer

class ReadAloudListView(ListAPIView):
    queryset = ReadAloud.objects.all()
    serializer_class = ReadAloudSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query')
        practiced = self.request.query_params.get('practiced') == 'true'
        if query and practiced:
            if query.isnumeric():
                return ReadAloud.objects.filter(
                    Q(title__icontains=query) | Q(id=query),
                    answer__isnull=not practiced
                )
            else:
                return ReadAloud.objects.filter(
                    title__icontains=query,
                    answer__isnull=not practiced
                )
        elif query:
            if query.isnumeric():
                return ReadAloud.objects.filter(
                    Q(title__icontains=query) | Q(id=query)
                )
            else:
                return ReadAloud.objects.filter(
                    title__icontains=query
                )
        return self.queryset.all()

def get_main_word(word):
    lemmatizer = WordNetLemmatizer()
    word_forms = word_tokenize(word)
    main_words = [lemmatizer.lemmatize(w, pos=get_wordnet_pos(pos)) for w, pos in nltk.pos_tag(word_forms)]
    return main_words

def get_wordnet_pos(tag):
    tag = tag[0].upper()
    tag_dict = {
        "J": wordnet.ADJ,
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "R": wordnet.ADV,
    }
    return tag_dict.get(tag, wordnet.NOUN)  # default to noun if the POS tag is not found

def get_word_details(word, num_examples=100):
    main_words = get_main_word(word)
    synsets = []
    for main_word in main_words:
        synsets.extend(wordnet.synsets(main_word))

    if not synsets:
        return None

    meanings = [synset.definition() for synset in synsets]

    examples_with_word = {}
    for pos in [wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV]:
        examples_with_word[pos] = []

    for synset in synsets:
        examples = synset.examples()
        for pos in [wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV]:
            if synset.pos() == pos:
                examples_with_word[pos].extend(examples)

    # Take num_examples from each type of example
    examples_with_word = {pos: examples[:num_examples] for pos, examples in examples_with_word.items()}

    synonyms = list(dict.fromkeys([lemma.name() for synset in synsets for lemma in synset.lemmas()]))
    antonyms = []
    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma.antonyms():
                antonyms.extend([antonym.name() for antonym in lemma.antonyms()])
    antonyms = list(dict.fromkeys(antonyms))

    return {
        # "main_word": main_words,
        "ipa": ipa.convert(word),
        "meanings": meanings,
        "examples_with_word": examples_with_word,
        "synonyms": synonyms[:5],
        "antonyms": antonyms[:5]
    }

class GetWordDetails(APIView):
    def get(self, request, *args, **kwargs):
        word = request.GET.get('word')
        details =  get_word_details(word)
        return JsonResponse(details, safe=False)


class SummarizeAnswerListView(ListAPIView):
    serializer_class = ReadAloudAnswerListSerializer
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(read_aloud=pk)

        return queryset

class MyAnswerListView(ListAPIView):
    serializer_class = ReadAloudAnswerListSerializer
    permission_classes = (IsStudentPermission,)
    def get_queryset(self):
        # Get the primary key (pk) from the URL query parameters
        pk = self.kwargs.get('pk')

        # Filter the Answer objects based on the 'summarize' field with the given 'pk'
        queryset = Answer.objects.filter(read_aloud=pk, user=self.request.user)

        return queryset