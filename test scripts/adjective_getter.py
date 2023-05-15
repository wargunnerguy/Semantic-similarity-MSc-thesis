import gensim
import nltk

# Load the GloVe model
#glove_model = gensim.models.KeyedVectors.load_word2vec_format('glove/glove.6B.300d.txt', binary=False, no_header=True)
numberbatch_model = gensim.models.KeyedVectors.load_word2vec_format('numberbatch19/numberbatch-en-19.08.txt', binary=False)


# Initialize the nltk POS tagger
nltk.download('averaged_perceptron_tagger')
pos_tagger = nltk.pos_tag

# Create a file to write the adjectives to
output_file = open('../input/glove_full_adjectives.txt', 'w')

# Iterate through the model's vocabulary and check the POS tag of each word
for word_index in numberbatch_model.key_to_index.values():
    word = numberbatch_model.index_to_key[word_index]
    pos = pos_tagger([word])[0][1]
    if pos.startswith('JJ'):  # check if the word is an adjective
        output_file.write(word + '\n')

# Close the output file
output_file.close()