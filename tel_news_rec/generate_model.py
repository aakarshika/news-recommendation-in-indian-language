# -*- coding: utf-8 -*-

import os
from gensim import corpora, models, similarities
from load_dataset import tokenize_article_text
from modelgen import ModelGen

from constants.model_path import dict_path, corpus_path, similarity_mapping, train_dir_path, model_path, similarity_index
import datetime

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

a = datetime.datetime.now()

if (os.path.exists(dict_path)):
   dictionary = corpora.Dictionary.load(dict_path)
   corpus = corpora.MmCorpus(corpus_path)
   print("Dictionary and corpus files loaded")
else:
   print("Error in loading dictionary and corpus file")
   raise "Error"

# generating model
# model_gen_obj = ModelGen(dictionary, corpus, 30, 5)
# model_gen_obj.save(model_path)
# model_gen_obj.show_topics()

# model = models.LdaMulticore.load(model_path)

# index = similarities.MatrixSimilarity(model[corpus]) ---> load index
# index.save(similarity_index)

ROOT_DIR = '/home/abhishek/python/telgu_tm/model/full_corpus_correct_names'
dictionary.save(ROOT_DIR + '/telugu_dictionary.dict')
corpora.MmCorpus.serialize(ROOT_DIR + '/telugu_corpus.mm', corpus)

model = models.LdaMulticore.load(model_path)
model.save(ROOT_DIR + "/telugu_model.model.out")

index = similarities.MatrixSimilarity.load(similarity_index)
index.save(ROOT_DIR + "/telugu_sim_index.index")

b = datetime.datetime.now()
print b-a

