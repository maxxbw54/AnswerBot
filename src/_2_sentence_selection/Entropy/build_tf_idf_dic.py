from utils.preprocessing_util import replace_double_space
from utils.Stemming import stemming_for_word_list
import math
from utils.file_util import write_file
from utils.StopWords import read_EN_stopwords, remove_stopwords
import time
from pathConfig import get_base_path
from utils.collection_util import remove_duplicate_element

path_of_voc = get_base_path() + '/_2_sentence_selection/Entropy/idf_voc.txt'


def read_voc():
    file = open(path_of_voc)
    voc = {}
    for line in file:
        word_idf = line.split('   ')
        word = word_idf[0]
        idf = float(word_idf[1].strip())
        voc[word] = idf
    return voc


if __name__ == '__main__':
    reponum = 50000
    voc_str = ''
    voc = read_voc()
    for key in voc.keys():
        voc_str += (key + '   ' + str(voc[key]) + '\n')
    write_file(path_of_voc, voc_str.strip())
    print 'Done.'
