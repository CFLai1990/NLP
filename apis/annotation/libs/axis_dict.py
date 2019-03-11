"""The dictionaries for describing axis-based locations"""

def get_std_axis(axis_text):
    """Get the standard color by its text"""
    std_axis = None
    # Find the color in the full dictionary
    loc_code = AXIS_FULL.get(axis_text)
    if loc_code is not None:
        std_axis = AXIS_STANDARD[loc_code]
    return std_axis

AXIS_STANDARD = [
    'at',
    'above',
    'below',
    'between',
    'after',
    'before',
    'from_to',
]

AXIS_FULL = {
    # at
    'at': 0,
    'during': 0,
    'in': 0,
    'within': 0,
    'to': 0,
    # above
    'above': 1,
    'over': 1,
    'beyond': 1,
    'high': 1,
    'more': 1,
    # below
    'below': 2,
    'under': 2,
    'low': 2,
    'less': 2,
    # between
    'between': 3,
    # after
    'after': 4,
    # before
    'before': 5,
    # from to
    'from': 6,
}
