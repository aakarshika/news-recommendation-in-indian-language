from __future__ import division
import os
import json

from gensim import corpora, models, similarities

from modelgen import ModelGen
from load_dataset import tokenize_article_text
from constants.model_path import model_path, similarity_index, similarity_mapping, dict_path, corpus_path


ROOT_DIR = '/home/abhishek/python/telgu_tm/dataset/test_corpus'


if (os.path.exists(dict_path)):
    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(corpus_path)
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")


model_gen = ModelGen(dictionary, corpus,  300, 5, model_path)

index = similarities.MatrixSimilarity.load('/home/abhishek/python/telgu_tm/model/test_corpus/simIndex.index')

file_obj = open('/home/abhishek/python/telgu_tm/model/test_corpus/corpus-filename-map.txt', 'r')
file_text = file_obj.read()
corpus_filename_dict = json.loads(file_text)


def test(similarity_count=10):

	category_analysis = {}

	list_dirs = os.listdir(ROOT_DIR)

	for dir_name in list_dirs:

		print "dir name - - ", dir_name
		category_list = []

		article_files = os.listdir(ROOT_DIR + '/' + dir_name)
		f_obj = open('dummy.txt', 'w')
		for article_name in article_files:

			similar_article_count = 0

			file_obj = open(ROOT_DIR + '/' + dir_name + '/' + article_name, 'r')
			article_text = file_obj.read()

			chunk = tokenize_article_text(article_text, f_obj, f_obj)

			test_data_vec = model_gen.get_document(chunk)

			sims = index[test_data_vec]
			sims = sorted(enumerate(sims), key=lambda item: -item[1])

			result = []
			for similar_articles in sims[1:similarity_count]:
				article_index  = similar_articles[0]
				article_file_name = corpus_filename_dict[str(article_index)]
				
				category_name = article_file_name.split('/')[0]

				if category_name == dir_name:
					similar_article_count += 1

			category_list.append((article_name, similar_article_count))

		category_analysis[dir_name] = category_list

	print category_analysis
	evaluate(category_analysis, similarity_count)



def evaluate(data, similarity_count):

	for category in data:

		article_list = data[category]
		scores_list = []

		for article in article_list:
			scores_list.append(article[1])

		score = sum(scores_list) / len(scores_list)

		print '{0}    {1}'.format(category, score*(10/ (similarity_count - 1)))


def create_sim_index():
	all_file_list ={}
	corpus_articles = []
	count = 0
	for category in ['business', 'politics', 'sports', 'entertainment', 'health', 'technology']:
		f_obj = open('dummy.txt', 'w')
		print category
		dir_name = ROOT_DIR + "/" + category
		all_files = [f for f in os.listdir(dir_name)]

		category_corpus_articles = []
		for file_name in all_files:
			file_obj = open(dir_name + '/' + file_name, 'r')
			file_text = file_obj.read()
			tokenized_article = tokenize_article_text(file_text, f_obj, f_obj)

			all_file_list[count] = category + '/' + file_name
			category_corpus_articles.append(tokenized_article)

			count += 1

		corpus_articles += category_corpus_articles

	corpus = [dictionary.doc2bow(article) for article in corpus_articles]
	index = similarities.MatrixSimilarity(model_gen.model[corpus])

	corpora.MmCorpus.serialize('/home/abhishek/python/telgu_tm/model/test_corpus/full_kannada.mm', corpus)
	index.save('/home/abhishek/python/telgu_tm/model/test_corpus/simIndex.index')

	with open('/home/abhishek/python/telgu_tm/model/test_corpus/corpus-filename-map.txt', 'w') as outfile:
		json.dump(all_file_list, outfile)



if __name__ == "__main__":
	test(4)
	# create_sim_index()


	# politics    1.86
	# business    5.02
	# sports    5.26
