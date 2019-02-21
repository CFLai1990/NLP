"""The pipeline for Natural Language Processing"""
from .color_detection import infer_color

class NLPPipeline:
    """The pipeline class"""
    def __init__(self, model):
        self.nlp = model

    def infer(self, sentence):
        """The main entry for NLP"""
        doc = self.nlp(sentence)
        entities = {}
        infer_color(doc, entities)
        return entities
