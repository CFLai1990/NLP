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
    # y_location - top
    'top': 1,
    # y_location - top
    'bottom': 2,
    # x_location - left
    'left': 3,
    'leftmost': 3,
    # x_location - right
    'right': 4,
    'rightmost': 4,
}
