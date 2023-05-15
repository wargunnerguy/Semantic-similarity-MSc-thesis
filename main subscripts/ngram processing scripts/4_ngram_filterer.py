import json

# Define the path to the input file and the list of common words
CLEANED_INPUT_FILE = "../../output/ngram/3_CLEANED_2ngram-organized-info.json"
COMMON_WORDS_FILE = "../../input/20k_common_words.txt"

# Define the path to the output file for filtered data
OUTPUT_FILE = "../../output/ngram/4_FILTERED_2ngram-organized-info.json"


def load_common_words():
    """Load the list of common words from the file."""
    with open(COMMON_WORDS_FILE, "r") as f:
        return set([word.strip().lower() for word in f.readlines()])


def filter_ngrams(ngrams, common_words):
    """Filter the ngrams based on whether both words are in the common words list."""
    filtered_ngrams = []
    for ngram in ngrams:
        # Check if both words are in the common words list
        if ngram["word1"].lower() in common_words and ngram["word2"].lower() in common_words:
            # Check if the ngram is not already in the filtered ngrams list
            if ngram not in filtered_ngrams:
                filtered_ngrams.append(ngram)

    return filtered_ngrams


def write_to_output_file(ngrams):
    """Write the filtered ngrams to the output file."""
    with open(OUTPUT_FILE, "w") as f:
        json.dump(ngrams, f, indent=4)

    print(f"{len(ngrams)} ngrams saved to {OUTPUT_FILE}")


def main():
    """Read the cleaned input file, filter the ngrams, and write to the output file."""
    common_words = load_common_words()
    print(f"Loaded {len(common_words)} common words")

    with open(CLEANED_INPUT_FILE, "r") as f:
        ngrams = json.load(f)
        print(f"Loaded {len(ngrams)} ngrams from {CLEANED_INPUT_FILE}")

    filtered_ngrams = filter_ngrams(ngrams, common_words)
    print(f'Filtered {len(filtered_ngrams)} ngrams.')

    # Write the filtered ngrams to the output file.
    write_to_output_file(filtered_ngrams)


if __name__ == '__main__':
    main()
