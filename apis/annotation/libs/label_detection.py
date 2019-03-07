"""The function for detecting the description of visible labels"""

def infer_label(doc, entity_dict, label_list):
    """Label detection function"""
    labels_info = search_for_labels(doc, label_list)
    for label_info in labels_info:
        if not label_info["mentioned"]:
            continue
        pack_entity_dict_by_label(doc, entity_dict, label_info)

def pack_entity_dict_by_label(doc, entity_dict, label_info):
    """Pack the results for a certain label"""
    entity_locations = label_info["locations"]
    if entity_locations:
        for entity_location in entity_locations:
            entity_id = 'entity_' + str(entity_location)
            entity = entity_dict.get(entity_id)
            if entity is None:
                e_token = doc[entity_location]
                entity = {
                    'name': e_token.lemma_,
                }
                pack_entity_by_label(entity, label_info["label"])
                entity_dict[entity_id] = entity
            else:
                pack_entity_by_label(entity, label_info["label"])

def pack_entity_by_label(entity, label):
    """Pack an entity for a certain label"""
    # Set the "label" attribute
    entity["label"] = label

def search_for_labels(doc, label_list):
    """Search for the labels in the list"""
    labels_info = []
    if label_list:
        for label in label_list:
            label_mentioned = False
            label_indices = []
            label_text = label.get("text")
            label_lemmas = label.get("lemma")
            label_root = label.get("root")
            label_mentioned, label_indices = search_for_label(doc, label_lemmas, label_root)
            labels_info.append({
                "label": label_text,
                "mentioned": label_mentioned,
                "locations": label_indices
            })
    return labels_info

def search_for_label(doc, label_lemmas, label_root):
    """Search for the label mentioned in the sentence"""
    # whether a label has been mentioned
    label_mentioned = False
    label_indices = []
    if label_lemmas:
        for t_id, token in enumerate(doc):
            id_next = 0
            for label_lemma in label_lemmas:
                if doc[t_id+id_next].lemma_ != label_lemma:
                    break
                else:
                    id_next = id_next + 1
            if id_next != 0 and id_next == len(label_lemmas):
                label_mentioned = True
                if label_root:
                    label_indices.append(t_id + label_root)
                else:
                    label_indices.append(t_id)
    return label_mentioned, label_indices
