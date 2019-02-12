from .__settings__ import API
import spacy

class apiClass(API):
  def __init__(self, parameters):
    API.__init__(self, parameters)
    self.nlp = spacy.load('en_coref')

  def NLP(self, text):
    result = self.nlp(text)
    print(type(result))
    return result

  def execute(self, text):
    result = self.NLP(text)
    self.emit2Client(result)
    self.logger.info('API executed')