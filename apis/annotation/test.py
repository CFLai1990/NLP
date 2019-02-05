from flask_socketio import emit
from .__settings__ import API
import spacy

nlp = spacy.load(str('en_coref_md'))

class apiClass(API):
  def __init__(self, logger, socket, message, namespace):
    API.__init__(self, logger, socket, message, namespace)

  def NLP(self, text):
    doc = nlp(text)

  def execute(self, text):
    # save the text into file
    self.NLP(text)
    self.socket.emit(self.message, 'NLP executed!', namespace=self.namespace)
    self.logger.info('API executed')