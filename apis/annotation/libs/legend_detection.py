"""The function for detecting legends"""

def infer_legend(doc, entity_dict, legend_list):
    """Legend detection function"""
    if legend_list:
        legends_info = search_for_legends(doc, legend_list)
    for legend_info in legends_info:
        if not legend_info["mentioned"]:
            continue
        pack_entity_dict_by_legend(doc, entity_dict, legend_info)

def pack_entity_dict_by_legend(doc, entity_dict, legend_info):
    """Pack the results for a certain legend"""
    entity_locations = legend_info["locations"]
    if entity_locations:
        for entity_location in entity_locations:
            entity_id = 'entity_' + str(entity_location)
            entity = entity_dict.get(entity_id)
            if entity is None:
                e_token = doc[entity_location]
                entity = {
                    'name': e_token.lemma_,
                }
                pack_entity_by_legend(entity, legend_info["label"], legend_info["feature"])
                entity_dict[entity_id] = entity
            else:
                pack_entity_by_legend(entity, legend_info["label"], legend_info["feature"])

def pack_entity_by_legend(entity, legend_label, legend_feature):
    """Pack an entity with certain features"""
    # Set the "legend" label
    entity["legend"] = legend_label
    # Set the legend color
    color = legend_feature.get("color")
    if color is not None:
        entity_color = entity.get("color")
        if entity_color is None:
            entity_color = []
            entity["color"] = entity_color
        entity_color[color] = True

def search_for_legends(doc, legend_list):
    """Search for the legends in the list"""
    legends_info = []
    for legend in legend_list:
        legend_mentioned = False
        label_indices = []
        legend_label = legend.get("label")
        if legend_label is not None:
            label_lemmas = legend_label.get("lemma")
            label_text = legend_label.get("text")
            if label_lemmas is not None:
                legend_mentioned, label_indices = search_for_label(doc, legend_label["lemma"])
            legends_info.append({
                "label": label_text,
                "feature": legend.get("feature"),
                "mentioned": legend_mentioned,
                "locations": label_indices
            })
    return legends_info

def search_for_label(doc, labels):
    """Search for the legend title mentioned in the sentence"""
    # whether a legend has been mentioned
    label_mentioned = False
    label_indices = []
    for t_id, token in enumerate(doc):
        id_next = 0
        for label_word in labels:
            if doc[t_id+id_next].lemma_ != label_word:
                break
            else:
                id_next = id_next + 1
        if id_next != 0 and id_next == len(labels):
            label_mentioned = True
            label_indices.append(t_id)
    return label_mentioned, label_indices
