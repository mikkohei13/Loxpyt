"""
WAMD data conversions done using code adapted from 'guano-py'

https://github.com/riggsd/guano-py

The MIT License (MIT)

Copyright (c)2015-2017 Myotisoft LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import chunk
import struct
from pprint import pprint
import datetime

# binary WAMD field identifiers
WAMD_IDS = {
    0x00: 'version',
    0x01: 'model',
    0x02: 'serial',
    0x03: 'firmware',
    0x04: 'prefix',
    0x05: 'timestamp',
    0x06: 'gpsfirst',
    0x07: 'gpstrack',
    0x08: 'software',
    0x09: 'license',
    0x0A: 'notes',
    0x0B: 'auto_id',
    0x0C: 'manual_id',
    0x0D: 'voicenotes',
    0x0E: 'auto_id_stats',
    0x0F: 'time_expansion',
    0x10: 'program',
    0x11: 'runstate',
    0x12: 'microphone',
    0x13: 'sensitivity',
}

# fields that we exclude from our in-memory representation
WAMD_DROP_IDS = (
    0x0D,    # voice note embedded .WAV
    0x10,    # program binary
    0x11,    # runstate giant binary blob
    0xFFFF,  # used for 16-bit alignment
)

# rules to coerce values from binary string to native types (default is `str`)
WAMD_COERCE = {
    'version': lambda x: struct.unpack('<H', x)[0],
    'timestamp': lambda x: (x),
    'gpsfirst': lambda x: _parse_wamd_gps(x),
    'time_expansion': lambda x: struct.unpack('<H', x)[0],
}


def _parse_text(value):
    """Default coercion function which assumes text is UTF-8 encoded"""
    return value.decode('utf-8')


def stringifyKeys(dict):
    stringifiedDict = {}
    for key, value in dict.items():
        stringifiedDict[str(key)] = value

    return stringifiedDict


def wamd(fname):
    """Extract WAMD metadata from a .WAV file as a dict"""
    with open(fname, 'rb') as f:
        ch = chunk.Chunk(f, bigendian=False)
        if ch.getname() != b'RIFF':
            raise Exception('%s is not a RIFF file!' % fname)
        if ch.read(4) != b'WAVE':
            raise Exception('%s is not a WAVE file!' % fname)

        wamd_chunk = None
        while True:
            try:
                subch = chunk.Chunk(ch, bigendian=False)
            except EOFError:
                break
            if subch.getname() == b'wamd':
                wamd_chunk = subch
                break
            else:
                subch.skip()
        if not wamd_chunk:
            raise Exception('"wamd" WAV chunk not found in file %s' % fname)

        metadata = {}
        offset = 0
        size = wamd_chunk.getsize()
        buf = wamd_chunk.read(size)
        while offset < size:
            id = struct.unpack_from('< H', buf, offset)[0]
            len = struct.unpack_from('< I', buf, offset+2)[0]
            val = struct.unpack_from('< %ds' % len, buf, offset+6)[0]
            if id not in WAMD_DROP_IDS:
                name = WAMD_IDS.get(id, id)
                val = WAMD_COERCE.get(name, _parse_text)(val)
                metadata[name] = val
            offset += 6 + len
        
        metadata = stringifyKeys(metadata)

        return metadata

