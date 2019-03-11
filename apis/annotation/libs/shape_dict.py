"""The dictionary for shapes"""

def get_std_shape(shape_text):
    """Get the standard shape by its text"""
    std_shape = None
    # Find the shape in the full dictionary
    shape_code = SHAPE_FULL.get(shape_text)
    if shape_code is not None:
        std_shape = SHAPE_STANDARD[shape_code]
    return std_shape

SHAPE_STANDARD = [
    'line',
    'circle',
    'rectangle',
    'sector',
]

SHAPE_FULL = {
    # line
    'line': 0,
    'polyline': 0,
    # circle
    'circle': 1,
    'point': 1,
    # rectangle
    'rectangle': 2,
    'bar': 2,
    # sector
    'sector': 3,
    'pie': 3,
}
