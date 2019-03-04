"""nlp: the main api for NLP"""
from .__settings__ import API, OD_PATH
from .libs import pipeline, parser

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)
        self.nlp_model = parameters['spacy']
        self.pipeline = pipeline(self.nlp_model)
        self.parser = parser(self.file_op)

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
        od_data = self.parser.load(OD_PATH)
        result = self.nlp(data, od_data)
        self.emit2client(result)
        self.logger.info('API executed')
