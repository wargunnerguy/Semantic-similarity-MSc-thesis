import json
import os
import time
import pytz
from datetime import datetime, timedelta
from tqdm import tqdm
import multiprocessing
from conceptnet_similar_terms_finder import get_related_terms
from sister_terms import get_type_of_words_from_sister_term_descriptions
from cooccurrence_finder import get_cooccurring_words
from cosinesimilarity_finder import get_similar_words
from gensim.models import KeyedVectors
from differentiating_words import find_differentiating_words

DEFAULT_NR_OF_SIMILAR_WORDS = 15

# Load the model
start_time = time.time()
model = KeyedVectors.load_word2vec_format('models/glove/glove.6B.300d.txt', binary=False, no_header=True)

loading_time = time.time() - start_time
print(f"Model loaded in {loading_time:.2f} seconds")

# Find top N similar words
def get_top_n_similar_words(word, n=15):
    try:
        return model.most_similar(word, topn=n)
    except KeyError:
        print(f"Warning: Word '{word}' not found in vocabulary. Skipping.")
        return []


# Process a word and its similar words to find differentiating words
def process_word(word_and_similar):
    word, similar_words = word_and_similar
    result = {word: []}
    for similar_word, similarity in similar_words:
        diff_words, _, _, _ = find_differentiating_words(word, similar_word, get_cooccurring_words, get_similar_words, get_type_of_words_from_sister_term_descriptions, get_related_terms)
        diff_words_list = [word_info["word"] for word_info in diff_words]
        result[word].append({similar_word: [similarity, diff_words_list]})
    return result

# Process input file and output to a JSON file
def process_input_file(input_file, output_file, top_n=10, num_processes=4):
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    # Read words from input file
    with open(input_file, "r") as f:
        words = [word.strip() for word in f.readlines()]

    # Find similar words for each input word
    similar_words_list = [(word, get_top_n_similar_words(word, top_n)) for word in words]

    # Use multiprocessing to process each input word and its similar words
    # Use multiprocessing to process each input word and its similar words
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = []
        with tqdm(total=len(similar_words_list), unit='word', desc=f"Processing {input_file}") as pbar:
            start_time_progress = datetime.now()
            for result in pool.imap_unordered(process_word, similar_words_list):
                results.append(result)
                pbar.update(1)

                progress = len(results) / len(similar_words_list)
                elapsed_time = datetime.now() - start_time_progress
                estimated_time_left = elapsed_time / progress - elapsed_time
                estimated_completion_time = datetime.now() + estimated_time_left

                # Convert the estimated completion time to local timezone
                local_timezone = pytz.timezone('Europe/Tallinn')
                local_completion_time = estimated_completion_time.astimezone(local_timezone)

                pbar.set_postfix({
                    'progress': f'{len(results)}/{len(similar_words_list)}',
                    'file': output_file,
                    'ETA': f'{estimated_time_left}',
                    'completion time': f'{local_completion_time}'
                })
    # Write results to output JSON file
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print some statistics
    total_time = time.time() - start_time
    print(f"Processed {len(similar_words_list)} words in {total_time:.2f} seconds")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    input_file = "input/20k_common_words_google.txt"
    output_file = "output/V2_20k_common_words_google_may_10_01_20_glove_300d.json"
    process_input_file(input_file, output_file, top_n=15, num_processes=4)
