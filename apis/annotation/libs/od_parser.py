"""The module for parsing results from Object Detection"""
import json
from .color_dict import get_std_color

class SpacyLabel:
    """The class for labels"""
    def __init__(self, model):
        self.model = model

    def get_data(self, label_text=None):
        """The function for parsing the text and getting the data result"""
        data = {
            "text": label_text,
            "lemma": [],
            "root": None
        }
        if label_text is not None:
            doc = self.model(label_text)
            for token in doc:
                data["lemma"].append(token.lemma_)
                if token.dep_ == "ROOT":
                    data["root"] = token.i
        return data

class ODParser:
    """The class for data parsing"""
    def __init__(self, file_op, model=None):
        self.file_op = file_op
        self.model = model
        self.data = None
        self.label_parser = SpacyLabel(model)

    def parse_axis_label(self, labels):
        """The function for parsing the axis label"""
        title = None
        unit = None
        if labels is not None:
            for label in labels:
                left_brc = label.find("(")
                right_brc = label.find(")")
                if left_brc >= 0 and right_brc >= 0:
                    # The unit does exist
                    # Case 1: "[title] ([unit])"
                    if title is None and left_brc > 0:
                        title = {}
                        title_text = label[0:left_brc]
                        if title_text[len(title_text)-1] == ' ':
                            title["text"] = label[0:left_brc-1]
                        else:
                            title["text"] = title_text
                        title["lemma"] = []
                        title["root"] = None
                    unit = {}
                    unit["text"] = label[(left_brc+1):right_brc]
                    unit["lemma"] = []
                    unit["root"] = None
                else:
                    # The unit does not exist
                    # or Case 2: "[title] \n ([units])"
                    if title is None:
                        title = {}
                        title["text"] = label
                        title["lemma"] = []
                        title["root"] = None
            # Assume the "labels" list contains only one title and one unit
            if unit is not None:
                # Get the unit
                unit_doc = self.model(unit["text"])
                for unit_id, unit_token in enumerate(unit_doc):
                    if unit_token.pos_ == "NOUN" or unit_token.pos_ == "SYM":
                        unit["lemma"].append(unit_token.lemma_)
                    if unit_token.dep_ == "ROOT":
                        unit["root"] = unit_id
            if title is not None:
                # Get the title
                title_doc = self.model(title["text"])
                for title_id, title_token in enumerate(title_doc):
                    title["lemma"].append(title_token.lemma_)
                    if title_token.dep_ == "ROOT":
                        title["root"] = title_id
        return title, unit

    def parse_axis_ticks(self, tick_list=None):
        """The function for parsing the axis ticks"""
        ticks = None
        if tick_list is not None:
            ticks = []
            for tick_text in tick_list:
                tick = self.label_parser.get_data(tick_text)
                ticks.append(tick)
        return ticks

    def parse_legend_label(self, label_text=None):
        """The function for parsing legends"""
        label = None
        print("label_text: ", label_text)
        if label_text is not None:
            label = self.label_parser.get_data(label_text)
        return label

    def parse_data_label(self, data_labels=None):
        """The function for parsing legends"""
        labels = None
        if data_labels:
            labels = []
            for data_label in data_labels:
                label_result = self.label_parser.get_data(data_label)
                labels.append(label_result)
        return labels

    def parse_legend_feature(self, feature_dict):
        """The function for parsing the legend features"""
        feature = None
        if feature_dict is not None:
            feature = {}
            for feature_name, feature_value in feature_dict.items():
                if feature_name == "color":
                    std_color = get_std_color(feature_value)
                    if std_color is not None:
                        feature["color"] = std_color
        return feature

    def parse(self, data):
        """The function for parsing the OD data"""
        # Initialize
        results = {
            "labels": None,
            "axes": None,
            "legends": None,
        }
        # Pack the results
        if data is not None:
            # Parse the labels
            print("labels")
            results["labels"] = self.parse_data_label(data.get("labels"))
            # Parse the axes
            if data.get("axes") is not None:
                axes = []
                for axis in data["axes"]:
                    print("axes")
                    axis_title, axis_unit = self.parse_axis_label(axis.get("label"))
                    axis_ticks = self.parse_axis_ticks(axis.get("ticks"))
                    axes.append({
                        "title": axis_title,
                        "unit": axis_unit,
                        "ticks": axis_ticks
                    })
                results["axes"] = axes
            # Parse the legends
            if data.get("legends") is not None:
                legends = []
                for legend in data["legends"]:
                    print("legends")
                    legend_label = self.parse_legend_label(legend.get("label"))
                    legend_feature = self.parse_legend_feature(legend.get("feature"))
                    legends.append({
                        "label": legend_label,
                        "feature": legend_feature
                    })
                results["legends"] = legends
        self.data = results

    def save(self, path, data=None):
        """The function for saving the OD data"""
        self.parse(data)
        data_path = self.file_op.get_path(path)
        with open(data_path, 'w') as file:
            json.dump(self.data, file)
            file.close()
        return True

    def load(self, path):
        """The function for loading the OD data"""
        od_data = None
        data_path = self.file_op.get_path(path)
        if self.file_op.exists(data_path):
            with open(data_path, 'r') as file:
                od_data = json.load(file)
                file.close()
        return od_data
