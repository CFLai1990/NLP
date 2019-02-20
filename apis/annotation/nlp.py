"""test: testing api for NLP"""
# import spacy
from .libs import nlp
from .__settings__ import API

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)

    def execute(self, data):
        sentence_list, entity_list = nlp(data)
        result = {
            'sentences': sentence_list,
            'entities': entity_list
        }
        self.emit2client(result)
        self.logger.info('API executed')
