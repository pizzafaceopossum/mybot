
from listener import *

my_listener: Listener = Listener()

def my_custom_function(self, name1, name2, name3, message_type, message_channel, message_text):
	print(f'Type: {message_type}, Channel: {message_channel}, Username: {name1}, Message: {message_text}')
	print(self.channel)
	if not message_text == 'test':
		self.socket.send(f'PRIVMSG {self.channel} :test\n'.encode('utf-8'))
my_listener.do_on_chat_message = my_custom_function

my_listener.open_connection()