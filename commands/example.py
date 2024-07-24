
name = 'Example'
syns = ['test']
desc = 'This is an example command for development purposes. Displays the arguments and keyword arguments used.'
priv = 0b11111
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