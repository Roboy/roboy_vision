import numpy

def _serialize(self, buff):
    return self.serialize_numpy(buff, numpy)

def _deserialize(self, str):
    return self.deserialize_numpy(str, numpy)

_numpy_msg_types = {}
def numpy_msg(msg_type):
    if msg_type in _numpy_msg_types:
        return _numpy_msg_types[msg_type]

    classdict = { '__slots__': msg_type.__slots__, '_slot_types': msg_type._slot_types,
        '_md5sum': msg_type._md5sum, '_type': msg_type._type,
        '_has_header': msg_type._has_header, '_full_text': msg_type._full_text,
        'serialize': _serialize, 'deserialize': _deserialize,
        'serialize_numpy': msg_type.serialize_numpy,
        'deserialize_numpy': msg_type.deserialize_numpy
    }

    msg_type_name = "Numpy_%s"%msg_type._type.replace('/', '__')
    numpy_type = type(msg_type_name,(msg_type,),classdict)
    _numpy_msg_types[msg_type] = numpy_type
    return numpy_type

