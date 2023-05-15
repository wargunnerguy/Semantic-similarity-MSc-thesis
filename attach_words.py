from conceptnet_similar_terms_finder import get_related_terms
from cooccurrence_finder import get_cooccurring_words
from cosinesimilarity_finder import get_similar_words
from sister_terms import get_type_of_words_from_sister_term_descriptions
from prettytable import PrettyTable


def attach_words_to_input(word, *methods):
    merged_words = {}
    for method in methods:
        method_name = method.method_name
        words = method(word)
        for w, weight in words.items():
            if w not in merged_words:
                merged_words[w] = {"count": 1, "methods": [method_name], "weight": weight}
            else:
                merged_words[w]["count"] += 1
                merged_words[w]["methods"].append(method_name)
                if weight > merged_words[w]["weight"]:
                    merged_words[w]["weight"] = weight
    return [{"input_word": word, "words": merged_words}]

def test_attach_words_to_input():
    while True:
        word = input("Enter a word (or type 'exit' to quit): ")
        if word.lower() == "exit":
            break

        attached_words = attach_words_to_input(word, get_cooccurring_words, get_related_terms, get_similar_words, get_type_of_words_from_sister_term_descriptions)

        table = PrettyTable()
        table.field_names = ["Input Word", "Word", "Methods", "Weight", "Count"]
        table.align["Word"] = "l"
        table.align["Methods"] = "l"

        for result in attached_words:
            input_word = result["input_word"]
            for word, word_info in result["words"].items():
                methods = ", ".join(word_info["methods"])
                table.add_row([input_word, word, methods, round(word_info["weight"], 2), word_info["count"]])

        print(table)

if __name__ == "__main__":
    test_attach_words_to_input()
