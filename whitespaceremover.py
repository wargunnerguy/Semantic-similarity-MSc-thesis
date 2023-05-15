import json

def remove_whitespace(json_file, output_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    with open(output_file, 'w') as file:
        json.dump(data, file, separators=(',', ':'))

# Example usage
json_file_path = 'output/V2_20k_common_words_google_may_10_01_20_glove_300d.json'  # Path to the input JSON file
output_file_path = 'output/V2_20k_common_words_google_may_10_01_20_glove_300d_nowhitespace.json'  # Path to the output file without whitespace

remove_whitespace(json_file_path, output_file_path)
