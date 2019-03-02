"""nlp: the main api for NLP"""
import json
from .__settings__ import API, OD_PATH
from .libs import pipeline

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)
        self.nlp_model = parameters['spacy']
        self.pipeline = pipeline(self.nlp_model)

    def get_od_data(self):
        """Get the results from the OD module"""
        od_path = self.file_op.get_path(OD_PATH)
        od_data = None
        if self.file_op.exists(od_path):
            with open(od_path, 'r') as file:
                od_data = json.load(file)
                file.close()
        return od_data

    def get_sentences(self, doc):
        """Get the sentence segmentation results"""
        sentences = []
        for index, sent in enumerate(doc.sents):
            sentences.append({
                'id': 'st_' + str(index),
                'content': sent.text,
                })
        return sentences

    def nlp(self, text, od_data):
        """The main entry for NLP functions"""
        doc = self.nlp_model(text)
        sentences = self.get_sentences(doc)
        entities = {}
        labels = {}
        for index, sent in enumerate(sentences):
            sent_entities, sent_labels = self.pipeline.infer(sent['content'], od_data)
            entities['st_' + str(index)] = sent_entities
            labels['st_' + str(index)] = sent_labels
        return {
            'sentences': sentences,
            'entities': entities,
            'labels': labels
        }

    def execute(self, data):
        od_data = self.get_od_data()
        result = self.nlp(data, od_data)
        self.emit2client(result)
        self.logger.info('API executed')
