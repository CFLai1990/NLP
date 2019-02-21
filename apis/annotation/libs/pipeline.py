"""The pipeline for Natural Language Processing"""
from .color_detection import infer_color

class NLPPipeline:
    """The pipeline class"""
    def __init__(self, model):
        self.nlp = model

    def infer(self, sentence):
        """The main entry for NLP"""
        print('pipeline started')
        doc = self.nlp(sentence)
        entities = {}
        print('middle')
        infer_color(doc, entities)
        print('pipeline finished')
        return entities
