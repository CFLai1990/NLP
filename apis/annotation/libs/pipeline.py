"""The pipeline for Natural Language Processing"""
from .color_detection import infer_color
from .size_detection import infer_size
<<<<<<< HEAD
=======
from .location_detection import infer_loc
>>>>>>> dev

class NLPPipeline:
    """The pipeline class"""
    def __init__(self, model):
        self.nlp = model

    def infer(self, sentence):
        """The main entry for NLP"""
        doc = self.nlp(sentence)
        entities = {}
        infer_color(doc, entities)
        infer_size(doc, entities)
<<<<<<< HEAD
=======
        infer_loc(doc, entities)
>>>>>>> dev
        return entities
