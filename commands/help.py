
name = 'Help'
description = 'Displays the list of registered commands available to the user.'
privileges = 0b11111

synonyms = tuple('commands')

def effect(self, **kwargs):
	self.socket.send(f'PRIVMSG {self.channel} :{kwargs.get('text', 'Empty Message')}\n'.encode('utf-8'))