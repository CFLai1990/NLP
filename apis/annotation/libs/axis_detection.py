"""The function for detecting axis-based location descriptions"""
from .axis_dict import get_std_axis
from .entity_detection import infer_entities

def infer_axis(doc, entity_dict, axis_list):
    """Axis-based location detection function"""
    if axis_list is None:
        return
    mentioned, axes_info = search_for_axes(doc, axis_list)
    if not mentioned:
        return
    for axis_info in axes_info:
        # the axis has not been mentioned
        if not axis_info["mentioned"]:
            continue
        # the axis has been mentioned
        axis_id = axis_info["id"]
        axis_data = axis_list[axis_id]
        title_to_entities = {}
        # infer the entities via the axis title
        if axis_info["title"]["mentioned"]:
            title_root_id = axis_data["title"]["root"]
            title_locations = []
            for location in axis_info["title"]["locations"]:
                title_locations.append(location + title_root_id)
            title_entities, title_signs, title_to_entities = infer_titles(doc, title_locations)
            pack_entity_dict_by_title(doc, entity_dict, title_entities, title_signs, {
                "title": axis_data["title"]["text"],
                "unit": axis_data["unit"]["text"],
                "ticks": []
                })
        # infer the entities via the axis ticks
        if axis_info["ticks"]["mentioned"]:
            ticks_info = axis_info["ticks"]["data"]
            tick_results = []
            for tick_info in ticks_info:
                tick_data = axis_data["ticks"][tick_info["id"]]
                tick_tokens = []
                for location in tick_info["locations"]:
                    tick_tokens.append(doc[location + tick_data["root"]])
                tick_result = infer_ticks(tick_tokens, tick_data["text"], title_to_entities)
                print(tick_result)
                tick_results.append(tick_result)
            # pack the results in tick_entities
            tick_entities = []
            for tick_result in tick_results:
                entities_by_location = tick_result["entities"]
                if entities_by_location:
                    for _id, entities_loc in enumerate(entities_by_location):
                        if entities_loc:
                            tick_entities.append({
                                "title": axis_data["title"]["text"],
                                "unit": axis_data["unit"]["text"],
                                "tick_texts": [tick_result["text"]],
                                "entities": entities_loc,
                                "signs": tick_result["signs"][_id],
                                "relation": tick_result["relations"][_id],
                                "locations": [tick_result["locations"][_id]],
                                })
            # handle conjunction to update tick_entities
            for tick_result in tick_results:
                tick_conjs = tick_result["conjunctions"]
                tick_text = tick_result["text"]
                for tick_id, tick_conj_id in enumerate(tick_conjs):
                    tick_location = tick_result["locations"][tick_id]
                    if tick_conj_id is not None:
                        # search for its conjunction in tick_entities
                        for tick_entity in tick_entities:
                            if tick_conj_id in tick_entity["locations"]:
                                std_prep = tick_entity["relation"]
                                if std_prep == "between":
                                    tick_entity["tick_texts"].append(tick_text)
                                    tick_entity["locations"].append(tick_location)
                                else:
                                    tick_entities.append({
                                        "title": tick_entity["title"],
                                        "unit": tick_entity["unit"],
                                        "tick_texts": [tick_text],
                                        "entities": tick_entity["entities"],
                                        "signs": tick_entity["signs"],
                                        "relation": tick_entity["relation"],
                                        "locations": [tick_location]
                                        })
                                break
            # pack the results
            for tick_entity in tick_entities:
                pack_entity_dict_by_tick(doc, entity_dict, tick_entity)

def pack_entity_dict_by_title(doc, entity_dict, entities, signs, state):
    """Pack the entity dict by the titles"""
    for _id, e_token_index in enumerate(entities):
        entity_id = 'entity_' + str(e_token_index)
        e_state = state.copy()
        e_state.update({
            'sign': signs[_id]
        })
        if not entity_dict.get(entity_id):
            e_token = doc[e_token_index]
            entity_dict[entity_id] = {
                'name': e_token.lemma_,
                'axis': [e_state]
            }
        else:
            if 'axis' not in entity_dict[entity_id]:
                entity_dict[entity_id]['axis'] = [e_state]
            else:
                entity_dict[entity_id]['axis'].append(e_state)

def pack_entity_dict_by_tick(doc, entity_dict, tick_entity):
    """Pack the entity dict by the ticks"""
    entities = tick_entity["entities"]
    signs = tick_entity["signs"]
    for _id, e_token_index in enumerate(entities):
        entity_id = 'entity_' + str(e_token_index)
        e_axis_state = {
            "title": tick_entity["title"],
            "unit": tick_entity["unit"],
            "sign": True,
        }
        e_tick_state = {
            "values": tick_entity["tick_texts"],
            "relation": tick_entity["relation"],
            "sign": signs[_id]
        }
        if not entity_dict.get(entity_id):
            e_token = doc[e_token_index]
            e_state = e_axis_state.update({
                "ticks": [e_tick_state]
            })
            entity_dict[entity_id] = {
                'name': e_token.lemma_,
                'axis': [e_state]
            }
        else:
            if 'axis' not in entity_dict[entity_id]:
                e_state = e_axis_state.update({
                    "ticks": [e_tick_state]
                })
                entity_dict[entity_id]['axis'] = [e_state]
            else:
                # search for the corresponding axis
                axis_found = False
                for axis_state in entity_dict[entity_id]["axis"]:
                    if e_axis_state["title"] is not None and axis_state["title"] == e_axis_state["title"]:
                        axis_found = True
                        if not axis_state["sign"]:
                            e_tick_state["sign"] = not e_tick_state["sign"]
                        axis_state["ticks"].append(e_tick_state)
                        break
                if not axis_found:
                    e_state = e_axis_state.update({
                        "ticks": [e_tick_state]
                    })
                    entity_dict[entity_id]['axis'].append(e_state)

def search_for_axes(doc, axis_list):
    """Determine if each axis has been mentioned"""
    mentioned = False
    axes_info = []
    for axis_id, axis in enumerate(axis_list):
        # whether the axis title has been mentioned
        title_mentioned = False
        if axis.get("title") is not None:
            title_mentioned, title_pos = search_for_label(doc, axis["title"]["lemma"])
        # whether the axis tick + unit has been mentioned
        unit_mentioned = True
        if axis.get("unit") is not None:
            unit_mentioned, unit_pos = search_for_label(doc, axis["unit"]["lemma"])
        # whether the tick values have been mentioned
        ticks = None
        ticks_mentioned = False
        if axis.get("ticks") is not None:
            ticks = []
            tick_mentioned = False
            for tick_id, tick in enumerate(axis["ticks"]):
                tick_mentioned, tick_pos = search_for_label(doc, tick["lemma"])
                if tick_mentioned:
                    ticks_mentioned = True
                    ticks.append({
                        "id": tick_id,
                        "mentioned": tick_mentioned,
                        "locations": tick_pos,
                    })
        axis_mentioned = ticks_mentioned and unit_mentioned
        axes_info.append({
            "mentioned": axis_mentioned,
            "id": axis_id,
            "title": {
                "mentioned": title_mentioned,
                "locations": title_pos,
                },
            "unit": {
                "mentioned": unit_mentioned,
                "locations": unit_pos,
                },
            "ticks": {
                "mentioned": ticks_mentioned,
                "data": ticks
            }
        })
        mentioned = mentioned or axis_mentioned
    return mentioned, axes_info

def search_for_label(doc, labels):
    """Search for the axis title or unit mentioned in the sentence"""
    # whether the axis title or unit has been mentioned
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
            break
    return label_mentioned, label_indices

def infer_titles(doc, title_locations):
    """Infer the described entities via the axis title"""
    entity_indices = []
    entity_signs = []
    location_to_entities = {}
    for title_location in title_locations:
        title_token = doc[title_location]
        location_entities = []
        location_signs = []
        # Case ~1: [subject] [have] [title]
        # Example: Beijing has a temperature ...
        if title_token.dep_ == "dobj" and title_token.head.lemma_ == "have":
            v_token = title_token.head
            for child in v_token.children:
                if child.dep_ == "nsubj":
                    entities, signs = infer_entities(child, True)
                    location_entities.extend(entities)
                    location_signs.extend(signs)
        for child in title_token.children:
            # Case ~2: [title] [prep] [subject]
            # Example: temperature of Beijing
            if child.dep_ == "prep":
                for grand_child in child.children:
                    if grand_child.dep_ == "pobj":
                        entities, signs = infer_entities(grand_child, True)
                        location_entities.extend(entities)
                        location_signs.extend(signs)
            # Case ~3: [subject] ['s] [title]
            # Example: Beijing's temperature
            if child.dep_ == "poss":
                entities, signs = infer_entities(child, True)
                location_entities.extend(entities)
                location_signs.extend(signs)
        entity_indices.extend(location_entities)
        entity_signs.extend(location_signs)
        location_to_entities[title_location] = location_entities
    return entity_indices, entity_signs, location_to_entities

def infer_ticks(tick_tokens, tick_text, title_to_entities):
    """Infer the described entities via the axis ticks"""
    tick_locations = []
    entity_indices = []
    entity_signs = []
    entity_preps = []
    entity_conjs = []
    for tick_token in tick_tokens:
        tick_locations.append(tick_token.i)
        tick_entities = []
        tick_signs = []
        std_prep = None
        v_token = None
        neg_sign = True
        conj_id = None
        # Handle conjunction
        if tick_token.dep_ == "conj":
            head_token = tick_token.head
            while head_token.dep_ == "conj":
                head_token = head_token.head
            conj_id = head_token.i
        else:
            # Find the standard prep and the verb token
            if tick_token.dep_ == "attr":
                than_found = False
                std_found = False
                for child in tick_token.children:
                    if child.dep_ == "quantmod" and child.lemma_ == "than":
                        than_found = True
                    if child.dep_ == "amod":
                        std_prep = get_std_axis(child.lemma_)
                        if std_prep is not None:
                            std_found = True
                if std_found and than_found:
                    v_token = tick_token.head
            if tick_token.dep_ == "pobj":
                prep_token = tick_token.head
                if prep_token.lemma_ == "than":
                    prep_token = prep_token.head
                std_prep = get_std_axis(prep_token)
                if std_prep is not None:
                    v_token = prep_token.head
                    # handle negation
                    for child in prep_token.children:
                        if child.dep_ == "neg":
                            neg_sign = False
            if tick_token.dep_ == "dobj":
                for child in tick_token.children:
                    if child.dep_ == "quantmod":
                        std_prep = get_std_axis(child.lemma_)
                        if std_prep is not None:
                            v_token = tick_token.head
            if std_prep is None or v_token is None:
                continue
            # Detect the entities
            if v_token.pos_ == "VERB":
                for child in v_token.children:
                    # handle negation
                    if child.dep_ == "neg":
                        neg_sign = False
                    if child.dep_ == "nsubj":
                        child_location = child.i
                        if title_to_entities.get(child_location) is None:
                            tick_entities, tick_signs = infer_entities(child, True)
                        else:
                            tick_entities = title_to_entities[child_location]
                            for tick_entity in tick_entities:
                                tick_signs.append(True)
            else:
                v_location = v_token.i
                if title_to_entities.get(v_location) is None:
                    tick_entities, tick_signs = infer_entities(v_token, True)
                else:
                    tick_entities = title_to_entities[v_location]
                    for tick_entity in tick_entities:
                        tick_signs.append(True)
            # Handle global negation
            if not neg_sign:
                for sign_id, tick_sign in enumerate(tick_signs):
                    tick_signs[sign_id] = not tick_sign
            # Update
        entity_indices.append(tick_entities)
        entity_signs.append(tick_signs)
        entity_preps.append(std_prep)
        entity_conjs.append(conj_id)
    return {
        "text": tick_text,
        "locations": tick_locations,
        "entities": entity_indices,
        "signs": entity_signs,
        "relations": entity_preps,
        "conjunctions": entity_conjs
    }
