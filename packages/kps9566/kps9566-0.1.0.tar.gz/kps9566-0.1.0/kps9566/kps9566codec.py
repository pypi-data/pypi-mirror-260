import codecs
from itertools import count
from .kps9566map import *
from .compat_map import *

def kps9566_encode(input_, errors='strict'):
    for k, v in list(CJK_COMPAT_MAP.items())+list(KPS9566ALTERNATIVES.items()):
        input_ = input_.replace(k, v)
    buffer = bytearray()
    for i, it in zip(count(0), input_):
        if 0x00 <= ord(it) <= 0x7f:
            buffer.append(ord(it))
        elif it in KPS9566MAP:
            index = KPS9566MAP.index(it)
            rowindex = index // len(KPS9566COL)
            colindex = index % len(KPS9566COL)
            buffer.append(KPS9566ROW[rowindex])
            buffer.append(KPS9566COL[colindex])
        else:
            if errors == 'strict':
                raise UnicodeEncodeError('kps9566', input_, i, i+1, 'invalid character')
            elif errors == 'ignore':
                pass
            elif errors == 'replace':
                buffer.append(ord('?'))
            else:
                raise UnicodeError('kps9566', input_, i, i+1, 'unknown error')
    return bytes(buffer), len(input_)

def kps9566_decode(input_, errors='strict'):
    buffer = []
    charlen = 0
    last = 0
    flag = False
    for i, it in zip(count(0), input_):
        if flag:
            if last in KPS9566ROW and it in KPS9566COL:
                rowindex = KPS9566ROW.index(last)
                colindex = KPS9566COL.index(it)
                char = KPS9566MAP[rowindex*len(KPS9566COL)+colindex]
                if char == '?':
                    if errors == 'strict':
                        raise UnicodeDecodeError('kps9566', input_, i, i+1, 'invalid kps9566 code')
                    elif errors == 'ignore':
                        pass
                    elif errors == 'replace':
                        buffer.append('\uFFFD')
                    else:
                        raise UnicodeError('kps9566', input_, i, i+1, 'unknown error')
                else:
                    buffer.append(char)
                charlen += 1
                flag = False
            else:
                if errors == 'strict':
                    raise UnicodeDecodeError('kps9566', input_, i, i+1, 'invalid kps9566 code')
                elif errors == 'ignore':
                    pass
                elif errors == 'replace':
                    buffer.append('\uFFFD')
                else:
                    raise UnicodeError('kps9566', input_, i, i+1, 'unknown error')
        elif 0x00 <= it <= 0x7f:
            buffer.append(chr(it))
            flag = False
            charlen += 1
        elif 0x80 <= it <= 0xff:
            flag = True
        last = it
    return ''.join(buffer), len(input_)


class Kps9566StreamWriter(codecs.StreamWriter):
    encode = lambda self, input_, errors='strict': kps9566_encode(input_, errors)

class Kps9566StreamReader(codecs.StreamReader):
    decode = lambda self, input_, errors='strict': kps9566_decode(input_, errors)

class Kps9566IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input_, final=False):
        return kps9566_encode(input_, self.errors)[0]

class Kps9566IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input_, final=False):
        return kps9566_decode(input_, self.errors)[0]



def getregentry():
    return codecs.CodecInfo(
        name='kps9566',
        encode=kps9566_encode,
        decode=kps9566_decode,
        streamreader=Kps9566StreamReader,
        streamwriter=Kps9566StreamWriter,
        incrementalencoder=Kps9566IncrementalEncoder,
        incrementaldecoder=Kps9566IncrementalDecoder,
    )


def kps9566_search_function(encoding):
    if encoding.upper() == 'KPS9566' or encoding == 'KPS-9566' or encoding == 'KPS_9566' or encoding == 'KPS 9566':
        return getregentry()
    return None

def register():
    codecs.register(kps9566_search_function)
