
name = 'Announce'
description = 'Sends the inputted message using bot\'s logged in twitch account.'
synonyms = tuple()

def effect(self, **kwargs):
	self.socket.send(f'PRIVMSG {self.channel} :{kwargs.get('text', 'Empty Message')}\n'.encode('utf-8'))