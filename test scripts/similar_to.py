import nltk
from nltk.corpus import wordnet as wn


def get_similar_and_related_words(word):
    similar_words = set()
    also_see_words = set()

    # Get synsets for the input word
    synsets = wn.synsets(word)

    for synset in synsets:
        # Get similar_to-s words
        for similar_synset in synset.similar_tos():
            for lemma in similar_synset.lemmas():
                similar_words.add(lemma.name())

        # Get also_see-s words
        for related_synset in synset.also_sees():
            for lemma in related_synset.lemmas():
                also_see_words.add(lemma.name())

    return similar_words, also_see_words

