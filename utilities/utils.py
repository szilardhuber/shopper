import json

def to_JSON(vect):
    ret = ''
    ret += '['
    first = True 
    for item in vect:
        import logging
        logging.info('Adding item: ' + dir(item))
        if not first:
	    ret += ', '
        else:
            first = False
        try:
	    ret += json.dumps(item.to_dict())
        except AttributeError:
	    ret += json.dumps(item)
    ret += ']'
    return ret
