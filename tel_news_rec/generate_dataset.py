import os
import shutil
from random import shuffle

ROOT_DIR = 'dataset/text_te'
TEST_DIR = 'dataset/text_te_200'
# EVALUATE_DIR = 'dataset/tamil_200/evaluate'


list_dir = os.listdir(ROOT_DIR)

for dir_name in ['business', 'entertainment', 'health', 'lifestyle', 'sports', 'topstories', 'politics', 'technology']:

	files_list = os.listdir(ROOT_DIR + "/" + dir_name)

	# if len(files_list) < 100:
	# 	continue

	os.mkdir(TEST_DIR + "/" + dir_name, 0755 )

	shuffle(files_list)

	print dir_name, len(files_list)

	count = 1
	for file_name in files_list[:200]:
			print file_name, "test - -"
			output_file_name = str(count) + '.txt'
			shutil.copy(ROOT_DIR + '/' + dir_name + '/' + file_name, TEST_DIR + '/' + dir_name + '/' + output_file_name)
			count += 1

