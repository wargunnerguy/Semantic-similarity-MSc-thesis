import requests
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

DEFAULT_NR_OF_SIMILAR_WORDS = 15


def remove_clutter(text):
    # remove articles and other clutter from text
    pattern = re.compile(r'\b(a|an|the|of|in|on|at|to|for|with|by)\b', re.I)
    text = re.sub(pattern, '', text).strip()
    return re.sub(r'\s+', ' ', text)  # remove extra spaces between words

def get_related_terms(word, limit=DEFAULT_NR_OF_SIMILAR_WORDS):
    url = f'http://api.conceptnet.io/c/en/{word}?rel=/r/RelatedTo&filter=/c/en/'
    response = requests.get(url)
    data = response.json()

    lemmatizer = WordNetLemmatizer()
    related_terms = {}
    for edge in data['edges']:
        term = edge['end']['label']
        if term != word:  # exclude input word
            weight = round(edge['weight'], 2)
            term = remove_clutter(term)
            if term and len(term.split()) == 1:  # skip terms with more than one word
                # lemmatize the term
                lemma = lemmatizer.lemmatize(term, wordnet.ADJ)
                if not wordnet.synsets(lemma, pos=wordnet.ADJ):  # check if it's a valid English word
                    lemma = lemmatizer.lemmatize(term, wordnet.NOUN)
                if not wordnet.synsets(lemma, pos=wordnet.NOUN):  # check if it's a valid English word
                    lemma = term
                related_terms[lemma.lower()] = weight
                if len(related_terms) == limit:  # check if the limit is reached
                    break

    if len(related_terms) > 0:
        total_weight = sum(related_terms.values())
        for term in related_terms:
            related_terms[term] /= total_weight  # normalize weights

    sorted_related_terms = {k: v for k, v in sorted(related_terms.items(), key=lambda item: item[1], reverse=True)}

    return sorted_related_terms


get_related_terms.method_name = "CN5"


if __name__ == '__main__':
    while True:
        word = input('[CONCEPTNET5] Enter a word to find related terms (or "exit" to quit): ')
        if word.lower() == 'exit':
            break

        related_terms = get_related_terms(word)

        if len(related_terms) > 0:
            print(f'Related terms and normalized weights for "{word}":')
            terms_string = ", ".join(f"{term}:{weight:.2f}" for term, weight in related_terms.items())
            print(terms_string)
        else:
            print(f'No related terms found for "{word}"')