import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

# Download necessary resources
nltk.download('wordnet')
nltk.download('wordnet_ic')

def calculate_similarity(input_word1, input_word2):
    # Get the first synset (set of synonyms) for the input words
    word1 = wn.synsets(input_word1)[0]
    word2 = wn.synsets(input_word2)[0]

    # Calculate path similarity (structural similarity)
    path_similarity = word1.path_similarity(word2)
    print("Path similarity:", path_similarity)

    # Calculate Wu-Palmer similarity (structural similarity)
    wup_similarity = word1.wup_similarity(word2)
    print("Wu-Palmer similarity:", wup_similarity)

    # Load information content
    ic = wordnet_ic.ic('ic-brown.dat')

    # Calculate Resnik similarity (semantic similarity)
    resnik_similarity = word1.res_similarity(word2, ic)
    print("Resnik similarity:", resnik_similarity)
    max_score = word1.res_similarity(word1, ic)
    normalized_resnik_similarity = resnik_similarity / max_score
    print("Resnik similarity (normalized):", normalized_resnik_similarity)

    # Calculate Lin similarity (semantic similarity)
    lin_similarity = word1.lin_similarity(word2, ic)
    print("Lin similarity:", lin_similarity)

    # Calculate Jiang-Conrath similarity (semantic similarity)
    jiang_conrath_similarity = word1.jcn_similarity(word2, ic)
    print("Jiang-Conrath similarity:", jiang_conrath_similarity)

    # Print separating line
    print("#" * 50)

while True:
    print("\nEnter two words to calculate their similarity (type 'exit' to quit):")
    input_word1 = input("Enter the first word: ")

    if input_word1.lower() == 'exit':
        break

    input_word2 = input("Enter the second word: ")

    if input_word2.lower() == 'exit':
        break

    calculate_similarity(input_word1, input_word2)
