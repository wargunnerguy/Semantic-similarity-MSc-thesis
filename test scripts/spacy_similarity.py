from gensim.models.keyedvectors import KeyedVectors
import itertools
import gensim.downloader as api

model = api.load("fasttext-wiki-news-subwords-300")
def get_similar_words(word, n=20):
    return [w[0] for w in model.most_similar(word, topn=n)]

def get_distinguishing_words(word1, word2, n=10):
    word1_similarities = get_similar_words(word1)
    word2_similarities = get_similar_words(word2)

    combined_similarities = list(itertools.product(word1_similarities, word2_similarities))
    differences = [(w1, w2, model.similarity(w1, w2)) for w1, w2 in combined_similarities]
    differences = sorted(differences, key=lambda x: x[2], reverse=False)

    return [(w1, w2) for w1, w2, _ in differences[:n]]

input_word = "queen"
similar_words = get_similar_words(input_word)

for similar_word in similar_words:
    print(f"Input word: {input_word}, Similar word: {similar_word}")
    distinguishing_words = get_distinguishing_words(input_word, similar_word)
    print("Distinguishing words:", distinguishing_words)
    print("\n")
