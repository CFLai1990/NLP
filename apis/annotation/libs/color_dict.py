"""The dictionary for colors"""

def get_std_color(color_text):
    """Get the standard color by its text"""
    std_color = None
    # Find the color in the full dictionary
    color_code = COLOR_FULL.get(color_text)
    if color_code is not None:
        std_color = COLOR_STANDARD[color_code]
    return std_color

COLOR_STANDARD = [
    'black',
    'gray',
    'white',
    'red',
    'orange',
    'brown',
    'yellow',
    'green',
    'blue',
    'purple',
    'pink',
]

COLOR_FULL = {
    'black': 0,
    'gray': 1,
    'grey': 1,
    'white': 2,
    'red': 3,
    'orange': 4,
    'brown': 5,
    'yellow': 6,
    'green': 7,
    'blue': 8,
    'purple': 9,
    'pink': 10,
}
