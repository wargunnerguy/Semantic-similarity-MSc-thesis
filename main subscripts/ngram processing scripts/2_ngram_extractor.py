import os
import gzip
import json
from tqdm import tqdm
import time

result = {}

# Keep track of processed files in a set
processed_files = set()

# Load the list of already processed files, if any
try:
    with open('../../output/ngram/1_processed-ngrams-info.json', 'r') as f:
        processed_files = set(json.load(f))
except (FileNotFoundError, json.decoder.JSONDecodeError):
    processed_files = set()

while True:
    # Get a list of all files in the downloads folder
    all_files = os.listdir('../downloads')

    # Filter for files that start with '2-' and end with '.gz'
    unprocessed_files = [
        filename for filename in all_files
        if filename.startswith('2-') and filename.endswith('.gz') and filename not in processed_files
    ]

    # If there are no unprocessed files, sleep for 5 seconds and check again
    if not unprocessed_files:
        print("No unprocessed files found. Sleeping for 5 seconds...")
        time.sleep(5)
        continue

    # Sort the unprocessed files by name
    unprocessed_files.sort()

    for filename in tqdm(unprocessed_files, desc='Processing files'):
        print(f"Processing {filename}...")
        filepath = os.path.join('../downloads', filename)
        try:
            with gzip.open(filepath, 'rt') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 3:
                        continue
                    word1, word2, info = parts
                    try:
                        freq_sum = sum(int(x.split(',')[1]) for x in info.split())
                    except IndexError:
                        continue
                    key = word1 + ' ' + word2
                    if key in result:
                        result[key] += freq_sum
                    else:
                        result[key] = freq_sum

                # Write info about the processed file to output file
                with open('../../output/ngram/2_2ngram-organized-info.json', 'a') as f_out:
                    for key, value in result.items():
                        word1, word2 = key.split()
                        obj = {'word1': word1, 'word2': word2, 'frequency_sum': value}
                        f_out.write(json.dumps(obj) + ',\n')
                    result = {}

                # Add the filename to the set of processed files
                processed_files.add(filename)
                with open('../../output/ngram/1_processed-ngrams-info.json', 'w') as f:
                    json.dump(list(processed_files), f, indent=4)

                # Remove the processed file from the downloads folder
                os.remove(filepath)

        except EOFError:
            print(f"Error processing file {filename}: compressed file ended before end-of-stream marker was reached")
            os.remove(filepath)
            continue

    print("Processed all available files. Waiting for new files...")
