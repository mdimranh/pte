import eng_to_ipa as ipa
import nltk
from django.http import JsonResponse
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from .models import ReadAloud
from .serializers import ReadAloudSerializer

# nltk.download("wordnet")
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')



class ReadAloudView(RetrieveAPIView):
    lookup_field = "pk"
    serializer_class = ReadAloudSerializer
    queryset = ReadAloud.objects.all()

class ReadAloudCreateView(CreateAPIView):
    # permission_classes = [IsAdminUser]
    queryset = ReadAloud.objects.all()
    serializer_class = ReadAloudSerializer

class ReadAloudListView(ListAPIView):
    queryset = ReadAloud.objects.all()
    serializer_class = ReadAloudSerializer



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
