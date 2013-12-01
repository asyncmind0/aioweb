from json import JSONEncoder, JSONDecoder, dumps
from .model import Model
import logging

class ModelEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
        
class ModelDecoder(JSONDecoder):
    def __init__(self):
        logger = logging.getLogger(self.__class__.__name__)
        def from_json(json_object):
            model = None
            if 'doc_type' in json_object:
                doc_type = json_object['doc_type']
                try:
                    model = Model.get_model_by_name(doc_type)
                except KeyError as e:
                    logger.warn("No model foud for: %s" % doc_type)
                if model:
                    return model(**json_object)
            return json_object
        super(ModelDecoder, self).__init__(object_hook=from_json)
        

def json_dumps(obj):
    return dumps(obj, cls=ModelEncoder)
    

def json_loads(data):
    return ModelDecoder().decode(data.decode('utf-8'))