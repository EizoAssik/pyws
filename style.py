# encoding=utf-8
"""
Use these dicts to make pyws works on different notations of WhiteSpace.
"""

ORIGIN = {' ': 'S', '\t': 'T', '\n': 'L'}
STL = {'S': 'S', 'T': 'T', 'L': 'L'}
GMH = {'草': 'S', '泥': 'T', '马': 'L'}