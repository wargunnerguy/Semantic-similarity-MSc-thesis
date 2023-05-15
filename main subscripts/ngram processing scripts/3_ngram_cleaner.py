import json

# Define the path to the input file and the tag list
INPUT_FILE = "../../output/ngram/2_2ngram-organized-info.json"
TAGS = ["NOUN", "VERB", "ADJ", "ADV", "PRON", "DET", "ADP", "NUM", "CONJ", "PRT", "ROOT", "START", "END"]

# Define the path to the output file for cleaned data
OUTPUT_FILE = "../../output/ngram/3_CLEANED_2ngram-organized-info.json"


def remove_tags(word):
    """Remove tags from a word."""
    for tag in TAGS:
        if word.endswith("_" + tag):
            word = word[:-len(tag) - 1]
        elif word.startswith(tag + "_"):
            word = word[len(tag) + 1:]
    return word


def main():
    """Read the input file, clean the words, and write to the output file."""
    cleaned_ngrams = []
    with open(INPUT_FILE, "r") as f:
        ngrams = json.load(f)
        for ngram in ngrams:
            # Clean the words in the ngram
            cleaned_ngram = {
                "word1": remove_tags(ngram["word1"]).lower(),
                "word2": remove_tags(ngram["word2"]).lower(),
                "frequency_sum": ngram["frequency_sum"]
            }
            cleaned_ngrams.append(cleaned_ngram)

    # Write the cleaned data to the output file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(cleaned_ngrams, f, indent=4)

    print(f"{len(cleaned_ngrams)} ngrams cleaned and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
