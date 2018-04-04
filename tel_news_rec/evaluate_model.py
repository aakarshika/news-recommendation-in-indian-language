# -*- coding: utf-8 -*-
import os, sys
import re
from gensim import corpora, models, similarities

from constants.model_path import dict_path, corpus_path, similarity_mapping, train_dir_path, stop_word_file

from polyglot.text import Text, Word

# current_dir_path = os.path.dirname(os.path.realpath(__file__))
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


class EvaluateLDA:

	def __init__(self, model_dir_path):
		"""
		model_dir_path is path where models are saved.

		init function loads dictionary and model which are previously trained.

		on the  basis of language we assign lang_obj which contains utility functions
		like tokenizing and cleanup of code for that particluar lang.
		"""
		self.dictionary = corpora.Dictionary.load(model_dir_path + '/full_hindi.dict')
		self.model = models.LdaMulticore.load(model_dir_path + '/full_hindi.model.out')

	def load_stop_words(self):
		stop_word_list = []
		f_obj = open(stop_word_file, 'r')
		words = f_obj.readlines()

		for stop_word in words:
			stop_word = stop_word.strip()

			stop_word_list.append(stop_word)

		return stop_word_list
	
	def clean_text(self, text):
		text=text.replace(",", " ")
		text=text.replace("\"", " ")
		text=text.replace("(", " ")
		text=text.replace(")", " ")
		text=text.replace(":", " ")
		text=text.replace("'", " ")
		text=text.replace("‘‘", " ")
		text=text.replace("’’", " ")
		text=text.replace("''", " ")
		text=text.replace(".", " ")
		text=text.replace("/", " ")
		text=text.replace("-", " ")
		text=text.replace('\n', " ")
		text=text.replace('‘', " ")    
		text=text.replace('’', " ")
		text=text.replace('#', " ")
		text=text.replace('@', " ")
		text=text.replace('!', " ")
		text=text.replace('–', " ")
		text=text.replace('*', " ")
		text=text.replace('%', " ")
		text=text.replace('|', " ")
		text=text.replace('$', " ")
		text=text.replace('+', " ")
		text=text.replace('\xc2\xa0', " ")
		return text

	def tokenize_article_text(self, text):
		article_vocab_list = []

		#remove english numbers 
		text = re.sub(r'\d+', ' ', text)

		#remove english letters from text
		text = re.sub(r'[a-zA-Z]', ' ', text)

		# print text
		cleaned_text = self.clean_text(text)
		cleaned_text = unicode(cleaned_text, 'utf-8')
		tokenize_text = cleaned_text.split()

		tamil_stop_words = self.load_stop_words()

		for word in tokenize_text:

			# steming
			w = Word(word, language="ta")
			if len(w.morphemes) > 1:
				word = ("").join(w.morphemes[:-1])
			else:
				word = w.morphemes[0]

			word = word.encode('utf-8')
			if word in tamil_stop_words:
				# rejected_f_obj.write("\n" + word)
				continue

			word = word.strip()
			if word:
				# selected_f_obj.write("\n" + word)
				article_vocab_list.append(word)

		return article_vocab_list

	def load_category_corpus(self, dir_path):
		"""
		In this dir path contains test data to evaluate model, we have assumed that inside 
		dir path there are folders for every category in which articles are there related to that 
		categories.
		
		dir_path
		|
		|__ business
		|		|
		|		|__business_article.txt
		|
		|__ sports
		|		|
		|		|__sports_article.txt
		|
		|
		|__ technology
		""" 
		corpus_map = {}
		index_map = {}

		corpus_articles = []
		
		for dir_name in os.listdir(dir_path):

			all_files = [f for f in os.listdir(dir_path + '/' + dir_name)]

			for file_name in all_files:
				file_obj = open(dir_path + '/' + dir_name + '/' + file_name, 'r')
				file_text = file_obj.read()
				tokenized_article = self.tokenize_article_text(file_text)
				corpus_articles.append(tokenized_article)

			category_corpus = ([self.dictionary.doc2bow(article) for article in corpus_articles])
			corpus_map[dir_name] = category_corpus


			category_index = similarities.MatrixSimilarity(self.model[category_corpus])
			index_map[dir_name] = category_index

		return (corpus_map, index_map)



	def compare_corpus(self, sim_index, test_corpus, same=False):
		"""Calculate the similarity for evry document in the index to the corpus."""
		sim_sum = 0
		for index, doc in enumerate(test_corpus):
			sim_result = sim_index[self.model[doc]]

			if(same):
				sim_result[index] = 0

			sim_sum = sim_sum + sum(sim_result)

		doc_count = len(test_corpus)

		if(same):
			index_count = len(sim_index)
		else:
			index_count = len(sim_index) - 1

		avg_sim = sim_sum/(doc_count * index_count)

		return(avg_sim)


	def ratio(self, a, b):
		"""Calculate F-SCore for two numbers

		Here 'a' is similarity with self and 'b' is avg of similarity with other categories.
		"""
		b = 1-b
		result = (2 * a * b) / (a + b)
		return result

	def evaluate(self, dir_path):
		""" In this we calculate the matrix similarity for every category with all the categories.

		same_category_scores contains the similarity of the category with itself.

		other_category_scores contains the avg of similarity  number with all other categories. 

		In end we take avg for both the lists other_category_scores and same_category_scores 
		and calculate the F-score for these two numbers. 
		"""

		file_obj = open('lda_output.txt', 'w')
		corpus_map, index_map = self.load_category_corpus(dir_path)
		same_category_scores = []
		other_category_scores = []

		for index in index_map:
			others_average = []

			for corpus in corpus_map:
				flag = False

				if index == corpus:
					flag = True

				try:
					result = self.compare_corpus(index_map[index], corpus_map[corpus], flag)
					file_obj.write("\n  " + index + "   " + corpus + "  " + str(result))

				except:
					import traceback
					traceback.print_exc()

				if flag:
					same_category_scores.append(result)

				else:
					others_average.append(result)

			other_category_scores.append(sum(others_average)/len(others_average))
			file_obj.write("\n  Other categories -  " + "  " + str(result))


		same_category_avg_score = sum(same_category_scores)/len(same_category_scores)
		other_category_avg_score = sum(other_category_scores)/len(other_category_scores)

		file_obj.write("\n  same category avg   - " + str(same_category_avg_score) + "   Other category avg  -  " + str(other_category_avg_score))
		file_obj.write("\n  F-score   " + str(self.ratio(same_category_avg_score, other_category_avg_score)))
		file_obj.close()




if __name__ == "__main__":

	model_dir_path = '/home/abhishek/python/tamil_tm/model/test'
	evaluate_model_obj = EvaluateLDA(model_dir_path)
	evaluate_model_obj.evaluate('/home/abhishek/python/tamil_tm/dataset/article_tamil')
