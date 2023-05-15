import os
import requests
import shutil
import json
from bs4 import BeautifulSoup

url = "http://storage.googleapis.com/books/ngrams/books/20200217/eng/eng-2-ngrams_exports.html"
download_dir = "../downloads"
processed_file = "../../output/ngram/1_processed-ngrams-info.json"

# Create the downloads directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Check if the processed file exists and load its contents
if os.path.isfile(processed_file):
    with open(processed_file, "r") as f:
        processed_ngrams = json.load(f)
else:
    processed_ngrams = []

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

start_downloading = False

for link in soup.find_all('a'):
    href = link.get('href')
    if start_downloading and href.endswith('.gz'):
        filename = os.path.basename(href)
        if filename in processed_ngrams:
            print(f"{filename} already processed, skipping")
        elif os.path.isfile(os.path.join(download_dir, filename)):
            print(f"{filename} already downloaded, skipping")
        else:
            filepath = os.path.join(download_dir, filename)
            print(f"Downloading {filename}...")
            with requests.get(href, stream=True) as r:
                with open(filepath, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    print(f"Downloaded {filename}")
        processed_ngrams.append(filename)
    elif href.endswith('2-00086-of-00589.gz'):
        start_downloading = True
        filename = os.path.basename(href)
        if filename in processed_ngrams:
            print(f"{filename} already processed, skipping")
        elif os.path.isfile(os.path.join(download_dir, filename)):
            print(f"{filename} already downloaded, skipping")
        else:
            filepath = os.path.join(download_dir, filename)
            print(f"Downloading {filename}...")
            with requests.get(href, stream=True) as r:
                with open(filepath, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    print(f"Downloaded {filename}")
        processed_ngrams.append(filename)

# Save the list of processed ngrams to the file
with open(processed_file, "w") as f:
    json.dump(processed_ngrams, f)
