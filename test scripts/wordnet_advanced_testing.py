import gensim
from scipy import spatial

# load the Word2Vec model
model = gensim.models.KeyedVectors.load_word2vec_format('numberbatch19/numberbatch-en-19.08.txt', binary=False)
# model = gensim.models.KeyedVectors.load_word2vec_format('glove/glove.6B.300d.txt', binary=False, no_header=True)


# define the input words
input_word1 = "man"
input_word2 = "woman"

# read the list of words from a file
with open("../input/1k_common_ADJECTIVES.txt", "r") as f:
    word_list = [line.strip() for line in f.readlines()]

# calculate the cosine similarity between each input word and each word in the list
similarities1 = {}
similarities2 = {}
for word in word_list:
    if word.lower() in model.key_to_index:
        vector1 = model[input_word1]
        vector2 = model[input_word2]
        vector3 = model[word.lower()]
        similarity1 = 1 - spatial.distance.cosine(vector1, vector3)
        similarity2 = 1 - spatial.distance.cosine(vector2, vector3)
        similarities1[word.lower()] = similarity1
        similarities2[word.lower()] = similarity2

# sort the dictionaries of similarities by descending value
sorted_similarities1 = sorted(similarities1.items(), key=lambda x: x[1], reverse=True)[:40]
sorted_similarities2 = sorted(similarities2.items(), key=lambda x: x[1], reverse=True)[:40]

# create sets of top 50 adjectives for each input word
adjectives1 = set([word[0] for word in sorted_similarities1])
adjectives2 = set([word[0] for word in sorted_similarities2])

# take the symmetric difference of both sets to get a list of unique adjectives for both words
unique_adjectives = adjectives1.symmetric_difference(adjectives2)

# print the unique adjectives
print(f"Unique adjectives for '{input_word1}' and '{input_word2}':")
print(unique_adjectives)

