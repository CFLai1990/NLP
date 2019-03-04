"""The pipeline for Natural Language Processing"""
from .label_detection import infer_label
from .color_detection import infer_color
from .size_detection import infer_size
from .location_detection import infer_loc
from .axis_detection import infer_axis

class NLPPipeline:
    """The pipeline class"""
    def __init__(self, model):
        self.nlp = model

    def infer(self, sentence, od_data=None):
        """The main entry for NLP"""
        doc = self.nlp(sentence)
        # Get the entities described by their labels
        labels = {}
        if od_data is not None:
            infer_label(sentence, labels, od_data["labels"])
        # Get the entities described by their visual features
        entities = {}
        infer_color(doc, entities)
        infer_size(doc, entities)
        infer_loc(doc, entities)
        print('started')
        infer_axis(doc, entities, od_data["axes"])
        print('ended')
        return entities, labels
