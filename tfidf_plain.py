# -*- coding: utf-8 -*-
# borrow from https://gist.github.com/vineetrok/1391957
import os
curdir = os.path.dirname(os.path.abspath(__file__))
import math
import pickle
from tqdm import tqdm
corpus_data_path = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg" % curdir
tfidf_model_path = "%s/data/zhwiki-latest-pages-articles.0620.chs.normalized.wordseg.tfidf" % curdir

def file_len(full_path):
    """ Count number of lines in a file."""
    f = open(full_path, encoding='utf-8')
    nr_of_lines = sum(1 for line in f)
    f.close()
    return nr_of_lines


def load_data():
    texts = []
    with tqdm(total=file_len(corpus_data_path)) as pbar:
        pbar.set_description("Parsing texts")
        with open(corpus_data_path, "r", encoding="utf-8") as f:
            for x in f:
                o = [y for y in x.strip().split('<s>') if y]
                for z in o:
                    t = [p for p in z.strip().split(' ') if p]
                    # only append big text as doc
                    if len(t) > 20:
                        texts.append(t)
                pbar.update(1)
    return texts



def compute():
    corpus = load_data()
    corpus_set = []
    total_words_lis = []
    total_docs=len(corpus)   #total number of documents

    for doc in corpus:
        corpus_set.append(set(doc))

    with tqdm(total=total_docs) as pbar:
        pbar.set_description("Generating dictionary")
        for doc in corpus_set:
            [total_words_lis.append(x) for x in doc]
            pbar.update(1)
    words = set(total_words_lis)
    dictionary = list(words)
    dictionary_enum = enumerate(dictionary) # dictionary for words

    # get word's doc freq for corpus
    doc_counts = []
    with tqdm(total=len(dictionary)) as pbar:
        pbar.set_description("Counting freq in docs for terms")
        for i, term in dictionary_enum:
            doc_counts.append(0)
            for doc in corpus_set:  # counts the no of times "term" is encountered in each doc
                if term in doc:
                    doc_counts[i] += 1  # this "term" is found
            pbar.update(1)

    assert len(dictionary) == len(doc_counts)

    # compute idf and weights
    idf=[]      # inverse document frequency      
    weights=[]  # weight
    with tqdm(total=len(doc_counts)) as pbar:
        pbar.set_description("Computing idf and weights")
        for doc_count in doc_counts:
            idf.append(round(math.log(total_docs/doc_count), 2)) #calculates idf for each "term"
            weights.append(round(idf[i]*doc_count, 2)) #calculate weight of the term
            pbar.update(1)

    assert len(dictionary) == len(idf)
    assert len(dictionary) == len(weights)

    tfidf_matrix = dict({
        "words": dictionary,
        "weights": weights,
        "idf": idf
    })

    # save model
    pickle.dump(tfidf_matrix, open(tfidf_model_path, "wb"))
    print("Done.")

    # Load data afterward
    # tfidf_model=pickle.load(
    #     open(
    #         tfidf_model_path,
    #         "rb")))

def main():
    compute()

if __name__ == '__main__':
    main()