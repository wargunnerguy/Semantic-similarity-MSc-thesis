from collections import defaultdict

from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

DEFAULT_NR_OF_SIMILAR_WORDS = 15
BASIC_WORDS_FILE = 'input/basic_words.txt'  # words to exclude


with open(BASIC_WORDS_FILE, "r") as f:
    common_words = set(line.strip().lower() for line in f)


def get_sister_terms(input_word):
    """
    Given an input word, return a list of sister terms from WordNet.
    """
    sister_terms = []
    synsets = wn.synsets(input_word)
    for synset in synsets:
        for hypernym in synset.hypernyms():
            sister_terms += hypernym.hyponyms()
    return sister_terms


def get_adjectives(sister_terms, word_types):
    """
    Given a list of sister terms or a single sister term, extract the words of the given types from their descriptions and
    return them in a list.
    """
    if not isinstance(sister_terms, list):
        sister_terms = [sister_terms]
    if not isinstance(word_types, list):
        word_types = [word_types]
    words = set()
    for sister_term in sister_terms:
        description = sister_term.definition()
        tokens = word_tokenize(description)
        tagged_tokens = pos_tag(tokens)
        words |= set(word.lower() for word, tag in tagged_tokens if tag in word_types)


    return list(words)



def get_type_of_words_from_sister_term_descriptions(input_word, limit=DEFAULT_NR_OF_SIMILAR_WORDS, types_of_words=['JJ', 'VB']):
    """
    Given an input word, return a dictionary of word counts from the descriptions of its sister terms in WordNet,
    with the number of occurrences of each word as the value, sorted by the value in descending order.
    """


    sister_terms = get_sister_terms(input_word)
    descriptive_words = []
    for sister_term in sister_terms:
        if '(' in sister_term.definition():
            descriptive_words += get_adjectives(sister_term, types_of_words)

    result = defaultdict(int)
    for word in descriptive_words:
        if word.lower() not in common_words:
            result[word] += 1

    sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:limit])
    return sorted_result



get_type_of_words_from_sister_term_descriptions.method_name = "WN_SIS"


def load_basic_words(basic_words_file):
    with open(basic_words_file, "r") as f:
        raw_basic_words = [line.strip() for line in f]
    return raw_basic_words

def load_non_exotic_words(non_exotic_words_file, basic_words_file, limit=7000):
    print("Setting up " + str(limit) + " non-exotic words: " + non_exotic_words_file)
    with open(non_exotic_words_file, "r") as f:
        non_exotic_words = [line.strip() for line in f]
    if limit is not None:
        non_exotic_words = non_exotic_words[:limit]
    print("Loading in basic words to leave out: " + basic_words_file)
    basic_words = load_basic_words(basic_words_file)
    non_exotic_words = [w for w in non_exotic_words if w not in basic_words]
    return non_exotic_words


if __name__ == '__main__':
    non_exotic_words = load_non_exotic_words("input/20k_common_words_google.txt", "input/basic_words.txt")
    while True:
        input_word = input('Enter a word (or type "quit" to exit): ')
        if input_word.lower() == 'quit':
            break
        adjectives = get_type_of_words_from_sister_term_descriptions(input_word)
        print(adjectives)

