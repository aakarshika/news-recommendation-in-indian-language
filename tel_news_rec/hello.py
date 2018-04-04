# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template
import os

import base64

import find_similarity

application = Flask(__name__)
train_dir = "/home/abhishek/python/malayalam_tm/dataset/partial_corpus_10k/"

@application.route('/news', methods=['GET', 'POST'])
def analyse_text():

    recommended_articles_list = []
    article_text = ""

    if request.method == 'POST':
        article_text = request.form['article_text']
        article_text = article_text
        files_list = find_similarity.finding_similar_articles(article_text.encode('utf-8'))

        print "filke list  -- - ", files_list
        for file in files_list:

            file_name = file[0]
            print "file name - -- ", file_name, file[1]
            file_obj = open(train_dir +  file_name, 'r')
            file_text = file_obj.read()

            recommended_articles_list.append((file_text.decode('utf-8'), file[1]))

    data = {'recommended_articles': recommended_articles_list, "article_text": article_text}
    return render_template('index-text.html', data=data)

