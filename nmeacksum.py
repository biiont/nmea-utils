#!/usr/bin/env python3

### TODO: Add option to calc checksum with '$' and '*' symbols and without (some implementations do break standard).
### TODO: Add option to read checksums from multiple files.
### TODO: Add mode to check one sentence (either cmdline or stdin or file) and return appropriate error code.
### TODO: Add mode to filter NMEA sentences by their checksum.

from __future__ import generators

import argparse
from functools import reduce
from operator import xor
from sys import stdin

def checksum_xor_8bit(data) :
    """ Calculates checksum XORing all passed symbols.
    
    Sutable for checksumming NMEA sentences. In this case pass NMEA sentence string without '$' and '*hh<CR><LF>' parts.
    """
    return reduce(lambda a, b: a ^ b, (ord(c) for c in data))

def strip_nmea_sentence(sentence) :
    """ Strip NMEA sentence from '$', '*' and checksum."""
    asterisk_idx = sentence.rfind('*')
    return sentence[0:asterisk_idx].lstrip('$')

def calculate_nmea_checksum(sentence) :
    return checksum_xor_8bit(strip_nmea_sentence(sentence))

def fix_nmea_checksum(sentence) :
    sentence = strip_nmea_sentence(sentence)
    return '${}*{:02X}\r\n'.format(sentence, checksum_xor_8bit(sentence))

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Calculate checksum for NMEA sentence.')
    parser.add_argument('--version', action='version', version='0.1')
    parser.add_argument('sentences', help='Quoted NMEA sentences with or without <CR><LF>, "$", "*".',
                        metavar="'NMEA'", nargs='*')
    args = parser.parse_args()

    sentences = args.sentences if len(args.sentences) > 0 else (line for line in stdin)

    try:
        for sentence in sentences :
            print(fix_nmea_checksum(sentence))
    except (KeyboardInterrupt, SystemExit):
        pass
