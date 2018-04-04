import os

CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR_PATH = os.path.abspath(os.path.join(CURRENT_DIR_PATH, os.pardir))


MODEL_DIR_PATH = '/model/full_corpus'
train_dir_path = "/home/abhishek/python/telgu_tm/dataset/text_te_200"


dict_path = PARENT_DIR_PATH + MODEL_DIR_PATH + '/full_telgu.dict'
corpus_path = PARENT_DIR_PATH + MODEL_DIR_PATH + '/full_telgu.mm'

model_path = PARENT_DIR_PATH + MODEL_DIR_PATH + '/full_telgu.model.out'

similarity_index = PARENT_DIR_PATH + MODEL_DIR_PATH + '/simIndex.index'

similarity_mapping = PARENT_DIR_PATH + MODEL_DIR_PATH + '/corpus-filename-map.txt'

stop_word_file = PARENT_DIR_PATH + '/stemmed_telgu_stop_words.txt'