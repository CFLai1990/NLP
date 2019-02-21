"""test: testing api for NLP"""
# from .libs import nlp
from .__settings__ import API
from .libs import pipeline

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)
        self.nlp_model = parameters['spacy']
        self.pipeline = pipeline(self.nlp_model)

    def get_sentences(self, doc):
        """Get the sentence segmentation results"""
        sentences = []
        for index, sent in enumerate(doc.sents):
            sentences.append({
                'id': 'st_' + str(index),
                'content': sent.text,
                })
        return sentences

    def nlp(self, text):
        """The main entry for NLP functions"""
        doc = self.nlp_model(text)
        sentences = self.get_sentences(doc)
        entities = {}
        for index, sent in enumerate(sentences):
            print('St_' + str(index) + 'started')
            sent_entities = self.pipeline.infer(sent['content'])
            entities['st_' + str(index)] = sent_entities
            print('St_' + str(index) + 'finished')
        return {
            'sentences': sentences,
            'entities': entities
        }

    def execute(self, data):
        # sentence_list, entity_list = nlp(data)
        result = self.nlp(data)
        self.emit2client(result)
        self.logger.info('API executed')
