
from command import *
from env import *
import types

# Returns a pickle serialized Command from a file 
def dump_from_path(path: str):
	c = None
	if path in sys.modules:
		c = sys.modules[path]
	else:
		c = __import__(path, fromlist = [path])
	
	arguments = {
		'name': c.name,
		'syns': c.syns,
		'desc': c.desc,
		'priv': c.priv,
		'fail_on_dedicated_keyword': c.fail_on_dedicated_keyword,
		}
	
	return (dump_method(types.FunctionType(c.effect.__code__,{})), arguments)

def serialize_commands():
	command_list = {}
	for filename in os.listdir(command_dir):
		f = os.path.join(command_dir, filename)
		if os.path.isfile(f) and f.endswith('.py'):
			dump = None
			arguments = None
			#try:
			dump, arguments = dump_from_path(filename[0:-3])
			#except:
			#	continue
			command_list[arguments['name']] = {'args': arguments, 'dump': bytes.decode(dump, 'latin')}
	
	#for key in command_list:
	#	reloaded = dill.loads(bytes(command_list[key]['dump'], 'latin'))
	#	reloaded(None, message_text='abc')
	print(JSON.dumps(command_list))
	f = open(commands_file, 'w')
	JSON.dump(command_list, f, indent=4)

serialize_commands()