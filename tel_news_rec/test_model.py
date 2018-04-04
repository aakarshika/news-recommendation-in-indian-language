
import os
from gensim import corpora, models, similarities
# from load_dataset import tokenize_article_text
from modelgen import ModelGen
from constants.model_path import dict_path, corpus_path, similarity_mapping, train_dir_path, model_path, similarity_index



if (os.path.exists(dict_path)):
   dictionary = corpora.Dictionary.load(dict_path)
   corpus = corpora.MmCorpus(corpus_path)
   print("Dictionary and corpus files loaded")
else:
   print("Error in loading dictionary and corpus file")
   raise "Error"

# generating model
model_gen_obj = ModelGen(dictionary, corpus, 30, 5, model_path)


for x in range(0, 30):
	topics = model_gen_obj.show_topic(topicid=x)
	
	print " - - - - - - -", x
	for topic in topics:
		print topic[0]


