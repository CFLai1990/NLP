"""The dictionary for relationships"""

def get_relation(keyword):
    """Get the sign of the keyword"""
    sign = RELATION_FULL.get(keyword)
    if sign is None:
        sign = True
    return sign

RELATION_FULL = {
    'both': True,
    'all': True,
    'neither': False,
    'none': False
}
