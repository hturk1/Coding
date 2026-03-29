import gzip
import re
from collections import Counter
from nltk.stem import SnowballStemmer
from multiprocessing import Pool, cpu_count

# Parameters

input_file = "tiny_wikipedia.txt.gz"
num_workers = max(cpu_count() - 1, 1)  # leave one core free
chunk_size = 10000  # lines per chunk for each process

TAG_RE = re.compile(r"<[^>]+>") # matches HTML tags 
ENTITY_RE = re.compile(r"&\w+;") # matches HTML entities
HASH_RE = re.compile(r"#\w+;") # matches patterns like #123;

# Helper Functions 

def process_lines(lines):

    stemmer = SnowballStemmer("english")

    """
    Process a chunk of lines:
    - Remove URL
    - Remove HTML tags
    - Tokenize
    - Stem
    - Count global TF and document DF
    """

    global_tf_chunk = Counter()
    doc_freq_chunk = Counter()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # remove url
        parts = line.split(" ", 1)
        if len(parts) < 2:
            continue
        text = parts[1]

        # remove html tags/entities and other unwanted characters
        text = TAG_RE.sub(" ", text)
        text = ENTITY_RE.sub(" ", text)
        text = HASH_RE.sub(" ", text)

        # make lowercase, remove hyphens, and remove apostrophes 
        text = text.lower()
        text = text.replace("-", " ")
        text = text.replace("'", "")

        # extract words
        tokens = re.findall(r"[a-z]+", text)

        # remove single letters because these are not words (except a/i)
        tokens = [w for w in tokens if len(w) > 1 or w in {"a", "i"}]

        # stem
        stemmed_tokens = [stemmer.stem(word) for word in tokens]      

        # count global frequency
        global_tf_chunk.update(stemmed_tokens)

        # count document frequency 
        doc_freq_chunk.update(set(stemmed_tokens))

    return global_tf_chunk, doc_freq_chunk

def merge_counters(counter_list):
    # merge a list of counters into a single counter
    result = Counter()
    for c in counter_list:
        result.update(c)
    return result

# Read File in Chunks

def chunked_file_reader(file_path, chunk_size=10000):

    # generator that yields chunks of lines
    chunk = []
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            chunk.append(line)
            if line_num % chunk_size == 0:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

# Multiprocessing 

if __name__ == "__main__":
    print(f"Starting processing...")

    # store partial counters from each process
    global_tf = Counter()
    doc_freq = Counter()

    # create a pool processes for parallel execution
    with Pool(num_workers) as pool:
        for idx, (tf_chunk, df_chunk) in enumerate(pool.imap_unordered(process_lines, chunked_file_reader(input_file, chunk_size)), 1):
            global_tf.update(tf_chunk)
            doc_freq.update(df_chunk)
            if idx % 10 == 0:
                print(f"Processed {idx} chunks...", flush=True)

    # merge all partial counters
    # global_tf = merge_counters(partial_tf)
    # doc_freq = merge_counters(partial_df)


    print(f"Finished processing file. Number of unique words: {len(global_tf)}")

    # Build dictionary.txt

    sorted_words = sorted(global_tf.keys())
    word_to_code = {word: idx for idx, word in enumerate(sorted_words)}

    with open("dictionary.txt", "w", encoding="utf-8") as f:
        for word in sorted_words:
            f.write(word + "\n")
    print(f"dictionary.txt created with {len(sorted_words)} words.")

    # Build unigrams.txt
  
    sorted_by_tf = sorted(global_tf.items(), key=lambda x: x[1], reverse=True)

    with open("unigrams.txt", "w", encoding="utf-8") as f:
        for word, tf in sorted_by_tf:
            code = word_to_code[word]
            df = doc_freq[word]
            f.write(f"{code} {word} {df} {tf}\n")

    print("unigrams.txt created.")
