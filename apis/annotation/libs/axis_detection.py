"""The function for detecting axis-based location descriptions"""
import copy
from .axis_dict import get_std_axis
from .entity_detection import infer_entities

def infer_axis(doc, entity_dict, axis_list):
    """Axis-based location detection function"""
    if axis_list is None:
        return
    mentioned, axes_info = search_for_axes(doc, axis_list)
    if not mentioned:
        return
    title_to_entities_all = {}
    title_to_entities_dict = {}
    # Step 1: Get all the titles mentioned
    for axis_info in axes_info:
        # the axis title or ticks have not been mentioned
        if not (axis_info["title"]["mentioned"] or axis_info["mentioned"]):
            continue
        # the axis title or ticks have been mentioned
        axis_id, axis_data, axis_title, axis_unit = extract_axis_info(axis_info, axis_list)
        title_to_entities = {}
        # infer the entities via the axis title
        if axis_info["title"]["existed"] and axis_info["title"]["mentioned"]:
            title_root_id = axis_data["title"]["root"]
            title_locations = []
            for location in axis_info["title"]["locations"]:
                title_locations.append(location + title_root_id)
            title_entities, title_signs, title_to_entities = infer_titles(doc, title_locations)
            # Pack the results whether or not the ticks have been mentioned
            pack_entity_dict_by_title(doc, entity_dict, title_entities, title_signs, {
                "title": axis_title,
                "unit": axis_unit,
                "ticks": []
                })
        if axis_title is not None:
            title_to_entities_dict[axis_title] = title_to_entities
        print("*** title_to_entities_dict", title_to_entities_dict)
        title_to_entities_all.update(title_to_entities)
    # Step 2: Get all the ticks mentioned
    for axis_info in axes_info:
        # the axis has not been mentioned
        if not axis_info["mentioned"]:
            continue
        # the axis has been mentioned
        axis_id, axis_data, axis_title, axis_unit = extract_axis_info(axis_info, axis_list)
        title_to_entities = {}
        if axis_title is not None:
            title_to_entities = title_to_entities_dict.get(axis_title)
        print(title_to_entities)
        # infer the entities via the axis ticks
        if axis_info["ticks"]["existed"] and axis_info["ticks"]["mentioned"]:
            ticks_info = axis_info["ticks"]["data"]
            tick_results = []
            unit_data = None
            if axis_info["unit"]["existed"] and axis_info["unit"]["mentioned"]:
                unit_data = axis_data["unit"]["lemma"]
            for tick_info in ticks_info:
                tick_data = axis_data["ticks"][tick_info["id"]]
                tick_tokens = []
                for location in tick_info["locations"]:
                    tick_tokens.append(doc[location + tick_data["root"]])
                tick_result = infer_ticks(tick_tokens, tick_data["text"], title_to_entities, title_to_entities_all, unit_data)
                tick_results.append(tick_result)
            # pack the results in tick_entities
            tick_entities = []
            for tick_result in tick_results:
                entities_by_location = tick_result["entities"]
                if entities_by_location:
                    for _id, entities_loc in enumerate(entities_by_location):
                        if entities_loc:
                            tick_entities.append({
                                "title": axis_title,
                                "unit": axis_unit,
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
                print("-- tick entity: ", tick_entity)
                pack_entity_dict_by_tick(doc, entity_dict, tick_entity)
    # Step 3 (optional): make up for the missing attributes
    make_up_for_axis(entity_dict)

def extract_axis_info(axis_info, axis_list):
    """Extract the axis information from the data structure"""
    axis_id = axis_info["id"]
    axis_data = axis_list[axis_id]
    axis_title = None
    axis_unit = None
    if axis_info["unit"]["existed"]:
        axis_unit = axis_data["unit"]["text"]
        # axis_unit = ' '.join(axis_data["unit"]["lemma"])
    if axis_info["title"]["existed"]:
        axis_title = axis_data["title"]["text"]
        # axis_title = ' '.join(axis_data["title"]["lemma"])
    return axis_id, axis_data, axis_title, axis_unit

def pack_entity_dict_by_title(doc, entity_dict, entities, signs, state):
    """Pack the entity dict by the titles"""
    for _id, e_token_index in enumerate(entities):
        entity_id = 'entity_' + str(e_token_index)
        e_state = copy.deepcopy(state)
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
        entity_id = 'entity_' + str(e_token_index)
        if not entity_dict.get(entity_id):
            e_token = doc[e_token_index]
            e_axis_state.update({
                "ticks": [e_tick_state]
            })
            entity_dict[entity_id] = {
                'name': e_token.lemma_,
                'axis': [e_axis_state]
            }
        else:
            if 'axis' not in entity_dict[entity_id]:
                print("axis not existed: ", tick_entity["title"])
                e_axis_state.update({
                    "ticks": [e_tick_state]
                })
                entity_dict[entity_id]['axis'] = [e_axis_state]
            else:
                # search for the corresponding axis
                axis_found = False
                for axis_state in entity_dict[entity_id]["axis"]:
                    print("axis: ", axis_state["title"], " entity: ", entity_id)
                    print("axis_state: ", axis_state)
                    if e_axis_state["title"] is not None and axis_state["title"] == e_axis_state["title"]:
                        axis_found = True
                        if not axis_state["sign"]:
                            e_tick_state["sign"] = not e_tick_state["sign"]
                        axis_state["ticks"].append(e_tick_state)
                        break
                for __id, entity in entity_dict.items():
                    print("---- entity: ", entity)
                if not axis_found:
                    print("axis not found: ", tick_entity["title"])
                    print('-- axis_state: ', e_axis_state)
                    print('-- tick_state: ', e_tick_state)
                    e_axis_state.update({
                        "ticks": [e_tick_state]
                    })
                    print('-- final_state: ', e_axis_state)
                    entity_dict[entity_id]['axis'].append(e_axis_state)
                else:
                    print("axis found: ", tick_entity["title"])

def search_for_axes(doc, axis_list):
    """Determine if each axis has been mentioned"""
    mentioned = False
    axes_info = []
    for axis_id, axis in enumerate(axis_list):
        # whether the axis title has been mentioned
        title_mentioned = False
        title_pos = None
        title_existed = False
        if axis.get("title") is not None:
            title_existed = True
            title_mentioned, title_pos = search_for_label(doc, axis["title"]["lemma"])
        # whether the axis tick + unit has been mentioned
        unit_mentioned = False
        unit_pos = None
        unit_existed = False
        if axis.get("unit") is not None:
            unit_existed = True
            unit_mentioned, unit_pos = search_for_label(doc, axis["unit"]["lemma"])
        # whether the tick values have been mentioned
        ticks = None
        ticks_mentioned = False
        ticks_existed = False
        if axis.get("ticks") is not None:
            ticks_existed = True
            ticks = []
            tick_mentioned = False
            tick_pos = None
            for tick_id, tick in enumerate(axis["ticks"]):
                tick_mentioned, tick_pos = search_for_label(doc, tick["lemma"])
                if tick_mentioned:
                    ticks_mentioned = True
                    ticks.append({
                        "id": tick_id,
                        "mentioned": tick_mentioned,
                        "locations": tick_pos,
                    })
        axis_mentioned = ticks_mentioned and (unit_mentioned or not unit_existed)
        axes_info.append({
            "mentioned": axis_mentioned,
            "id": axis_id,
            "title": {
                "existed": title_existed,
                "mentioned": title_mentioned,
                "locations": title_pos,
                },
            "unit": {
                "existed": unit_existed,
                "mentioned": unit_mentioned,
                "locations": unit_pos,
                },
            "ticks": {
                "existed": ticks_existed,
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
            if child.dep_ == "prep" and child.lemma_ == "of":
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

def match_units(tick_token, unit_lemmas):
    """The function for matching units"""
    num_token = tick_token
    unit_token = tick_token
    # Shift if the value is mentioned with the count and the unit
    if unit_lemmas:
        unit_match_count = 0
        temp_num = tick_token
        temp_unit = tick_token
        if tick_token.head.lemma_ == unit_lemmas[0]:
            head_token = tick_token
            num_stop = False
            for unit_lemma in unit_lemmas:
                if head_token.head.lemma_ == unit_lemma:
                    unit_match_count = unit_match_count + 1
                    # Pass on the num root and the unit root
                    if head_token.dep_ == "compound":
                        if not num_stop:
                            temp_num = head_token.head
                            temp_unit = temp_num
                        else:
                            temp_unit = head_token.head
                    if head_token.dep_ == "nummod":
                        num_stop = True
                        temp_unit = head_token.head
                    # Trace back
                    head_token = head_token.head
                else:
                    break
        # Successfully match
        if unit_match_count == len(unit_lemmas):
            num_token = temp_num
            unit_token = temp_unit
    return num_token, unit_token

def infer_ticks(tick_tokens, tick_text, title_to_entities, title_to_entities_all, unit_lemmas=None):
    """Infer the described entities via the axis ticks"""
    print('tick started')
    tick_locations = []
    entity_indices = []
    entity_signs = []
    entity_preps = []
    entity_conjs = []
    for tick_token in tick_tokens:
        tick_entities = []
        tick_signs = []
        std_prep = None
        v_token = None
        neg_sign = True
        conj_id = None
        num_token, unit_token = match_units(tick_token, unit_lemmas)
        tick_locations.append(unit_token.i)
        # Handle conjunction
        if unit_token.dep_ == "conj":
            head_token = unit_token.head
            while head_token.dep_ == "conj":
                head_token = head_token.head
            conj_id = head_token.i
        else:
            other_title = {
                "found": False,
                "location": None
            }
            # Find the standard prep and the verb token
            if unit_token.head.pos_ == "VERB":
                temp_v = unit_token.head
                than_found = False
                amod_found = False
                prep_lemma = None
                # Case: [verb] [more] [than] [tick] and [verb] [tick]
                for child in num_token.children:
                    if child.dep_ == "quantmod" and child.lemma_ == "than":
                        than_found = True
                    if child.dep_ == "amod" and child.tag_ == "JJR":
                        amod_found = True
                        prep_lemma = child.lemma_
                # Found the "[than]" but cannot find the "[more]"
                if than_found and not amod_found:
                    for child in temp_v.children:
                        if child.dep_ == "acomp" and child.tag_ == "JJR":
                            amod_found = True
                            prep_lemma = child.lemma_
                # Case: [verb] [more] [than] [tick]
                if than_found and amod_found:
                    std_prep = get_std_axis(prep_lemma)
                    if std_prep is not None:
                        std_found = True
                else:
                    # Case: [verb] [tick]
                    std_prep = get_std_axis('at')
                    std_found = True
                if std_found:
                    v_token = temp_v
                    neg_sign = get_negation(v_token)
            else:
                # Case: [verb] [prep] [tick] and [entities] [prep] [tick]
                if unit_token.dep_ == "pobj":
                    prep_token = unit_token.head
                    # Case: [prep] [than] [tick]
                    if prep_token.lemma_ == "than":
                        prep_token = prep_token.head
                    std_prep = get_std_axis(prep_token.lemma_)
                    if std_prep is not None:
                        v_token = prep_token.head
                    # Special Cases for 'in time' descriptions
                    if v_token is not None:
                        if v_token.lemma_ == "than":
                            v_token = v_token.head.head
                        if v_token.dep_ == "amod":
                            v_token = v_token.head
                        if v_token.dep_ == "attr" and v_token.head.pos_ == "VERB":
                            v_token = v_token.head.head
                        if v_token.dep_ == "pobj":
                            v_token = v_token.head.head
                            if v_token.dep_ == "acomp":
                                v_token = v_token.head
                        if v_token.dep_ == "dobj":
                            v_token = v_token.head
                        # Handle the case when other titles have been mentioned
                        if title_to_entities_all.get(v_token.i) is not None:
                            other_title["found"] = True
                            other_title["location"] = v_token.i
                    # Case: [verb] [prep] [tick]
                    if v_token is not None and v_token.pos_ == "VERB":
                        neg_sign = get_negation(v_token)
                    # Case: [entities] [prep] [tick] and [entities] [prep] [than] [tick]
                    else:
                        neg_sign = get_negation(prep_token)
            if std_prep is None or v_token is None:
                continue
            print("-- num token: ", num_token.lemma_)
            print("-- prep token: ", std_prep)
            print("-- verb token: ", v_token.lemma_)
            # Detect the entities
            if v_token.pos_ == "VERB":
                print("is VERB")
                while v_token.dep_ == "xcomp" and v_token.head.pos_ == "VERB":
                    v_token = v_token.head
                for child in v_token.children:
                    if child.dep_ == "nsubj":
                        # The entry token for entities
                        child_location = child.i
                        print("-- entity location: ", child_location)
                        print("-- title_to_entities: ", title_to_entities)
                        if title_to_entities.get(child_location) is None:
                            tick_entities, tick_signs = infer_entities(child, True)
                        else:
                            tick_entities = title_to_entities[child_location]
                            for tick_entity in tick_entities:
                                tick_signs.append(True)
            else:
                print("is not VERB")
                print(other_title)
                if other_title["found"]:
                    v_location = other_title["location"]
                    tick_entities = title_to_entities_all[v_location]
                    for tick_entity in tick_entities:
                        tick_signs.append(True)
                else:
                    v_location = v_token.i
                    if title_to_entities.get(v_location) is None:
                        tick_entities, tick_signs = infer_entities(v_token, False)
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
    print("-- entities", entity_indices)
    print('tick ended')
    return {
        "text": tick_text,
        "locations": tick_locations,
        "entities": entity_indices,
        "signs": entity_signs,
        "relations": entity_preps,
        "conjunctions": entity_conjs
    }

def get_negation(token):
    """Get the negation of some token"""
    sign = True
    for child in token.children:
        if child.dep_ == "neg":
            sign = False
            break
    return sign

def make_up_for_axis(entity_dict):
    """Make up for the missing axes"""
    print("make up started")
    axis_mention_list = {}
    id_to_entity = {}
    for entity_id, entity in entity_dict.items():
        e_id = int(entity_id.replace('entity_', ''))
        id_to_entity[e_id] = entity
        entity_axes = entity.get("axis")
        if entity_axes:
            for entity_axis in entity_axes:
                axis_title = entity_axis["title"]
            if axis_title is not None:
                if axis_mention_list.get(axis_title) is None:
                    axis_mention_list[axis_title] = [e_id]
                else:
                    axis_mention_list[axis_title].append(e_id)
    print("preparation ended")
    for e_id, entity in id_to_entity.items():
        entity_axes = entity.get("axis")
        if entity_axes is None:
            entity_axes = []
            entity["axis"] = entity_axes
        for axis_title, mentioned_ids in axis_mention_list.items():
            # If the axis is not mentioned with this entity
            if e_id not in mentioned_ids:
                min_dist = float('inf')
                min_id = None
                # Find the closest entity that has this axis
                for m_id in mentioned_ids:
                    dist = abs(m_id - e_id)
                    if dist < min_dist:
                        min_dist = dist
                        min_id = e_id
                # Copy the axis of the closest entity
                target_axes = id_to_entity[min_id]["axis"]
                for axis in target_axes.values():
                    if axis["title"] == axis_title:
                        entity_axes.append(copy.deepcopy(axis))
