import os
import re
from collections import defaultdict, Counter
from multiprocessing import Pool, cpu_count
from nltk.stem import SnowballStemmer

# Parameters

DATASET_FOLDER = "wiki2022"
DICTIONARY_FILE = "dictionary_cp2.txt"

num_workers = max(cpu_count() - 1, 1) # number of worker processes (leave 1 CPU free)
chunk_size = 10000 # number of lines processed at a time (controls memory usage)

TAG_RE = re.compile(r"<[^>]+>") # removes HTML tags like <p>
ENTITY_RE = re.compile(r"&\w+;") # removes entities like &nbsp;
HASH_RE = re.compile(r"#\w+;") # removes weird hash patterns 

STOP_WORDS = set([ # These words will be completely ignored 
    "the", "and", "of", "to", "in", "a", "is", "it", "that", "for",
    "on", "with", "as", "by", "at", "an"
])


# Processing Lines 

def process_lines(lines):
    stemmer = SnowballStemmer("english") # create a stemmer

    inverted_index_chunk = defaultdict(list) # stores postings for this chunk
    vocab_chunk = set() # stores unique words for dictionary building

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(" ", 1) # split into URL and text content
        if len(parts) < 2:
            continue

        url = parts[0]
        text = parts[1]

        # extract doc_id
        match = re.search(r"curid=(\d+)", url)
        if not match:
            continue
        doc_id = int(match.group(1))

        # test cleaning 

        # remove html tags and entities
        text = TAG_RE.sub(" ", text) 
        text = ENTITY_RE.sub(" ", text)
        text = HASH_RE.sub(" ", text)

        # normalize text
        text = text.lower()
        text = text.replace("-", " ")
        text = text.replace("'", "")

        tokens = re.findall(r"[a-z]+", text) # extract words
        tokens = [w for w in tokens if len(w) > 1 or w in {"a", "i"}] # Keep valid tokens

        tokens = [w for w in tokens if w not in STOP_WORDS] # stop word removal 

        stemmed_tokens = [stemmer.stem(word) for word in tokens] # apply stemming

        # build vocab (for dictionary)
        vocab_chunk.update(stemmed_tokens)

        # term frequency per document
        tf_counter = Counter(stemmed_tokens)

        for word, tf in tf_counter.items():
            inverted_index_chunk[word].append((doc_id, tf))

    return vocab_chunk, inverted_index_chunk


# Chunk Reader 

def chunked_file_reader(file_path, chunk_size=10000):
    chunk = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            chunk.append(line)
            if line_num % chunk_size == 0:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


# Main

if __name__ == "__main__":
    print("Starting Checkpoint 2 processing...")

    global_vocab = set()

    # Pass 1: Build Dictionary 

    print("Building dictionary (pass 1)...")

    for filename in sorted(os.listdir(DATASET_FOLDER)): # tterate through all dataset files
        if not filename.startswith("wiki2022_small"):
            continue

        file_path = os.path.join(DATASET_FOLDER, filename)
        print(f"Processing {filename} for dictionary...")

        with Pool(num_workers) as pool: # parallel processing of chunks
            for vocab_chunk, _ in pool.imap_unordered(
                process_lines,
                chunked_file_reader(file_path, chunk_size)
            ):
                global_vocab.update(vocab_chunk)

    sorted_words = sorted(global_vocab) # sort words alphabetically
    word_to_code = {word: idx for idx, word in enumerate(sorted_words)} # assign word codes

    with open(DICTIONARY_FILE, "w", encoding="utf-8") as f: # write dictionary file 
        for word in sorted_words:
            f.write(word + "\n")

    print(f"Dictionary created with {len(sorted_words)} words.")


    # Pass 2: Build Indexes 

    print("Building inverted indexes (pass 2)...")

    for file_idx, filename in enumerate(sorted(os.listdir(DATASET_FOLDER))):
        if not filename.startswith("wiki2022_small"):
            continue

        file_path = os.path.join(DATASET_FOLDER, filename)
        print(f"Processing {filename} for index...")

        global_index = defaultdict(list) # stores  inverted index for given file

        with Pool(num_workers) as pool:
            for _, index_chunk in pool.imap_unordered(
                process_lines,
                chunked_file_reader(file_path, chunk_size)
            ):
                # merge chunk indexes into global index
                for word, postings in index_chunk.items():
                    global_index[word].extend(postings)

       
        # Write Index File

        index_filename = f"index{file_idx:06d}.txt"

        with open(index_filename, "w", encoding="utf-8") as f:
            for word in sorted(global_index.keys(), key=lambda w: word_to_code[w]):
                raw_postings = global_index[word]

                merged = defaultdict(int) # merge duplicate doc entires  
                for doc, tf in raw_postings:
                    merged[doc] += tf

                postings = list(merged.items())

                df = len(postings) # number of documents containing the word

                code = word_to_code[word] # get word code from dictionary

                postings = sorted(postings, key=lambda x: x[0])

                postings_str = " ".join(f"({doc},{tf})" for doc, tf in postings) # format postings as string

                f.write(f"{code} {word} {df} {postings_str}\n")

        print(f"{index_filename} created.")

    print("Checkpoint 2 complete.")
