
from listener import *
from command import *

class CommandListener(Listener):
	def __init__(self, **kwargs):
		super().__init__()
		self.registered_commands = {}
		f = open(commands_file, 'r')
		command_list = JSON.load(f)
		for name in command_list:
			command = Command(**command_list[name]['args'])
			command.effect = dill.loads(bytes(command_list[name]['dump'], 'latin'))
			self.register_command(command)
	
	def register_command(self, command) -> bool:
		for alias in command.syns:
			if alias in self.registered_commands:
				# At least one of the aliases for the command is already registered.
				return False
		for alias in command.syns:
			self.registered_commands[alias] = command
		self.registered_commands[command.name.upper()] = command
		return True
	
	def unregister_command(self, name: str) -> bool:
		name = name.upper()
		command = None
		if name in self.registered_commands:
			command = self.registered_commands[name]
		else:
			return False
		for alias in command.syns:
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
my_listener.open_connection()