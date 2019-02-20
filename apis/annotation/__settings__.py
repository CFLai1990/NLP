"""annotation APIs: __settings__"""
import os
from ..libs import API, APIs

# settings for this package
NAMESPACE = '/api/annotation'
PACKAGE = 'apis.annotation'
OUTPUT_DIR = os.path.abspath('./files/annotation')

# message - apiName
EVENT_DICT = {
    'Test': 'test'
}
