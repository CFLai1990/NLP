"""oddata: parse the data returned from the Object Detection module"""
import json
from .__settings__ import API, OD_PATH

class ApiClass(API):
    """API Class"""
    def __init__(self, parameters):
        API.__init__(self, parameters)

    def save_od_data(self, data):
        """The main function for parsing the OD data"""
        od_path = self.file_op.get_path(OD_PATH)
        with open(od_path, 'w') as file:
            json.dump(data, file)
            file.close()
        return True

    def execute(self, data):
        success = self.save_od_data(data)
        info = 'SUCCESS: the OD data has been saved successfully.'
        if not success:
            info = 'FAILURE: the OD data has not been saved.'
        self.emit2client({
            'state': success,
            'info': info
        })
        self.logger.info('API executed')
