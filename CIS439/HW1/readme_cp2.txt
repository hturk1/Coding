Project: Checkpoint 02 – Inverted Index Construction

Description:
This project implements an inverted index for the wiki2022 dataset. 
The dataset consists of 32 text files (wiki2022_small.nnnnnn), each containing multiple documents.

The program processes all files and produces:
. A global dictionary (dictionary_cp2.txt)
. A local inverted index for each dataset chunk (index000000.txt through index000031.txt)

Requirements
- Python 3.x
- nltk library (was given permission from ta on checkpoint01, so I assumed it was okay to use it for checkpoint02 as well since it builds off the same idea)
- standard Python libraries: os, re, collections, multiprocessing

Install NLTK (if not already installed):
pip install nltk

Dataset Setup
Download and extract the dataset: wiki2022.zip
Place the folder wiki2022 in the same directory as the program.

How to Run
Run the program using: python3 checkpoint02.py


Output Files: 

1. dictionary_cp2.txt
Contains all stemmed words from the dataset
One word per line
Sorted in alphabetical order
The position of each word defines its word-code

2. Inverted Index Files

Files generated:index000000.txt ... index000031.txt
Each file corresponds to one dataset chunk.

Index Format
Each line in an index file has the format:
<word-code> <word> <document-frequency> (<doc-id>, <tf>) (<doc-id>, <tf>)

Explanation:
word-code: Index of the word in dictionary_cp2.txt
word: The stemmed term
document-frequency (df): Number of documents containing the word
doc-id: Unique document identifier
tf: Number of times the word appears in that document

Implementation Details:
1. Text Processing
HTML tags and entities are removed
Text is converted to lowercase
Non-alphabetic characters are removed
Words are tokenized
Stop-words are removed
Words are stemmed 

2. Dictionary Construction
All dataset files are processed (Pass 1)
A global vocabulary is built
Words are sorted alphabetically
Word-codes are assigned based on position

3. Inverted Index Construction
Each file is processed separately (Pass 2)
A local inverted index is created per file
Term frequencies (tf) are computed per document
Duplicate document entries are merged
Document frequency (df) is calculated
Output is sorted by word-code

4. Performance Features
Uses multiprocessing to speed up processing
Reads files in chunks to reduce memory usage

Included:
checkpoint02.py
readme_cp2.txt
dictionary_cp2.txt
