# Description
This repository holds pre-generated dataset of 20 000 most common English words with most similar words attached. For each word + similar word it also holds information of differentiating words (words that make the original word and similar word different from each other).
* This codebase and its software is free to use for everyone. 
* For viewing pre-generated results you don't need to run the analysis program
* What the included code does is that it takes an input of words (text-file) and outputs similar and differentiating words (JSON-file). Once given a pre-trained model, list of words to analyze (input file) it will generate a file in json format that includes: words similar to the words in the input file and a similarity score based on cosine similarity. Also it will output a list of descriptive words that make the input-word and the found similar words different from each other (dissimilarity). For ease of use the pre-trained models (cosine similarity) should be either downloaded to the models directory in the main directory or automatically loaded in the semantism.py file through gensim API. 

## Viewing pre-generated results
In the repository you will find semantism_VIEWER.py file, which is espescially made to view the generated JSON files in the output directory. 
* When running the viewer it will ask for input words
* Will output a table in the terminal (input word, similar word, similarity score, differentiating words)

## Setup for generating results (optional)
In the inputs directory in the main directory there has to be a "20k_common_words_google.txt" file for it to be used as the main source of input words that will be analyzed. The name can be changed if it is updated in the respective place in the semantism.py file. Once these conditions are met the program can be run as it will take a while to process through all of the input words if there are many of them (20 000 in this example took me ~48 hours to complete on 4 CPU cores.)

### Important input files: 
* INPUT_FILE = "20k_common_words_google.txt" - the main list of words that will be processed. One word per row
* BASIC_WORDS_FILE = "357_basic_words.txt" - used to disregard basic words like "be", "to", "have" etc (can be left empty)

## System requirements to process the words
To successfully implement the proposed methodology, the following system requirements should be met:
- A computer with a modern operating system (Windows or macOS, but preferrably Linux, as it was ran and tested on it) capable of running Python 3.
- Sufficient memory (RAM) to process and store the word embeddings and WordNet data, with at least 2 GB of available memory recommended.
- Python 3 installed, along with the necessary libraries and packages in the requirements.txt

# How to run the analysis program
## Step 1 - Setup
Clone repository
Install NLTK: run `pip install --user -U nltk`  
Install all required packages `pip install -r requirements.txt`

## Step 2 - Getting models
Go to 'semantic-similarity' main folder and download Numberbatch 19.08 or GloVe or any other pretrained model
`wget https://conceptnet.s3.amazonaws.com/downloads/2019/numberbatch/numberbatch-en-19.08.txt.gz`
(`wget https://nlp.stanford.edu/data/glove.840B.300d.zip`)
Unzip
`gunzip numberbatch-en-19.08.txt.gz`
 
## Step 3 - Analysis (optional) 
If you want to recollect and analyze all the words run semantism.py

- Rename `INPUT_FILE = '20k_common_words_google.txt'` to any text file you want to analyze. Format: 1 word per row
- Rename `OUTPUT_FILE = 'output/20k_common_words_google_glove_300d_may1_13_02.json'` to what you want your file to be called

Run `python3 semantism.py` or press run from IDE

## Step 4 - Viewing results 

Run `python3 semantism_VIEWER.py` or press run from IDE
Enter any number of words that you want to find similar words and words that make the similar words different from each other


## Additional experimental code: Incorporating Google 2ngrams [DISABLED]
* These scripts download, extract, clean and filter information from google 2ngrams, but as of now the final filtered file only has useless information in it. If the filterer script gets updated, it might be worth incorporating into the code again.

Run the scripts in the numerical order
Run `python3 1_ngram_downloader.py` or press run from IDE and wait for it to finish (~12h)
Run `python3 2_ngram_extractor.py` or press run from IDE and wait for it to finish
Run `python3 3_ngram_cleaner.py` or press run from IDE and wait for it to finish
Run `python3 4_ngram_filterer.py` or press run from IDE and wait for it to finish

You will end up with the following files in the output directory:
1_processed-ngrams-info.json
2_2ngram-organized-info.json
3_CLEANED_2ngram-organized-info.json
4_FILTERED_2ngram-organized-info.json

As of now, they contain only noise and there is no value in them, but feel free to dabble around and find ways to make them useful. Could also try with 3ngrams etc.
