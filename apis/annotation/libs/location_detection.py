"""The function for detecting location descriptions"""
from .location_dict import get_std_loc
from .entity_detection import infer_entities

def infer_loc(doc, entity_dict):
    """Loction detection function"""
    loc_indices = []

    for t_id, token in enumerate(doc):
        original_text = token.lemma_
        # Identify the valid location words
        std_loc = get_std_loc(original_text)
        if std_loc is None:
            continue
        loc_indices.append(t_id)
        indices = []
        signs = []
        if token.pos_ == 'ADJ':
            indices, signs = infer_adj_loc(token)
        elif token.pos_ == 'NOUN':
            indices, signs = infer_noun_loc(token)

        for _id, e_token_index in enumerate(indices):
            entity_id = 'entity_' + str(e_token_index)
            loc_sign = signs[_id]
            if not entity_dict.get(entity_id):
                e_token = doc[e_token_index]
                entity_dict[entity_id] = {
                    'name': e_token.lemma_,
                    'location': {
                        std_loc: loc_sign
                    }
                }
            else:
                if 'location' not in entity_dict[entity_id]:
                    entity_dict[entity_id]['location'] = {
                        std_loc: loc_sign
                    }
                else:
                    entity_dict[entity_id]['location'].update({
                        std_loc: loc_sign
                        })

def infer_adj_loc(token):
    """Infer the entities when the loc is an ADJ"""
    if token.dep_ == 'amod':
        if token.head.dep_ == 'pobj':
            # Case 2~7
            indices, signs = infer_noun_loc(token.head)
        else:
            # Case 1
            indices, signs = infer_adj_loc_amod(token)
        return indices, signs
    return [], []


def infer_noun_loc(token):
    """Infer the locations when the loc is a NOUN"""
    if token.dep_ == 'pobj' and token.head.dep_ == 'prep':
        v_token = token.head.head
        if not v_token:
            return [], []
        if v_token.pos_ == 'VERB':
            if v_token.lemma_ == 'be':
                # Case 3: [prep] [location] [be] [entities]
                for child in v_token.children:
                    if child.dep_ == 'attr':
                        return infer_noun_loc_attr(child)
                # Case 2: [entities] [be] [prep] [location]
                return infer_noun_loc_subjects(v_token, True)
            else:
                has_be = False
                for child in v_token.children:
                    if child.dep_ == 'nsubjpass':
                        has_be = True
                if has_be:
                    # Case 4: [entities] [be] [verb] [prep] [location]
                    return infer_noun_loc_subjects(v_token)
                # Case 5: [verb] [prep] [location] [be] [entities]
                # Case 6: [entities] [verb] [prep] [location]
                return infer_noun_size_objects(v_token, True)
        # Case 7: [entities] [prep] [location]
        if v_token.pos_ == 'NOUN' or v_token.pos_ == 'PROPN':
            return infer_noun_size_objects(token.head)
    return [], []


def infer_adj_loc_amod(token):
    """infer function for adj_case 1"""
    entity_indices = [token.head.i]
    entity_signs = [True]
    return entity_indices, entity_signs


def infer_noun_loc_subjects(token, be_verb=False):
    """infer function for noun_case 2, 4"""
    entity_indices = []
    entity_signs = []
    if token.children:
        for child in token.children:
            if be_verb and child.dep_ == 'nsubj' or (not be_verb and child.dep_ == 'nsubjpass'):
                entities, signs = infer_entities(child, True)
                entity_indices.extend(entities)
                entity_signs.extend(signs)
            # handle negation
            if child.dep_ == "neg":
                for index, e_sign in enumerate(entity_signs):
                    entity_signs[index] = not e_sign
    return entity_indices, entity_signs


def infer_noun_loc_attr(token):
    """infer function for noun_case 3"""
    entity_indices = [token.i]
    entity_signs = [True]
    return entity_indices, entity_signs


def infer_noun_size_objects(token, verb=False):
    """infer function for noun_case 5, 6, 7"""
    entity_indices = []
    entity_signs = []
    if verb:
        # case 6
        if token.dep_ == 'acl':
            return infer_noun_loc_attr(token.head)
        # case 5
        else:
            for child in token.children:
                if child.dep_ == 'auxpass':
                    for _child in child.children:
                        if _child.dep_ == 'attr':
                            return infer_noun_loc_attr(_child)
    else:
        # case 7
        entities, signs = infer_entities(token.head, False)
        entity_indices.extend(entities)
        entity_signs.extend(signs)
        for child in token.children:
            # handle negation
            if child.dep_ == "neg":
                for index, e_sign in enumerate(entity_signs):
                    entity_signs[index] = not e_sign
        return entity_indices, entity_signs

    return [], []
