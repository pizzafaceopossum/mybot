
from env import *
import socket # For opening and holding a connection to the chat server
import threading # For using a separate thread so that chat can be constantly listened to while executing commands, etc.

# Listener class.
# Opens and retains a connection to an irc-based chat service.

class Listener(object):
	def __init__(self, **kwargs):
		# Login/authentication details and server details.
		defaults = JSON.loads(open('.auth/auths.json', 'r').read())
		try:
			self.server: str = kwargs.get('server', defaults['server'])
			self.port: int = kwargs.get('port', defaults['port'])
			self.identity: str = kwargs.get('identity', defaults['identity'])
			self.host: str = kwargs.get('host', defaults['host'])
			self.username: str = kwargs.get('username', defaults['username'])
			self.token: str = kwargs.get('token', defaults['token'])
			self.channel: str = kwargs.get('channel', defaults['channel'])
		except Exception as e:
			print(f'{type(e).__name__}: auths.json does not have key \'{e.args[0]}\'')
			exit()
		self.socket: socket.socket = socket.socket()
		self.listening = True
		self.thread: threading.Thread = threading.Thread(target=self.listen)
	
	# Info used when printing.
	def __str__(self) -> str:
		string: str = f"Listener set to {self.server}:{self.port}. "
		if self.listening:
			return string + "Currently listening."
		else:
			return string + "Not currently listening."
	
	# Opens the connection to the chat server.
	def open_connection(self) -> None:
		self.socket.connect((self.server, self.port))
		#self.send(f'CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands')
		self.send(f'PASS oauth:{self.token}')
		self.send(f'NICK {self.username}')
		self.send(f'USER {self.identity} {self.host} bla :{self.username}\r')
		self.send(f'JOIN {self.channel}')
		self.thread.start()
	
	# Shortens further code. All messages need to be sent with an ending newline and encoded anyway.
	def send(self, message_text):
		self.socket.send((message_text + '\n').encode('utf-8'))
	
	# Listening loop.
	def listen(self) -> None:
		while self.listening:
			raw_message: str = self.socket.recv(2048).decode('utf-8')
			
			# Respond to twitch's occasional pinging message.
			if raw_message.startswith('PING'):
				print("Pinged")
				self.sendUTF("PONG")
				continue
			
			# Slice up recieved twitch messages (currently not sure of any difference in the various name displays)
			name1, name2, name3, message_type, message_channel, message_text = ('', '', '', '', '', raw_message)
			regex_groups = re.search('^:(.+?)!(.+?)@(.+?).tmi.twitch.tv (.+?) (#.+?) :(.*)$', raw_message)
			
			# If the recieved message can be sliced up as described, it's a normal message. Execute commands, etc.
			if regex_groups:
				name1, name2, name3, message_type, message_channel, message_text = regex_groups.groups()
				self.do_on_chat_message(self, name1=name1, name2=name2, name3=name3, message_type=message_type, message_channel=message_channel, message_text=message_text)
			else:
				print(raw_message)
		
		# If the listening loop ends, rejoin the main thread.
		self.thread.join()
	
	def send_message(self, message_text):
		self.send(f'PRIVMSG {self.channel} :{message_text}')
	
	def close_connection(self) -> None:
		self.listening = False
		self.socket.close()
	
	# Defined here as an example. Called when a chat message is recieved.
	def do_on_chat_message(self, *args, **kwargs):
		pass