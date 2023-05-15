import json
from prettytable import PrettyTable, ALL


def lookup(word, data):
    for obj in data:
        for key, value in obj.items():
            if word == key:
                if len(value) > 0:
                    related_word = list(value[0].keys())[0]
                    related_word_score = value[0][related_word][0]
                    descriptive_words = ", ".join(value[0][related_word][1])
                    return key, related_word_score, descriptive_words
                else:
                    return None, None, None
    return None, None, None


if __name__ == '__main__':
    with open('output/V2_20k_common_words_google_may_10_01_20_glove_300d.json') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError as e:
            # Load the JSON data from the modified contents string
            file_contents = f.read()
            # Remove the last comma
            print("Error decoding JSON. Details:")
            print(e)
            error_position = e.pos
            print("Surrounding JSON data:")
            print(file_contents[max(0, error_position - 50):min(len(file_contents), error_position + 50)])
            print("Attempting to fix JSON and trying again...")
            fixed_file_contents = file_contents[:error_position] + ',' + file_contents[error_position:]
            data = json.loads(fixed_file_contents)

    objects = [list(d.keys())[0] for d in data]

    while True:
        words = input("Enter one or more words (separated by spaces): ")
        if words == "":
            break
        words = words.split()

        table = PrettyTable()
        table.field_names = ["Word", "Related word", "Score", "Related Words"]
        table.max_width["Related Words"] = 150  # Set maximum width of Related Words column to 50 characters
        # Add horizontal lines to table
        table.hrules = ALL

        # Add rows to table here
        table.align["Word"] = "l"
        table.align["Related word"] = "l"
        table.align["Score"] = "l"
        table.align["Related Words"] = "l"
        table.wrap = True

        for word in words:
            if word in objects:
                related_objects = data[objects.index(word)][word]
                for related_object in related_objects:
                    related_word = list(related_object.keys())[0]
                    related_word_score = related_object[related_word][0]
                    descriptive_words = ", ".join(related_object[related_word][1])
                    if related_word_score is None:
                        table.add_row([word.upper(), related_word.upper(), "not found", "-"])
                    else:
                        table.add_row([word.upper(), related_word, related_word_score, descriptive_words])
            else:
                related_word, related_word_score, descriptive_words = lookup(word, data)
                if related_word_score is None:
                    table.add_row([word.upper(), "not found", "-", "-"])
                else:
                    table.add_row([word.upper(), related_word, related_word_score, descriptive_words])

        print(table)
