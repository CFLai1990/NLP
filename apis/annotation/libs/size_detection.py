"""The function for detecting size descriptions"""
from .size_dict import get_std_size
from .entity_detection import infer_entities

def infer_size(doc, entity_dict):
	"""Size detection function"""
	size_indices = []

	for t_id, token in enumerate(doc):
		original_text = token.lemma_
		# Identify the valid size words
		std_size = get_std_size(original_text)
		if std_size is None:
			continue
		size_indices.append(t_id)
		indices = []
		signs = []
		if token.pos_ == 'ADJ':
			indices, signs = infer_adj_size(token)
		for _id, e_token_index in enumerate(indices):
			entity_id = 'entity_' + str(e_token_index)
			size_sign = signs[_id]
			if not entity_dict.get(entity_id):
				e_token = doc[e_token_index]
				entity_dict[entity_id] = {
					'name': e_token.lemma_,
					'size': {
						std_size: size_sign
					}
				}
			else:
				if not entity_dict[entity_id]['size']:
					entity_dict[entity_id]['size'] = {
						std_size: size_sign
					}
				else:
					entity_dict[entity_id]['size'].update({
						std_size: size_sign
						})

def infer_adj_size(token):
	"""Infer the entities when the size is an ADJ"""
	# Case 1: [size] [entities]
	if token.dep_ == 'amod':
		indices, signs = infer_adj_size_amod(token)
		return indices, signs
	# Case 2: [entities] [be] [size]
	if token.dep_ == 'acomp' and token.head.lemma_ == 'be':
		v_token = token.head
		return infer_adj_size_subjects(v_token, True)
	return [], []


def infer_adj_size_amod(token):
	"""infer function for adj_case 1"""
	entity_indices = [token.head.i]
	entity_signs = [True]
	return entity_indices, entity_signs


def infer_adj_size_subjects(token, be_verb=False):
	"""infer function for adj_case 2"""
	entity_indices = []
	entity_signs = []
	if token.children:
		for child in token.children:
			if be_verb and child.dep_ == 'nsubj':
				entities, signs = infer_entities(child, True)
				entity_indices.extend(entities)
				entity_signs.extend(signs)
			# handle negation
			if child.dep_ == "neg":
				for index, e_sign in enumerate(entity_signs):
					entity_signs[index] = not e_sign
	return entity_indices, entity_signs

