"""The module for detecting co-mentioned entities"""
from .relation_dict import get_relation

def infer_entities(token, is_subject=False):
    """The function for detecting entities and their relationships"""
    if is_subject:
        entities, signs = infer_subjects(token)
    else:
        entities, signs = infer_objects(token)
    return entities, signs

def infer_subjects(token):
    """Entity detection when the entities are subjects"""
    entities = []
    signs = []
    overall_sign = True
    is_pron = False
    if token.children:
        for child in token.children:
            # Case 1: A, B, C, ... [conj] N
            # Example: A, B, and C are ...
            if child.dep_ == "conj":
                if token.i not in entities:
                    entities.append(token.i)
                    signs.append(True)
                get_children(child, entities, signs, is_subject=True)
            # Case 2: [pron] of A, B, ... [conj] N
            # Example: None of A, B, and C is ...
            if child.dep_ == "prep":
                token_text = token.lemma_
                child_overall_sign = get_relation(token_text)
                is_pron = True
                if child.text == 'of' and child.children:
                    for grand_child in child.children:
                        if grand_child.dep_ == "pobj":
                            get_children(grand_child, entities, signs,
                                         child_overall_sign, is_subject=True)
            # Case 3: "Both A and B" or "Neither A or B"
            if child.dep_ == "preconj":
                child_text = child.lemma_
                overall_sign = get_relation(child_text)
            # Case 4: "A's XXX"
            if child.dep_ == "poss":
                is_pron = True
                if child.i not in entities:
                    entities.append(child.i)
                    signs.append(True)
    if not is_pron:
        if token.i not in entities:
            entities.append(token.i)
            signs.append(True)
    # Handle case 3: neither ...
    if not overall_sign:
        for index, sign in enumerate(signs):
            signs[index] = not sign
    return entities, signs

def infer_objects(token):
    """Entity detection when the entities are objects"""
    entities = []
    signs = []
    if token.i not in entities:
        entities.append(token.i)
        signs.append(True)
    if token.children:
        for child in token.children:
            # Case 1: A, B, C, ... [conj] N
            # Example: A, B, and C ...
            if child.dep_ == "conj":
                get_children(child, entities, signs)
    return entities, signs

def get_children(child, entities, signs, overall_sign=True, is_subject=False):
    """Merge the children results"""
    child_entities, child_signs = infer_entities(child, is_subject)
    if overall_sign is False:
        for index, c_sign in enumerate(child_signs):
            child_signs[index] = not c_sign
    entities.extend(child_entities)
    signs.extend(child_signs)
    