import gensim.downloader as api
from gensim.models import KeyedVectors
model = api.load('glove-wiki-gigaword-300') # Load the glove model

# model = KeyedVectors.load_word2vec_format('glove/glove.6B.300d.txt', binary=False, no_header=True)


def get_distinctive_adjectives(word1, word2, model):
    word1_adjectives = []
    word2_adjectives = []
    # Get adjectives for word1
    for adj in model.most_similar(positive=[word1, 'JJ'], topn=500):
        word1_adjectives.append(adj[0])
    # Get adjectives for word2
    for adj in model.most_similar(positive=[word2, 'JJ'], topn=500):
        word2_adjectives.append(adj[0])
    # Find distinctive adjectives
    distinctive_adjectives = list(set(word1_adjectives) ^ set(word2_adjectives))
    return distinctive_adjectives


get_distinctive_adjectives("king", "queen", model)
