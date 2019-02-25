"""The dictionaries for size words"""

def get_std_size(size_text):
    """Get the standard color by its text"""
    std_size = None
    # Find the color in the full dictionary
    size_code = SIZE_FULL.get(size_text)
    if size_code is not None:
        std_size = SIZE_STANDARD[size_code]
    return std_size

SIZE_STANDARD = [
    # area
    'large',
    'small',
    # y_range and length/height
    'long',
    'short',
    # x_range and width
    'wide',
    'narrow',
    # z_range and depth
    'deep',
    'shallow'
]

SIZE_FULL = {
    # area - large
    'large': 0,
    'big': 0,
    'huge': 0,
    'giant': 0,
    # area - small
    'small': 1,
    'tiny': 1,
    'little': 1,
    # y_range/length - long
    'long': 2,
    'tall': 2,
    # y_range/length - short
    'short': 3,
    # x_range/width - wide
    'wide': 4,
    'thick': 4,
    'broad': 4,
    'fat': 4,
    # x_range/width - narrow
    'narrow': 5,
    'thin': 5,
    # z_range/depth - deep
    'deep': 6,
    # z_range/depth - shallow
    'shallow': 7
}
