"""The module for parsing results from Object Detection"""
import json
from .color_dict import get_std_color

class ODParser:
    """The class for data parsing"""
    def __init__(self, file_op, model=None):
        self.file_op = file_op
        self.model = model
        self.data = None

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
                        title["text"] = label[0:left_brc]
                        title["lemma"] = []
                    unit = {}
                    unit["text"] = label[(left_brc+1):right_brc]
                    unit["lemma"] = []
                else:
                    # The unit does not exist
                    # or Case 2: "[title] \n ([units])"
                    if title is None:
                        title = {}
                        title["text"] = label
                        title["lemma"] = []
            # Assume the "labels" list contains only one title and one unit
            if unit is not None:
                # Get the unit
                unit_doc = self.model(unit["text"])
                for unit_token in unit_doc:
                    if unit_token.pos_ == "NOUN" or unit_token.pos_ == "SYM":
                        unit["lemma"].append(unit_token.lemma_)
            if title is not None:
                # Get the title
                title_doc = self.model(title["text"])
                for title_token in title_doc:
                    title["lemma"].append(title_token.lemma_)
        return title, unit

    def parse_axis_ticks(self, tick_list):
        """The function for parsing the axis ticks"""
        ticks = None
        if tick_list is not None:
            ticks = []
            for tick_text in tick_list:
                tick = {}
                tick["text"] = tick_text
                ticks.append(tick)
        return ticks

    def parse_legend_label(self, label_list):
        """The function for parsing legends"""
        label = None
        if label_list is not None:
            label = {
                "text": None,
                "lemma": []
            }
            # Assume the "labels" list contains only one category name
            for label_text in label_list:
                label["text"] = label_text
                label_doc = self.model(label_text)
                for label_token in label_doc:
                    label["lemma"].append(label_token.lemma_)
        return label

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
            if data.get("labels") is not None:
                results["labels"] = data["labels"]
            else:
                results["labels"] = []
            # Parse the axes
            if data.get("axes") is not None:
                axes = []
                for axis in data["axes"]:
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
