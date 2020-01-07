"""The default APIs"""
import spacy
from .__settings__ import APIs, NAMESPACE, PACKAGE, OUTPUT_DIR, EVENT_DICT

SPACY = spacy.load('en')#en_coref en

class THISAPIs(APIs):
    """The wrapper for all default APIs"""
    def __init__(self, logger, socket):
        APIs.__init__(self, {
            'namespace': NAMESPACE,
            'logger': logger,
            'socket': socket,
            'events': EVENT_DICT,
            'package': PACKAGE,
            'output_dir': OUTPUT_DIR
        })
        self.api_parms({
            'spacy': SPACY
        })
        self.start()
