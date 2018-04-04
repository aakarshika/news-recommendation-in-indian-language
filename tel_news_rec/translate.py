# -*- coding: utf-8 -*-
import urllib2
import goslate
import requests

# proxy_handler = urllib2.ProxyHandler({"http" : "http://proxy-domain.name:8080"})
# proxy_opener = urllib2.build_opener(urllib2.HTTPHandler(proxy_handler),
#                                     urllib2.HTTPSHandler(proxy_handler))

# gs_with_proxy = goslate.Goslate(opener=proxy_opener)

tamil_word_list = []
f_obj = open('stemmed_tamil_stop_words.txt', 'r')
tamil_words = f_obj.readlines()

for word in tamil_words:
	if word.strip():
		tamil_word_list.append(word.strip())

print len(tamil_word_list)
tamil_word_list.sort()


def test():
	api_key = 'AIzaSyCaLQ1tTvC6f7t2EE9XmcH_fno0N733Rq4'
	sourceLang = 'ta'
	targetLang = 'en'
	sourceText = 'hello world'

	f_obj = open('test.txt', 'w')
	for word in tamil_word_list:
		word = word.strip()
		# word  = 'आतंकी'#.decode('utf-8')
		# print type(word)
		# word = word.decode('utf-8')
		# url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + sourceLang + "&tl=" + targetLang + "&dt=t&q=" + word;

		data = {'q': word, 'target': targetLang, 'format': 'text', 'source': sourceLang, 'key': api_key}
		url2 = 'https://translation.googleapis.com/language/translate/v2'

		r = requests.post(url2, data=data)
		english_word = r.json()['data']['translations'][0]['translatedText']


		print '{0}   {1}    {2}'.format(r.status_code, word, english_word)

		f_obj.write("\n" + word + "      " +english_word.encode('utf-8'))
		# break
	f_obj.close()

if __name__ == "__main__":
	# translate_text('ta', 'hello')
	test()