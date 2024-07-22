
from listener import *
from command import *
import sys
sys.path.append('./commands/')
import importlib

class CommandListener(Listener):
	def __init__(self, **kwargs):
		super().__init__()
		self.registered_commands: dict = {}
	
	def register_command(self, path: str) -> bool:
		command_module = None
		if path in sys.modules:
			command_module = sys.modules[path]
		else:
			command_module = __import__(path, fromlist = [path])
		
		command = Command(name=command_module.name, description=command_module.description, synonyms=command_module.synonyms, fail_on_dedicated_keyword=command_module.fail_on_dedicated_keyword)
		command.effect = command_module.effect
		for alias in command.synonyms:
			if alias in self.registered_commands:
				# At least one of the aliases for the command is already registered.
				return False
		for alias in command.synonyms:
			self.registered_commands[alias] = command
		self.registered_commands[command_module.name.upper()] = command
		return True
	
	def unregister_command(path: str) -> bool:
		command_module = None
		if path in sys.modules:
			command_module = sys.modules[path]
		else:
			command_module = __import__(path, fromlist = [path])
		command = None
		if command_module.name.upper() in self.registered_commands:
			command = self.registered_commands[command_module.name.upper()]
		else:
			return False
		for alias in command.synonyms:
			del self.registered_commands[alias]
		del command
		return True
	
	def do_on_chat_message(self, *args, **kwargs):
		parsed_message = kwargs.get('message_text', '').split()
		print(f'Type: {kwargs.get('message_type', '')}, Channel: {kwargs.get('message_channel', '')}, Username: {kwargs.get('name1', '')}, Message: {kwargs.get('message_text', '')}')
		print(parsed_message)
		if len(parsed_message) > 0 and parsed_message[0].lower() in self.registered_commands:
			message_args = []
			message_kwargs = {}
			unique_kwargs = False
			for chat_argument in parsed_message[1:]:
				parsed_chat_argument = chat_argument.split('=')
				if len(parsed_chat_argument) > 1 and parsed_chat_argument[0] not in kwargs and parsed_chat_argument[0] not in message_kwargs:
					message_kwargs[parsed_chat_argument[0]] = parsed_chat_argument[1]
					unique_kwargs = True
				elif len(parsed_chat_argument) == 1:
					message_args.append(parsed_chat_argument[0])
				elif self.registered_commands[parsed_message[0]].fail_on_dedicated_keyword:
					print(f'Command \'{self.registered_commands[parsed_message[0]].name}\' failed because a dedicated keyword was used or a keyword argument was repeated.')
					return None
			message_kwargs.update(kwargs)
			if len(message_args) > 0 and not unique_kwargs and (message_args[0].lower() == 'help'):
				self.send_message(self.registered_commands[parsed_message[0]])
			else:
				print(f'Command \'{self.registered_commands[parsed_message[0]].name}\' executed.')
				self.registered_commands[parsed_message[0]].effect(self, *message_args, **message_kwargs)

my_listener: CommandListener = CommandListener()

my_listener.register_command('example')
my_listener.open_connection()