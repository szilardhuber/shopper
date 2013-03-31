import json

def to_JSON(vect):
	ret = ''
	ret += '['
	first = True 
	for item in vect:
		if not first:
			ret += ', '
		else:
			first = False
		ret += json.dumps(item.to_dict())
	ret += ']'
	return ret
