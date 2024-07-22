
name = 'Example'
description = 'This is an example command for development purposes. Displays the arguments and keyword arguments used.'
privileges = 0b11111
synonyms = ('test',)
fail_on_dedicated_keyword = False

def effect(self, *args, **kwargs):
	#chatstring = ''
	printstring = ''
	for i in range(len(args)):
		#chatstring += f'args[{i}] = {args[i]}, \t'
		printstring += f'args[{i}] = {args[i]}\n'
	for kwarg in kwargs:
		#chatstring += f'kwargs[{kwarg}] = {kwargs[kwarg]}, \t'
		printstring += f'kwargs[{kwarg}] = {kwargs[kwarg]}\n'
	#self.send_message(chatstring)
	print(printstring)