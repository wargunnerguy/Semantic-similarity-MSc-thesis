import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

DEFAULT_NR_OF_SIMILAR_WORDS = 15
BASIC_WORDS_FILE = 'input/basic_words.txt'  # words to exclude


with open(BASIC_WORDS_FILE, "r") as f:
    common_words = set(line.strip().lower() for line in f)

# create a lemmatizer object
lemmatizer = WordNetLemmatizer()

# read in the file and split each line by comma
filename = "input/wikicooccurrence/wikimatrixrelatedtop20000"
with open(filename, 'r') as f:
    data = [line.strip().split(',') for line in f.readlines()]

# define a function to extract the cooccurring words for a given input word
def get_cooccurring_words(input_word, limit=DEFAULT_NR_OF_SIMILAR_WORDS):
    # find the line with the input word
    for line in data:
        if line[0] == input_word:
            # extract the cooccurring words and their occurrence numbers
            cooccurring_words = line[2::2]
            cooccurring_occurrences = [int(o) for o in line[3::2]]
            main_occurrences = int(line[1])
            # calculate the weights and store in a dictionary
            weights = {}
            counter = 0  # initialize the counter variable
            for i, word in enumerate(cooccurring_words):
                # check if the word is in the common word list and skip it if it is
                if word in common_words:
                    continue
                # perform POS tagging on the cooccurring word
                pos_tag = nltk.pos_tag([word])[0][1]
                if pos_tag.startswith('JJ') or pos_tag.startswith('VB'):
                    if word not in weights and cooccurring_occurrences[i] > 0:
                        # lemmatize the word
                        lemma = lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos_tag))
                        weight = round(cooccurring_occurrences[i] / main_occurrences, 2)
                        weights[lemma] = weight
                        counter += 1  # increment the counter
                        if counter == limit:  # check if the limit has been reached
                            break
            # sort the words by their weights in descending order
            sorted_words = sorted(weights.keys(), key=lambda w: weights[w], reverse=True)
            # return the words and their weights as a dictionary
            return {word: weights[word] for word in sorted_words}
    # if the input word isn't found, return an empty dictionary
    return {}

# define a helper function to convert nltk POS tags to WordNet POS tags
def get_wordnet_pos(nltk_pos):
    if nltk_pos.startswith('J'):
        return wordnet.ADJ
    elif nltk_pos.startswith('V'):
        return wordnet.VERB
    elif nltk_pos.startswith('N'):
        return wordnet.NOUN
    elif nltk_pos.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

get_cooccurring_words.method_name = "WIKI_CO"

if __name__ == '__main__':
    while True:
        # ask the user for an input word and print out the cooccurring words and their weights
        input_word = input("[WIKI COOCCURRENCE]: Enter a word (or 'exit' to quit): ")
        if input_word.lower() == 'exit':
            break
        cooccurring_words = get_cooccurring_words(input_word)
        if len(cooccurring_words) == 0:
            print("Sorry, that word was not found.")
        else:
            print("Cooccurring adjectives and verbs for", input_word + ":")
            print(", ".join([f"{word}: {weight}" for word, weight in cooccurring_words.items()]))