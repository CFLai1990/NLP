"""oddata: parse the data returned from the Object Detection module"""
from .__settings__ import API, OD_PATH
from .libs import parser

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)
        self.parser = parser(self.file_op, parameters['spacy'])

    def execute(self, data):
        success = self.parser.save(OD_PATH, data)
        info = 'SUCCESS: the OD data has been saved successfully.'
        if not success:
            info = 'FAILURE: the OD data has not been saved.'
        self.emit2client({
            'state': success,
            'info': info
        })
        self.logger.info('API executed')
