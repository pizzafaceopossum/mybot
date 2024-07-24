
from env import *

def func(self, *args, **kwargs):
	return kwargs['x']+5

def dump_method(method):
	dump = dill.dumps(method, recurse=True)
	replacement_bytes = b'?'*len(command.effect.__code__.co_filename)
	replaced_dump = re.sub(bytes(r'\??' + command.effect.__code__.co_filename, 'utf-8'), replacement_bytes, dump)
	return set_bytes(replaced_dump, 3, (len(replaced_dump) - 11).to_bytes(8, 'little'))