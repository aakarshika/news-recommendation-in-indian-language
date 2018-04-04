# -*- coding: utf-8 -*-
import sys
import os

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

# indic_string = u"இந்தியாவில் ஸ்கூட்டர்கள் விற்பனையில் இரண்டாமிடத்திலிருந்த ஹீரோ மோட்டோகார்ப் நிறுவனத்தை சென்னையைச் சேர்ந்த டி.வி.எஸ். நிறுவனம் பின்னுக்குத் தள்ளியுள்ளது. முதலிடத்தை எப்போதும் போல் ஹோண்டா தக்க வைத்துக் கொண்டது."
# print type(indic_string)

# print "original -  ", indic_string
# print "segmentation - ", analyzes_tokens

f_obj = open('stemmed_tamil_stop_words', 'w')
file_obj = open('tamil_stop_words.txt', 'r')
words_list = file_obj.readlines()
file_obj.close()
for word in words_list:
	analyzes_tokens=analyzer.morph_analyze_document([word.strip()])
	for w in analyzes_tokens:
		f_obj.write("\n" + w[0])

f_obj.close()