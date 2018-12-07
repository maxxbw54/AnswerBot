from nltk import word_tokenize
from utils.StopWords import read_EN_stopwords, remove_stopwords


def load_w2v_model(model_fpath):
    import gensim
    word2vector_model = gensim.models.Word2Vec.load(model_fpath)
    return word2vector_model


def load_idf_vocab(vocab_fpath):
    import csv
    vocab_dict = dict()
    with open(vocab_fpath, 'r') as csvfile:
        rd = csv.reader(csvfile)
        next(rd)
        for row in rd:
            vocab_dict[str(row[0])] = float(row[1])
    return vocab_dict


def preprocessing_for_query(q):
    # basic preprocessing for query
    qw = word_tokenize(q.lower())
    stopwords = read_EN_stopwords()
    qw = remove_stopwords(qw, stopwords)
    return qw
