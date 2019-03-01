"""The function for detecting the description of visible labels"""

def infer_label(sentence, label_dict, visible_labels):
    """Label detection function"""
    st_lower = sentence.lower()
    if visible_labels is not None:
        for label in visible_labels:
            label_lower = label.lower()
            index = st_lower.find(label_lower)
            if index >= 0:
                if label_dict.get(label) is None:
                    label_dict[label] = {
                        'positions': [index]
                    }
                else:
                    label_dict[label]['positions'].push(index)
