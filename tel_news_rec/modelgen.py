
from gensim import corpora, models, similarities

class ModelGen:

    def __init__(self, dictionary, corpus, ntops, passes=5, model_file=None):
        self.dictionary = dictionary
        self.corpus = corpus

        if(model_file != None):
            # model has been provided. Load it. 
            self.model = models.LdaMulticore.load(model_file)
        else:
            # else generate it from corpus    
            self.model = models.LdaMulticore(corpus, id2word=dictionary, num_topics=ntops, workers=4, passes=passes)
        
        self.ntops = ntops
    
    def show_topics(self):
        self.model.show_topics(num_topics=self.ntops, log=True)

    def show_topic(self, topicid):
        topics = self.model.show_topic(topicid=topicid)
        return topics    


    def get_document(self, document, minimum_probability = 0):
        chunk = self.dictionary.doc2bow(document)
        top_dist = self.model[chunk]

        return [(idx, prob) for (idx, prob) in top_dist if prob >= minimum_probability]

    def save(self, file_name):
        self.model.save(file_name)