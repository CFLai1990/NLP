"""The dictionaries for location words"""

def get_std_loc(loc_text):
    """Get the standard color by its text"""
    std_loc = None
    # Find the color in the full dictionary
    loc_code = LOCATION_FULL.get(loc_text)
    if loc_code is not None:
        std_loc = LOCATION_STANDARD[loc_code]
    return std_loc


LOCATION_STANDARD = [
    # middle
    'middle',
    # axis_location
    'high',
    'low',
    # y_location
    'top',
    'bottom',
    # x_location
    'left',
    'right',
]

LOCATION_FULL = {
    # middle
    'middle': 0,
    # axis_location - high
    'high': 1,
    # axis_location - low
    'low': 2,
    # y_location - top
    'top': 3,
    # y_location - top
    'bottom': 4,
    # x_location - left
    'left': 5,
    'leftmost': 5,
    # x_location - right
    'right': 6,
    'rightmost': 6,
}
