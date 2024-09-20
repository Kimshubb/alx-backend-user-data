#!/usr/bin/env python3
'''personal data protection module
'''
import re

def filter_datum(fields, redaction, message, separator):
    pattern = '|'.join([f'{field}=[^"{separator}]*' for field in fields])
    return re.sub(pattern, lambda match: re.sub('=[^"{separator}]*', f'={redaction}', match.group()), message)
