"""The dictionary for units"""

UNIT_STANDARD = [
    # percentage
    'percent',
    # currency
    'dollar',
    'euro',
    'yuan',
    'yen',
    # length
    'meter',
    'decimetre',
    'centimetre',
    'millimetre',
    'micrometre',
    'nanometre',
    'kilometre'
]

UNIT_FULL = {
    # percentage
    '%': 0,
    'percent': 0,
    # currency
    '$': 1,
    'dollar': 1,
    '€': 2,
    'euro': 2,
    '¥': [3, 4],
    'yuan': 3,
    'yen': 4,
    # length
    'm': 5,
    'meter': 5,
    'metre': 5,
    'dm': 6,
    'decimeter': 6,
    'decimetre': 6,
    'cm': 7,
    'centimeter': 7,
    'centimetre': 7,
    'mm': 8,
    'millimeter': 8,
    'millimetre': 8,
    'μm': 9,
    'micrometer': 9,
    'micrometre': 9,
    'nm': 10,
    'nanometer': 10,
    'nanometre': 10,
    'km': 11,
    'kilometer': 11,
    'kilometre': 11
}
