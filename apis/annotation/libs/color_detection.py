"""The function for detecting color descriptions"""
from .color_dict import get_std_color
from .entity_detection import infer_entities

def infer_color(doc, entity_dict):
    """Color detection function"""
    color_indices = []
    for t_id, token in enumerate(doc):
        original_text = token.lemma_
        # Identify the valid color words
        std_color = get_std_color(original_text)
        if std_color is None:
            continue
        # Identify the entities it describes
        color_indices.append(t_id)
        indices = []
        signs = []
        print('color: ' + std_color + ', POS: ' + token.pos_)
        if token.pos_ == 'ADJ':
            indices, signs = infer_adj_color(token)
        for stored_id, e_id in enumerate(indices):
            entity_id = 'entity_' + str(e_id)
            color_sign = signs[stored_id]
            if entity_dict.get(entity_id) is None:
                e_token = doc[e_id]
                entity_dict[entity_id] = {
                    'name': e_token.lemma_,
                    'color': {
                        std_color: color_sign
                    }
                }
            else:
                if entity_dict[entity_id]['color'] is None:
                    entity_dict[entity_id]['color'] = {
                        std_color: color_sign
                    }
                else:
                    entity_dict[entity_id]['color'].update({
                        std_color: color_sign
                    })

def infer_adj_color(token):
    """Infer the entities when the color is an ADJ"""
    # Case 1: [color] [entities]
    if token.dep_ == 'amod':
        indices, signs, cont_sign = infer_adj_color_amod(token)
        if cont_sign:
            return infer_adj_color(token.head)
        return indices, signs
    # Case 2: [entities] [be] [color]
    if token.dep_ == 'acomp' and token.head.lemma_ == 'be':
        v_token = token.head
        return infer_adj_color_subjects(v_token, True)
    # Case 3~6: ... [prep] [color]
    if token.dep_ == 'pobj' and token.head.dep_ == 'prep':
        v_token = token.head.head
        if not v_token:
            return [], []
        if v_token.pos_ == 'VERB':
            # Case 3: [entities] [be] [prep] [color]
            if v_token.lemma_ == 'be':
                return infer_adj_color_subjects(v_token, True)
            # Case 4: [entities] [be] [verb] [prep] [color]
            if v_token.head and v_token.head.lemma_ == 'be':
                return infer_adj_color_subjects(v_token)
            # Case 5: [entities] [verb] [prep] [color]
            return infer_adj_color_objects(v_token, True)
        # Case 6: [entities] [prep] [color]
        if v_token.pos_ == 'NOUN' or v_token.pos_ == 'PROPN':
            return infer_adj_color_objects(token.head)
    return [], []

def infer_adj_color_amod(token):
    """infer function for adj_case 1"""
    cont_sign = False
    # Special case: e.g. replace 'blue' with 'a blue color', then continue
    if token.head.lemma_ == 'color':
        cont_sign = True
        return [], [], cont_sign
    entity_indices = [token.head.i]
    entity_signs = [True]
    return entity_indices, entity_signs, cont_sign

def infer_adj_color_subjects(token, be_verb=False):
    """infer function for adj_case 2~4"""
    entity_indices = []
    entity_signs = []
    if token.children:
        for child in token.children:
            if (be_verb and child.dep_ == 'nsubj') or (not be_verb and child.dep_ == 'nsubjpass'):
                entities, signs = infer_entities(child, True)
                entity_indices.extend(entities)
                entity_signs.extend(signs)
            # handle negation
            if child.dep_ == "neg":
                for index, e_sign in enumerate(entity_signs):
                    entity_signs[index] = not e_sign
    return entity_indices, entity_signs

def infer_adj_color_objects(token, verb=False):
    """infer function for adj_case 5 and 6"""
    entity_indices = []
    entity_signs = []
    # case 6
    if not verb:
        entities, signs = infer_entities(token.head, False)
        entity_indices.extend(entities)
        entity_signs.extend(signs)
        for child in token.children:
            # handle negation
            if child.dep_ == "neg":
                for index, e_sign in enumerate(entity_signs):
                    entity_signs[index] = not e_sign
        return entity_indices, entity_signs
    # case 5
    if token.head and token.dep_ == "acl":
        entities, signs = infer_entities(token.head, False)
        entity_indices.extend(entities)
        entity_signs.extend(signs)
    if token.children:
        for child in token.children:
            if child.dep_ == 'nsubj':
                entities, signs = infer_entities(child, False)
                entity_indices.extend(entities)
                entity_signs.extend(signs)
            # handle negation
            if child.dep_ == "neg":
                for index, e_sign in enumerate(entity_signs):
                    entity_signs[index] = not e_sign
    return entity_indices, entity_signs
