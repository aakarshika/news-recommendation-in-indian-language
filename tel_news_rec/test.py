# -*- coding: utf-8 -*-
from polyglot.text import Text, Word
import requests
import operator
import sys
import os
# f_obj = open('test.txt', 'r')


# words_list = f_obj.readlines()
# for word in words_list:
# 	tamil_word, english_word = word.split('      ')

# 	# print '{0}  {1}'.format(tamil_word, english_word)
# 	tamil_english_dict[tamil_word] = english_word


# print len(tamil_english_dict)
# sorted_x = sorted(tamil_english_dict.items(), key=operator.itemgetter(1))
# f_obj.close()

def test(word):
	api_key = 'AIzaSyCaLQ1tTvC6f7t2EE9XmcH_fno0N733Rq4'
	sourceLang = 'ml'
	targetLang = 'en'
	sourceText = 'hello world'

	data = {'q': word, 'target': targetLang, 'format': 'text', 'source': sourceLang, 'key': api_key}
	url2 = 'https://translation.googleapis.com/language/translate/v2'

	r = requests.post(url2, data=data)
	english_word = r.json()['data']['translations'][0]['translatedText']
	english_word = english_word.strip()
	print "data  --  -", r.json()
	# print "word - - - ", english_word
	# print '{0}   {1}  {2}'.format(r.status_code, word, english_word)

	return english_word


def steming():
	tamil_english_dict = {}
	f_obj = open('malayalam_stop_words.txt', 'r')

	words_list = f_obj.readlines()

	for word in words_list:
		tamil_word, _ = word.split('    ')
		
		tamil_word = unicode(tamil_word, 'utf-8')

		if not tamil_word:
			continue


		w = Word(tamil_word, language="ml")
		if len(w.morphemes) > 1:
			stemmed_word = ("").join(w.morphemes[:-1])
		else:
			stemmed_word = w.morphemes[0]

		stemmed_word = stemmed_word.encode('utf-8')
		stemmed_word = stemmed_word.strip()
		english_word = test(stemmed_word)

		print "mal word  -  -  ",tamil_word
		print "en word  - - - - -", english_word

		if stemmed_word and english_word:
			tamil_english_dict[stemmed_word] = english_word

		# print '{0}  {1}'.format(tamil_word.encode('utf-8'), stemmed_word) 


	f_obj.close()

	sorted_x = sorted(tamil_english_dict.items(), key=operator.itemgetter(1))

	f_obj = open('stemmed_malayalam_stop_words.txt', 'w')
	for word in sorted_x:
		# print word
		# print '{0}  {1} {2}'.format(word[0], word[1], ' - - - ')
		f_obj.write('\n' + word[0] + '    ' + word[1].encode('utf-8'))

	f_obj.close()


def testing(word):
	tamil_word = unicode(word, 'utf-8')

	print  word
	print " - - - -  - -"
	w = Word(tamil_word, language="ml")
	if len(w.morphemes) > 1:
		stemmed_word = ("").join(w.morphemes[:-1])
	else:
		stemmed_word = w.morphemes[0]

	for morph in w.morphemes:
		print morph

	stemmed_word = stemmed_word.encode('utf-8')
	print '  - - - - - - -'
	print stemmed_word


ROOT_DIR = 'dataset/test_corpus'
TEST_DIR = 'dataset/test_corpus_en'


def translate_dataset():
	for dir_name in ['business', 'entertainment', 'health', 'lifestyle', 'politics', 'sports', 'technology', 'topstories']:

		files_list = os.listdir(ROOT_DIR + "/" + dir_name)

		# if len(files_list) < 100:
		# 	continue

		os.mkdir(TEST_DIR + "/" + dir_name, 0755 )
		# os.mkdir(EVALUATE_DIR + "/" + dir_name, 0755 )
		count = 0
		for file_name in files_list:

			print dir_name, count
			file_obj = open(ROOT_DIR + "/" + dir_name + "/" + file_name)
			tamil_text = file_obj.read()
			file_obj.close()

			try:
				english_text = test(tamil_text)
			except:
				print "some error"
				continue
			f_obj = open(TEST_DIR + "/" + dir_name + "/" + file_name, 'w')
			f_obj.write(english_text.encode('utf-8'))
			f_obj.close()
			count += 1


if __name__ == "__main__":

	# word = sys.argv[1]
	# testing(word)
	# steming()
	translate_dataset()