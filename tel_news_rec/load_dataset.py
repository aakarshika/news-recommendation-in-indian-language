# -*- coding: utf-8 -*-
import os, sys
import re
import codecs
import sys
import json

from gensim import corpora

from constants.model_path import dict_path, corpus_path, similarity_mapping, train_dir_path, stop_word_file
import logging
import datetime

from polyglot.text import Text, Word

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
from collections import Counter

# INDIC_NLP_LIB_HOME = "/home/abhishek/python/indian_lang_test/indic_nlp_library"
# INDIC_NLP_RESOURCES = "/home/abhishek/python/indian_lang_test/indic_nlp_resources-master"

# sys.path.insert(0, '{}/src'.format(INDIC_NLP_LIB_HOME))

# from indicnlp import common
# common.set_resources_path(INDIC_NLP_RESOURCES)

# from indicnlp import loader
# loader.load()

# from indicnlp.morph import unsupervised_morph 
# from indicnlp import common

# analyzer=unsupervised_morph.UnsupervisedMorphAnalyzer('ta')



def load_stop_words():
    stop_word_list = []
    f_obj = open(stop_word_file, 'r')
    words = f_obj.readlines()

    for stop_word in words:
        # malayalam_word, _ = stop_word.split('    ')
        stop_word =stop_word.strip()

        stop_word_list.append(stop_word)

    # 
    return stop_word_list


def clean_text(text):
    text=text.replace(",", " ")
    text=text.replace("\"", " ")
    text=text.replace("(", " ")
    text=text.replace(")", " ")
    text=text.replace(":", " ")
    text=text.replace(";", " ")
    text=text.replace("'", " ")
    text=text.replace("\"", " ")
    text=text.replace("‘‘", " ")
    text=text.replace("’’", " ")
    text=text.replace("''", " ")
    text=text.replace(".", " ")
    text=text.replace("/", " ")
    text=text.replace("\\", " ")
    text=text.replace("-", " ")
    text=text.replace('\n', " ")
    text=text.replace('‘', " ")    
    text=text.replace('’', " ")
    text=text.replace('#', " ")
    text=text.replace('@', " ")
    text=text.replace('!', " ")
    text=text.replace('–', " ")
    text=text.replace('=', " ")
    text=text.replace('*', " ")
    text=text.replace('%', " ")
    text=text.replace('|', " ")
    text=text.replace('$', " ")
    text=text.replace('+', " ")
    text=text.replace('?', " ")
    text=text.replace('[', " ")
    text=text.replace(']', " ")
    text=text.replace('>', " ")
    text=text.replace('<', " ")
    text=text.replace('\xc2\xa0', " ")
    return text

def tokenize_article_text(text, selected_f_obj, rejected_f_obj):
    article_vocab_list = []

    #remove english numbers 
    text = re.sub(r'\d+', ' ', text)

    #remove english letters from text
    text = re.sub(r'[a-zA-Z]', ' ', text)

    # print text
    cleaned_text = clean_text(text)
    cleaned_text = unicode(cleaned_text, 'utf-8')
    tokenize_text = cleaned_text.split()

    malayalam_stop_words = load_stop_words()
    # print malayalam_stop_words[:3]
    for word in tokenize_text:
        
        # steming
        w = Word(word, language="te")
        if len(w.morphemes) > 1:
            word = ("").join(w.morphemes[:-1])
        else:
            word = w.morphemes[0]

        word = word.encode('utf-8')
        if word in malayalam_stop_words:
            rejected_f_obj.write("\n" + word)
            continue

        word = word.strip()
        if word:
            selected_f_obj.write("\n" + word)
            article_vocab_list.append(word)

    return article_vocab_list


def get_files_list(train_dir, all_files):
    words_list = []
    all_vocab_list = []
    all_file_list = {}
   
    selected_f_obj = open('selected_words.txt', 'w')
    rejected_f_obj = open('rejected_words.txt', 'w')
    for index, file_name in enumerate(all_files):
        article_vocab_list = []
        file_obj = open(train_dir + '/' + file_name, 'r')
        file_text = file_obj.read()
        print("filename  -   - ", file_name)
        article_vocab_list = tokenize_article_text(file_text, selected_f_obj, rejected_f_obj)

        all_vocab_list.append(article_vocab_list)
        # words_list += article_vocab_list
        all_file_list[index] = file_name

    # print " - - - - - ", len(words_list)
    # print words_list[:10]
    # c = Counter(words_list)
    # words = c.most_common()

    # for w in words[:1000]:
    #     print '{0}    {1}'.format(w[0], w[1])


    dictionary = corpora.Dictionary(all_vocab_list)
    
    print(len(dictionary))
    dictionary.filter_extremes(no_below=2)
    print(len(dictionary))
    dictionary.save(dict_path)

    corpus = [dictionary.doc2bow(article_vocab) for article_vocab in all_vocab_list]
    corpora.MmCorpus.serialize(corpus_path, corpus)  # store to disk, for later use
     
    with open(similarity_mapping, 'w') as outfile:
        json.dump(all_file_list, outfile)

    # with open('words_dict.txt', 'w') as outfile:
    #     json.dump(words_list, outfile)


if __name__ == "__main__":
    a = datetime.datetime.now()
    

    all_dir  = os.listdir(train_dir_path)

    all_text_files_list = []
    for directory in all_dir:

        # if not directory in ['']:
        #     print "ignoring these directories - - - - -  - - -", directory
        #     # continue
        #     pass

        all_files = [f for f in os.listdir(train_dir_path + "/" + directory)]

        for file in all_files:
            all_text_files_list.append(directory + "/" + file)

    get_files_list(train_dir_path, all_text_files_list)
    b = datetime.datetime.now()

    print b-a
