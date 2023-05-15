from gensim.models import KeyedVectors
import nltk
from nltk.stem import WordNetLemmatizer

DEFAULT_NR_OF_SIMILAR_WORDS = 15

# Load the pre-trained vectors
model = KeyedVectors.load_word2vec_format('models/glove/glove.6B.50d.txt', binary=False, no_header=True)

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()


import logging

def get_similar_words(input_word, limit=DEFAULT_NR_OF_SIMILAR_WORDS):
    try:
        # Find the most similar words
        similar_words = model.similar_by_word(input_word, topn=200)
    except:
        return {}

    # Filter the similar words to only include adjectives and verbs
    filtered_words = []
    for word, score in similar_words:
        pos_tag = nltk.pos_tag([word])[0][1]
        if pos_tag.startswith('JJ') or pos_tag.startswith('VB'):
            filtered_words.append(word.lower())
        if len(filtered_words) == limit: # Change 50 to the desired length
            break

    # Lemmatize the filtered words
    lemmatized_words = [lemmatizer.lemmatize(word, pos='v') for word in filtered_words]

    # Keep track of the highest score for each base word
    base_words = {}
    for word, score in similar_words:
        for lemma in lemmatized_words:
            if word.lower() == lemma.lower():
                base_word = lemmatizer.lemmatize(word.lower(), pos='v')
                if base_word not in base_words or score > base_words[base_word]:
                    base_words[base_word] = score

    # Remove duplicates and sort alphabetically
    unique_words = sorted(list(set(base_words.keys())))

    # Calculate the cosine similarity scores for the filtered and lemmatized words
    similar_words_filtered = {word: score for word, score in similar_words if lemmatizer.lemmatize(word, pos='v') in unique_words and score == base_words[lemmatizer.lemmatize(word, pos='v')]}

    return similar_words_filtered


get_similar_words.method_name = "COS_SIM"

if __name__ == '__main__':
    while True:
        # Ask for user input
        input_word = input("[COSINE SIMILARITY]: Enter a word (or 'exit' to quit): ")
        if input_word.lower() == 'exit':
            break

        # Get similar words and their cosine similarity scores
        similar_words = get_similar_words(input_word)

        # Print out the similar words and their cosine similarity scores
        print(f"Words similar to '{input_word}':")
        for word, score in similar_words.items():
            print(f"{word}:{score}")

