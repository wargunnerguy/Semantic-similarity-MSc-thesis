from conceptnet_similar_terms_finder import get_related_terms
from cooccurrence_finder import get_cooccurring_words
from cosinesimilarity_finder import get_similar_words
from sister_terms import get_type_of_words_from_sister_term_descriptions
from attach_words import attach_words_to_input
from prettytable import PrettyTable

def find_differentiating_words(word1, word2, *methods):
    results_word1 = attach_words_to_input(word1, *methods)[0]["words"]
    results_word2 = attach_words_to_input(word2, *methods)[0]["words"]

    # Compute the symmetric difference while preserving the order
    symmetric_difference = [word for word in results_word1.keys() if word not in results_word2.keys()]
    symmetric_difference.extend([word for word in results_word2.keys() if word not in results_word1.keys()])

    # Remove the input words
    symmetric_difference = [word for word in symmetric_difference if word != word1 and word != word2]

    ordered_result = []
    word_data = {}
    for word in symmetric_difference:
        methods = []
        if word in results_word1:
            methods.extend(results_word1[word]["methods"])
        if word in results_word2:
            methods.extend(results_word2[word]["methods"])

        count = 0
        if word in results_word1:
            count += results_word1[word]["count"]
        if word in results_word2:
            count += results_word2[word]["count"]

        word_data[word] = {"count": count, "methods": methods}

    # Sort words based on count and method
    sorted_word_data = sorted(word_data.items(), key=lambda x: (x[1]["count"], x[1]["methods"][0]), reverse=True)

    # Group words by method
    method_groups = {}
    for word, data in sorted_word_data:
        method = data["methods"][0]
        if method not in method_groups:
            method_groups[method] = []
        method_groups[method].append({"word": word, "methods": data["methods"], "count": data["count"]})

    # Combine words by alternating methods
    ordered_result = []
    while method_groups:
        for method in list(method_groups):
            if method_groups[method]:
                ordered_result.append(method_groups[method].pop(0))
            else:
                del method_groups[method]

    return ordered_result, results_word1, results_word2, word_data

def test_find_differentiating_words():
    while True:
        word1 = input("Enter the first word (or type 'exit' to quit): ")
        if word1.lower() == "exit":
            break

        word2 = input("Enter the second word (or type 'exit' to quit): ")
        if word2.lower() == "exit":
            break

        differentiating_words, results_word1, results_word2, word_count = find_differentiating_words(word1, word2, get_cooccurring_words, get_related_terms, get_similar_words, get_type_of_words_from_sister_term_descriptions)

        table = PrettyTable()
        table.field_names = ["Word", "Method", "Weight", "Occurrences"]
        table.align["Word"] = "l"
        table.align["Method"] = "l"

        for word_info in differentiating_words:
            methods = ', '.join(word_info['methods'])
            weight = 0
            if word_info['word'] in results_word1:
                weight = results_word1[word_info['word']]["weight"]
            elif word_info['word'] in results_word2:
                weight = results_word2[word_info['word']]["weight"]
            table.add_row([word_info['word'], methods, f"{weight:.2f}", word_info['count']])



        print(table)

if __name__ == "__main__":
    test_find_differentiating_words()
