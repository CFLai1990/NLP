"""The function for detecting shape descriptions"""
from .shape_dict import get_std_shape

def infer_shape(doc, entity_dict):
    """Shape detection function"""
    for t_id, token in enumerate(doc):
        token_lemma = token.lemma_
        # Identify the valid shape words
        std_shape = get_std_shape(token_lemma)
        if std_shape is None:
            continue
        pack_entity_dict_by_shape(entity_dict, token, std_shape)

def pack_entity_dict_by_shape(entity_dict, token, std_shape):
    """Pack the entity_dict by standard shapes"""
    token_location = token.i
    token_id = 'entity_' + str(token_location)
    entity = entity_dict.get(token_id)
    if entity is None:
        entity = {
            "name": token.lemma_
        }
        entity_dict[token_id] = entity
    entity["shape"] = std_shape
