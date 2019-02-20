"""test: testing api for NLP"""
# import spacy
from .__settings__ import API

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)
        # self.nlp_model = spacy.load('en_coref')

    def nlp(self, text):
        """NLP for the given text"""
        # result = self.nlp_model(text)
        result = None
        return result

    def execute(self, data):
        result = self.nlp(data)
        self.emit2client('NLP executed for text: ' + data)
        self.logger.info('API executed')
