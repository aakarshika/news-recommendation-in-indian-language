# -*- coding: utf-8 -*-
from modelgen import ModelGen
import os
from gensim import corpora, models
from gensim import similarities
from gensim.similarities.docsim import Similarity
from load_dataset import tokenize_article_text

import json
import logging

from constants.model_path import dict_path, corpus_path, similarity_mapping, train_dir_path, model_path, similarity_index

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


if (os.path.exists(dict_path)):
    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(corpus_path)
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")


if(os.path.exists(model_path)):
    model_gen = ModelGen(dictionary, corpus,  100, 5, model_path)   
else:
    model_gen = ModelGen(dictionary, corpus,  100)
    model_gen.save(model_path)

index = similarities.MatrixSimilarity.load(similarity_index)

def finding_similar_articles(input_text):
    f_obj = open('dummy.txt', 'w')
    chunk = tokenize_article_text(input_text, f_obj, f_obj)

    print "showing topics - - - -- "
    # model_gen.show_topics()

    print "topics of test dataset - - - -  -"
    test_data_vec = model_gen.get_document(chunk)
    # print "test_vec- - -", test_data_vec
    # print "model for matrix similarity initialized -  -  -"

    print "topics - - - - -"

    for topic in test_data_vec:
        print "topic id -  -- -- ", topic[0], topic[1]
        topic_words = model_gen.show_topic(topicid=topic[0])

        for word in topic_words:
            print word[0]

    sims = index[test_data_vec]
    # print "sims - - - -", sims
    # print " - - - - -"
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    file_obj = open(similarity_mapping, 'r')
    file_text = file_obj.read()

    print sims[:10]
    corpus_filename_dict = json.loads(file_text)

    result = []
    for similar_articles in sims[:10]:
        article_index  = similar_articles[0]
        article_file_name = corpus_filename_dict[str(article_index)]
        result.append((article_file_name, similar_articles[1]))

   	# print "result -- - ", result
    return result
# finding_similar_articles(text_1, text_2)