Checkpoint #01 

Files:
- checkpoint01.py            : script to build dictionary.txt and unigrams.txt
- tiny_wikipedia.txt.gz      : input data
- dictionary.txt             : Output file with all stemmed words in alphabetical order
- unigrams.txt               : Output file with <word-code> <word> <document-frequency> <global-term-frequency>

Requirements:
- Python 3.8 or higher
- Libraries: 
    - nltk (was given permission by TA)
    - (standard library modules: gzip, re, collections, multiprocessing)

Installation of nltk:
pip install nltk

Running the script:
1. Make sure tiny_wikipedia.txt.gz is in the same folder as checkpoint01.py
2. Run the script: python3 checkpoint01.py
3. The script will process the dataset and generate:
    - dictionary.txt
    - unigrams.txt

Notes:
- The script is optimized for large files using multiprocessing.
- It will ignore URLs, markup tags, and HTML entities.

